filename = "bgpdumpers.txt"

prefixToHops = defaultdict(set())

with open(filename, 'r') as fp:
	for line in fp:
		splitLine = line.split('|')
		if splitLine[2] == 'A':
			prefixToHops[splitLine[5]].add(splitLine[6].split()[0])
		elif splitLine[2] == 'W':
			prefixToHops[splitLine[5]].remove(splitLine[6].split()[0])


nextHops = set([pair[1] for pair in prefixHopPairs])
prefixes = set([pair[0] for pair in prefixHopPairs])


print("%d nexthops, %d prefixes" % (len(nextHops), len(prefixes)))

prefixToHops = {prefix:[] for prefix in prefixes}
for (prefix, hop) in prefixHopPairs:
    prefixToHops[prefix].append(hop)

counts = set([len(set(hopset)) for hopset in prefixToHops.values()])
print(counts)
