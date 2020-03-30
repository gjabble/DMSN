# Step D.1: Building the vocabulary
# Step D.2: Matching tweets against our vocabulary
# Step D.3: Building our feature vector
# Step D.4: Training the classifier

# read tweets out of files and build test set - {'text': '', 'label': ''}
import csv
import re
import pickle
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

testDataSet = []
testDataFileName = 'AD.csv'

with open(testDataFileName, encoding='utf8') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  for row in csv_reader:
    if len(row) == 12:
      testDataSet.append({
        'text': row[5],
        'label': None
      })

print('finished test set')
# get training data set from online corpus tweet["text"],tweet["label"]
corpusFile = 'trainingset2.csv'
trainingData = []
with open(corpusFile, encoding='utf8') as f:
  r = csv.reader(f, delimiter=',')
  for row in r:
    if len(row) == 5:
      trainingData.append({
        'text' : row[4],
        'label' : row[1]
      })
print('finished training set')

# # pre process the tweets in the training set
class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])

    def processTweets(self, list_of_tweets):
        processedTweets=[]
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
        return processedTweets

    def _processTweet(self, tweet):
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]

tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet[:1000])

def buildVocabulary(preprocessedTrainingData):
    all_words = []

    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()

    return word_features

def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:
        features['contains(%s)' % word]=(word in tweet_words)
    return features

def save_classifier(nltk_classifier):
    f = open("tweet_classifier.pickle", 'wb')
    pickle.dump(nltk_classifier, f)
    f.close()

# Now we can extract the features and train the classifier
word_features = buildVocabulary(preprocessedTrainingSet)
trainingFeatures=nltk.classify.apply_features(extract_features,preprocessedTrainingSet)
print('features extracted')

NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)

print('trained')

save_classifier(NBayesClassifier)

NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in preprocessedTestSet]

print('tested')
# NBResultLabels = []
# for tweet in preprocessedTestSet:
#   r = NBayesClassifier.classify(extract_features(tweet[0]))
#   print(r)
#   NBResultLabels.append(r)

# get the majority vote
if NBResultLabels.count('positive') > NBResultLabels.count('negative'):
    print("Overall Positive Sentiment")
    print("Positive Sentiment Percentage = " + str(100*NBResultLabels.count('positive')/len(NBResultLabels)) + "%")
else:
    print("Overall Negative Sentiment")
    print("Negative Sentiment Percentage = " + str(100*NBResultLabels.count('negative')/len(NBResultLabels)) + "%")
