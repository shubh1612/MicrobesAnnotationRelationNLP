import nltk
import subprocess
import re
import queue

# returns dict and adjacency list representation 
def graph(sentence):
	
	with open('input.txt', 'w', encoding = 'utf-8') as file:
		file.write(sentence)

	# auto annotate makes a file input.txt in dependency parse folder 
	subprocess.call('java -cp "..\stanford_nlp_adj_extract\stanford-corenlp-full-2017-06-09\stanford-corenlp-full-2017-06-09\*" -Xmx1g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,depparse -file input.txt', shell = True)

	with open('input.txt.xml', 'r', encoding="UTF-8") as myfile:
		line = myfile.readlines()
	line = [x.strip() for x in line]

	dict_char_begin = {}
	dict_token = {}
	
	dict_token[0] = 'ROOT'

	for i in range(len(line)):
		if '/tokens' in line[i]:
			break
		if 'token id' in line[i]:
			dict_char_begin[int(line[i+2][22:-23])] = int(line[i][11:-2])
			dict_token[int(line[i][11:-2])] = line[i+1][6:-7]

	adj_list = [[] for x in range(len(dict_token) + 1)]

	p = re.compile('\d+')

	for i in range(len(line)):
		if '</dependencies>' in line[i]:
			break
		if 'governor' in line[i]:
			x = int(p.findall(line[i])[0])
			y = int(p.findall(line[i+1])[0])
			adj_list[x].append(y)
			adj_list[y].append(x)

	return [adj_list, dict_char_begin, dict_token]

def dist_n1_n2(adj_list, n1, n2, num):
	dist = [0]*(num+1)
	visited = [0]*(num+1)
	s = queue.Queue(maxsize=0)
	s.put(n1)
	while s.empty() == False:
		pres = s.get()
		if visited[pres] == 0:
			visited[pres]  = 1
			for neigh in adj_list[pres]:
				s.put(neigh)
				dist[neigh] = dist[pres] + 1

		if visited[n2] == 1:
			break

	return dist[n2]