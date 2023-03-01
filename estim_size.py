import networkx as nx
import matplotlib.pyplot as plt
import random
import imageio
import numpy


def coinToss(p):
	prob = numpy.random.binomial(1, p)
	return prob

def find_new_state():
	probability = 0.2
	samplespace = [0, 1]

	for i in range(10):
		result = coinToss(probability)
	print(samplespace[result])


def display_graph(G, iteration = 0):
	ideal_node_size = int(2000/N)
	nodes_g = nx.draw_networkx_nodes(G, pos, node_color = 'green', nodelist = type1_node_list, node_size = ideal_node_size)#40)
	nodes_r = nx.draw_networkx_nodes(G, pos, node_color = 'red', nodelist = type0_node_list, node_size=ideal_node_size)#40)
	nodes_b = nx.draw_networkx_nodes(G, pos, node_color = 'blue', nodelist = type2_node_list, node_size=ideal_node_size)#40)
	nx.draw_networkx_edges(G,pos)
	
	title_str = "Configuration at iteration " + str(iteration)
	plt.title(title_str)
	plt.show()
	plt.show(block=False)
	plt.pause(0.3)
	plt.close()

def find_eight_neighbors(node):
	x = node[0]
	y = node[1]
	if x > 0 and x < N - 1:
		east_x = x + 1;
		west_x = x - 1;
		north_x = x;
		south_x = x;
	if y > 0 and y < N - 1:
		east_y = y
		west_y = y
		north_y = y + 1
		south_y = y - 1
	if x == 0:
		west_x = N - 1
		east_x = x + 1
		north_x = x
		south_x = x
	if x == N - 1:
		west_x = x - 1
		east_x = 0
		north_x = x
		south_x = x
	if y == 0:
		west_y = y
		east_y = y
		north_y = y + 1
		south_y = N - 1
	if y == N - 1:
		west_y = y
		east_y = y
		north_y = 0
		south_y = y - 1

	east = (east_x, east_y)
	west = (west_x, west_y)
	north = (north_x, north_y)
	south = (south_x, south_y)
	north_east = (east_x, north_y)
	north_west = (west_x, north_y)
	south_east = (east_x, south_y)
	south_west = (west_x, south_y)
	# print('neigh',[east, west, north, south])
	return [east, west, north, south, north_east, north_west, south_east, south_west]

def find_neighbors(node):
	x = node[0]
	y = node[1]
	if x > 0 and x < N-1:
		east_x = x+1; 
		west_x = x-1; 
		north_x = x; 
		south_x = x; 
	if y>0 and y<N-1:
		east_y = y
		west_y = y
		north_y = y+1
		south_y = y-1
	if x == 0:
		west_x = N-1
		east_x = x+1
		north_x = x
		south_x = x
	if x == N-1:
		west_x = x-1
		east_x = 0
		north_x = x
		south_x = x
	if y == 0:
		west_y = y
		east_y = y
		north_y = y+1
		south_y = N-1
	if y == N-1:
		west_y = y
		east_y = y
		north_y = 0
		south_y = y-1
	
	east = (east_x, east_y)
	west = (west_x, west_y)
	north = (north_x, north_y)
	south = (south_x, south_y)
	#print('neigh',[east, west, north, south])
	return [east, west, north, south]

def checkneigh(node, neighbor_count = 4):
	flag1 = False
	if neighbor_count == 4:
		neighbors = find_neighbors(node)
	elif neighbor_count == 8:
		neighbors = find_eight_neighbors(node)
	for neigh in neighbors:
		#print('node',neigh,'prev',G.nodes[neigh]['prev_signal'], end = ". ")
		if G.nodes[neigh]['prev_signal'] == True:
			flag1 = True
			break
	#print("\n")
	return flag1

#Grid creation
N = 10; H = N; W = N;
Ref_timer = 20
p = 0.0105
neigh_count = 8
G = nx.grid_2d_graph(N,N)
pos = dict((n,n) for n in G.nodes())
for ((u,v),d) in G.nodes(data = True):
	if(u+1 <= N-1) and (v+1 <= N-1):
		continue
		#G.add_edge((u,v), (u+1,v+1))
	if(u+1 <= N-1) and (v-1 >= 0):
		continue
		#G.add_edge((u,v), (u+1,v-1))
count = 0
frames = []

for n in G.nodes():
	#type 1 is for susceptible state and 0 for refractory state
	G.nodes[n]['type'] = 1
	G.nodes[n]['size'] = 1
	G.nodes[n]['initiated'] = False
	G.nodes[n]['time_since_signal'] = 0
	G.nodes[n]['signal_sent'] = False
	G.nodes[n]['prev_signal'] = False
	G.nodes[n]['refractory_timer'] = 0
	G.nodes[n]['count'] = 1
	G.nodes[n]['done'] = False

type1_node_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 1]
type2_node_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 2]
type0_node_list = [n for (n,d) in G.nodes(data = True) if d['type'] == 0]
#display_graph(G)
max_iter = 100000
next = 0


while True:
	done_count = 0
	for node in G.nodes():
		if G.nodes[node]['done'] == True:
			done_count += 1
	if done_count == len(G.nodes()):
		print('all', done_count,'nodes set to done at iter', count)
		break

	for node in G.nodes():
		if G.nodes[node]['type'] == 1:
			if G.nodes[node]['prev_signal'] == False and checkneigh(node, neigh_count):
				#print('node changed by induction')
				G.nodes[node]['signal_sent'] = True
				G.nodes[node]['type'] = 0                  #refractory
				G.nodes[node]['refractory_timer'] = Ref_timer
				G.nodes[node]['size'] += 1
				G.nodes[node]['time_since_signal'] = 0

			elif G.nodes[node]['initiated'] == False:
				check = random.randint(1,100)
				if check < 100*p:
					G.nodes[node]['signal_sent'] = True
					G.nodes[node]['time_since_signal'] = 0
					G.nodes[node]['refractory_timer'] = Ref_timer
					G.nodes[node]['type'] = 0                  #refractory
					G.nodes[node]['initiated'] = True
					G.nodes[node]['size'] += 1
					#print('setting node to initialized', node)
			else:
				G.nodes[node]['time_since_signal'] += 1
				G.nodes[node]['prev_signal'] = False

		else:
			G.nodes[node]['refractory_timer'] -= 1
			#G.nodes[node]['signal_sent'] = False
			if G.nodes[node]['refractory_timer'] <= 0:
				G.nodes[node]['type'] = 1                  #susceptible



	count += 1
	if count >= max_iter:
		#print('max iters reached')
		break
	for node in G.nodes():
		if G.nodes[node]['signal_sent'] == True:
			G.nodes[node]['prev_signal'] = True
			G.nodes[node]['signal_sent'] = False
		else:
			G.nodes[node]['prev_signal'] = False


	for node in G.nodes():
		if G.nodes[node]['time_since_signal'] >= 1/p:
			G.nodes[node]['done'] = True
		else:
			G.nodes[node]['done'] = False

	#for i in range(N):
	#	for j in range(N):
			# print(G.nodes[(i, j)]['time_since_signal'], end=",")
	#		print(G.nodes[(i, j)]['prev_signal'], end=",")
	#	print("\n")

print('Size estimation done with initiation probability, p=', p, 'and refractory timer, R=', Ref_timer, 'for', neigh_count, 'neighbors')
for i in range(N):
	for j in range(N):
		print(G.nodes[(i, j)]['size'], end=",")
	print("\n")
#for i in range(N):
#	for j in range(N):
#		print(G.nodes[(i, j)]['time_since_signal'], end=",")

#	print("\n")