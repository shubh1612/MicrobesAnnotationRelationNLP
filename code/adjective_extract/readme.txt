extra - contains list of stopwords and files

Some POS tags:
CC Coordinating conjunction
JJ Adjective
NN Noun, singular or mass
NNS Noun, plural
NNP Proper noun, singular
NNPS Proper noun, plural
VB Verb, base form
VBD Verb, past tense
VBG Verb, gerund or present participle
VBN Verb, past participle
VBP Verb, non-3rd person singular present
VBZ Verb, 3rd person singular present


Let E be the entity

adj_extract_0.py
	
	1) Extracts entities of type JJ JJ ..... E
	2) If entity of type "oil-degrading sediment" is present, extracts all entities of type "'word' degrading E"
	3) If entity of type "oil-contaminated sediment" is present, extracts all entities of type "NN contaminated E"

adj_extract_0.1.py
	
	1) Slightly modified version of version 0

adj_extract_1.py
	
	Extracts entities of type 
	1) JJ JJ ..... E
	2) JJ NN/NNS/NNP/NNPS E
	3) NN/NNS/NNP/NNPS JJ E
	4) NN/NNS/NNP/NNPS VB/VBG/VBN/VBP/VBZ E
	
adj_extract_1.1.py
	
	1) First checks if the entity itself is an adjective
	2) Checks the words on right for being potential entity
	3) In addition to version 1.1 extracts entities of type:
		a)JJ CC JJ E 
	

################################################################################

DIRECTORY STRUCTURE

1) extra and .py files are placed in the Stanford NLP folder.
3) keep all articles in articles/ in the Stanford NLP folder.
2) create article_xmls/

