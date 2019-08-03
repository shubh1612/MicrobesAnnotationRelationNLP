import numpy as np
from nltk.tokenize import sent_tokenize
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

### Start of program ###
### open the txt files which are listed in file_list.txt 
with open('file_list.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]

### open the ann files which are listed in file_list_1.txt 
with open('file_list_1.txt', 'r') as file2:
	file_names_1 = file2.readlines()
file_names_1 = [x.strip() for x in file_names_1]

### universe/dictionary of words corressponding to each relation
found = []
occurs = []
of = []
act_on = []
carried = []
produce = []
inhibit = []

#for i in range(0,7):
#	fp = open(str(i)+'.txt', 'r', encoding='utf-8')
#	data = fp.read()
#	data = data.split('\n')
#	if(i == 0):
#		found = list(set(data))
#	elif(i==1):
#		occurs = list(set(data))
#	elif(i==2):
#		act_on = list(set(data))
#	elif(i==3):
#		carried = list(set(data))
#	elif(i==4):
#		produce = list(set(data))
#	elif(i==5):
#		of = list(set(data))
#	elif(i==6):
#		inhibit = list(set(data))

### microbes - 0, environment - 1, enzyme - 2, nutrient - 3, process - 4, property - 5, substrate - 6

with open('dist.txt', 'r') as file:
	data = file.readlines()
data = [x.strip() for x in data]
file.close()

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


fp = open('dict.txt', 'r', encoding='utf-8')
data = fp.read()
data = data.split('\n')
universe_dict = list(set(data))
total = len(universe_dict)
trial_features = np.zeros(9)
universe_dict.extend(trial_features)

found_x = []
occurs_x = []
of_x = []
act_on_x = []
carried_x = []
produce_x = []
inhibit_x = []
found_y = []
occurs_y = []
of_y = []
act_on_y = []
carried_y = []
produce_y = []
inhibit_y = []

def entity_name(entity_type):
	if(entity_type == 'Microbes'):
		return 0
	if(entity_type == 'Environment'):
		return 1
	if(entity_type == 'Enzyme'):
		return 2
	if(entity_type == 'Nutrient'):
		return 3
	if(entity_type == 'ReactionOrProcess'):
		return 4
	if(entity_type == 'Property'):
		return 5
	if(entity_type == 'Substrate'):
		return 6

def relation_name(name):
	if(name == 'FoundIn' or name == 'FoundIn_No'):
		return found_x, found_y
	elif(name == 'CarriedOn' or name == 'CarriedOn_No'):
		return carried_x, carried_y
	elif(name == 'OccursIn' or name == 'OccursIn_No'):
		return occurs_x, occurs_y
	elif(name == 'Of' or name == 'Of_No'):
		return of_x, of_y
	elif(name == 'Produce' or name == 'Produce_No'):
		return produce_x, produce_y
	elif(name == 'Inhibit_Catalyse' or name == 'Inhibit_Catalyse_No'):
		return inhibit_x, inhibit_y
	elif(name == 'ActOn' or name == 'ActOn_No'):
		return act_on_x, act_on_y


def make_file(relation_list, start, end, total, num1, num2, file, distance):

	### name is the type of entity eg. environment, microbes etc.
	#fp = open(mydict[name]+'.txt', 'a', encoding='utf-8')
	index = start
	word = ""
	feature = np.zeros(len(relation_list))
	count = 0
	### loop to go from last character of 1st word till the first character of last word
	while index <= end:
		c = file[int(index)]
		if (c is not (' ' or '\n' or '.')):
			word = word + (c)
		elif ( c == ' ' or '.' or '\n'):
			count = count + 1
			if (word in relation_list):
				idx = relation_list.index(word)
#				print (word, index)
				feature[idx] = 1
			word = ""
		index = index + 1
	if(word in relation_list):
		count = count + 1
		index = relation_list.index(word)
		feature[index] = 1
	feature[total+num1] = 1
	feature[total+num2] = 1
	feature[total+7] = count
	feature[total+8] = distance
	return feature

### index is a 2d array where index[i] denotes the start and end value of entity Ti
### index[i][0] contains the start index of entity Ti and index[i][1] contains the end index of entity Ti
index = np.zeros((10000, 3))

for j in range(len(file_names_1)):
#	print (file_names_1[j])
	with open(file_names[j], 'r', encoding='utf-8') as myfile:
		data=myfile.read()
	with open(file_names_1[j], 'r', encoding='utf-8') as myfile_1:
		data_1=myfile_1.read().replace('\n',' . ')
		data_1=data_1.replace('\t', ' ')

	for sentence in sent_tokenize(data_1):
		text = sentence.split(" ")
		if (text[0][0] == 'R'):
			### if a relation is found in ann file
			### we see if the start of second entity in relation in greater than end of 1st entity
			## it means, we look for the word which comes earlier in document 
			feature_x, label_y = relation_name(text[1])
			#print (text[0][1:])
			if(index[int(text[2][6:])][2] < index[int(text[3][6:])][1]):
				start = index[int(text[2][6:])][2] + 1
				end = index[int(text[3][6:])][1] - 1
			else:
				start = index[int(text[3][6:])][2] + 1
				end = index[int(text[2][6:])][1] - 1				
			num1 = int(index[int(text[2][6:])][0])
			num2 = int(index[int(text[3][6:])][0])
			print (file_names[j], text[0][1:])
			distance = dict[file_names[j]][int(text[0][1:])]
			feature = make_file(universe_dict, start, end, total, num1, num2, data, distance)
			feature_x.append(feature)
			if(text[1][-2:]=='No'):
				label_y.append(0)
			else:
				label_y.append(1)

		elif (text[0][0] == 'T'):
			### make the index array
			num = entity_name(text[1])
			index[int(text[0][1:])][0] = num
			index[int(text[0][1:])][1] = int(text[2])
			index[int(text[0][1:])][2] = int(text[3])

add_label = np.zeros(len(found_y)+len(act_on_y)+len(occurs_y))
feature_string = carried_x
feature_string.extend(act_on_x + found_x + occurs_x)
label_string = carried_y
label_string.extend(add_label)
data_split_ratio = 0.7

"""
##Negative Examples only
test_x = occurs_x
test_y = np.zeros(len(occurs_y))

## training data
train_x = feature_string
train_y = label_string
"""

train_x, test_x, train_y, test_y = train_test_split(feature_string, label_string, train_size = data_split_ratio)
train_neg = 0
for i in range(len(train_y)):
	if (train_y[i] == 0):
		train_neg = train_neg + 1
test_neg = 0
for i in range(len(test_y)):
	if(test_y[i]==0):
		test_neg = test_neg + 1
print ('\n\nNumber of features: ', len(train_x[0]),'\nNumber of training examples: ', len(train_x), '\nNumber of test examples: ', len(test_x))#, ' vds',(test_x[0]))#, (test_y[0]))
print ('\nNegtaive Training Examples: ', train_neg, '\nNegative Test Examples: ', test_neg)

found_classifier = LogisticRegression()
found_classifier.fit(train_x, train_y)

accuracy = found_classifier.score(train_x, train_y)
print ('accuracy of train score: ', accuracy)
accuracy = found_classifier.score(test_x, test_y)
print ('accuracy of test score: ', accuracy)
