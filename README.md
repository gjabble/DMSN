# Group 55 Deliverable 2

Directory structure:
```
.
├── Classifier/
├── Communities/
├── edge_lists/
├── Plots/
├── Report/
├── Sentiments/
├── classify.py
├── co_occurrence.py
├── community_detection.py
├── louvain.py
├── network_stats.py
├── plot_sentiment.py
├── README.md
├── tweet_classifier.pickle
├── utils.py
└── word_features.txt
```

## Classifier
Contains all the code used to train the classifier and the training dataset. 

Further explanation can be found within the folder's README.

## Communities
Folder containing JSON files representing the communities. The JSON files are produced by running `community_detection.py`. It uses a function `save_communities` which can be found in `utils.py` to save the JSON files. 

Each file is a dictionary where the keys are the community index and the values are a list of the hashtags which make up the community.

## edge_lists/
Folder containing the edge lists produced by `co_occurrence.py`. There are several variants of the file, each stream type has a variant that is:
    
- not weighted and has no header
- weighted and has a header
- weighted and has no header

## Plots
Folder containing plots produced by `network_stats.py` and `plot_sentiment.py`. These plots will be used as part of the report.

## Report
Folder containing files related to the final written report. Final report is written in Latex so this contains the tex file, the pdf, other miscellaneous Latex files, an `images` folder for figures used in the report, and a `code` folder for code snippets contained in the report.

## Sentiments
Contains the sentiment outputs by running `classify.py`. Each file is in JSON format the same as in __Communities/__ above. The keys are the community index and the values are a dictionary with data about the community. There is also an overview file which contains all data about all communties from each dataset.

## `classify.py`
Uses the Naive Bayes classifier trained from code in the __Classifier/__ folder to produce an overall sentiment of *positive*, *neutral*, or *negative*. Reads the data from the __Communities/__ folder to obtain the hashtag communities. For each community it builds a SQL query to obtain all the tweets which have used at least one of the hashtags in the community. The classifier is then used on these tweets to produce a final sentiment output.

More detailed explanation of how the output data is structured can be found in the __Sentiments/__ folder.

## `co_occurrence.py`
Reads community data from the SQL database to produce co-occurrence lists which can be read by igraph and Gephi. Results are saved in __edge\_lists/__.

## `community_detection.py`
Performs community detection using the `igraph` package and its `community_multilevel` method. This method implements the agglomerative Louvain community detection algorithm. We use it to find the communities for each dataset. Results are output to __Communities/__.

## `louvain.py`
Not actually sure whether this is still being used. **`TO BE UPDATED`**

## `network_stats.py`
Prints network statistics to the terminal and produces a log-log graph of the node degree for every stream. 

## `plot_results.py`
Plots the results found, so generates a plot for community detection and a plot for sentiment data. Sentiment data plots every stream on a single bar chart where each stream has three bars representing the total number of *positive*, *neutral*, and *negative* communities.

## `tweet_classifier.pickle`
The saved classifier. This is produced by running `./Classifier/naive_bayes_classifier.py` or `classify.py` which in turn runs the former if this file does not exist. 

Needed to perform any classification.

## `utils.py`
File containing useful functions for use in the above so as not to repeatedly define the same functions and make each files purpose less clear. 

## `word_features.txt`
Word features found by the classifier. This is produced by running `./Classifier/naive_bayes_classifier.py` or `classify.py` which in turn runs the former if this file does not exist. 

Needed to perform any classification.