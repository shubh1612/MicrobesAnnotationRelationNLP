from nltk import sent_tokenize
import os
import subprocess

###########################################################
#make list of articles
subprocess.call('ls ../training_set/corrected_articles/done/ | grep \'.txt\' > ../training_set/extra/file_list.txt' , shell = True)

with open('../training_set/extra/file_list.txt', 'r') as filel:
	file_names = filel.readlines()
file_names = [x.strip() for x in file_names]

for file in file_names:

	with open('../training_set/corrected_articles/done/' + file, 'r', encoding='utf-8') as myfile:
		data=myfile.read().replace('\n',' ')

	i = 1;
	j = 1;
	for sentence in sent_tokenize(data):
		if os.path.isfile('../training_set/corrected_articles/divided_articles/'+file[:-4]+'__'+str(j)+'.txt'):
			with open('../training_set/corrected_articles/divided_articles/'+file[:-4]+'__'+str(j)+'.txt','a', encoding='utf-8') as myfile:
				myfile.write(sentence + ' ')
				i += 1
		else:
			with open('../training_set/corrected_articles/divided_articles/'+file[:-4]+'__'+str(j)+'.txt','w', encoding='utf-8') as myfile:
				myfile.write(sentence + ' ')
				i += 1
		if i%30 == 0:
			i = 1
			j += 1
			print(j)

	print (file)
