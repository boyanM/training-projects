#!/usr/bin/python3

class roads:
	def __init__(self,a,b,c):
		self.a = a
		self.b = b
		self.c = c

	def print_roads(self):
		print(self.a," ",self.b," ",self.c)


	def __lt__(self,other):
		return self.c < other.c


def add_road(graph,road):
	graph[road.a].append(road.b)
	graph[road.b].append(road.a)

def remove_road(graph,road):
	graph[road.a].pop(0)
	graph[road.b].pop(0)


def update(speed_min,speed_max):
	global min_optimal,max_optimal
	if (speed_max - speed_min < max_optimal - min_optimal):
		min_optimal = speed_min
		max_optimal = speed_max

def input(all_roads):
	#input=[
	#(1, 3, 2),
	#(4 ,2, 8),
	#(1 ,2, 11),
	#(1 ,4, 3),
	#(1 ,3, 6),
	#(5 ,3, 5),
	#(3 ,6, 9),
	#(7 ,6, 6),
	#(5 ,6, 3),
	#(2 ,5, 7)
	#]
	file = open('/home/boyanm/Downloads/probeSpeed.txt','r')
	while True:
		line = file.readline()
		if not line:
			break;
		data=line.split()
		all_roads.append(roads(int(data[0]),int(data[1]),int(data[2])))

	file.close()

def bfs(graph,cities):
	count = 0
	queue = []

	visited = [False]*1000

	visited[1] = True
	queue.append(1)
	count += 1

	while len(queue) != 0:
		position = queue[0]
		queue.pop(0)
		for i in graph[position]:
			if visited[i] != True:
				visited[i] = True
				queue.append(i)
				count += 1

	return count == cities 



cities = 500
num_roads = 2000

all_roads = []
input(all_roads)

all_roads.sort()

min_optimal = 0
max_optimal = 30000

graph = [[] for i in range(1000)]

memory = []

for i in range(len(all_roads)):
	add_road(graph,all_roads[i])
	memory.append(i)

	while len(memory) != 0 and bfs(graph,cities):
		oldest = memory[0]
		print(all_roads[oldest].c," ",all_roads[i].c)
		update(all_roads[oldest].c,all_roads[i].c)

		memory.pop(0)
		remove_road(graph,all_roads[oldest])

print(min_optimal,max_optimal)
