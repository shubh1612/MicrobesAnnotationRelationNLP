dependency_parse_tree.py

	Uses Stanford NLP to crete a dependency graph and distance between two words is calculated using BFS

annotation_dependency_correction.py
	
	Forms dependency graph for all sentences in an article, removes relations if the distance between the entities is greater than 'threshold' variable presently set to 3

###########################################################################

DIRECTORY STRUCTURE

	1) Stanford NLP should be in the following directory - "..\stanford_nlp_adj_extract\stanford-corenlp-full-2017-06-09\stanford-corenlp-full-2017-06-09\"

	2) Make a directory - "../training_set/corrected_articles/" , training_set should also contain a directory extra/
	Store articles in "../training_set/corrected_articles/" + search_dest
	The path of files that need to be annotated is stored in variable "'search_dest" which can be changed accordingly