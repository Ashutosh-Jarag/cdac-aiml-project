# Standalone script to test preprocessing.pkl and model_svm.pkl in complete isolation
# (no dependency on the Jupyter notebook's in-memory state)

import pickle
import re
import string
import contractions
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ---------- one-time NLTK downloads (safe to run every time, skips if already present) ----------
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# ---------- the exact same preprocessing function used during training ----------
def preprocess_text(text):
    text = text.lower()                                          # lowercase
    text = re.sub(r'https?://\S+|www\.\S+', '', text)              # remove URLs
    text = re.sub(r'<.*?>', '', text)                               # remove HTML tags
    text = contractions.fix(text)                                   # expand contractions
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    text = re.sub(r'\d+', '', text)                                 # remove numbers
    text = emoji.replace_emoji(text, replace='')                    # remove emojis
    text = re.sub(r'[^a-zA-Z\s]', '', text)                          # remove remaining special chars
    tokens = word_tokenize(text)                                    # tokenize
    tokens = [t for t in tokens if t not in stop_words]              # remove stopwords
    tokens = [lemmatizer.lemmatize(t) for t in tokens]                # lemmatize
    return ' '.join(tokens)                                          # rejoin into a string

# ---------- update this path to wherever your models folder actually is ----------
SAVE_DIR = 'C:/Users/hp/Desktop/ML project CDAC/cdac-aiml-project/models'

# ---------- load the preprocessing pickle ----------
with open(f'{SAVE_DIR}/preprocessing.pkl', 'rb') as f:
    preprocessing_artifacts = pickle.load(f)

tfidf = preprocessing_artifacts['tfidf_vectorizer']
mlb = preprocessing_artifacts['mlb_labels']

# ---------- load the trained SVM model pickle ----------
with open(f'{SAVE_DIR}/model_svm.pkl', 'rb') as f:
    svm_clf = pickle.load(f)

print("Loaded preprocessing.pkl and model_svm.pkl successfully.")
print("TF-IDF vocabulary size:", len(tfidf.vocabulary_))
print("Number of categories:", len(mlb.classes_))
print("Category names:", list(mlb.classes_))
print()

# ---------- 4 test cases spanning different subject areas ----------
test_cases = [
    {
        "title": "Deep Learning Approaches for Galaxy Classification in Astronomical Surveys",
        "abstract": "We propose a convolutional neural network architecture for classifying galaxy morphology from large-scale astronomical survey images, achieving state-of-the-art accuracy on benchmark datasets.",
    },
    {
        "title": "A New Algorithm for Solving Sparse Linear Systems",
        "abstract": "We present a novel iterative method for solving large sparse linear systems arising in numerical optimization, with convergence guarantees under mild assumptions.",
    },
    {
        "title": "Quantum Entanglement in Many-Body Systems",
        "abstract": "We study the entanglement entropy of ground states in strongly correlated many-body quantum systems using tensor network methods.",
    },
    {
        "title": "Macroeconomic Effects of Interest Rate Policy",
        "abstract": "This paper examines the transmission mechanism of monetary policy on inflation and unemployment using a dynamic stochastic general equilibrium model.",
    },
]

# ---------- STEP 1: test preprocessing pickle alone ----------
print("=" * 60)
print("STEP 1: Testing preprocessing pickle (cleaning + TF-IDF transform)")
print("=" * 60)

tfidf_vectors = []
for i, case in enumerate(test_cases):
    raw_text = case["title"] + " " + case["abstract"]
    cleaned_text = preprocess_text(raw_text)            # apply manual cleaning
    text_tfidf = tfidf.transform([cleaned_text])          # transform using FITTED vectorizer
    tfidf_vectors.append(text_tfidf)

    print(f"--- Test case {i + 1} ---")
    print("Cleaned text (first 100 chars):", cleaned_text[:100])
    print("TF-IDF vector shape:", text_tfidf.shape)         # should be (1, 30000)
    print("Non-zero features:", text_tfidf.nnz)
    print()

# ---------- STEP 2: test full pipeline including model predictions ----------
print("=" * 60)
print("STEP 2: Testing full pipeline (preprocessing + model prediction)")
print("=" * 60)

for i, case in enumerate(test_cases):
    prediction = svm_clf.predict(tfidf_vectors[i])           # reuse the already-transformed vectors
    predicted_categories = mlb.inverse_transform(prediction)[0]

    print(f"--- Test case {i + 1} ---")
    print("Title:", case["title"])
    print("Predicted categories:", predicted_categories)
    print()

print("All tests completed.")


