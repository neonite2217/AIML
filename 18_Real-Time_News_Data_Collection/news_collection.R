# Lab Project: Real-Time News Data Collection in R
# Enhanced Version with API Integration, SQLite Storage, Logging, and Sentiment Analysis

suppressPackageStartupMessages({
  library(tidyverse)
  library(jsonlite)
  library(httr)
  library(wordcloud)
  library(tm)
  library(RSQLite)
  library(lubridate)
})

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG <- list(
  api_key = Sys.getenv("NEWS_API_KEY", ""),
  api_url = "https://newsapi.org/v2/everything",
  db_path = "news_database.sqlite",
  log_file = "news_collection.log",
  query = "technology",
  language = "en",
  page_size = 20
)

# ============================================================================
# LOGGING SYSTEM
# ============================================================================

log_message <- function(level, message) {
  timestamp <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  log_entry <- sprintf("[%s] [%s] %s\n", timestamp, toupper(level), message)
  cat(log_entry)
  cat(log_entry, file = CONFIG$log_file, append = TRUE)
}

log_info <- function(message) log_message("INFO", message)
log_error <- function(message) log_message("ERROR", message)
log_warning <- function(message) log_message("WARNING", message)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

init_database <- function() {
  con <- dbConnect(SQLite(), CONFIG$db_path)
  
  if (!dbExistsTable(con, "articles")) {
    dbExecute(con, "
      CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT,
        source_name TEXT,
        author TEXT,
        title TEXT,
        description TEXT,
        url TEXT UNIQUE,
        published_at TEXT,
        content TEXT,
        collected_at TEXT,
        sentiment_score REAL
      )
    ")
    log_info("Database initialized with new articles table")
  }
  
  if (!dbExistsTable(con, "collection_log")) {
    dbExecute(con, "
      CREATE TABLE collection_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        status TEXT,
        articles_collected INTEGER,
        new_articles INTEGER,
        errors TEXT
      )
    ")
    log_info("Database initialized with collection_log table")
  }
  
  con
}

check_duplicate <- function(con, url) {
  query <- sprintf("SELECT COUNT(*) as count FROM articles WHERE url = '%s'", 
                   gsub("'", "''", url))
  result <- dbGetQuery(con, query)
  result$count > 0
}

insert_article <- function(con, article, sentiment_score = NA) {
  if (check_duplicate(con, article$url)) {
    return(FALSE)
  }
  
  query <- sprintf("
    INSERT INTO articles (source_id, source_name, author, title, description, 
                        url, published_at, content, collected_at, sentiment_score)
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)
  ",
    gsub("'", "''", article$source$id %||% ""),
    gsub("'", "''", article$source$name %||% ""),
    gsub("'", "''", article$author %||% ""),
    gsub("'", "''", article$title %||% ""),
    gsub("'", "''", article$description %||% ""),
    gsub("'", "''", article$url %||% ""),
    gsub("'", "''", article$publishedAt %||% ""),
    gsub("'", "''", article$content %||% ""),
    gsub("'", "''", Sys.time()),
    ifelse(is.na(sentiment_score), "NULL", sprintf("%.4f", sentiment_score))
  )
  
  tryCatch({
    dbExecute(con, query)
    TRUE
  }, error = function(e) {
    log_error(paste("Failed to insert article:", e$message))
    FALSE
  })
}

log_collection <- function(con, status, articles_collected, new_articles, errors = "") {
  query <- sprintf("
    INSERT INTO collection_log (timestamp, status, articles_collected, new_articles, errors)
    VALUES ('%s', '%s', %d, %d, '%s')
  ",
    Sys.time(),
    status,
    articles_collected,
    new_articles,
    gsub("'", "''", errors)
  )
  dbExecute(con, query)
}

# ============================================================================
# API FUNCTIONS
# ============================================================================

