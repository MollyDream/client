from collections import defaultdict

filename = "peers.csv"

with open(filename, 'r') as fp:
        fp.readline()
        ASset = set([line.split(',')[2] for line in fp])

with open(filename, 'r') as fp:
        fp.readline()
        sessiontoLine = {int(line.split(',')[-1].rstrip()):line.rstrip() for line in fp}

filename = "fulldumpers.txt"

prefixtoAS = defaultdict(set)
pathIDtoAS = defaultdict(set)
pathIDtoSession = defaultdict(set)

ASnotInSet = defaultdict(set)

with open(filename, 'r') as fp:
        AS = ''
        pathID = ''
        oldPathID = ''
        prefix = ''
        session = ''
        flag = 0
        firstNLRI = 0
        for line in fp:
                line = line.rstrip()
                if "            Path Segment Value: " in line:
                        AS = line.replace("            Path Segment Value: ", '').split(' ')[0]
                if "        COMMUNITY: " in line:
                        line = line.replace("        COMMUNITY: ", '')
                        sessionMap = {pair.split(":")[0] : pair.split(":")[1] for pair in line.split(' ')}
                        session = sessionMap["47065"]
                if "        Path Identifier: " in line:
                        pathID = line.replace("        Path Identifier: ", '')
                        if firstNLRI == 0:
                                firstNLRI = 1
                        elif flag == 1:
                                assert oldPathID == pathID
                        oldPathID = pathID
                        if flag == 1:
                                pathIDtoAS[pathID].add(AS)
                                pathIDtoSession[pathID].add(session)
                                if AS not in ASset:
                                        ASnotInSet[pathID].add(AS)
                if line == "    NLRI":
                        flag = 1
                if line == "    Withdrawn Routes":
                        flag = 2
                if line == "---------------------------------------------------------------":
                        firstNLRI = 0
                if "        Prefix: " in line:
                        prefix = line.replace("        Prefix: ", '')
                        if flag == 1:
                                prefixtoAS[prefix].add(AS)
                        if flag == 2:
                                prefixtoAS[prefix] = set([AS for AS in prefixtoAS[prefix] if AS not in pathIDtoAS[pathID]])
                                if len(prefixtoAS[prefix]) == 0:
                                        del prefixtoAS[prefix]

print("\n Changing session for pathID: ", {key:value for key, value in pathIDtoSession.items() if len(value) > 1})
print("\n Changing AS for session: ")
sessiontoAS = {list(pathIDtoSession[key])[0] : value for key, value in pathIDtoAS.items() if len(value) > 1}
for key, value in sessiontoAS.items():
        print("session ID: ", key)
        print("peer Info: ", sessiontoLine[int(key)-10000])
        print("Next-Hop ASes: ", value)
print("\n Session for not-in ASes: ", {key : pathIDtoSession[key] for key in ASnotInSet.keys()})
print("\n not-in ASes: ", ASnotInSet.keys())

prefixes = set(prefixtoAS.keys())
nextHops = set.union(*list(prefixtoAS.values()))

print("\n %d nexthops, %d prefixes" % (len(nextHops), len(prefixes)))
counts = set([len(set(hopset)) for hopset in prefixtoAS.values()])
print(counts)

print("\n count of in ASes: ", len(ASset))
print("\n count of intersecting ASes: ", len(ASset.intersection(nextHops)))
