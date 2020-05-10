from igraph import *
from utils import *
import matplotlib.pyplot as plt
import os
import pathlib
import json
import numpy as np
from collections import Counter, OrderedDict

plt.style.use('ggplot')

def plot_sentiment():
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

def _plot_community_sizes(data, stream):
    fig, ax = plt.subplots(figsize=(10,6))
    community_sizes = OrderedDict(sorted(Counter([len(x) for x in data.values()]).items(), 
                                            key=lambda x: int(x[0])))
    x = list(community_sizes.keys())
    y = list(community_sizes.values())
    ax.semilogx(x, y, 'ro-')
    ax.set_title(f"{stream} stream: Community Size vs Frequency of Size")
    ax.set_xlabel("Community size (number of hashtags)")
    ax.set_ylabel("Number of communities of size")
    plt.savefig(f"./Plots/{stream.lower()}_community_size_frequency.png")

def plot_communities():
    INPUT_DIR = os.path.join(os.getcwd(), 'Communities')
    community_files = list()
    with os.scandir(INPUT_DIR) as it:
        for f in it:
            if not f.name.startswith('.') and f.is_file():
                community_files.append(os.path.join(INPUT_DIR, f.name))
    
    labels = list()
    total_communities = list()
    for cfile in community_files:
        stream = pathlib.Path(cfile).stem
        if stream == "TF":
            stream = "Adaptive"
        elif stream == "BL":
            stream = "Baseline"
        labels.append(stream)
        with open(cfile) as f:
            data = json.load(f)
        total_communities.append(len(data.keys()))
        _plot_community_sizes(data, stream)
    
    fig, ax = plt.subplots(figsize=(10,6))
    x = np.arange(len(labels))
    ax.bar(x, total_communities, label="Count")
    ax.set_title('Sentiment values for communities of each dataset')
    ax.set_xlabel('Dataset')
    ax.set_ylabel('Number of communities')
    ax.legend()
    plt.xticks(x, labels)
    plt.savefig('./Plots/community_counts.png')

if __name__ == "__main__":
    #plot_sentiment()
    plot_communities()