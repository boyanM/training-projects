#!/usr/bin/python3

#Speed



def dfs(roads,cities,optimal):
	stack = []

	new_roads  = []

	for i in roads:
		if optimal[0] <= i[2] and optimal[1] >= i[2]:
			new_roads.append(i)

	seen = [False] * len(new_roads)

	seenCities = [False] * 7
	seenCities[0] = True
	
	start_of_graph = 1
	stack.append(start_of_graph)
	current_pos = -1
	while len(stack) != 0:
		current_pos = stack[-1]
		for i in range(len(new_roads)):
			if current_pos == new_roads[i][0] and seen[i] is False:
				stack.append(new_roads[i][1])
				seen[i] = True
				seenCities[new_roads[i][1]-1] = True

			elif current_pos == new_roads[i][1] and seen[i] is False:
				stack.append(new_roads[i][0])
				seen[i] = True
				seenCities[new_roads[i][0]-1] = True

		try:
			delitem = stack.index(current_pos)
		except:
			delitem = -1

		if delitem != -1:		
			stack = stack[:delitem] + stack[delitem+1:]

	if False in seenCities:
		return False
	else:
		return True		


cities = 7;
num_road = 10;

roads = [(1,3,2),(4,2,8),(1,2,11),(1,4,3),(1,3,6),(5,3,5),(3,6,9),(7,6,6),(5,6,3),(2,5,7)];

optimalSpeeds = []

for i in roads:
	if i[2] not in optimalSpeeds:
		optimalSpeeds.append(i[2])
optimalSpeeds.sort()

all_tuple = []
for i in optimalSpeeds:
	for j in optimalSpeeds:
		if i < j:
			all_tuple.append((i,j))


valid_answers = []

current_optimal_sum = 1000000000

for i in all_tuple:
	check = dfs(roads,cities,i)
	if	check and (abs(i[0] - i[1]) < current_optimal_sum):
		valid_answers = valid_answers[:-1]
		valid_answers.append(i)
		current_optimal_sum = abs(i[0] - i[1])
	elif check and (abs(i[0] - i[1]) == current_optimal_sum):
		valid_answers.append(i)

valid_answers = sorted(valid_answers, key=lambda tup: tup[0])

print("The most optimal way is ->",valid_answers[0])

#print(all_tuple)



