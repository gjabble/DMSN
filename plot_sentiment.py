from igraph import *
from utils import *
import matplotlib.pyplot as plt
import os
import json
import numpy as np

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10,6))
INPUT_FILE = os.path.join(os.getcwd(), 'Sentiments', 'sentiments_overview.json')
with open(INPUT_FILE) as f:
    data = json.load(f)

labels = list()
positive_counts = list()
neutral_counts = list()
negative_counts = list()
width = 0.25
for stream, communities in data.items():
    if stream == "TF":
        stream = "Adaptive"
    elif stream == "BL":
        stream = "Baseline"
    labels.append(stream)
    counts = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }
    for cidx, cdata in communities.items():
        sentiment = cdata['sentiment']
        try:
            counts[sentiment] += 1
        except KeyError:
            pass
    positive_counts.append(counts['positive'])
    neutral_counts.append(counts['neutral'])
    negative_counts.append(counts['negative'])

x = np.arange(len(labels))
ax.bar(x, positive_counts, width, color = 'g', label="Positive")
ax.bar(x + width, neutral_counts, width, color = 'b', label="Neutral")
ax.bar(x + 2*width, negative_counts, width, color = 'r', label="Negative")
ax.set_title('Sentiment values for communities of each dataset')
ax.set_xlabel('Dataset')
ax.set_ylabel('Number of communities')
ax.legend()
plt.xticks(x + width, labels)
plt.savefig('./Plots/sentiment_counts.png')