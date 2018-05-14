from mymodule import Graph
import mymodule as mm
#import numpy as np


 #tworzenie pustego grafu
graph=Graph()

print("Wybierz operacje")
print("1. Wczytanie ciągu i sprawdzenie czy jest graficzny")
print("2. Randomizacja grafu z pliku")
print("3. Szukanie najwiekszej spojnen skladowej grafu z pliku")
print("4. Losowy graf eulerowski")
print("5. Losowy graf k-regularny")
print("6. Losowy graf hamiltonowski")
print("Wybieram:")
task=input()
if task=='1':
	#seq(lista intów) to ciag wprowadzany z klawiatury
	seq=input("Podaj ciag odzielony spacjami:")
	seq=list(map(int,seq.split()))

	#sprawdza czy podana sekwencja to ciag graficzny (jak jest to tworzy na jej podstawie graf i liste sasiedztwa do pliku)
	if Graph.is_graphic(seq):
		print("Ta sekwencja jest ciagiem graficznym")
		flag = False
		while flag == False:
			flag=graph.add_seq(seq)
		graph.save_to_file('lista_sasiedztwa.txt')
		print(graph.m_dict)
	else:
		print("Ta sekwencja nie jest ciagiem graficznym")


elif task=='2':
	graph.load_from_file('lista_sasiedztwa.txt')
	flag=False
	while flag==False:
		flag=graph.randomize()
	graph.save_to_file('lista_sasiedztwa.txt')

elif task=='3':
	graph.load_from_file('lista_sasiedztwa.txt')
	graph.max_component()

elif task=='4':
	flag=False
	while flag==False:
		flag=graph.generate_euleric()
	graph.save_to_file('lista_sasiedztwa.txt')
	graph.eulerian_cycle()
elif task=='5':
	graph.k_regular()
elif task=='6':
	flag=False
	while flag==False:
		flag=graph.hamilton()