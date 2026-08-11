"""
NLP Preprocessing Utility Module
--------------------------------
This module provides text normalization, cleaning, tokenization, and lemmatization 
routines designed for Machine Learning and Natural Language Processing pipelines.

Key Preprocessing Pipeline Steps:
  1. Lowercasing input text.
  2. URL and HTML tag removal.
  3. Contraction expansion (e.g., "don't" -> "do not").
  4. Removal of punctuation, numbers, and emojis.
  5. Removal of non-alphabetic characters.
  6. Tokenization via NLTK `word_tokenize`.
  7. English stop word removal.
  8. WordNet lemmatization.

Dependencies / NLTK Resources Downloaded:
  - `punkt`, `punkt_tab`, `stopwords`, `wordnet`, `omw-1.4`

Exports:
  - preprocess_text: Core utility function for string cleaning and normalization.
"""

import re
import string
import contractions
import emoji
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK corpora and models are downloaded
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

# Pre-load stopwords set and lemmatizer for efficiency
stop_words: set[str] = set(stopwords.words("english"))
lemmatizer: WordNetLemmatizer = WordNetLemmatizer()


def preprocess_text(text: str) -> str:
    """
    Cleans, normalizes, tokenizes, removes stop words, and lemmatizes raw text.

    Args:
        text (str): Raw input text string.

    Returns:
        str: Cleaned and normalized text with space-separated tokens.
    """

    text = text.lower()

    # Remove URLs (http/https and www)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Expand contractions (e.g., "don't" -> "do not")
    text = contractions.fix(text)

    # Remove standard punctuation
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    # Remove digits/numbers
    text = re.sub(r'\d+', '', text)

    # Remove emojis
    text = emoji.replace_emoji(text, replace='')

    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize text
    tokens = word_tokenize(text)

    # Remove English stop words
    tokens = [
        token
        for token in tokens
        if token not in stop_words
    ]

    # Lemmatize words to their root forms
    tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
    ]

    return " ".join(tokens)