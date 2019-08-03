import subprocess
import operator
from nltk import word_tokenize

#search_dest = 'divided_articles/'

###################################################################
#subprocess.call('ls ../training_set/corrected_articles/'+search_dest+' | grep \'.ann\' > ../training_set/extra/ann_list.txt' , shell = True)

with open('file_list_2.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]
###################################################################
class entity_obj:
	
	def __init__(self, num, type1, start, end, name):
		self.num = num
		self.type = type1
		self.start = start
		self.end = end
		self.name = name

	def string_entity(self):
		return str('T'+self.num+'\t'+self.type+' '+str(self.start)+' '+str(self.end)+'\t'+self.name)

	def list_entity(self):
		l = []
		l.append(self.num)
		l.append(self.start)
		l.append(self.end)
		l.append(self)
		return l

###################################################################
class rel_obj:
	
	def __init__(self, num, type1, first, second):
		self.num = num
		self.type = type1
		self.first = first
		self.second = second

	def string_rel(self):
		return str(self.num+'\t'+self.type+' Arg1:'+self.first+' Arg2:'+self.second)	

	def contains(self, arg):
		if self.first == arg or self.second == arg:
			return 1
		else:
			return 0
	
	def change_first(self):
		self.first = -1

	def print_check(self):
		if self.first == -1 :
			return 0
		else:
			return 1


###################################################################
def remove_rel(rel_list, num_entity):
	for i in rel_list:
		# print(i.string_rel())
		if i.contains('T'+ str(num_entity)):
			i.change_first()


###################################################################
for j in file_names:
	with open(j[:-4] + '__.ann', 'r', encoding='utf-8') as myfile:
		data=myfile.readlines()
	data = [x.strip() for x in data]
	entity_list = []
	entity_obj_list = []
	rel_list = []
	for line in data:
		if line[0] == 'T':
			word = word_tokenize(line)
			obj = entity_obj(word[0][1:], word[1], int(word[2]), int(word[3]), ' '.join(word[4:]))
			entity_obj_list.append(obj)
			entity_list.append(obj.list_entity())
		else:
			word = word_tokenize(line)
			obj = rel_obj(word[0], word[1], word[4], word[7])
			rel_list.append(obj)
	sort_start = sorted(entity_list, key=operator.itemgetter(1,2))
	if (len(sort_start) == 0):
		continue
	prev = sort_start[len(sort_start)-1]
	for i in range(len(sort_start)-2, -1, -1):
		if sort_start[i][1] == prev[1]:
			entity_obj_list.remove(sort_start[i][3])
			entity_list.remove(sort_start[i])
			remove_rel(rel_list, sort_start[i][0])
		else:
			prev = sort_start[i]
	
	sort_end = sorted(entity_list, key=operator.itemgetter(2,1))
	# print (sort_end)
	prev = sort_end[0]
	for i in range(1,len(sort_end)):
		if sort_end[i][2] == prev[2]:
			entity_obj_list.remove(sort_end[i][3])
			entity_list.remove(sort_end[i])
			remove_rel(rel_list, sort_end[i][0])
		else:
			prev = sort_end[i]	

	fp = open(j[:-4] + '__.ann', 'w', encoding='utf-8')
	for i in entity_obj_list:
		fp.write(i.string_entity() + '\n')
	for i in rel_list:
		if i.print_check() == 1:
			fp.write(i.string_rel() + '\n')
	fp.close() 
	print(j)