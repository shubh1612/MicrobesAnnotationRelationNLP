#manas
# place this file in some directory "abc"
# in abc keep all the lists of entities - environment, substrate etc.
# in the previous directory make a directory 'training_set'
# inside training_set make another directory 'extra'
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import subprocess
import re
import string

############################################################
# important lists containing probabilities from training data
namepos_list = []
nameneg_list = []
probneg_list = []
probpos_list = []

# Set threshold for making relation between two entities
threshold = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

############################################################
#input microbes,environment etc. as a list 
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
dict = {tuple(M):'Microbes', tuple(E):'Enzyme', tuple(Env):'Environment', tuple(S):'Substrate', tuple(P):'Property', tuple(Pro):'ReactionOrProcess', tuple(N):'Nutrient' }

############################################################
#make list of articles
#subprocess.call('ls ../training_set/trn/ | grep \'.txt\' > ../training_set/extra/file_list.txt' , shell = True)

with open('file_list.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]

############################################################
#function to make relations
def make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, name):
	entity_name.append(name)
	if(dict[tuple(entity)] == 'Microbes'):
		micr.append('T'+str(entity_num))
	elif(dict[tuple(entity)] == 'Environment'):
		envr.append('T'+str(entity_num))
	elif(dict[tuple(entity)] == 'Substrate'):
		subs.append('T'+str(entity_num))
	elif(dict[tuple(entity)] == 'Property'):
		prop.append('T'+str(entity_num))
	elif(dict[tuple(entity)] == 'ReactionOrProcess'):
		proc.append('T'+str(entity_num))
	elif(dict[tuple(entity)] == 'Nutrient'):
		nutr.append('T'+str(entity_num))
	elif(dict[tuple(entity)] == 'Enzyme'):
		enz.append('T'+str(entity_num))

############################################################
# Probability calculate for each relation
def make_relation(x, y, words, entity_name, count):
	ind1 = int(x[1:])
	ind2 = int(y[1:])
	x_start = entity_name[ind1].split(" ")
	y_start = entity_name[ind2].split(" ")
	### print statement
	#print (entity_name, ind2, y_start, len(entity_name))
	###

	if (y_start[0] not in words or x_start[len(x_start)-1] not in words):
		return 0
	ind3 = words.index(x_start[len(x_start)-1])
	ind4 = words.index(y_start[0])
	prob = 0
	#print(ind3,ind4)
	for num in range(ind3+1, ind4):
		if (words[num] in namepos_list[count]) != False:
			ind = namepos_list[count].index(words[num])
			prob = prob + probpos_list[count][ind]
		elif (words[num] in nameneg_list[count]) != False:
			ind = nameneg_list[count].index(words[num])
			prob = prob - probneg_list[count][ind]
	if((prob) >= threshold[count]):
		return True
	return False

############################################################
# make list containing probability for each type of relation
def prob_for_model():
	datapos = []
	dataneg = []
	filepos_names = []
	fileneg_names = []
#	subprocess.call('ls ../training_set/ | grep \'.txt\' > ../training_set/extra/filepos_list.txt' , shell = True)
#	subprocess.call('ls ../training_set/ | grep \'.txt\' > ../training_set/extra/fileneg_list.txt' , shell = True)

### open the file containing the names and load them in a list

	with open('filepos_list.txt', 'r') as filel:
		filepos_names = filel.readlines()
	filepos_names = [x.strip() for x in filepos_names]

	with open('fileneg_list.txt', 'r') as file2:
		fileneg_names = file2.readlines	()
	fileneg_names = [x.strip() for x in fileneg_names]


	### for each of the positive example file

	for i in filepos_names:
		entity_name = []
		entity_prob = []
		with open(i, 'r', encoding='utf-8') as myfile:
			datapos = myfile.readlines()
		prev = datapos[0][:-1]
		count = 1;
		for x in range(1,len(datapos)-1):
			if(datapos[x] == prev):
				count+=1
			else:
				entity_name.append(prev)
				entity_prob.append((count/len(datapos)))
				prev = datapos[x][:-1]
				count = 1
		if(prev == datapos[len(datapos)-1]):
			count += 1
		else:
			entity_name.append(prev)
			entity_prob.append((count/len(datapos)))
			prev = datapos[len(datapos)-1]
			count = 1			
		entity_name.append(prev)
		entity_prob.append((count/len(datapos)))
		namepos_list.append(entity_name)
		probpos_list.append(entity_prob)

	for i in fileneg_names:
		entity_name = []
		entity_prob = []
		with open(i, 'r', encoding='utf-8') as myfile:
			dataneg = myfile.readlines()
		if (len(dataneg) == 0):
			continue
		prev = dataneg[0][:-1]
		count = 1;
		for x in range(1,len(dataneg)-1):
			if(dataneg[x] == prev):
				count+=1
			else:
				entity_name.append(prev)
				entity_prob.append((count/len(dataneg)))
				prev = x
				count = 1
		if(prev == dataneg[len(dataneg)-1]):
			count += 1
		else:
			entity_name.append(prev)
			entity_prob.append((count/len(dataneg)))
			prev = dataneg[len(dataneg)-1]
			count = 1			
		entity_name.append(prev)
		entity_prob.append((count/len(dataneg)))
		nameneg_list.append(entity_name)
		probneg_list.append(entity_prob)
	print (len(nameneg_list))
