# News Analysis Dashboard - R Shiny
# Run with: shiny::runApp("app.R") or RStudio

suppressPackageStartupMessages({
  library(shiny)
  library(tidyverse)
  library(RSQLite)
  library(wordcloud)
  library(tm)
  library(DT)
})

DB_PATH <- "news_database.sqlite"

get_articles <- function() {
  if (!file.exists(DB_PATH)) {
    return(NULL)
  }
  
  con <- dbConnect(SQLite(), DB_PATH)
  articles <- dbGetQuery(con, "SELECT * FROM articles ORDER BY published_at DESC")
  dbDisconnect(con)
  
  articles
}

get_sources <- function() {
  articles <- get_articles()
  if (is.null(articles)) {
    return(character(0))
  }
  unique(na.omit(articles$source_name))
}

get_sentiment_stats <- function() {
  articles <- get_articles()
  if (is.null(articles) || nrow(articles) == 0) {
    return(data.frame(source = character(), avg_sentiment = numeric(), count = integer()))
  }
  
  articles %>%
    group_by(source_name) %>%
    summarise(
      avg_sentiment = mean(sentiment_score, na.rm = TRUE),
      count = n(),
      .groups = "drop"
    ) %>%
    rename(source = source_name)
}

get_word_freq <- function() {
  articles <- get_articles()
  if (is.null(articles) || nrow(articles) == 0) {
    return(NULL)
  }
  
  text <- paste(articles$title, articles$description, collapse = " ")
  corpus <- Corpus(VectorSource(text))
  corpus <- tm_map(corpus, content_transformer(tolower))
  corpus <- tm_map(corpus, removePunctuation)
  corpus <- tm_map(corpus, removeWords, c(stopwords("english"), "will", "said", "also"))
  
  dtm <- DocumentTermMatrix(corpus)
  
  if (ncol(dtm) > 0) {
    term_freq <- colSums(as.matrix(dtm))
    data.frame(word = names(term_freq), freq = term_freq)
  } else {
    NULL
  }
}

ui <- fluidPage(
  titlePanel("Real-Time News Analysis Dashboard"),
  
  fluidRow(
    column(3,
           wellPanel(
             h4("Filters"),
             selectInput("source_filter", "News Source:", 
                        choices = c("All" = "all", get_sources()),
                        selected = "all"),
             actionButton("refresh_btn", "Refresh Data", icon = icon("refresh")),
             br(), br(),
             p(style = "font-size: 12px;", 
               "Data source: SQLite database")
           )
    ),
    column(9,
           tabsetPanel(
             tabPanel("Latest News",
                      DTOutput("articles_table")),
             tabPanel("Word Cloud",
                      plotOutput("wordcloud_plot", height = "500px")),
             tabPanel("Sentiment Analysis",
                      plotOutput("sentiment_plot", height = "400px"),
                      br(),
                      DTOutput("sentiment_table")),
             tabPanel("Collection History",
                      DTOutput("log_table"))
           )
    )
  )
)

server <- function(input, output, session) {
  articles_data <- reactive({
    input$refresh_btn
    get_articles()
  })
  
  filtered_articles <- reactive({
    req(articles_data())
    
    if (input$source_filter == "all") {
      articles_data()
    } else {
      articles_data() %>% filter(source_name == input$source_filter)
    }
  })
  
  output$articles_table <- renderDT({
    req(filtered_articles())
    
    filtered_articles() %>%
      select(title, source_name, author, published_at, sentiment_score) %>%
      rename(
        Title = title,
        Source = source_name,
        Author = author,
        Published = published_at,
        Sentiment = sentiment_score
      ) %>%
      datatable(
        options = list(pageLength = 10, scrollX = TRUE),
        rownames = FALSE
      )
  })
  
  output$wordcloud_plot <- renderPlot({
    req(articles_data())
    
    word_freq <- get_word_freq()
    
    if (!is.null(word_freq) && nrow(word_freq) > 0) {
      wordcloud(
        words = word_freq$word,
        freq = word_freq$freq,
        min.freq = 1,
        max.words = 80,
        random.order = FALSE,
        rot.per = 0.35,
        colors = brewer.pal(8, "Dark2")
      )
    } else {
      plot.new()
      text(0.5, 0.5, "No data available")
    }
  })
  
  output$sentiment_plot <- renderPlot({
    req(articles_data())
    
    stats <- get_sentiment_stats()
    
    if (!is.null(stats) && nrow(stats) > 0) {
      ggplot(stats, aes(x = reorder(source, avg_sentiment), y = avg_sentiment, fill = avg_sentiment)) +
        geom_bar(stat = "identity") +
        coord_flip() +
        scale_fill_gradient2(low = "red", mid = "gray", high = "green", midpoint = 0) +
        labs(x = "News Source", y = "Average Sentiment Score", title = "Sentiment by Source") +
        theme_minimal()
    } else {
      plot.new()
      text(0.5, 0.5, "No sentiment data available")
    }
  })
  
  output$sentiment_table <- renderDT({
    req(articles_data())
    
    stats <- get_sentiment_stats()
    
    if (!is.null(stats) && nrow(stats) > 0) {
      datatable(stats, options = list(pageLength = 5), rownames = FALSE)
    }
  })
  
  output$log_table <- renderDT({
    if (!file.exists(DB_PATH)) {
      return(NULL)
    }
    
    con <- dbConnect(SQLite(), DB_PATH)
    logs <- dbGetQuery(con, "SELECT * FROM collection_log ORDER BY timestamp DESC")
    dbDisconnect(con)
    
    datatable(logs, options = list(pageLength = 10), rownames = FALSE)
  })
  
  observe({
    updateSelectInput(session, "source_filter", 
                      choices = c("All" = "all", get_sources()))
  })
}

shinyApp(ui = ui, server = server)
