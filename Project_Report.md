# Final Project Report: Natural Language Processing Pipeline for Video Game Sentiment & QA Analysis
**Dataset Focus:** Cyberpunk 2077 (Steam Reviews)

---

## 1. Project Overview & The "Mega-Scope"

This project is a massive, two-part Data Science pipeline designed to process unstructured internet text.
* **Part 1 (Supervised Learning):** We built a Sentiment Analysis engine to gauge the overall emotional temperature of the community.
* **Part 2 (Unsupervised Learning):** Realizing that simple sentiment isn't actionable enough for developers, we built an Unsupervised QA (Quality Assurance) Assistant. This algorithm automatically groups the reviews and extracts exactly *why* the players are happy or angry.

By restricting the dataset to a single game (*Cyberpunk 2077*), the AI was able to accurately learn the context of that specific community, allowing it to discover hyper-specific in-game lore (like the character "Panam" or the slang word "Preem").

---

## 2. The NLP Methods Implemented (Deep Dive)

### Phase 1: Data Collection & Cleaning
**1. API Data Extraction:** Wrote a Python script using the `requests` library to paginate through the Steam API, extracting 100,000 raw JSON review objects.
**2. Regular Expressions (Regex):** Used `re.sub()` to strip URLs, special characters, and numbers.
**3. Tokenization:** Used `nltk.word_tokenize` to split full sentences into arrays of individual words.
**4. Stop-Word Removal:** Filtered out common filler words ("the", "and") while specifically keeping the word "not" to preserve sentiment polarity.
**5. Lemmatization:** Used `WordNetLemmatizer` to reduce words to their dictionary roots (e.g., "crashing" -> "crash"), reducing dimensionality.

### Phase 2: Exploratory Data Analysis (EDA)
**6. Word Frequency & Word Clouds:** Generated visual Word Clouds separating Positive and Negative reviews.
**7. N-Grams Analysis (Bigrams):** Used `CountVectorizer(ngram_range=(2,2))` to find the most common 2-word phrases (e.g., "game crash").
**8. Part-of-Speech (POS) Tagging:** Used NLTK to automatically tag nouns, adjectives, and verbs, proving we can isolate descriptive emotional language.

### Phase 3: Supervised Machine Learning (Sentiment Analysis)
**9. TF-IDF Vectorization:** Converted our cleaned words into a numerical matrix. We chose TF-IDF over Bag of Words because it mathematically penalizes common words and rewards unique words.
**10. Supervised Machine Learning (Logistic Regression):** Trained a Logistic Regression classifier on 80% of the dataset to predict if a review was a "Thumbs Up" or "Thumbs Down".
**11. Model Evaluation:** Tested the model on the remaining 20% unseen data, generating a Confusion Matrix and achieving ~95% Accuracy.

### Phase 4: Unsupervised Learning (The QA Assistant)
**12. K-Means Clustering:** Deployed an unsupervised algorithm to mathematically group the 100,000 reviews into distinct Quality Assurance categories based on vocabulary distance, acting as an automated bug-reporting tool.
**13. Topic Modeling (LDA):** Used Latent Dirichlet Allocation to scan the text and discover 3 hidden themes without any human labeling.

### Phase 5: Advanced Feature Extraction
**14. Time-Series Sentiment Analysis:** Converted UNIX timestamps to `datetime` objects to plot the percentage of positive reviews over a 2-year period, proving the developer's patches successfully stabilized the community's opinion.
**15. Named Entity Recognition (NER):** Used the `spaCy` Deep Learning pipeline to automatically extract Proper Nouns. Proved we can extract exact characters (Johnny Silverhand, Panam, David Martinez) from messy text without a character dictionary.

---

## 3. The Unsupervised QA Assistant Code (K-Means)

```python
from sklearn.cluster import KMeans

print("Initializing the Automated QA Assistant...")

# We use the TF-IDF vectorizer we already built
# Clustering 100,000 reviews into 4 main QA categories
num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
kmeans.fit(X_vectorized) # Notice we do NOT give it the y-labels! The AI learns entirely on its own.

# Assign the AI's discovered cluster labels back to our dataset
df['qa_category'] = kmeans.labels_

print("\n" + "="*50)
print(" 📋 AUTOMATED EXECUTIVE QA REPORT")
print("="*50)

order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

for i in range(num_clusters):
    print(f"\n📁 QA CLUSTER {i+1} (Focus Areas):")
    top_terms = [terms[ind] for ind in order_centroids[i, :10]]
    print("Keywords: " + " | ".join(top_terms))
    
    sample_review = df[df['qa_category'] == i]['review_text'].sample(1).values[0]
    sample_review_clean = " ".join(str(sample_review).split())
    print(f"Example Feedback: \"{sample_review_clean[:200]}...\"")
```
