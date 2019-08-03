with open('entity_list.txt', 'r') as file:
	I = file.readlines()
I = [x.strip() for x in I]


I = list(set(I))
I.sort()

f = open('entity_list.txt','w')
for x in I:
	f.write(x+'\n')
f.close()
