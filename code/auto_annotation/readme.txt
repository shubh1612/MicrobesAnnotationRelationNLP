remove_repeated_data.py 

	Filters the entity list for repeated entities

auto_annotate_relations_1.py 
	
	Uses pattern matching for marking entities and cooccurence to mark the relations

auto_annotate_relations_2.py
	
	Annotates similar to auto_annotate_relations_1.py, also filters overlapping entites of type "oil-degrading petroleum soil" and "petroleum"

auto_annotate_relations_remove_side_overlap.py
	
	From the annotations obtained using auto_annotate_relations, filters overlapping entites of type "oil-degrading sediment" and "sediment"

###########################################################################

DIRECTORY STRUCTURE

	1) Keep all the lists of entity files in this directory (environment.txt, substrate.txt etc.)
	2) Make a directory - "../training_set/corrected_articles/" , training_set should also contain a directory extra/
	Store articles in "../training_set/corrected_articles/" + search_dest
	The path of files that need to be annotated is stored in variable "'search_dest'" which can be changed accordingly