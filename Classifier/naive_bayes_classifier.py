import re
import pickle
import nltk
import os
import sys
import pymysql
import json
import collections
import csv
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

package_path = os.path.dirname(os.path.realpath(__file__))
base_dir = os.path.dirname(package_path)
base_output_dir = os.path.join(base_dir, "Sentiments")
stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
results = dict()
classifier = None
word_features = None

# get training data set from online corpus tweet["text"],tweet["label"]
def load_training_data(training_data_file_name):
    data = list()
    with open(training_data_file_name, encoding='utf8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if len(row) == 5:
                if row[1] == "positive" or row[1] == "negative" or row[1] == "neutral":
                    data.append({
                        'text' : row[4],
                        'label' : row[1]
                    })

    print('Loaded training data')
    return data

def load_test_data(test_data_file_name):
    data = None
    with open(test_data_file_name, encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append({
                'text': row[0],
                'label': None
            })
    print("Loaded test data")
    return data

def build_vocabulary(processed_training_data):
    all_words = []

    for (words, sentiment) in processed_training_data:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = list(wordlist.keys())

    return word_features

def process_tweets(tweets):
    processed_tweets = []
    for tweet in tweets:
        tweet['text'] = tweet['text'].lower() # convert text to lower-case
        tweet['text'] = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet['text']) # remove URLs
        tweet['text'] = re.sub('@[^\s]+', 'AT_USER', tweet['text']) # remove usernames
        tweet['text'] = re.sub(r'#([^\s]+)', r'\1', tweet['text']) # remove the # in #hashtag
        tweet['text'] = word_tokenize(tweet['text']) # remove repeated characters (helloooooooo into hello)
        processed_tweets.append(([word for word in tweet['text'] if word not in stopwords], tweet['label']))
    return processed_tweets

def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features[word] = (word in tweet_words)
    return features

def classify_extract_features(tweet, word_features):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features[word] = (word in tweet_words)
    return features

def save_classifier(nltk_classifier, word_features, file_name="tweet_classifier.pickle"):
    if not file_name.endswith(".pickle"):
        file_name = "{}.pickle".format(file_name)

    output_file = os.path.join(base_dir, file_name)
    with open(output_file, 'wb') as f:
        pickle.dump(nltk_classifier, f)
    print("Classifier saved as {}".format(file_name))

    with open("word_features.txt", "w") as wf:
        for feature in word_features:
            print(feature, file=wf)

def load_classifier():
    classifier_file = os.path.join(base_dir, "tweet_classifier.pickle")
    with open(classifier_file, 'rb') as f:
        classifier = pickle.load(f)
    features = list()
    with open("word_features.txt", 'r') as wf:
        features = wf.read().splitlines()
    return classifier, features

def train_classifier():
    global word_features
    dataset_file = os.path.join(package_path, "trainingset2.csv")
    training_data = load_training_data(dataset_file)
    processed_training_data = process_tweets(training_data)
    # Extract features
    word_features = build_vocabulary(processed_training_data)
    training_features = nltk.classify.apply_features(extract_features, processed_training_data)
    print('Features extracted')
    # Train classifier
    NBayesClassifier = nltk.NaiveBayesClassifier.train(training_features)
    print('Classifier trained')
    # Save classifier
    save_classifier(NBayesClassifier, word_features)
    return NBayesClassifier, word_features

if __name__ == "__main__":
    if not os.path.isdir(base_output_dir):
        try:
            os.mkdir(base_output_dir)
        except OSError:
            print("Failed to create the base output directory.")

    train_classifier(training_data)