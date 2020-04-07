import matplotlib.pyplot as plt
import numpy, json, collections

with open('./sentiments/overview.json') as js:
    data = json.load(js)

community_stats = {
    'streams': dict(),
    'total_communities': None
}
for stream_type, communities in data.items():
    print(len(communities))
    base = dict()
    base['total_communities'] = len(communities)
    base['largest_community'] = max(communities, key=lambda x: communities[x]['community_size'])
    base['smallest_community'] = min(communities, key=lambda x: communities[x]['community_size'])
    base['community_sizes'] = [communities[x]['community_size'] for x in communities]
    plt.figure()
    plt.hist(base['community_sizes'],
            bins=len(communities),
            density=True,
            cumulative=True)
    plt.xlabel('Community size')
    plt.ylabel('Probability')
    plt.title('Distribution of community sizes for {} stream'.format(stream_type))
    plt.ylim(0.75, 1)
    plt.grid(True)
    plt.savefig('./plots/{}_community_size_hist.png'.format(stream_type))
    community_stats['streams'][stream_type] = base

streams = community_stats['streams'].keys()
total_community_sizes = [community_stats['streams'][y]['total_communities'] for y in streams]
plt.figure()
plt.bar(x=streams, height=total_community_sizes)
plt.xlabel('Tweet streams')
plt.ylabel('Total number of communities')
plt.title('Total number of communities for all streams')
plt.grid(True)
plt.savefig('./plots/stream_community_size_comparison.png')