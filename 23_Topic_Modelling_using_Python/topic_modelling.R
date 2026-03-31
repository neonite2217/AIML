# Lab Project: Topic Modelling in R

# 1. Import libraries
# You may need to install these packages first:
# install.packages("tidyverse")
# install.packages("quanteda")
# install.packages("topicmodels")

library(tidyverse)
library(quanteda)
library(topicmodels)

# 2. Load dataset
# Create a dummy articles.csv if it doesn't exist
if (!file.exists("articles.csv")) {
  tibble(
    title = c("Article 1", "Article 2", "Article 3", "Article 4", "Article 5"),
    text = c(
      "Machine learning is a field of study in artificial intelligence concerned with the development and study of statistical algorithms that can learn from and make predictions on data.",
      "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning.",
      "Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language.",
      "A neural network is a network or circuit of neurons, or in a modern sense, an artificial neural network, composed of artificial neurons or nodes.",
      "Artificial intelligence is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans and animals."
    )
  ) %>%
  write_csv("articles.csv")
}

articles <- read_csv("articles.csv")

# 3. Clean text
# Create a corpus
corpus <- corpus(articles, text_field = "text")

# Tokenize, remove punctuation, stopwords, and stem
tokens <- tokens(corpus, what = "word", remove_punct = TRUE, remove_symbols = TRUE, remove_numbers = TRUE) %>%
  tokens_tolower() %>%
  tokens_remove(stopwords("en")) %>%
  tokens_wordstem()

# 4. Create a document-feature matrix (DFM)
dfm <- dfm(tokens)

# 5. Fit LDA
# Ensure the DFM is in a format suitable for topicmodels
dfm_topicmodels <- convert(dfm, to = "topicmodels")

# Fit the LDA model
lda_model <- LDA(dfm_topicmodels, k = 2, control = list(seed = 1234))

# 6. Assign topic label
# Get the topic probabilities for each document
doc_topics <- posterior(lda_model, dfm_topicmodels)$topics

# Assign the most likely topic
articles$topic <- apply(doc_topics, 1, which.max)

# 7. Visualize the topics
# Get the terms for each topic
topic_terms <- terms(lda_model, 10)
print("Top 10 terms per topic:")
print(topic_terms)

# Print the articles with their assigned topics
print("Articles with their assigned topics:")
print(articles)
