
import re
import nltk
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

from . import preprocessing


nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()

stemmer = PorterStemmer()


# -----------------------------
# Cleaning Functions
# -----------------------------

def remove_html(text):
    return re.sub(r"<.*?>", "", str(text))


def remove_urls(text):
    return re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        str(text)
    )


def lowercase(text):
    return str(text).lower()


def remove_special_chars(text):
    return re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        str(text)
    )


def remove_stopwords(text):

    words = text.split()

    words = [
        word 
        for word in words 
        if word not in stop_words
    ]

    return " ".join(words)


def lemmatize(text):

    words = text.split()

    words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]

    return " ".join(words)


def stemming(text):

    words = text.split()

    words = [
        stemmer.stem(word)
        for word in words
    ]

    return " ".join(words)


def normalize_spaces(text):

    return re.sub(
        r"\s+",
        " ",
        str(text)
    ).strip()



# -----------------------------
# Single Text Preprocessing
# -----------------------------

def preprocess(text):

    text = remove_html(text)

    text = remove_urls(text)

    text = lowercase(text)

    text = remove_special_chars(text)

    text = remove_stopwords(text)

    text = lemmatize(text)

    text = stemming(text)

    text = normalize_spaces(text)

    return text



# -----------------------------
# Batch Processing Function
# -----------------------------

def preprocess_batch(series, batch_size=5000):

    processed_text = []

    total = len(series)


    for start in range(0, total, batch_size):

        end = min(start + batch_size, total)

        print(
            f"Processing rows {start} - {end}"
        )


        batch = series.iloc[start:end]


        result = batch.apply(preprocess)


        processed_text.extend(result)


    return processed_text

