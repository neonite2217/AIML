#!/usr/bin/env python3
"""
Geospatial Clustering in Python
Enhanced version with outlier detection, zone labeling, and cluster profiling
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


# ==============================================================================
# HELPER FUNCTIONS (EXPORTABLE FOR TESTING)
# ==============================================================================

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate haversine distance between two points in km."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))


def nearest_neighbor_tsp(points):
    """Solve TSP using nearest neighbor heuristic."""
    n = len(points)
    if n <= 2:
        return list(range(n)), 0 if n == 1 else haversine_distance(
            points[0][0], points[0][1], points[1][0], points[1][1]
        )
    
    visited = [False] * n
    route = [0]
    visited[0] = True
    total_dist = 0
    
    for _ in range(n - 1):
        current = route[-1]
        nearest = None
        min_dist = float('inf')
        
        for j in range(n):
            if not visited[j]:
                dist = haversine_distance(
                    points[current][0], points[current][1],
                    points[j][0], points[j][1]
                )
                if dist < min_dist:
                    min_dist = dist
                    nearest = j
        
        if nearest is None:
            break
        route.append(nearest)
        visited[nearest] = True
        total_dist += min_dist
    
    total_dist += haversine_distance(
        points[route[-1]][0], points[route[-1]][1],
        points[route[0]][0], points[route[0]][1]
    )
    
    return route, total_dist


def assign_zone(row):
    """Assign zone label based on lat/lng coordinates."""
    if row['lng'] > -73.99:
        return "Downtown/Financial District"
    elif row['lat'] > 40.75:
        return "Uptown/North Zone"
    else:
        return "Midtown/Central Zone"


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    # 1. LOAD AND EXPLORE DATA
    print("\n=== DATA EXPLORATION ===")
    coords = pd.read_csv("deliverytime.txt")
    print(f"Dataset dimensions: {coords.shape[0]} rows, {coords.shape[1]} columns")
    print("\nFirst 10 rows:")
    print(coords.head(10))
    print("\nData summary:")
    print(coords.describe())

    # ==============================================================================
    # 2. VISUALIZE RAW POINTS
    # ==============================================================================

    print("\n=== VISUALIZING RAW DELIVERY LOCATIONS ===")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(coords['lng'], coords['lat'], alpha=0.7, s=50, c='steelblue')
    ax.set_title(f'Raw Delivery Locations\nTotal points: {len(coords)}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plot_1_raw_locations.png', dpi=150)
    plt.close()
    print("Saved: plot_1_raw_locations.png")

    # ==============================================================================
    # 3. PREPROCESSING: SCALE COORDINATES FOR K-MEANS
    # ==============================================================================

    print("\n=== PREPROCESSING ===")

    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords[['lat', 'lng']])

    # ==============================================================================
    # 4. DETERMINE OPTIMAL K USING ELBOW METHOD
    # ==============================================================================

    print("\n=== DETERMINING OPTIMAL K (ELBOW METHOD) ===")

    k_values = range(2, 9)
    wss = []

    for k in k_values:
        kmeans_temp = KMeans(n_clusters=k, n_init=10, random_state=42)
        kmeans_temp.fit(coords_scaled)
        wss.append(kmeans_temp.inertia_)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(list(k_values), wss, 'bo-', linewidth=2, markersize=8)
    ax.set_title('Elbow Method for Optimal K')
    ax.set_xlabel('Number of Clusters (k)')
    ax.set_ylabel('Within-Cluster Sum of Squares')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plot_2_elbow_method.png', dpi=150)
    plt.close()
    print("Saved: plot_2_elbow_method.png")

    # ==============================================================================
    # 5. RUN K-MEANS CLUSTERING
    # ==============================================================================

    print("\n=== K-MEANS CLUSTERING ===")

    optimal_k = 3
    print(f"Using k = {optimal_k} clusters")

    kmeans = KMeans(n_clusters=optimal_k, n_init=20, random_state=42)
    coords['cluster_id'] = kmeans.fit_predict(coords_scaled)

    print("\nCluster distribution:")
    print(coords['cluster_id'].value_counts().sort_index())

    print("\nCluster centers (original scale):")
    centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    centers_df = pd.DataFrame(centers_original, columns=['lat', 'lng'])
    centers_df['cluster_id'] = range(optimal_k)
    print(centers_df)

    # ==============================================================================
    # 6. OUTLIER DETECTION AND REMOVAL
    # ==============================================================================

    print("\n=== OUTLIER DETECTION ===")

    distances = []
    for i in range(len(coords_scaled)):
        center_idx = coords['cluster_id'].iloc[i]
        center = kmeans.cluster_centers_[center_idx]
        dist = np.linalg.norm(coords_scaled[i] - center)
        distances.append(dist)

    coords['distance_to_center'] = distances

    Q1 = np.percentile(coords['distance_to_center'], 25)
    Q3 = np.percentile(coords['distance_to_center'], 75)
    IQR = Q3 - Q1
    threshold = Q3 + 1.5 * IQR

    coords['is_outlier'] = coords['distance_to_center'] > threshold
    outliers = coords[coords['is_outlier']]
    print(f"Number of outliers detected: {len(outliers)}")

    if len(outliers) > 0:
        print("Outlier coordinates:")
        print(outliers[['lat', 'lng', 'cluster_id', 'distance_to_center']])

    # ==============================================================================
    # 7. CLEAN DATA (REMOVE OUTLIERS)
    # ==============================================================================

    print("\n=== CLEANING DATA ===")

    coords_clean = coords[~coords['is_outlier']].copy()
    print(f"Points after removing outliers: {len(coords_clean)}")

    # Re-run K-Means on clean data
    coords_clean_scaled = scaler.fit_transform(coords_clean[['lat', 'lng']])
    kmeans_clean = KMeans(n_clusters=optimal_k, n_init=20, random_state=42)
    coords_clean['cluster_id'] = kmeans_clean.fit_predict(coords_clean_scaled)

    print("\nUpdated cluster distribution:")
    print(coords_clean['cluster_id'].value_counts().sort_index())

    # ==============================================================================
    # 8. LABEL CLUSTERS AS MEANINGFUL ZONES
    # ==============================================================================

    print("\n=== LABELING ZONES ===")

    cluster_centers = coords_clean.groupby('cluster_id').agg({
        'lat': 'mean',
        'lng': 'mean',
        'cluster_id': 'count'
    }).rename(columns={'cluster_id': 'n_points'}).reset_index()

    cluster_centers = cluster_centers.sort_values('lng', ascending=False)

    cluster_centers['zone'] = cluster_centers.apply(assign_zone, axis=1)
    print(cluster_centers)

    zone_mapping = dict(zip(cluster_centers['cluster_id'], cluster_centers['zone']))
    coords_clean['zone'] = coords_clean['cluster_id'].map(zone_mapping)

    # ==============================================================================
    # 9. CLUSTER PROFILING
    # ==============================================================================

    print("\n=== CLUSTER PROFILING ===")

    profile = coords_clean.groupby(['cluster_id', 'zone']).agg(
        n_deliveries=('lat', 'count'),
        lat_min=('lat', 'min'),
        lat_max=('lat', 'max'),
        lng_min=('lng', 'min'),
        lng_max=('lng', 'max'),
        centroid_lat=('lat', 'mean'),
        centroid_lng=('lng', 'mean')
    ).reset_index()

    profile['lat_range'] = profile['lat_max'] - profile['lat_min']
    profile['lng_range'] = profile['lng_max'] - profile['lng_min']
    profile['area_approx'] = profile['lat_range'] * profile['lng_range'] * 111 * 111
    profile['density'] = profile['n_deliveries'] / profile['area_approx']

    print("\nCluster Profile:")
    print(profile[['zone', 'n_deliveries', 'centroid_lat', 'centroid_lng', 'density']])

    # ==============================================================================
    # 10. VISUALIZE CLUSTERS WITH ZONES
    # ==============================================================================

    print("\n=== VISUALIZING CLUSTERS ===")

    fig, ax = plt.subplots(figsize=(12, 9))

    colors = {'Downtown/Financial District': 'red', 
              'Midtown/Central Zone': 'green', 
              'Uptown/North Zone': 'blue'}

    for zone in coords_clean['zone'].unique():
        zone_data = coords_clean[coords_clean['zone'] == zone]
        ax.scatter(zone_data['lng'], zone_data['lat'], 
                   alpha=0.7, s=60, c=colors.get(zone, 'gray'), 
                   label=zone, edgecolors='white', linewidth=0.5)

    centers = scaler.inverse_transform(kmeans_clean.cluster_centers_)
    ax.scatter(centers[:, 1], centers[:, 0], marker='X', s=200, 
               c='black', edgecolors='white', linewidth=2, label='Centroids')

    ax.set_title(f'Delivery Locations by Cluster Zone\nK-Means with k = {optimal_k}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plot_3_kmeans_clusters.png', dpi=150)
    plt.close()
    print("Saved: plot_3_kmeans_clusters.png")

    # ==============================================================================
    # 11. DBSCAN COMPARISON (ENHANCEMENT)
    # ==============================================================================

    print("\n=== DBSCAN CLUSTERING (COMPARISON) ===")

    eps_value = 0.15
    min_pts = 3

    dbscan = DBSCAN(eps=eps_value, min_samples=min_pts)
    coords_clean['dbscan_cluster'] = dbscan.fit_predict(coords_clean_scaled)

    n_dbscan_clusters = len(set(coords_clean['dbscan_cluster'])) - (1 if -1 in coords_clean['dbscan_cluster'].values else 0)
    n_noise = list(coords_clean['dbscan_cluster']).count(-1)

    print(f"DBSCAN found {n_dbscan_clusters} clusters")
    print(f"Noise points (outliers): {n_noise}")

    fig, ax = plt.subplots(figsize=(12, 9))

    unique_clusters = coords_clean['dbscan_cluster'].unique()
    color_map = plt.cm.get_cmap('tab10', len(unique_clusters))
    colors_dbscan = {c: color_map(i) for i, c in enumerate(unique_clusters)}
    colors_dbscan[-1] = 'gray'

    for cluster in sorted(unique_clusters):
        cluster_data = coords_clean[coords_clean['dbscan_cluster'] == cluster]
        label = f"Cluster {cluster}" if cluster != -1 else "Noise"
        ax.scatter(cluster_data['lng'], cluster_data['lat'],
                   alpha=0.7, s=60, c=[colors_dbscan[cluster]], 
                   label=label, edgecolors='white', linewidth=0.5)

    ax.set_title(f'DBSCAN Clustering Result\neps = {eps_value}, minPts = {min_pts}')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plot_4_dbscan_clusters.png', dpi=150)
    plt.close()
    print("Saved: plot_4_dbscan_clusters.png")

    # ==============================================================================
    # 12. COMPARISON SUMMARY
    # ==============================================================================

    print("\n=== COMPARISON: K-MEANS vs DBSCAN ===")
    print(f"K-Means clusters: {optimal_k}")
    print(f"DBSCAN clusters: {n_dbscan_clusters}")
    print(f"DBSCAN noise points: {n_noise}")

    print("\n=== ANALYSIS COMPLETE ===")
    print("K-Means is suitable for spherical clusters but may struggle with irregular shapes.")
    print("DBSCAN automatically identifies outliers and can find arbitrarily shaped clusters.")

    # ==============================================================================
    # 13. SAVE RESULTS
    # ==============================================================================

    coords_clean.to_csv('clustered_deliveries.csv', index=False)
    print("\nResults saved to: clustered_deliveries.csv")

    print("\n=== FINAL ZONE SUMMARY ===")
    final_summary = coords_clean.groupby('zone').agg(
        deliveries=('lat', 'count'),
        centroid_lat=('lat', 'mean'),
        centroid_lng=('lng', 'mean')
    ).reset_index()
    final_summary['centroid_lat'] = final_summary['centroid_lat'].round(4)
    final_summary['centroid_lng'] = final_summary['centroid_lng'].round(4)
    print(final_summary)

    # ==============================================================================
    # 14. INTERACTIVE MAP VISUALIZATION (LEAFLET)
    # ==============================================================================

    print("\n=== CREATING INTERACTIVE MAP ===")

    try:
        import folium
        from folium.plugins import MarkerCluster
        
        center_lat = coords_clean['lat'].mean()
        center_lng = coords_clean['lng'].mean()
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=11, tiles='OpenStreetMap')
        
        zone_colors = {
            'Downtown/Financial District': 'red',
            'Midtown/Central Zone': 'green',
            'Uptown/North Zone': 'blue'
        }
        
        for idx, row in coords_clean.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lng']],
                radius=8,
                color=zone_colors.get(row['zone'], 'gray'),
                fill=True,
                fill_color=zone_colors.get(row['zone'], 'gray'),
                fill_opacity=0.7,
                popup=f"Zone: {row['zone']}<br>Lat: {row['lat']:.4f}<br>Lng: {row['lng']:.4f}"
            ).add_to(m)
        
        for zone, color in zone_colors.items():
            folium.Marker(
                location=[0, 0],
                icon=folium.Icon(color=color, icon='info-sign'),
                popup=zone
            )
        
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                    background-color: white; padding: 10px; border: 2px solid gray;
                    border-radius: 5px;">
            <h4 style="margin: 0;">Zone Legend</h4>
            <p style="margin: 5px 0;"><span style="color: red;">●</span> Downtown/Financial District</p>
            <p style="margin: 5px 0;"><span style="color: green;">●</span> Midtown/Central Zone</p>
            <p style="margin: 5px 0;"><span style="color: blue;">●</span> Uptown/North Zone</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        m.save('interactive_map.html')
        print("Saved: interactive_map.html")
        
    except ImportError:
        print("Note: Install folium for interactive maps: pip install folium")

    # ==============================================================================
    # 15. CLUSTER-BASED ROUTE OPTIMIZATION (TSP)
    # ==============================================================================

    print("\n=== ROUTE OPTIMIZATION (TSP) ===")

    print("\nOptimized Routes per Zone:")
    print("-" * 60)

    route_results = []

    for zone in coords_clean['zone'].unique():
        zone_data = coords_clean[coords_clean['zone'] == zone].reset_index(drop=True)
        
        if len(zone_data) < 2:
            print(f"\n{zone}: Single point - no route needed")
            continue
        
        points = list(zip(zone_data['lat'].values, zone_data['lng'].values))
        route, total_dist = nearest_neighbor_tsp(points)
        
        print(f"\n{zone}:")
        print(f"  Deliveries: {len(zone_data)}")
        print(f"  Optimized route (delivery order): { [i+1 for i in route] }")
        print(f"  Total distance: {total_dist:.2f} km")
        
        route_results.append({
            'zone': zone,
            'n_deliveries': len(zone_data),
            'route_order': route,
            'total_distance_km': round(total_dist, 2)
        })

    print("\n" + "=" * 60)
    print("ROUTE OPTIMIZATION SUMMARY")
    print("=" * 60)

    route_df = pd.DataFrame(route_results)
    print(route_df)

    route_df.to_csv('optimized_routes.csv', index=False)
    print("\nRoute optimization saved to: optimized_routes.csv")

    print("\n" + "=" * 60)
    print("ALL ENHANCEMENTS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
