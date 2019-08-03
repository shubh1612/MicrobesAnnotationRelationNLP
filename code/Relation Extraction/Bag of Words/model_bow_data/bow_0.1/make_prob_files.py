import numpy as np
from nltk.tokenize import sent_tokenize

search_dest = ''

#subprocess.call('ls ../training_set/corrected_articles/'+search_dest+' | grep \'.txt\' > ../training_set/extra/file_list.txt' , shell = True)
#subprocess.call('ls ../training_set/corrected_articles/'+search_dest+' | grep \'.ann\' > ../training_set/extra/file_list_1.txt' , shell = True)

for i in range(14):
	fp = open(str(i)+'.txt', 'w+', encoding='utf-8')

### file names such as 0.txt for found_in 
mydict = {"FoundIn": '0', "FoundIn_No": '1', "Of": '2', "Of_No": '3', "ActOn": '4', "ActOn_No": '5', "CarriedOn": '6', "CarriedOn_No": '7', "Produce": '8', "Produce_No": '9', "OccursIn": '10', "OccursIn_No": '11', "Inhibit_Catalyse": '12', "Inhibit_Catalyse_No": '13'}


### open the txt files which are listed in file_list.txt 
with open('file_list.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]


### open the ann files which are listed in file_list_1.txt 
with open('file_list_1.txt', 'r') as file2:
	file_names_1 = file2.readlines()
file_names_1 = [x.strip() for x in file_names_1]


### function that makes new files or append words in 0.txt etc corressponding to each relation
def make_file(name, start, end, file):

	### name is the type of entity eg. environment, microbes etc.
	fp = open(mydict[name]+'.txt', 'a', encoding='utf-8')
	index = start
	word = ""

	### loop to go from last character of 1st word till the first character of last word
	while index <= end:
		c = file[int(index)]
		if (c is not (' ' or '\n' or '.')):
			word = word + (c)
		elif ( c == ' ' or '.' or '\n'):
			fp.write(word+'\n')
			word = ""
		index = index + 1
	fp.write(word)
	fp.close()


### index is a 2d array where index[i] denotes the start and end value of entity Ti
### index[i][0] contains the start index of entity Ti and index[i][1] contains the end index of entity Ti
index = np.zeros((10000, 2))
for j in range(len(file_names_1)):
	print (file_names_1[j])
	with open(file_names[j], 'r', encoding='utf-8') as myfile:
		data=myfile.read()
	with open(file_names_1[j], 'r', encoding='utf-8') as myfile_1:
		data_1=myfile_1.read().replace('\n',' . ')
		data_1=data_1.replace('\t', ' ')


	### data_1 contains ann files
	for sentence in sent_tokenize(data_1):
		text = sentence.split(" ")
		if (text[0][0] == 'R'):

			### if a relation is found in ann file
			### we see if the start of second entity in relation in greater than end of 1st entity
			## it means, we look for the word which comes earlier in document 
			
			if(index[int(text[2][6:])][1] < index[int(text[3][6:])][0]):
				start = index[int(text[2][6:])][1] + 1
				end = index[int(text[3][6:])][0] - 1
			else:
				start = index[int(text[3][6:])][1] + 1
				end = index[int(text[2][6:])][0] - 1				
			make_file(text[1], start, end, data)

		elif (text[0][0] == 'T'):
			
			### make the index array
			
			index[int(text[0][1:])][0] = int(text[2])
			index[int(text[0][1:])][1] = int(text[3])

