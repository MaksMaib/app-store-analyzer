import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import copy
import pandas as pd
from sklearn.metrics import accuracy_score
import io
import base64


def preprocess_text(text):

    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    processed_text = ' '.join(lemmatized_tokens)

    return processed_text

def preprocess_negative_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = word_tokenize(text)  # Tokenization
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
    return tokens

def get_sentiment(text):
    """Compound score > 0.05: Positive sentiment
        Compound score < -0.05: Negative sentiment
        Compound score between -0.05 and 0.05: Neutral sentiment"""
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    if scores['compound'] > 0.05:
        sentiment = 'positive'
    elif scores['compound'] < -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment


def create_insights(data):
    insights_data = copy.deepcopy(data)
    insights_data['review_proc'] = insights_data['review'].apply(preprocess_text)
    insights_data['title_proc'] = insights_data['title'].apply(preprocess_text)
    insights_data['sentiment_review'] = insights_data['review_proc'].apply(get_sentiment)
    insights_data['sentiment_title'] = insights_data['title_proc'].apply(get_sentiment)

    insights_data['rating_gt'] = pd.cut(insights_data['rating'],
                                     bins=[0, 2, 3, 5],  #(0,2] negative, (2,3] neutral, (3,5] positive
                                     labels=['negative', 'neutral', 'positive'])

    accuracy_title = accuracy_score(insights_data['rating_gt'], insights_data['sentiment_title'])
    accuracy_review = accuracy_score(insights_data['rating_gt'], insights_data['sentiment_review'])
    return {'insights_data':insights_data, 'accuracy_title':accuracy_title, 'accuracy_review':accuracy_review}

def commonn_words(data, source='review'):

    negative_comments = data[data['rating_gt'] == 'negative'].reindex()

    common_phrases_list = common_phrases(negative_comments[source])

    negative_comments['Tokens'] = negative_comments[source].apply(preprocess_negative_text)
    all_words = [word for tokens in negative_comments['Tokens'] for word in tokens]

    word_freq = Counter(all_words)
    common_words = word_freq.most_common(10)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    img_io = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(img_io, format="png", bbox_inches="tight", pad_inches=0)
    plt.close()
    img_io.seek(0)
    base64_img = base64.b64encode(img_io.read()).decode("utf-8")
    return common_words, common_phrases_list,  base64_img

def common_phrases(data):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(2, 2))  # Unigrams & Bigrams
    X = vectorizer.fit_transform(data)
    tfidf_scores = dict(zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0)))
    sorted_tfidf = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:10]

    top_phrases = [phrase for phrase, score in sorted_tfidf]
    return top_phrases