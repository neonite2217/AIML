#!/usr/bin/env python3
"""
Topic Modelling using Python
Lab Project: Discover hidden topics in documents using LDA
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re
import warnings
warnings.filterwarnings('ignore')

DATA_PATH = "articles.csv"
OUTPUT_PATH = "topic_results.csv"

STOP_WORDS = [
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
    'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
    'don', 'should', 'now'
]

def load_data(path):
    """Load the articles dataset"""
    if not path.endswith('.csv'):
        path = path + '.csv'
    
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(f"Error: {path} not found!")
        raise
    
    required_cols = ['title', 'text']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    print(f"Loaded {len(df)} articles")
    return df

def preprocess_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text):
        return ""
    
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in STOP_WORDS and len(w) > 2]
    return ' '.join(words)

def create_vectorizer():
    """Create CountVectorizer for document-term matrix"""
    vectorizer = CountVectorizer(
        max_df=0.95,
        min_df=1,
        max_features=1000,
        stop_words='english'
    )
    return vectorizer

def fit_lda(dtm, n_topics=5, random_state=42):
    """Fit LDA model to document-term matrix"""
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=random_state,
        max_iter=50,
        learning_method='online',
        learning_offset=50.,
        n_jobs=-1
    )
    lda.fit(dtm)
    return lda

def get_top_words(lda, feature_names, n_top_words=10):
    """Extract top words for each topic"""
    topics = {}
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        topics[topic_idx] = top_words
    return topics

def assign_topics(lda, dtm):
    """Assign most likely topic to each document"""
    topic_probs = lda.transform(dtm)
    return topic_probs.argmax(axis=1), topic_probs

def main():
    print("=" * 60)
    print("Topic Modelling - Python Implementation")
    print("=" * 60)
    
    print("\n[1/6] Loading data...")
    df = load_data(DATA_PATH)
    print(f"  - Found {len(df)} articles")
    
    print("\n[2/6] Preprocessing text...")
    df['cleaned_text'] = df['text'].apply(preprocess_text)
    print("  - Text cleaned and normalized")
    
    print("\n[3/6] Creating document-term matrix...")
    vectorizer = create_vectorizer()
    dtm = vectorizer.fit_transform(df['cleaned_text'])
    feature_names = vectorizer.get_feature_names_out()
    print(f"  - DTM shape: {dtm.shape}")
    
    print("\n[4/6] Fitting LDA model (k=5 topics)...")
    n_topics = 5
    lda = fit_lda(dtm, n_topics=n_topics)
    print(f"  - Model fitted with {n_topics} topics")
    
    print("\n[5/6] Extracting topics and assigning to documents...")
    topics = get_top_words(lda, feature_names, n_top_words=10)
    
    for topic_id, words in topics.items():
        print(f"  Topic {topic_id}: {', '.join(words[:5])}...")
    
    topic_assignments, topic_probs = assign_topics(lda, dtm)
    df['topic'] = topic_assignments
    
    topic_labels = {
        0: "Machine Learning",
        1: "Deep Learning", 
        2: "Natural Language Processing",
        3: "Neural Networks",
        4: "Artificial Intelligence"
    }
    df['topic_label'] = df['topic'].map(topic_labels)
    
    print("\n[6/6] Saving results...")
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"  - Results saved to {OUTPUT_PATH}")
    
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print("\nDocument-Topic Assignments:")
    print(df[['title', 'topic_label']].to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Topic Modelling completed successfully!")
    print("=" * 60)
    
    return df, lda, vectorizer

if __name__ == "__main__":
    df, lda, vectorizer = main()