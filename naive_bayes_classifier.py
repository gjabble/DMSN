# Step D.1: Building the vocabulary
# Step D.2: Matching tweets against our vocabulary
# Step D.3: Building our feature vector
# Step D.4: Training the classifier

import csv
import re
import pickle
import nltk
import os
import sys
import pymysql
import json
import collections
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

input_directory = os.path.join(os.getcwd(), "communities")
base_output_dir = os.path.join(os.getcwd(), "sentiments")
stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
results = dict()
classifier = None
connection = pymysql.connect(
    host='localhost',
    user='root',
    password=os.environ.get('MYSQL_PWD'),
    db='ecs637u_digitalmedia',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

if not os.path.isdir(base_output_dir):
    try:
        os.mkdir(base_output_dir)
    except OSError:
        print("Failed to create the base output directory.")

# get training data set from online corpus tweet["text"],tweet["label"]
def load_training_data(training_data_file_name):
    data = list()
    with open(training_data_file_name, encoding='utf8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if len(row) == 5:
                if row[1] == "positive" or row[1] == "negative":
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

def load_hashtags(file_name):
    data = list()
    with open(file_name, encoding='utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 2:
                data.append({
                    'text': row[1],
                    'label': None
                })

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

def save_classifier(nltk_classifier, word_features, file_name="tweet_classifier"):
    f = open("{}.pickle".format(file_name), 'wb')
    pickle.dump(nltk_classifier, f)
    f.close()
    print("Classifier saved as {}.pickle".format(file_name))
    with open("word_features.txt", "w") as wf:
        for feature in word_features:
            print(feature, file=wf)

def load_classifier():
    f = open("tweet_classifier.pickle", 'rb')
    classifier = pickle.load(f)
    f.close()
    features = list()
    with open("word_features.txt", 'r') as wf:
        features = wf.read().splitlines()
    return classifier, features


# Check if we have already trained a Classifier
# if so then load otherwise create one and train it
NBayesClassifier = None
word_features = None
if os.path.isfile("tweet_classifier.pickle") is not True:
    corpus_file = 'trainingset2.csv'
    training_data = load_training_data(corpus_file)
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
else:
    NBayesClassifier, word_features = load_classifier()


for stream_type in os.listdir(input_directory):
    community_dir = os.path.join(input_directory, stream_type)
    results[stream_type] = dict()
    print("Processing stream: {}".format(stream_type))
    for community in os.listdir(community_dir):
        data = list()
        hashtags = list()
        data_path = os.path.join(community_dir, community)
        print("Processing community: {}".format(community))
        with open(data_path, 'r') as f:
            hashtags = f.read().splitlines()
            print("Hashtags: {}".format(hashtags))

        with connection:
            cursor = connection.cursor()
            table_name = "glaston29_{}".format(stream_type)
            base_query = "SELECT `tweet` FROM {} WHERE ".format(table_name)
            conditions = list()
            for tag in hashtags:
                #query = "SELECT `tweet` FROM {} WHERE `hashtags` LIKE '%{}' OR `hashtags` LIKE '%{} ';".format(table_name, tag, tag)
                condition = "`hashtags` LIKE '%{}' OR `hashtags` LIKE '%{} '".format(tag, tag)
                conditions.append(condition)
            query = base_query + " OR ".join(conditions)
            #print("Executing query: {}".format(query))
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                data.append({
                    'text': row['tweet'],
                    'label': None
                })
        processed_data = process_tweets(data)
        NBResultLabels = collections.Counter(
            [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in processed_data]
        )
        #NBResultLabels = NBayesClassifier.classify_many([extract_features(tweet[0]) for tweet in processed_data])
        try:
            print(NBResultLabels.most_common())
            sentiment = NBResultLabels.most_common()[0][0]
            probability = float(NBResultLabels.most_common()[0][1]/sum(NBResultLabels.values()))
        except:
            sentiment = "unknown"
            probability = None
        print("Community {} sentiment: {} -> {}".format(community, sentiment, probability))
        results[stream_type][community] = {
            'community_size': len(hashtags),
            'sentiment': sentiment,
            'probability': probability
        }

    output_path = os.path.join(base_output_dir, "{}.json".format(stream_type))
    with open(output_path, 'w') as res:
        json.dump(results[stream_type], res)
        print("Output {} data to file {}".format(stream_type, output_path))

    output_path = os.path.join(base_output_dir, "overview.json")
    with open(output_path, 'w') as res:
        json.dump(results, res)
