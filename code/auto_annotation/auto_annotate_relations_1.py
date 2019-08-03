# place this file in some directory "abc"
# in abc keep all the lists of entities - environment, substrate etc.

from nltk.tokenize import sent_tokenize, word_tokenize
import subprocess
import re
import string

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


search_dest = ''
############################################################
#make list of articles
subprocess.call('ls ../training_set/corrected_articles/'+search_dest+' | grep \'.txt\' > ../training_set/extra/file_list.txt' , shell = True)

with open('../training_set/extra/file_list.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]

############################################################
#function to make relations
def make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz):
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
# Annotation Code
for j in file_names:
	
	
	with open('../training_set/corrected_articles/'+search_dest+j, 'r', encoding='utf-8') as myfile:
		data=myfile.read().replace('\n',' ')
	fp = open('../training_set/corrected_articles/'+search_dest+j[:-4]+'.ann', 'w', encoding='utf-8')
	
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
		for entity in l:
			for obj in entity:
			
				obj = obj.lower()
			
				# Annotate entities

				if (' '+obj+' ' in lowered_sent )!= False:
					obj_starts = (m.start() for m in re.finditer(' '+obj+' ', lowered_sent))
					for i in obj_starts:
						start = char_num + i + 1 # extra space before
						entity_num += 1
						fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
						make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz)
				punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'		
				for punc in punctuation:
					if (' '+obj+punc in lowered_sent )!= False:
						obj_starts = (m.start() for m in re.finditer(' '+obj+re.escape(punc), lowered_sent))
						for i in obj_starts:
							start = char_num + i + 1 # extra space before
							entity_num += 1
							fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
							make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz)
				if (obj in lowered_sent and (obj[0:len(obj)] == lowered_sent[0:len(obj)]))!= False:
					# print(obj + ' 1212\n')
					start = char_num
					entity_num += 1
					# print('test')
					# print(sentence[0 : len(obj)])
					fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[0:len(obj)] +'\n')
					make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz)	

				obj = obj+'s'	
				
				if (' '+obj+' ' in lowered_sent )!= False:
					obj_starts = (m.start() for m in re.finditer(' '+obj+' ', lowered_sent))
					for i in obj_starts:
						start = char_num + i + 1 # extra space before
						entity_num += 1
						fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
						make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz)
				punctuation = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'		
				for punc in punctuation:
					if (' '+obj+punc in lowered_sent )!= False:
						obj_starts = (m.start() for m in re.finditer(' '+obj+re.escape(punc), lowered_sent))
						for i in obj_starts:
							start = char_num + i + 1 # extra space before
							entity_num += 1
							fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[i+1 : i+1+len(obj)] +'\n')
							make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz)

				if (obj in lowered_sent and obj[0:len(obj)] == lowered_sent[0:len(obj)])!= False:
					# print(obj + ' 1212\n')
					start = char_num
					entity_num += 1
					fp.write('T'+str(entity_num)+'\t'+dict[tuple(entity)] +' '+str(start)+' '+str(start+len(obj))+'\t'+ sentence[0:len(obj)] +'\n')
					make_relation_list(entity, entity_num, micr, envr, subs, prop, proc, nutr, enz)				

		char_num += len(sentence) + 1
		if len(sentence) == 1:
			char_num += 1

		# Make relations based on co-occurences

		for x in micr:
			for y in envr:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'FoundIn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in prop:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'Of'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in subs:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'ActOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in micr:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'CarriedOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in micr:
			for y in enz:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'Produce'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in subs:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'CarriedOn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in proc:
			for y in envr:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'OccursIn'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		for x in enz:
			for y in proc:
				rel_num += 1
				fp.write('R'+str(rel_num)+'\t'+'Inhibit_Catalyse'+' Arg1:'+str(x)+' Arg2:'+str(y)+'\n')
		
	fp.close()
	myfile.close()
	print(j)

############################################################
subprocess.call('python auto_annotate_relations_remove_side_overlap.py', shell = True)