############################################################
# Annotation Code
prob_for_model()
for j in file_names:
	
	with open(j, 'r', encoding='utf-8') as myfile:
		data=myfile.read().replace('\n',' ')
	fp = open(j[:-4]+'.ann', 'w', encoding='utf-8')
	
	entity_num = 0
	char_num = 0
	rel_num = 0
	entity_name = []
	entity_name.append('Random')

	for sentence in sent_tokenize(data):
		lowered_sent = sentence.lower()
		micr = []
		envr = []
		subs = []
		enz  = []
		prop = []
		proc = []
		nutr = []

		#################################################
		# list to store the name for each entity type
		
		for entity in l:
			for obj in entity:
				obj = obj.lower()

				# Annotate entities

				if (' '+obj+' ' in lowered_sent )!= False:
					#print (obj + '0')
					obj_starts = (m.start() for m in re.finditer(' '+obj+' ', lowered_sent))
					for i in obj_starts:
						start = char_num + i + 1 # extra space before
						entity_num += 1
						fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
						make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, sentence[i+1 : i+1+len(obj)])
				punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'		
				for punc in punctuation:
					if (' '+obj+punc in lowered_sent )!= False:
						#print (obj + '1')
						obj_starts = (m.start() for m in re.finditer(' '+obj+re.escape(punc), lowered_sent))
						for i in obj_starts:
							start = char_num + i + 1 # extra space before
							entity_num += 1
							fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
							make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, sentence[i+1 : i+1+len(obj)])

				if (obj in lowered_sent and obj[0:len(obj)] == lowered_sent[0:len(obj)])!= False:
				#	print (obj + '2')
					start = char_num
					entity_num += 1
					fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[0 : len(obj)] +'\n')
					make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, sentence[0 : len(obj)])

				obj = obj + 's'

				
				if (' '+obj+' ' in lowered_sent )!= False:
					#print (obj + '3')
					obj_starts = (m.start() for m in re.finditer(' '+obj+' ', lowered_sent))
					for i in obj_starts:
						start = char_num + i + 1 # extra space before
						entity_num += 1
						fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
						make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, sentence[i+1 : i+1+len(obj)])
				punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'		
				for punc in punctuation:
					if (' '+obj+punc in lowered_sent )!= False:
						obj_starts = (m.start() for m in re.finditer(' '+obj+re.escape(punc), lowered_sent))
						for i in obj_starts:
							start = char_num + i + 1 # extra space before
							entity_num += 1
							fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
							make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, sentence[i+1 : i+1+len(obj)])

				if (obj in lowered_sent and obj[0:len(obj)] == lowered_sent[0:len(obj)])!= False:
					# print(obj + ' 1212\n')
					start = char_num
					entity_num += 1
					fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[0 : len(obj)] +'\n')
					make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz, entity_name, sentence[0 : len(obj)])	

		char_num += len(sentence) + 1
		if len(sentence) == 1:
			char_num += 1
		words = word_tokenize(sentence)

		# Make relations based on co-occurences

		for x in micr:
			for y in envr:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 0)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'FoundIn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in prop:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 1)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'Of'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in subs:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 2)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'ActOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in micr:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 4)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'CarriedOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in enz:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 3)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'Produce'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in subs:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 4)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'CarriedOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in envr:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 5)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'OccursIn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in enz:
			for y in proc:
				#print (x, y)
				if(make_relation(x, y, words, entity_name, 6)):
					rel_num += 1
					fp.write('R'+str(rel_num)+'\t'+'Inhibit_Catalyse'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		
	fp.close()
	myfile.close()
	print(j)

############################################################
