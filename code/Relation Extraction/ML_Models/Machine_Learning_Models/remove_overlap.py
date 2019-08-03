import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.cross_validation import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import subprocess
import re
import string

################################################################################################
### open diffenet files and list the files in list for which operations need to be performed ###
################################################################################################

### open the txt files which are listed in file_list.txt 
with open('file_list.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]

### open the ann files which are listed in file_list_1.txt 
with open('file_list_1.txt', 'r') as file2:
	file_names_1 = file2.readlines()
file_names_1 = [x.strip() for x in file_names_1]

### open txt files which are listed in file1__ for which new ann are to be made	
with open('file_list_2.txt', 'r') as filel__:
	file_names__ = filel__.readlines()
file_names__ = [x.strip() for x in file_names__]

################################################################################################
### open diffenet files and list the files in list for which operations need to be performed ###
################################################################################################

punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
stemmer = PorterStemmer()  ## Try out Stemming ##
lemma = WordNetLemmatizer() ## Try out Lemmatizing ##
################################################################################################
#input microbes,environment etc. as a list and create dictionary for them
################################################################################################

with open('microbes.txt', 'r', encoding = 'utf-8') as file_1:
	M = file_1.readlines()
M = [x.strip() for x in M]

with open('enzyme.txt', 'r', encoding = 'utf-8') as file_1:
	E = file_1.readlines()
E = [x.strip() for x in E]

with open('environment.txt', 'r', encoding = 'utf-8') as file_1:
	Env = file_1.readlines()
Env = [x.strip() for x in Env]

with open('substrate.txt', 'r', encoding = 'utf-8') as file_1:
	S = file_1.readlines()
S = [x.strip() for x in S]

with open('property.txt', 'r', encoding = 'utf-8') as file_1:
	P = file_1.readlines()
P = [x.strip() for x in P]

with open('process.txt', 'r', encoding = 'utf-8') as file_1:
	Pro = file_1.readlines()
Pro = [x.strip() for x in Pro]

with open('nutrient.txt', 'r', encoding = 'utf-8') as file_1:
	N = file_1.readlines()
N = [x.strip() for x in N]

l = [M, E, Env, S, P, Pro, N]
dic = {tuple(M):'Microbes', tuple(E):'Enzyme', tuple(Env):'Environment', tuple(S):'Substrate', tuple(P):'Property', tuple(Pro):'ReactionOrProcess', tuple(N):'Nutrient' }


################################################################################################
###### create universe of words list ############
################################################################################################

### create dict
"""
fp = open('dict.txt', 'w', encoding='utf-8')
for j in file_names:
	with open(j, 'r', encoding='utf-8') as myfile__:
		data = myfile__.read()
	words = word_tokenize(data)
	for word in words:
		if (word not in punctuation):
			fp.write(word+'\n')
	myfile__.close()
fp.close()
"""
### Load universe of words from file into list

print ("\nLoading universe of words....\n")
fp = open('dict.txt', 'r', encoding='utf-8')
data = fp.read()
data = data.split('\n')
universe_dict = list(set(data))
universe_dict = [lemma.lemmatize(universe_words) for universe_words in universe_dict]
total = len(universe_dict)
fp.close()

### extend list of universe of words by the extra features that we want to add
trial_features = np.zeros(2)
universe_dict.extend(trial_features)
print ("Universe of words Loading complete.\n")

################################################################################################
###### dependency distance files ############
################################################################################################

with open('dist_sushant_corrected.txt', 'r') as file:
	data = file.readlines()
data = [x.strip() for x in data]

with open('cooccurence_dist.txt', 'r') as file1:
	data1 = file1.readlines()
data1= [x.strip() for x in data1]

dict = {}
test = {}

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

for sent in data1:
	words = sent.split()
	if len(words) == 0:
		continue
	if words[0] not in test:
		test[words[0]] = {}
	if int(words[1][1:]) in test[words[0]]:
		test[words[0]][int(words[1][1:])] = min(int(words[2]), test[words[0]][int(words[1][1:])])
	else:
		test[words[0]][int(words[1][1:])] = int(words[2])

file.close()
file1.close()


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


### function to return the feature vector ###
## relation_list is universe of word list, start is starting character of relation, end in ending character
## total is total number of words in universe of words, num1 and num2 denotes the entity type
## file is txt document, dis is dependency distance between the entities
def make_file(relation_list, start, end, total, num1, num2, file, dis):

	index = start
	word = ""
	feature = np.zeros((len(relation_list)))
	count = 0

	### loop to go from last character of 1st word till the first character of last word
	while index <= end:
		c = file[int(index)]
		if (c not in punctuation):
			word = word + (c)
		elif ( c in punctuation or '\n'):
			count = count + 1
			if (lemma.lemmatize(word) in relation_list):
				idx = relation_list.index(lemma.lemmatize(word))
				feature[idx] = 1
			word = ""
		index = index + 1
	if(lemma.lemmatize(word) in relation_list):
		count = count + 1
		index = relation_list.index(lemma.lemmatize(word))
		feature[index] = 1

	#feature[total+num1] = 1
	#feature[total+num2] = 1
	feature[total] = count
	feature[total+1] = dis
	return feature


## used if creating a new ann file from txt file
def make_relation_list(entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_type):
	if(entity_type == 'Microbes'):
		micr.append('T'+str(entity_num))
	elif(entity_type == 'Environment'):
		envr.append('T'+str(entity_num))
	elif(entity_type == 'Substrate'):
		subs.append('T'+str(entity_num))
	elif(entity_type == 'Property'):
		prop.append('T'+str(entity_num))
	elif(entity_type == 'ReactionOrProcess'):
		proc.append('T'+str(entity_num))
	elif(entity_type == 'Nutrient'):
		nutr.append('T'+str(entity_num))
	elif(entity_type == 'Enzyme'):
		enz.append('T'+str(entity_num))


# Remove Repetitions
def repeat(fp, entity_num, micr, envr, subs, prop, proc, nutr, enz, index):
	with open('trial.ann', 'r', encoding='utf-8') as myfile:
		data=myfile.readlines()
	start = []
	end = []
	check = []
	entity_type = []
	entity_name = []
	for sent in data:
		words = word_tokenize(sent)
		start.append(int(words[2]))
		end.append(int(words[3]))
		entity_type.append(words[1])
		entity_name.append(words[4:])
		check.append(1)
	for i in range(0, len(check)):
		if (check[i]==1):
			for j in range(i+1, len(start)):
				if (start[i] >= start[j] and end[i] <= end[j]):
					check[i] = 0
				elif (start[i] <= start[j] and end[i] >= end[j]):
					check[j] = 0
			if (check[i]==1):
				entity_num += 1
				index[entity_num][0] = 0
				index[entity_num][1] = start[i]
				index[entity_num][2] = end[i]
				fp.write('T'+str(entity_num)+'\t'+str(entity_type[i]) +' '+str(start[i])+' '+str(end[i])+'\t'+ str(' '.join(entity_name[i])) +'\n')
				make_relation_list(entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_type[i])
	return entity_num



##############################################################################
#### training starts ############################################################
##############################################################################

print ("Data Loading for training has started .....\n")
### index is a 3d array where index[i] denotes the type, start and end value of entity Ti
### index[i][0] stores integer to denote the type of entity 
### index[i][1] contains the start index of entity Ti and index[i][2] contains the end index of entity Ti
index = np.zeros((10000, 3))

for j in range(len(file_names_1)):
	with open("Sushant Files\\" + file_names[j], 'r', encoding='utf-8') as myfile:
		data=myfile.read()
	with open("Sushant Files\\" + file_names_1[j], 'r', encoding='utf-8') as myfile_1:
		data_1=myfile_1.read().replace('\n',' . ')
		data_1=data_1.replace('\t', ' ')

	for sentence in sent_tokenize(data_1):
		text = sentence.split(" ")
		if (text[0][0] == 'R'):

			### if a relation is found in ann file
			### we see if the start of second entity in relation in greater than end of 1st entity
			## it means, we look for the word which comes earlier in document 
			feature_x, label_y = relation_name(text[1])
			if(index[int(text[2][6:])][2] < index[int(text[3][6:])][1]):
				start = index[int(text[2][6:])][2] + 1
				end = index[int(text[3][6:])][1] - 1
			else:
				start = index[int(text[3][6:])][2] + 1
				end = index[int(text[2][6:])][1] - 1				
			
			## num1 and num2 denote the entity types
			num1 = int(index[int(text[2][6:])][0])
			num2 = int(index[int(text[3][6:])][0])

			## dis is dependency distance between entities
			dis = dict[file_names[j]][int(text[0][1:])]

			feature = make_file(universe_dict, start, end, total, num1, num2, data, dis)
			feature_x.append(feature)
			
			if(text[1][-2:]=='No'):
				label_y.append(0)
			else:
				label_y.append(1)

		elif (text[0][0] == 'T'):
			
			### make the index array defined at the beginning of loop
			num = entity_name(text[1])
			index[int(text[0][1:])][0] = num
			index[int(text[0][1:])][1] = int(text[2])
			index[int(text[0][1:])][2] = int(text[3])
	
	myfile.close()
	myfile_1.close()

print ("Data Loading for training has completed .....\n")

### define the classifiers and start training on the classifiers

print ("Training the classifiers.....")

train_x = found_x + act_on_x + of_x
train_y = found_y
length = len(found_y)
train_y.extend(np.zeros(len(act_on_y) + len(of_y)))
found_clf = LogisticRegression()
found_clf.fit(train_x, train_y)
found_y = found_y[0:length]

train_x = carried_x + found_x + act_on_x + occurs_x
train_y = carried_y
length = len(carried_y)
train_y.extend(np.zeros(len(act_on_y) + len(found_y) + len(occurs_y)))
carried_clf = LogisticRegression()
carried_clf.fit(train_x, train_y)
carried_y = carried_y[0:length]

train_x = occurs_x + found_x + of_x
train_y = occurs_y
length = len(occurs_y)
train_y.extend(np.zeros(len(found_y) + len(of_y)))
occurs_clf = LogisticRegression()
occurs_clf.fit(train_x, train_y)
occurs_y = occurs_y[0:length]

train_x = act_on_x + of_x
train_y = act_on_y
length = len(act_on_y)
train_y.extend(np.zeros(len(of_y)))
act_clf = LogisticRegression()
act_clf.fit(train_x, train_y)
act_on_y = act_on_y[0:length]

train_x = of_x + act_on_x
train_y = of_y
length = len(of_y)
train_y.extend(np.zeros(len(act_on_y)))
of_clf = LogisticRegression()
of_clf.fit(train_x, train_y)
of_y = of_y[0:length]

print ("Training completed....\n")
##############################################################################
#### training end ############################################################
##############################################################################



##############################################################################
#### testing starts ############################################################
##############################################################################

print ("Testing started.....\n")

### Program Starts ##############################################################################
### Code for Co-ocurence. Reads ann file and produces a new ann file after applying the model ###
### Runs on similar line as the code for training to extract feature vector #####################
index = np.zeros((10000, 3))

for j in range(len(file_names_1)):
	with open("Co-occurence files\\" + file_names[j], 'r', encoding='utf-8') as myfile:
		data=myfile.read()
	with open("Co-occurence files\\" + file_names_1[j][:-4] + '__.ann', 'r', encoding='utf-8') as myfile_1:
		data_1=myfile_1.read().replace('\n',' . ')
		data_1=data_1.replace('\t', ' ')
	
	### fp is the new ann file after using the model
	fp = open("Test Data Files\\" + file_names_1[j], 'w', encoding='utf-8')

	for sentence in sent_tokenize(data_1):
		text = sentence.split(" ")
		if (text[0][0] == 'R'):

			### if a relation is found in ann file
			### we see if the start of second entity in relation in greater than end of 1st entity
			## it means, we look for the word which comes earlier in document 
			#feature_x, label_y = relation_name(text[1])
			if(index[int(text[2][6:])][2] < index[int(text[3][6:])][1]):
				start = index[int(text[2][6:])][2] + 1
				end = index[int(text[3][6:])][1] - 1
			else:
				start = index[int(text[3][6:])][2] + 1
				end = index[int(text[2][6:])][1] - 1				
			
			num1 = int(index[int(text[2][6:])][0])
			num2 = int(index[int(text[3][6:])][0])

			## Dependency distance already stored
			dis = test[file_names[j]][int(text[0][1:])]

			feature = make_file(universe_dict, start, end, total, num1, num2, data, dis)
			feature = feature.reshape(1, -1)
			
			if(text[1] == "FoundIn"):
				if(found_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			elif(text[1] == "CarriedOn"):
				if(carried_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			elif(text[1] == "OccursIn"):
				if(occurs_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			elif(text[1] == "Of"):
				if(of_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			elif(text[1] == "ActOn"):
				if(act_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			
			elif(text[1] == "Inhibit_Catalyse"):
				## No ML Model since training data is insufficient
				if(1):#carried_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			elif(text[1] == "Produce"):
				if(1):#carried_clf.predict(feature)):
					fp.write(sentence[:-2] + "\n")
			
		elif (text[0][0] == 'T'):
			num = entity_name(text[1])
			index[int(text[0][1:])][0] = num
			index[int(text[0][1:])][1] = int(text[2])
			index[int(text[0][1:])][2] = int(text[3])
			fp.write(sentence[:-2] + "\n")

	print (file_names[j])

	fp.close()
	myfile.close()
	myfile_1.close()

### Code for Co-ocurence. Reads ann file and produces a new ann file after applying the model ###
### Runs on similar line as the code for training to extract feature vector #####################
### Program Ends ################################################################################


"""
############################################################
### function to create new ann files from txt files
############################################################
# Annotation Code

index = np.zeros((10000, 3))
for j in file_names__:
	
	with open(j, 'r', encoding='utf-8') as myfile__:
		data__ = myfile__.read()
		data = data__.replace('\n',' ')
	fp = open(j[:-4] + '__.ann', 'w', encoding='utf-8')
	
	entity_num = 0
	char_num = 0
	rel_num = 0
	for sentence in sent_tokenize(data):
		lowered_sent = sentence.lower()
		micr = []
		envr = []
		subs = []
		enz  = []
		prop = []
		proc = []
		nutr = []
		trial = open('trial.ann', 'w', encoding='utf-8')
		for entity in l:
			for obj in entity:
				
				obj = obj.lower()

				# Annotate entities

				if (' '+obj+' ' in lowered_sent )!= False:
					obj_starts = (m.start() for m in re.finditer(' '+obj+' ', lowered_sent))
					for i in obj_starts:
						start = char_num + i + 1 # extra space before
						trial.write('T0'+'\t'+dic[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
				punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'		
				for punc in punctuation:
					if (' '+obj+punc in lowered_sent )!= False:
						obj_starts = (m.start() for m in re.finditer(' '+obj+re.escape(punc), lowered_sent))
						for i in obj_starts:
							start = char_num + i + 1 # extra space before
							trial.write('T0'+'\t'+dic[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')

				if (obj in lowered_sent and obj[0:len(obj)] == lowered_sent[0:len(obj)])!= False:
					start = char_num
					trial.write('T0'+'\t'+dic[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[0 : len(obj)] +'\n')

				obj = obj+'s'	
				
				if (' '+obj+' ' in lowered_sent )!= False:
					obj_starts = (m.start() for m in re.finditer(' '+obj+' ', lowered_sent))
					for i in obj_starts:
						start = char_num + i + 1 # extra space before
						trial.write('T0'+'\t'+dic[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
				punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'		
				for punc in punctuation:
					if (' '+obj+punc in lowered_sent )!= False:
						obj_starts = (m.start() for m in re.finditer(' '+obj+re.escape(punc), lowered_sent))
						for i in obj_starts:
							start = char_num + i + 1 # extra space before
							trial.write('T0'+'\t'+dic[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')

				if (obj in lowered_sent and obj[0:len(obj)] == lowered_sent[0:len(obj)])!= False:
					start = char_num
					trial.write('T0'+'\t'+dic[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[0 : len(obj)] +'\n')
		trial.close()
		entity_num = repeat(fp, entity_num, micr, envr, subs, prop, proc, nutr, enz, index)
		subprocess.call('del -f trial.ann', shell = True)

		char_num += len(sentence) + 1
		if len(sentence) == 1:
			char_num += 1

	# Make relations based on co-occurences or ML Model

		for x in micr:
			for y in envr:
				if(index[int(x[1:])][1] < index[int(y[1:])][0]):
					start = index[int(x[1:])][2] + 1
					end = index[int(y[1:])][1] - 1
				else:
					start = index[int(y[1:])][2] + 1
					end = index[int(x[1:])][1] - 1				
				input_vect = make_file(universe_dict, start, end, total, 0, 1, data__)
				input_vect = input_vect.reshape(1, -1)
				if (1):#found_clf.predict(input_vect)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'FoundIn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in prop:
				if(index[int(x[1:])][1] < index[int(y[1:])][0]):
					start = index[int(x[1:])][2] + 1
					end = index[int(y[1:])][1] - 1
				else:
					start = index[int(y[1:])][2] + 1
					end = index[int(x[1:])][1] - 1				
				input_vect = make_file(universe_dict, start, end, total, 0, 5, data__, dist)
				input_vect = input_vect.reshape(1, -1)
				if (1):#of_clf.predict(input_vect)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'Of'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in subs:
				if(index[int(x[1:])][1] < index[int(y[1:])][0]):
					start = index[int(x[1:])][2] + 1
					end = index[int(y[1:])][1] - 1
				else:
					start = index[int(y[1:])][2] + 1
					end = index[int(x[1:])][1] - 1				
				input_vect = make_file(universe_dict, start, end, total, 0, 6, data__)
				input_vect = input_vect.reshape(1, -1)
				if (1):#act_clf.predict(input_vect)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'ActOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in micr:
				if(index[int(x[1:])][1] < index[int(y[1:])][0]):
					start = index[int(x[1:])][2] + 1
					end = index[int(y[1:])][1] - 1
				else:
					start = index[int(y[1:])][2] + 1
					end = index[int(x[1:])][1] - 1				
				input_vect = make_file(universe_dict, start, end, total, 5, 0, data__)
				input_vect = input_vect.reshape(1, -1)
				if (1):#carried_clf.predict(input_vect)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'CarriedOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in enz:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'Produce'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in subs:
				if(index[int(x[1:])][1] < index[int(y[1:])][0]):
					start = index[int(x[1:])][2] + 1
					end = index[int(y[1:])][1] - 1
				else:
					start = index[int(y[1:])][2] + 1
					end = index[int(x[1:])][1] - 1				
				input_vect = make_file(universe_dict, start, end, total, 5, 6, data__)
				input_vect = input_vect.reshape(1, -1)
				if (1):#carried_clf.predict(input_vect)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'CarriedOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in envr:
				if(index[int(x[1:])][1] < index[int(y[1:])][0]):
					start = index[int(x[1:])][2] + 1
					end = index[int(y[1:])][1] - 1
				else:
					start = index[int(y[1:])][2] + 1
					end = index[int(x[1:])][1] - 1				
				input_vect = make_file(universe_dict, start, end, total, 5, 1, data__)
				input_vect = input_vect.reshape(1, -1)
				if (1):#occurs_clf.predict(input_vect)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'OccursIn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in enz:
			for y in proc:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'Inhibit_Catalyse'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		
	fp.close()
	myfile.close()
	print(j)

subprocess.call('python extra_remove.py', shell = True)

############################################################
### function to create new ann files from txt files
############################################################
"""
print ("Testing Completed....\n")

###########################################################################################
### Calls compare.py file which compares actual ann files with Model generated ML files ###
###########################################################################################

print ("Comparisons of file going on.....")
subprocess.call('python compare.py', shell = True)