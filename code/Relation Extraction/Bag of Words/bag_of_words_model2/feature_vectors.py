import sys
sys.path.insert(0, '../relation_words')
import bisect
import file_map
import numpy as np 
import nltk

global feature_vector
global project_home
global relation_map

relation_map = file_map.mapping()
project_home = '../../'

class EntityObj:
	def __init__(self, num, type_inp, start, end, name):
		self.num = num
		self.type = type_inp
		self.start = start
		self.end = end
		self.name = name

class RelObj:
	def __init__(self, num, type_inp, first, second):
		self.num = num
		self.type = type_inp
		self.first = first
		self.second = second

def all_word_features():
	word_dict_all = [{} for i in range(len(relation_map)/2)]
	
	for relation in relation_map.keys():
		if int(relation_map[relation])%2 == 0 :
			word_list = []
			with open(project_home + 'relation_extraction/relation_words/' + relation_map[relation] + '.txt', 'r') as file:
				data = file.readlines()
			data = [x.strip() for x in data]

			for line in data:
				words = nltk.word_tokenize(line)
				sn = nltk.stem.SnowballStemmer('english')
				lm = nltk.stemWordNetLemmatizer()
				################## take lemmatized words - preferred - **** default pos = 'n' ****
				# for w in words:
				# 	lm.lemmatize(w)

				################## take stemmed words
				# for w in words:
				# 	sn.stem(w)

				################## taking normal words

				for w in words:
					word_list.append(w)
			
			set(word_list)
			list(word_list)
			word_list.sort()

			word_dict = {}
			for i in range(len(word_list)):
				word_dict[word_list[i]] = i
			
			word_dict_all[int(relation_map[relation])/2] = word_dict

	return word_dict_all

def entity_relation_obj(training_dir):
	subprocess.call('ls ' + project_home + training_dir + ' | grep \'.txt\' > ' + project_home + 'training_set/extra/file_list.txt', shell = True)
	
	with open(project_home + 'training_set/extra/file_list.txt', 'r') as input_file:
		file_list = input_file.readlines()
	file_list = [x.strip() for x in file_list]

	entity_maps_all = []
	relation_lists_all = []
	data_all = []

	for file in file_list:
		with open(project_home + training_dir + file, 'r') as input_file:
			data=input_file.read().replace('\n',' ')
		data_all.append(data)	
		
		with open(project_home + training_dir + file[:-4] + '.ann', 'r') as input_file:
			ann_input=input_file.readlines()
		ann_input = [x.strip() for x in ann_input]

		entity_map = {}
		relation_list = []
		for line in ann_input:
			if line[0] == 'T':
				word = word_tokenize(line)
				if len(word) < 5 :
					continue
				obj = EntityObj(int(word[0][1:]), word[1], int(word[2]), int(word[3]), ' '.join(word[4:]))
				entity_map[obj.num] = obj
			else:
				word = word_tokenize(line)
				if len(word) < 8 :
					continue
				if word[1][-3:] == '_No':
					continue
				obj = RelObj(int(word[0][1:]), word[1], int(word[4][1:]), int(word[7][1:]))
				relation_list.append(obj)

		entity_maps_all.append(entity_map)
		relation_lists_all.append(relation_list)

	return [entity_maps_all, relation_lists_all, data_all]


def add_word_features(entity_maps_all, relation_lists_all, data_all, training_dir):
	word_dict_all = all_word_features()
	rel = len(relation_map)/2
	word_vec_all = [np.zeros([num_relations[i], len(word_dict_all[i])]) for i in range(rel)]

	num_files = len(data_all)
	index = [0]*rel
	for i in range(num_files):
		data = data_all[i]
		entity_map = entity_maps_all[i]
		relation_list = relation_lists_all[i]

		for relation in relation_list:
			rel_num = int(relation_map[relation.type])/2
			if relation.first not in entity_map.keys() or relation.second not in entity_map.keys():
				continue
			start = min(entity_map[relation.first].end, entity_map[relation.second].end)
			end = max(entity_map[relation.first].start, entity_map[relation.second].start)
			line = data[start:end] 
			for word in word_tokenize(line):
				word_vec_all[rel_num][index[rel_num], word_dict_all[rel_num][word]] = 1	
			index[rel_num] += 1

	return word_vec_all
 

# def add_pos_features(entity_maps_all, relation_lists_all, data_all, training_dir):


# def add_dependency_features(entity_maps_all, relation_lists_all, data_all, training_dir):


# def add_char_len_features(entity_maps_all, relation_lists_all, data_all, training_dir):



# Returns [feature_vector_for each_relation_as_list] 
# where each feature vector is np.ndarray of size [number_of_those_relations, unique_words_between_that_relation] 
# present at (relation's file number)/2 in list 
def get_feature_vectors():
	global num_relations
	num_relations = [0]*len(relation_map)/2
	training_dir = 'training_set/corrected_articles/biotech_corrected/training/'
	[entity_maps_all, relation_lists_all, data_all] = entity_relation_obj(training_dir)
	for rel_l in relation_lists_all:
		for rel in rel_l:
			num_relations[int(relation_map[rel.type])/2] += 1

	feature_vec_words = add_word_features(entity_maps_all, relation_lists_all, data_all, training_dir)
	# feature_vec_pos = add_pos_features(entity_maps_all, relation_lists_all, data_all, training_dir)
	# feature_vec_depen = add_dependency_features(entity_maps_all, relation_lists_all, data_all, training_dir)
	# feature_vec_len_c = add_char_len_features(entity_maps_all, relation_lists_all, data_all, training_dir)

	feature_vec = feature_vec_words

	# for i in range(len(feature_vec)):
	# 	feature_vec[i] = np.c_[feature_vec[i], feature_vec_pos[i], feature_vec_depen[i], feature_vec_len_c[i]] 



	return feature_vec
