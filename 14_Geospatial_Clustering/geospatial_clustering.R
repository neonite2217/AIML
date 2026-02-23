# Lab Project: Geospatial Clustering in R
# Enhanced version with outlier detection, zone labeling, and cluster profiling

library(tidyverse)
library(sf)
library(geosphere)

# ==============================================================================
# 1. LOAD AND EXPLORE DATA
# ==============================================================================

coords <- read_csv("deliverytime.txt")

cat("\n=== DATA EXPLORATION ===\n")
cat("Dataset dimensions:", nrow(coords), "rows,", ncol(coords), "columns\n")
cat("\nFirst 10 rows:\n")
print(head(coords, 10))
cat("\nData summary:\n")
print(summary(coords))

# ==============================================================================
# 2. VISUALIZE RAW POINTS
# ==============================================================================

cat("\n=== VISUALIZING RAW DELIVERY LOCATIONS ===\n")

raw_plot <- ggplot(coords, aes(x = lng, y = lat)) +
  geom_point(alpha = 0.7, size = 3, color = "steelblue") +
  labs(
    title = "Raw Delivery Locations",
    subtitle = paste("Total points:", nrow(coords)),
    x = "Longitude",
    y = "Latitude"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5)
  )

print(raw_plot)

# ==============================================================================
# 3. PREPROCESSING: SCALE COORDINATES FOR K-MEANS
# ==============================================================================

cat("\n=== PREPROCESSING ===\n")

coords_scaled <- coords %>%
  mutate(
    lat_scaled = scale(lat),
    lng_scaled = scale(lng)
  )

# ==============================================================================
# 4. DETERMINE OPTIMAL K USING ELBOW METHOD
# ==============================================================================

cat("\n=== DETERMINING OPTIMAL K (ELBOW METHOD) ===\n")

set.seed(42)
k_values <- 2:8
wss <- numeric(length(k_values))

for (i in seq_along(k_values)) {
  kmeans_temp <- kmeans(coords_scaled[, c("lat_scaled", "lng_scaled")], 
                        centers = k_values[i], nstart = 10)
  wss[i] <- kmeans_temp$tot.withinss
}

elbow_df <- tibble(k = k_values, wss = wss)

elbow_plot <- ggplot(elbow_df, aes(x = k, y = wss)) +
  geom_line(color = "steelblue", linewidth = 1) +
  geom_point(color = "steelblue", size = 3) +
  labs(title = "Elbow Method for Optimal K", x = "Number of Clusters (k)", 
       y = "Within-Cluster Sum of Squares") +
  theme_minimal() +
  theme(plot.title = element_text(hjust = 0.5))

print(elbow_plot)

# ==============================================================================
# 5. RUN K-MEANS CLUSTERING
# ==============================================================================

cat("\n=== K-MEANS CLUSTERING ===\n")

optimal_k <- 3
cat("Using k =", optimal_k, "clusters\n")

set.seed(42)
kmeans_result <- kmeans(coords_scaled[, c("lat_scaled", "lng_scaled")], 
                       centers = optimal_k, nstart = 20)

coords$cluster_id <- kmeans_result$cluster

cat("\nCluster distribution:\n")
print(table(coords$cluster_id))

cat("\nCluster centers (original scale):\n")
print(kmeans_result$centers)

# ==============================================================================
# 6. OUTLIER DETECTION AND REMOVAL
# ==============================================================================

cat("\n=== OUTLIER DETECTION ===\n")

coords <- coords %>%
  mutate(
    center_lat = kmeans_result$centers[cluster_id, "lat_scaled"],
    center_lng = kmeans_result$centers[cluster_id, "lng_scaled"],
    distance_to_center = sqrt((lat_scaled - center_lat)^2 + (lng_scaled - center_lng)^2)
  )

q75 <- quantile(coords$distance_to_center, 0.75)
q75 <- quantile(coords$distance_to_center, 0.75)
iqr <- IQR(coords$distance_to_center)
threshold <- q75 + 1.5 * iqr

coords <- coords %>%
  mutate(is_outlier = distance_to_center > threshold)

outliers <- coords %>% filter(is_outlier)
cat("Number of outliers detected:", nrow(outliers), "\n")

if (nrow(outliers) > 0) {
  cat("Outlier coordinates:\n")
  print(outliers[, c("lat", "lng", "cluster_id", "distance_to_center")])
}

# ==============================================================================
# 7. CLEAN DATA (REMOVE OUTLIERS)
# ==============================================================================

cat("\n=== CLEANING DATA ===\n")

coords_clean <- coords %>% filter(!is_outlier)
cat("Points after removing outliers:", nrow(coords_clean), "\n")

# Re-run K-Means on clean data
set.seed(42)
kmeans_clean <- kmeans(coords_clean[, c("lat_scaled", "lng_scaled")], 
                       centers = optimal_k, nstart = 20)
coords_clean$cluster_id <- kmeans_clean$cluster

cat("\nUpdated cluster distribution:\n")
print(table(coords_clean$cluster_id))

# ==============================================================================
# 8. LABEL CLUSTERS AS MEANINGFUL ZONES
# ==============================================================================

cat("\n=== LABELING ZONES ===\n")

