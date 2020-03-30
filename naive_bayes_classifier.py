# Step D.1: Building the vocabulary
# Step D.2: Matching tweets against our vocabulary
# Step D.3: Building our feature vector
# Step D.4: Training the classifier

import csv
import re
import pickle
import nltk
import sys
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
test_data = []
test_data_file_name = sys.argv[1] if 1 <= len(sys.argv) else 'AD.csv'
classifier = None

# get training data set from online corpus tweet["text"],tweet["label"]
def load_training_data(training_data_file_name):
    data = list()
    with open(training_data_file_name, encoding='utf8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if len(row) == 5:
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

def build_vocabulary(preprocessedTrainingData):
    all_words = []

    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()

    return word_features

def process_tweets(tweets):
    processed_tweets = []
    for tweet in list_of_tweets:
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        processed_tweets.append([word for word in tweet if word not in stopwords])
    return processed_tweets

def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)' % word]=(word in tweet_words)
    return features

def save_classifier(nltk_classifier, file_name="tweet_classifier"):
    f = open("{}.pickle".format(file_name), 'wb')
    pickle.dump(nltk_classifier, f)
    f.close()
    print("Classifier saved as {}.pickle".format(file_name))

# Check if we have already trained a Classifier
# if so then load otherwise create one and train it
NBayesClassifier = None
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
    save_classifier(NBayesClassifier)
else:
    f = open("tweet_classifier.pickle", 'rb')
    NBayesClassifier = pickle.load(f)
    f.close()

processed_test_data = process_tweets(test_data)

NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in processed_test_data]

print('Tested')

# get the majority vote
if NBResultLabels.count('positive') > NBResultLabels.count('negative'):
    print("Overall Positive Sentiment")
    print("Positive Sentiment Percentage = " + str(100*NBResultLabels.count('positive')/len(NBResultLabels)) + "%")
else:
    print("Overall Negative Sentiment")
    print("Negative Sentiment Percentage = " + str(100*NBResultLabels.count('negative')/len(NBResultLabels)) + "%")
