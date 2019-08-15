
filename = "bgpdumpers.txt"

fp =  open(filename, 'r')
splitLines = [line.split('|') for line in fp]
prefixHopPairs = [(line[5], line[6].split()[0]) for line in splitLines if line[2] == 'A']
print(prefixHopPairs[:10])

nextHops = set([pair[1] for pair in prefixHopPairs])
prefixes = set([pair[0] for pair in prefixHopPairs])

print("%d nexthops, %d prefixes" % (len(nextHops), len(prefixes)))

prefixToHops = {prefix:[] for prefix in prefixes}
for (prefix, hop) in prefixHopPairs:
    prefixToHops[prefix].append(hop)

counts = set([len(set(hopset)) for hopset in prefixToHops.values()])
print(counts)
