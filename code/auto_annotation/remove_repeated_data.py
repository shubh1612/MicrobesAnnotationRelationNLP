################
with open('microbes.txt', 'r', encoding = 'utf-8') as file_1:
	M = file_1.readlines()
M = [x.strip() for x in M]

M = set(M)
M = list(M)

with open('microbes.txt', 'w', encoding = 'utf-8') as file_1:
	for i in M:
		file_1.write(i+'\n')

###########
with open('enzyme.txt', 'r', encoding = 'utf-8') as file_1:
	E = file_1.readlines()
E = [x.strip() for x in E]

E = set(E)
E = list(E)


with open('enzyme.txt', 'w', encoding = 'utf-8') as file_1:
	for i in E:
		file_1.write(i+'\n')


################
with open('environment.txt', 'r', encoding = 'utf-8') as file_1:
	Env = file_1.readlines()
Env = [x.strip() for x in Env]

Env = set(Env)
Env = list(Env)

with open('environment.txt', 'w', encoding = 'utf-8') as file_1:
	for i in Env:
		file_1.write(i+'\n')

# ##############
with open('substrate.txt', 'r', encoding = 'utf-8') as file_1:
	S = file_1.readlines()
S = [x.strip() for x in S]


S = set(S)
S = list(S)

with open('substrate.txt', 'w', encoding = 'utf-8') as file_1:
	for i in S:
		file_1.write(i+'\n')

# ###################
with open('property.txt', 'r', encoding = 'utf-8') as file_1:
	P = file_1.readlines()
P = [x.strip() for x in P]

P = set(P)
P = list(P)


with open('property.txt', 'w', encoding = 'utf-8') as file_1:
	for i in P:
		file_1.write(i+'\n')

###################
with open('process.txt', 'r', encoding = 'utf-8') as file_1:
	Pro = file_1.readlines()
Pro = [x.strip() for x in Pro]

Pro = set(Pro)
Pro = list(Pro)


with open('process.txt', 'w', encoding = 'utf-8') as file_1:
	for i in Pro:
		file_1.write(i+'\n')

##############
with open('nutrient.txt', 'r', encoding = 'utf-8') as file_1:
	N = file_1.readlines()
N = [x.strip() for x in N]

N = set(N)
N = list(N)


with open('nutrient.txt', 'w', encoding = 'utf-8') as file_1:
	for i in N:
		file_1.write(i+'\n')