fetch_news_from_api <- function() {
  if (nzchar(CONFIG$api_key)) {
    log_info(paste("Fetching news with query:", CONFIG$query))
    
    tryCatch({
      response <- GET(
        CONFIG$api_url,
        query = list(
          q = CONFIG$query,
          language = CONFIG$language,
          pageSize = CONFIG$page_size,
          apiKey = CONFIG$api_key
        )
      )
      
      if (status_code(response) == 200) {
        content <- content(response, as = "text", encoding = "UTF-8")
        data <- fromJSON(content)
        
        if (data$status == "ok") {
          log_info(paste("API returned", data$totalResults, "articles"))
          return(data$articles)
        } else {
          log_error(paste("API error:", data$message))
        }
      } else {
        log_error(paste("HTTP error:", status_code(response)))
      }
    }, error = function(e) {
      log_error(paste("API request failed:", e$message))
    })
  } else {
    log_warning("No API key found. Using dummy data.")
  }
  
  NULL
}

load_dummy_data <- function() {
  if (file.exists("news_response.json")) {
    log_info("Loading from local news_response.json")
    fromJSON("news_response.json")$articles
  } else {
    log_info("Creating dummy data")
    list(
      list(
        source = list(id = "cnn", name = "CNN"),
        author = "John Doe",
        title = "Big Tech Stocks Soar",
        description = "Shares of major technology companies saw a significant increase today.",
        url = "https://example.com/1",
        publishedAt = "2024-01-01T12:00:00Z",
        content = "..."
      ),
      list(
        source = list(id = "bbc-news", name = "BBC News"),
        author = "Jane Smith",
        title = "AI Regulation Debated by Lawmakers",
        description = "Governments around the world are discussing how to regulate artificial intelligence.",
        url = "https://example.com/2",
        publishedAt = "2024-01-01T13:00:00Z",
        content = "..."
      )
    )
  }
}

# ============================================================================
# SENTIMENT ANALYSIS
# ============================================================================

calculate_sentiment <- function(text) {
  if (is.null(text) || nchar(trimws(text)) == 0) {
    return(NA)
  }
  
  text <- tolower(text)
  positive_words <- c("good", "great", "excellent", "amazing", "soar", "increase", 
                      "positive", "growth", "success", "best", "winner", "gain",
                      "profit", "rise", "up", "strong", "boost", "improve")
  negative_words <- c("bad", "terrible", "awful", "fall", "decrease", "negative",
                      "loss", "fail", "worst", "loser", "drop", "down", "weak",
                      "decline", "crash", "problem", "issue", "concern", "risk")
  
  words <- unlist(strsplit(text, "\\s+"))
  pos_count <- sum(words %in% positive_words)
  neg_count <- sum(words %in% negative_words)
  total <- pos_count + neg_count
  
  if (total == 0) return(0)
  (pos_count - neg_count) / total
}

# ============================================================================
# DATA PROCESSING
# ============================================================================

process_articles <- function(articles) {
  if (is.null(articles) || length(articles) == 0) {
    return(NULL)
  }
  
  articles_df <- tibble(
    source_id = sapply(articles, function(x) x$source$id %||% NA),
    source_name = sapply(articles, function(x) x$source$name %||% NA),
    author = sapply(articles, function(x) x$author %||% NA),
    title = sapply(articles, function(x) x$title %||% NA),
    description = sapply(articles, function(x) x$description %||% NA),
    url = sapply(articles, function(x) x$url %||% NA),
    published_at = sapply(articles, function(x) x$publishedAt %||% NA),
    content = sapply(articles, function(x) x$content %||% NA)
  )
  
  articles_df$sentiment <- sapply(
    paste(articles_df$title, articles_df$description),
    calculate_sentiment
  )
  
  articles_df
}

# ============================================================================
# TREND DETECTION
# ============================================================================

detect_trends <- function(articles_df, top_n = 10) {
  text <- paste(articles_df$title, articles_df$description, collapse = " ")
  corpus <- Corpus(VectorSource(text))
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, removeWords, c(stopwords("english"), "will", "said", "also", "the", "this"))
  
  dtm <- DocumentTermMatrix(corpus)
  
  if (ncol(dtm) > 0) {
    term_freq <- colSums(as.matrix(dtm))
    trends <- data.frame(
      term = names(term_freq),
      frequency = term_freq
    ) %>%
      arrange(desc(frequency)) %>%
      head(top_n)
    
    log_info("Top trending terms:")
    print(trends)
    return(trends)
  }
  
  NULL
}

