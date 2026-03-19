# Lab Project: Text Classification Pipeline in R

# Optional packages (used when available):
# install.packages(c("quanteda", "quanteda.textmodels"))

quanteda_available <- requireNamespace("quanteda", quietly = TRUE) &&
  requireNamespace("quanteda.textmodels", quietly = TRUE)

# 1. Load dataset
if (!file.exists("newsgroups.csv")) {
  sample_data <- data.frame(
    text = c(
      "The new graphics card is amazing for gaming.",
      "NASA is launching a new mission to Mars.",
      "The latest CPU benchmarks are out.",
      "The rover landed safely on the red planet.",
      "I need help configuring my new GPU."
    ),
    topic = c("comp.graphics", "sci.space", "comp.graphics", "sci.space", "comp.graphics"),
    stringsAsFactors = FALSE
  )
  write.csv(sample_data, "newsgroups.csv", row.names = FALSE)
}

news <- read.csv("newsgroups.csv", stringsAsFactors = FALSE)
if (!all(c("text", "topic") %in% names(news))) {
  stop("Input CSV must contain columns: text, topic")
}
if (nrow(news) < 2) {
  stop("Not enough data to split into training and testing sets.")
}

set.seed(123)


evaluate_predictions <- function(predicted_classes, test_labels) {
  conf_matrix <- table(predicted_classes, test_labels)
  print("Confusion Matrix:")
  print(conf_matrix)

  accuracy <- sum(diag(conf_matrix)) / sum(conf_matrix)
  print(paste("Accuracy:", accuracy))
}


run_quanteda_pipeline <- function(news) {
  cat("Backend: quanteda + quanteda.textmodels\n")
  corpus_obj <- quanteda::corpus(news, text_field = "text")
  toks <- quanteda::tokens(
    corpus_obj,
    remove_punct = TRUE,
    remove_numbers = TRUE,
    remove_symbols = TRUE
  )
  toks <- quanteda::tokens_remove(toks, quanteda::stopwords("en"))
  dfm_obj <- quanteda::dfm(toks)

  n_docs <- quanteda::ndoc(dfm_obj)
  train_indices <- sample(seq_len(n_docs), floor(0.8 * n_docs))
  test_indices <- setdiff(seq_len(n_docs), train_indices)

  train_dfm <- dfm_obj[train_indices, ]
  test_dfm <- dfm_obj[test_indices, ]
  train_labels <- news$topic[train_indices]
  test_labels <- news$topic[test_indices]

  if (quanteda::ndoc(test_dfm) == 0) {
    print("No documents in the test set to evaluate.")
    return(invisible(NULL))
  }

  nb_model <- quanteda.textmodels::textmodel_nb(train_dfm, train_labels)
  predicted_classes <- as.character(predict(nb_model, newdata = test_dfm))
  evaluate_predictions(predicted_classes, test_labels)
}


run_base_pipeline <- function(news) {
  cat("Backend: base R fallback (no external NLP packages)\n")

  stop_words <- c(
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
    "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will",
    "with", "i", "you", "your", "my", "our", "this", "these", "those", "or", "but"
  )

  tokenize_text <- function(text) {
    text <- tolower(text)
    text <- gsub("[^a-z\\s]", " ", text)
    text <- gsub("\\s+", " ", text)
    tokens <- trimws(unlist(strsplit(text, " ", fixed = TRUE)))
    tokens <- tokens[nchar(tokens) > 0]
    tokens[!(tokens %in% stop_words)]
  }

  doc_tokens <- lapply(news$text, tokenize_text)
  n_docs <- length(doc_tokens)

  train_indices <- sample(seq_len(n_docs), floor(0.8 * n_docs))
  test_indices <- setdiff(seq_len(n_docs), train_indices)

  train_tokens <- doc_tokens[train_indices]
  test_tokens <- doc_tokens[test_indices]
  train_labels <- news$topic[train_indices]
  test_labels <- news$topic[test_indices]

  if (length(test_tokens) == 0) {
    print("No documents in the test set to evaluate.")
    return(invisible(NULL))
  }

  vocab <- sort(unique(unlist(train_tokens)))
  if (length(vocab) == 0) {
    stop("Vocabulary is empty after preprocessing.")
  }

  vectorize_docs <- function(token_list, vocab) {
    m <- matrix(0, nrow = length(token_list), ncol = length(vocab))
    colnames(m) <- vocab
    for (i in seq_along(token_list)) {
      toks <- token_list[[i]]
      if (length(toks) == 0) next
      counts <- table(factor(toks, levels = vocab))
      m[i, ] <- as.numeric(counts)
    }
    m
  }

  train_matrix <- vectorize_docs(train_tokens, vocab)
  test_matrix <- vectorize_docs(test_tokens, vocab)

  classes <- sort(unique(train_labels))
  class_log_prior <- setNames(numeric(length(classes)), classes)
  class_log_word_prob <- vector("list", length(classes))
  names(class_log_word_prob) <- classes

  for (cl in classes) {
    class_rows <- which(train_labels == cl)
    class_log_prior[cl] <- log(length(class_rows) / length(train_labels))
    word_counts <- colSums(train_matrix[class_rows, , drop = FALSE]) + 1
    class_log_word_prob[[cl]] <- log(word_counts / sum(word_counts))
  }

  predict_nb <- function(x_row) {
    scores <- sapply(classes, function(cl) {
      as.numeric(class_log_prior[cl]) + sum(x_row * class_log_word_prob[[cl]])
    })
    classes[which.max(scores)]
  }

  predicted_classes <- apply(test_matrix, 1, predict_nb)
  evaluate_predictions(predicted_classes, test_labels)
}


if (quanteda_available) {
  run_quanteda_pipeline(news)
} else {
  run_base_pipeline(news)
}
