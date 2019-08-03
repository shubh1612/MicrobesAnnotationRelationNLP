with open('dist.txt', 'r') as file:
	data = file.readlines()
data = [x.strip() for x in data]

dict = {}

for sent in data:
	words = sent.split()
	if len(words) == 0:
		continue
	if words[0] not in dict:
		dict[words[0]] = {}
	if int(words[1][1:]) in dict[words[0]]:
		dict[words[0]][int(words[1][1:])] = min(int(words[2]), dict[words[0]][int(words[1][1:])])
	else:
		dict[words[0]][int(words[1][1:])] = int(words[2])

print(dict['A08__7.txt'][4])
print(dict['14A__8.txt'][5])
print(dict['14_Molecular_characterization_of_bacterial_communities__10.txt'][11])
print(dict['16_es960793i__1.txt'][8])