detect_anomalies <- function(articles_df) {
  if (!"sentiment" %in% names(articles_df) || nrow(articles_df) < 3) {
    return(NULL)
  }
  
  sentiment_values <- articles_df$sentiment[!is.na(articles_df$sentiment)]
  
  if (length(sentiment_values) < 3) {
    return(NULL)
  }
  
  mean_sent <- mean(sentiment_values)
  sd_sent <- sd(sentiment_values)
  
  anomalies <- articles_df %>%
    mutate(
      z_score = (sentiment - mean_sent) / sd_sent,
      is_anomaly = abs(z_score) > 2
    ) %>%
    filter(is_anomaly) %>%
    select(title, source_name, sentiment, z_score)
  
  if (nrow(anomalies) > 0) {
    log_warning(paste("Detected", nrow(anomalies), "anomalies in sentiment"))
    print(anomalies)
  }
  
  anomalies
}

# ============================================================================
# VISUALIZATION
# ============================================================================

create_wordcloud <- function(articles_df) {
  text <- paste(articles_df$title, articles_df$description, collapse = " ")
  corpus <- Corpus(VectorSource(text))
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, removeWords, c(stopwords("english"), "will", "said", "also"))
  
  dtm <- DocumentTermMatrix(corpus)
  
  if (ncol(dtm) > 0) {
    wordcloud(
      words = colnames(dtm),
      freq = colSums(as.matrix(dtm)),
      min.freq = 1,
      max.words = 100,
      random.order = FALSE,
      rot.per = 0.35,
      colors = brewer.pal(8, "Dark2")
    )
    log_info("Word cloud created successfully")
  } else {
    log_warning("No words available for word cloud")
  }
}

create_sentiment_summary <- function(articles_df) {
  if (!"sentiment" %in% names(articles_df)) {
    return(NULL)
  }
  
  summary_df <- articles_df %>%
    group_by(source_name) %>%
    summarise(
      avg_sentiment = mean(sentiment, na.rm = TRUE),
      article_count = n(),
      .groups = "drop"
    ) %>%
    arrange(desc(avg_sentiment))
  
  log_info("Sentiment summary:")
  print(summary_df)
  
  summary_df
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

main <- function() {
  log_info("===========================================")
  log_info("Starting News Collection Pipeline")
  log_info("===========================================")
  
  con <- NULL
  articles_collected <- 0
  new_articles <- 0
  status <- "SUCCESS"
  error_msg <- ""
  
  tryCatch({
    con <- init_database()
    
    articles <- fetch_news_from_api()
    
    if (is.null(articles) || length(articles) == 0) {
      log_warning("API fetch returned no data, using dummy data")
      articles <- load_dummy_data()
    }
    
    articles_collected <- length(articles)
    log_info(paste("Processing", articles_collected, "articles"))
    
    articles_df <- process_articles(articles)
    
    for (i in seq_len(nrow(articles_df))) {
      row <- articles_df[i, ]
      if (insert_article(con, row, row$sentiment)) {
        new_articles <- new_articles + 1
      }
    }
    
    log_info(paste("New articles stored:", new_articles))
    
    write_csv(articles_df, "news_articles.csv")
    log_info("Articles saved to news_articles.csv")
    
    create_wordcloud(articles_df)
    
    create_sentiment_summary(articles_df)
    
    trends <- detect_trends(articles_df)
    anomalies <- detect_anomalies(articles_df)
    
  }, error = function(e) {
    status <- "ERROR"
    error_msg <- e$message
    log_error(paste("Pipeline failed:", e$message))
  }, finally = {
    if (!is.null(con)) {
      log_collection(con, status, articles_collected, new_articles, error_msg)
      dbDisconnect(con)
    }
    
    log_info(paste("Pipeline completed. Status:", status))
    log_info("===========================================")
  })
}

# Run if executed directly
if (!interactive()) {
  main()
}