cluster_centers <- coords_clean %>%
  group_by(cluster_id) %>%
  summarise(
    avg_lat = mean(lat),
    avg_lng = mean(lng),
    n_points = n(),
    .groups = "drop"
  ) %>%
  arrange(desc(avg_lng))

print(cluster_centers)

zone_labels <- case_when(
  cluster_centers$avg_lng > -73.99 ~ "Downtown/Financial District",
  cluster_centers$avg_lat > 40.75 ~ "Uptown/North Zone",
  TRUE ~ "Midtown/Central Zone"
)

zone_mapping <- setNames(zone_labels, cluster_centers$cluster_id)
cat("\nZone mapping:\n")
print(zone_mapping)

coords_clean$zone <- zone_labels[match(coords_clean$cluster_id, cluster_centers$cluster_id)]

# ==============================================================================
# 9. CLUSTER PROFILING
# ==============================================================================

cat("\n=== CLUSTER PROFILING ===\n")

profile <- coords_clean %>%
  group_by(cluster_id, zone) %>%
  summarise(
    n_deliveries = n(),
    lat_range = max(lat) - min(lat),
    lng_range = max(lng) - min(lng),
    centroid_lat = mean(lat),
    centroid_lng = mean(lng),
    .groups = "drop"
  ) %>%
  mutate(
    area_approx = lat_range * lng_range * 111 * 111,
    density = n_deliveries / area_approx
  )

cat("\nCluster Profile:\n")
print(profile)

# ==============================================================================
# 10. VISUALIZE CLUSTERS WITH ZONES
# ==============================================================================

cat("\n=== VISUALIZING CLUSTERS ===\n")

cluster_plot <- ggplot(coords_clean, aes(x = lng, y = lat, color = zone)) +
  geom_point(alpha = 0.7, size = 4) +
  geom_point(data = as_tibble(kmeans_clean$centers) %>% 
               mutate(lat = lat * sd(coords$lat) + mean(coords$lat),
                      lng = lng * sd(coords$lng) + mean(coords$lng)),
             aes(x = lng, y = lat), 
             shape = "X", size = 8, color = "black", stroke = 2) +
  labs(
    title = "Delivery Locations by Cluster Zone",
    subtitle = paste("K-Means with k =", optimal_k),
    x = "Longitude",
    y = "Latitude",
    color = "Zone"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5),
    legend.position = "bottom"
  )

print(cluster_plot)

# ==============================================================================
# 11. DBSCAN COMPARISON (ENHANCEMENT)
# ==============================================================================

cat("\n=== DBSCAN CLUSTERING (COMPARISON) ===\n")

if (!require("dbscan", quietly = TRUE)) {
  install.packages("dbscan", repos = "https://cloud.r-project.org")
  library(dbscan)
}

set.seed(42)
eps_value <- 0.15
min_pts <- 3

dbscan_result <- dbscan(coords_clean[, c("lat_scaled", "lng_scaled")], 
                        eps = eps_value, minPts = min_pts)

coords_clean$dbscan_cluster <- dbscan_result$cluster

cat("DBSCAN found", length(unique(dbscan_result$cluster)) - 1, "clusters\n")
cat("Noise points (outliers):", sum(dbscan_result$cluster == 0), "\n")

dbscan_plot <- ggplot(coords_clean, aes(x = lng, y = lat, color = factor(dbscan_cluster))) +
  geom_point(alpha = 0.7, size = 4) +
  scale_color_manual(values = c("gray", "red", "green", "blue", "orange", "purple"),
                     name = "DBSCAN Cluster") +
  labs(
    title = "DBSCAN Clustering Result",
    subtitle = paste("eps =", eps_value, ", minPts =", min_pts),
    x = "Longitude",
    y = "Latitude"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5),
    legend.position = "bottom"
  )

print(dbscan_plot)

# ==============================================================================
# 12. COMPARISON SUMMARY
# ==============================================================================

cat("\n=== COMPARISON: K-MEANS vs DBSCAN ===\n")

kmeans_clusters <- length(unique(coords_clean$cluster_id))
dbscan_clusters <- length(unique(dbscan_result$cluster)) - 1
dbscan_noise <- sum(dbscan_result$cluster == 0)

cat("K-Means clusters:", kmeans_clusters, "\n")
cat("DBSCAN clusters:", dbscan_clusters, "\n")
cat("DBSCAN noise points:", dbscan_noise, "\n")

cat("\n=== ANALYSIS COMPLETE ===\n")
cat("K-Means is suitable for spherical clusters but may struggle with irregular shapes.\n")
cat("DBSCAN automatically identifies outliers and can find arbitrarily shaped clusters.\n")

# ==============================================================================
# 13. SAVE RESULTS
# ==============================================================================

write_csv(coords_clean, "clustered_deliveries.csv")
cat("\nResults saved to: clustered_deliveries.csv\n")

cat("\n=== FINAL ZONE SUMMARY ===\n")
final_summary <- coords_clean %>%
  group_by(zone) %>%
  summarise(
    deliveries = n(),
    centroid_lat = round(mean(lat), 4),
    centroid_lng = round(mean(lng), 4),
    .groups = "drop"
  )
print(final_summary)
