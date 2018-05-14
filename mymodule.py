#klasa reprezentujaca graf
from random import randint
from random import choice
from random import randrange
from copy import copy
import numpy as np


class Graph(object):
	#konstruktor
	def __init__(self, m_dict=None):
		if m_dict == None:
			m_dict={}
		self.m_dict=m_dict

	#zwracaa liste wierzcholkow
	def vertices(self):
		return list(self.m_dict.keys())

	#zwraca liste krawedzi
	def edges(self):
		return self.generate_edges()

	#dodawanie wierzcholka bez krawedzi (jak juz jest to nic nie robi)
	def add_vertex(self,vertex):
		if vertex not in self.m_dict:
			self.m_dict[vertex]=[]
		else:
			print("this vertex already exsist")

	#dodawanie krawedzi, parametr edge to set z 2 wierzcholkami
	def add_edge(self, vertex1, vertex2):
		self.m_dict[vertex1].append(vertex2)
		self.m_dict[vertex2].append(vertex1)


	#generowanie krawedzi
	def generate_edges(self):
		edges=[]
		for v in self.m_dict:
			for linked in self.m_dict[v]:
				if [v, linked] not in edges and [linked, v] not in edges: #tu mozna rozszezyc na graf skierowany (chyba)
					edges.append([v, linked])
		return edges

	#oblicza stopien wierzcholka vertex
	def degree(self, vertex):
		return len(self.m_dict[vertex])

	#zwraca sekwencje stopni wierzcholkow posortowana malejaco
	def degree_seq(self):
		seq=[]
		for vertex in self.m_dict:
			seq.append(self.degree(vertex))
		seq.sort(reverse=True)
		return seq
	
	#sprawdza czy ciag seq jest graficzny
	def is_graphic(seq):
		seq=np.array(seq)
		while True:
			seq[::-1].sort()
			print(seq)
			if(not np.any(seq) == True): #jezeli sa same 0 to jest ciag graficzny
			#if(not any(seq) == True): #jezeli sa same 0 to jest ciag graficzny
				return True
			if seq[0]<0 or seq[0]>=len(seq):
				return False
			for i in range(1,seq[0]+1):
				if seq[i]==0:
					return False
				seq[i]-=1
			seq[0]=0

	#zapis do pliku 'name'
	def save_to_file(self, name):
		file=open(name,'w')
		for i in self.m_dict:
			file.write(str(i)+': ')
			for x in self.m_dict[i]:
				file.write(str(x)+',')
			file.write('\n')	
		file.close()

	def load_from_file(self, name):
		with open(name) as file:
			lines=file.readlines()
			lines=[x.strip() for x in lines]

		for i in lines:
			self.add_vertex(int(i[0]))

		for i in lines:
			vertice=int(i[0])
			for x in (i[3:-1].split(',')):
				if int(x) not in self.m_dict[vertice] and vertice not in self.m_dict[int(x)]:
					self.add_edge(vertice, int(x))

	#dodaje sekwencje(liste) do grafu
	def add_seq(self, seq):
		self.m_dict.clear()
		counter=0
		seq[::-1].sort()
		tmp=seq[:]
		for i in range(1, len(seq)+1):
			self.add_vertex(i)
		while tmp != len(seq)*[0]:
			a=randint(1,len(seq))
			b=randint(1,len(seq))
			if a!=b and a not in self.m_dict[b] and b not in self.m_dict[a] and tmp[a-1]>0 and tmp[b-1]>0:
				self.add_edge(a,b)
				tmp[a-1]-=1
				tmp[b-1]-=1
			counter +=1
			if counter>200:
				return False
		print(self.m_dict)
		print()
		print('seq',seq)
		print('tmp',tmp)
		return True

	#zamienia losowo wybrana pare krawedzi ab i cd a pare ad i bc (a b c d to rozne liczby (nie powtarzaja sie))
	def randomize(self):
		flag=False
		counter=0
		while flag==False:
			counter +=1
			if counter>100:
				return False
			a=randint(min(self.m_dict),max(self.m_dict))
			c=randint(min(self.m_dict),max(self.m_dict))
			if self.m_dict[a] == [] or self.m_dict[c] == []:
				return False
			while c==a and self.m_dict[c] == []:									#petla po to zeby c bylo rozne od a
				c=randint(min(self.m_dict),max(self.m_dict))
				#while a!=d and b!=c:
			b=choice(self.m_dict[a])
			d=choice(self.m_dict[c])

			if a!=b and a!=c and b!=d and c!=d and a!=d and b!=c:
				if d not in self.m_dict[a] and c not in self.m_dict[b]:
					flag=True
				else:
					return False
		print('zamieniam\n',a,b,' i ',c,d,'\nna\n',a,d,' i ',b,c)

		self.m_dict[a].remove(b)
		self.m_dict[b].remove(a)
		self.m_dict[c].remove(d)
		self.m_dict[d].remove(c)

		self.m_dict[a].append(d)	
		self.m_dict[d].append(a)	
		self.m_dict[b].append(c)	
		self.m_dict[c].append(b)
		return True

	#najwieksza spojna skladowa
	def max_component(self):
		stack=[]
		tab=[0 for i in range(len(self.m_dict))]
		max_tab=[0 for i in range(len(self.m_dict))] # przechwuje ilosc elementow skladowej (indeks to nr skladowej -1)
		counter=0
		for i in range(len(self.vertices())): #takie iterowanie zeby za pomoca i odnosic sie do tab
			if tab[i]==0:
				counter+=1
				stack.append(i+1)
				tab[i]=counter
				while stack != []:
					v=stack.pop()
					for u in self.m_dict[v]:
						if tab[u-1] == 0:
							stack.append(u)
							tab[u-1]=counter
		for i in range(1,counter+1):
			print('skladowa ',i,':')
			for j in range(len(self.vertices())):
				if tab[j]==i:
					print(j+1)
					max_tab[i-1]+=1
		print('najwieksza skladowa to skladowa nr:',max_tab.index(max(max_tab))+1)

	#generuje graf eulerowski
	def generate_euleric(self):
		flag =False #flaga do wyjscia z petli jak bedzie eulerowski
		flag2= False
		seq=[]
		size=randint(4,8)

		while flag == False:
			if size%2==0:
				seq=[randrange(2,size-1,2) for i in range(size)]
			else:
				seq=[randrange(2,size,2) for i in range(size)]
			if Graph.is_graphic(seq) == True:
				flag=True
		self.m_dict.clear()
		return self.add_seq(seq)



	def from_dict(self):
		links=[]
		for u in self.m_dict:
			for v in self.m_dict[u]:
				links.append((u,v))
		return links

	def is_connected(self):
		start_node=list(self.m_dict)[0]
		color = {v: 'white' for v in self.m_dict}
		color[start_node]='red'
		stack=[start_node]
		while len(stack) != 0:
			u=stack.pop()
			for v in self.m_dict[u]:
				if color[v] == 'white':
					color[v]='red'
					stack.append(v)
				color[u]='black'
		return list(color.values()).count('black') == len(self.m_dict)

	def eulerian_cycle(self):
		g=copy(self)
		cycle=[]
		u=list(g.m_dict)[1]
		while len(g.from_dict()) > 0:
			current_vertex=u
			for u in g.m_dict[current_vertex]:
				g.m_dict[current_vertex].remove(u)
				g.m_dict[u].remove(current_vertex)
				bridge = not g.is_connected()
				if bridge:
					g.m_dict[current_vertex].append(u)
					g.m_dict[u].append(current_vertex)
				else:
					break
			if bridge:
				print(u,current_vertex)
				g.m_dict[current_vertex].remove(u)
				g.m_dict[u].remove(current_vertex)
				g.m_dict.pop(current_vertex)
			cycle.append((current_vertex,u))
		print("Cykl Eulera:")
		print(cycle)

	def has_key(self, x):
		if x in self.m_dict:
			return True
		else:
			return False

	def hamilton(self):
		flag=False
		while flag == False:
			self.generate_euleric()
			for i in range(6,randint(10,13)):
				self.randomize()
			tab=find_paths(self)
			if tab != []:
				flag=True
			if len(tab)-1 < 1:
				return False
			x=randint(0,len(tab)-1)
			self.save_to_file('lista_sasiedztwa.txt')
			print(tab[x])
		return True

	def k_regular(self):
		print('Podaj liczbe wierzcholkow:')
		n=int(input())
		print('Podaj stopien wierzcholkow:')
		k=int(input())
		if n>=k+1 and (n*k)%2==0:
			flag=False
			while flag == False:
				flag=self.add_seq(n*[k])
		else:
			print('Podane liczby nie spelniaja warunkow do utworzenia grafu')
			return False
		self.save_to_file('lista_sasiedztwa.txt')
		return True
########################################################
#    			FUNCKJE
########################################################
def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph.m_dict[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
def find_paths(graph):
    cycles=[]
    for startnode in graph.m_dict:
        for endnode in graph.m_dict:
            newpaths = find_all_paths(graph, startnode, endnode)
            for path in newpaths:
                if (len(path)==len(graph.m_dict)):                    
                    cycles.append(path)
    return cycles

