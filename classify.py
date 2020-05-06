import nltk, pickle, pymysql, json, os, collections
from Classifier import naive_bayes_classifier as nbc

base_dir = os.path.join(os.getcwd(), 'Communities')
base_output_dir = os.path.join(os.getcwd(), 'Sentiments')
connection = pymysql.connect(
    host='localhost',
    user='root',
    password=os.environ.get('MYSQL_PWD'),
    db='ecs637u_digitalmedia',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    NBayesClassifier, word_features = nbc.load_classifier()
    print("Loaded classifier...")
except FileNotFoundError:
    print("Classifier not found.")
    print("Training classifier...")
    NBayesClassifier, word_features = nbc.train_classifier()

results = dict()
for community_file in os.listdir(base_dir):
    stream_type = community_file.split('.')[0]
    results[stream_type] = dict()
    with open(os.path.join(base_dir, community_file)) as f:
        communities = json.load(f)

    for idx, community in communities.items():
        hashtags = community
        tweets = list()
        with connection:
            cursor = connection.cursor()
            table_name = "glaston29_{}".format(stream_type)
            base_query = "SELECT `tweet` FROM {} WHERE ".format(table_name)
            conditions = list()
            for tag in community:
                condition = "`hashtags` LIKE '%{}' OR `hashtags` LIKE '%{} '".format(tag, tag)
                conditions.append(condition)
            query = base_query + " OR ".join(conditions)
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                tweets.append({
                    'text': row['tweet'],
                    'label': None
                })
        tweet_count = len(tweets)
        processed_data = nbc.process_tweets(tweets)
        NBResultLabels = collections.Counter(
            [NBayesClassifier.classify(nbc.classify_extract_features(tweet[0], word_features)) for tweet in processed_data]
        )
        try:
            sentiment = NBResultLabels.most_common()[0][0]
            probability = float(NBResultLabels.most_common()[0][1]/sum(NBResultLabels.values()))
        except:
            sentiment = "unknown"
            probability = None
        print("Community {} sentiment: {} -> {}".format(idx, sentiment, probability))
        results[stream_type][idx] = {
            'community_size': len(hashtags),
            'tweet_count': tweet_count,
            'sentiment': sentiment,
            'probability': probability
        }

    output_path = os.path.join(base_output_dir, "{}_sentiments.json".format(stream_type))
    with open(output_path, 'w') as res:
        json.dump(results[stream_type], res)
        print("Output {} data to file {}".format(stream_type, output_path))

    output_path = os.path.join(base_output_dir, "sentiments_overview.json")
    with open(output_path, 'w') as res:
        json.dump(results, res)