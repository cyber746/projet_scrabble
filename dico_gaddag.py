import time

class GaddagNode:
	"""Classe de noeuds constituant le gaddag"""
	def __init__(self, id):
		self.id = id
		self.possibles = ""
		self.edges = {}

	def __str__(self):
		str_list = [self.possibles]
		for (label, node) in self.edges.items():
			str_list.append(label)
			str_list.append(str(node.id))
		return '_'.join(str_list)

	def __hash__(self):
		return self.__str__().__hash__()

	def __eq__(self, autre):
		return self.__str__() == autre.__str__()

	def copy(self):
		new_node = GaddagNode(self.id)
		new_node.possibles = self.possibles
		new_node.edges = self.edges
		return new_node

class Gaddag:
	"""Classe du gaddag (cf article pour son principe)"""
	compteurNodes = 0
	def __init__(self):
		self.root = GaddagNode(Gaddag.compteurNodes)
		self.mot_precedent = ""
		self.a_verifier = []
		self.Node_minimises = {}
		self.Node_list = []
		Gaddag.compteurNodes += 1

	def inserer(self, mot):
		"""routine d'insertion des mots dans le gaddag (cf. article)"""
		if mot <= self.mot_precedent:
			raise Exception("Erreur: les mots doivent être insérés dans l'ordre alphabétique")
		prefixe_commun = 0
		for i in range(min(len(mot), len(self.mot_precedent))):
			if mot[i] != self.mot_precedent[i]:
				break
			prefixe_commun += 1
		
		if len(self.mot_precedent) == prefixe_commun and self.mot_precedent != "":
			prefixe_commun -= 1

		self.minimize(prefixe_commun)

		if len(self.a_verifier) == 0:
			node = self.root
		else:
			node = self.a_verifier[-1][2]

		for lettre in mot[prefixe_commun:len(mot)-1]:
			node_suivant = GaddagNode(Gaddag.compteurNodes)
			Gaddag.compteurNodes += 1
			node.edges[lettre] = node_suivant
			self.a_verifier.append((node, lettre, node_suivant))
			node = node_suivant

		node.possibles =''.join(sorted(node.possibles+mot[-1]))
		self.mot_precedent = mot

	def termine(self):
		"""routine terminant la simplification du gaddag quand le dernier mot est ajouté"""
		self.minimize(0)
		self.Node_minimises[self.root] = self.root
		self.renumber()

	def renumber(self):
		"""routine de redéfinition des labels des noeuds"""
		node_list = []
		id_map = {}
		def ajoute_node_list(node):
			if str(node.id) in id_map.keys():
				return
			node_list.append(node)
			id_map[str(node.id)] = len(id_map)
			for label, fils in node.edges.items():
				ajoute_node_list(fils)
		ajoute_node_list(self.root)
		for i in range(len(node_list)):
			node = node_list[i].copy()
			for label, fils in node.edges.items():
				node.edges[label] = id_map[str(fils.id)]
			node_list[i] = node
		for i in range(len(node_list)):
			node_list[i].id = id_map[str(node_list[i].id)]
		self.Node_list = node_list

	def minimize(self, ind_reduc):
		"""routine de minimisation du gaddag par recherche de noeuds identiques"""
		for i in range(len(self.a_verifier)-1, ind_reduc-1, -1):
			(parent, lettre, fils) = self.a_verifier[i]
			if fils in self.Node_minimises:
				parent.edges[lettre] = self.Node_minimises[fils]
			else:
				self.Node_minimises[fils] = fils
			self.a_verifier.pop()

	def parcours(self, node, pile):
		"""routine de parcours de l'arbre à partir d'un noeud donné et d'un chemin à suivre (donné sous forme de pile)"""
		while pile:
			lettre = pile.pop()
			try:
				node = node.edges[lettre]
			except KeyError:
				return None
		return node			

	def parcours_list(self, index, pile):
		"""routine de parcours de l'arbre quand il est sous forme de liste (à tester)"""
		while pile:
			lettre = pile.pop()
			try:
				index = self.Node_list[index][lettre]
			except KeyError:
				return None
		return self.Node_list[index]

	def cherche(self, mot):
		"""routine de recherche d'un mot dans l'arbre"""
		node = self.root
		pile = list(mot)
		lettre1 = pile.pop(0)
		node = self.parcours(node, pile)
		return lettre1 in node.possibles
	
	def cherche_list(self, mot):
		"""routine de recherche d'un mot dans l'arbre quand il a été mis sous forme de liste (à tester)"""
		pile = list(mot)
		lettre1 = pile.pop(0)
		node = self.parcours_list(0, pile)
		return lettre1 in node.possibles

	def anagram_list(self, tirage):
		"""routine de recherche d'anagramme (à faire)"""
		pass
		

	def pivot(self, pref, suff):
		"""routine de recherche des pivots"""
		node = self.root
		if len(suff) >= len(pref):
			pile = list(suff)	
			node = self.parcours(node, pile)
			if node is None:
				return ""
			if pref == "":
				return node.possibles
			else:
				possibles = ""
				for char in node.edges.keys():
					node_test = self.parcours(node, list(pref[1:]+char))
					if node_test is not None and pref[0] in node_test.possibles:
						possibles += char
				return possibles
		else:
			pile = list(reversed(pref))
			pile.insert(-1, "!")
			node = self.parcours(node, pile)
			if node is None:
				return ""
			if suff == "":
				return node.possibles
			else:
				possibles = ""
				for char in node.edges.keys():
					node_test = self.parcours(node, list(reversed(char+suff[:-1])))
					if node_test is not None and suff[-1] in node_test.possibles:
						possibles += char
				return possibles


	def pivot2(self, pref, suff):
		"""routine de recherche des pivots, simple mais pas opti"""
		pivot_possible = ""
		for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if self.cherche(pref+char+suff):
				pivot_possible += char
		return pivot_possible


	def nb_nodes(self):
		"""routine donnant le nombre de noeuds de l'arbre"""
		return len(self.Node_minimises)

	def nb_aretes(self):
		"""routine donnant le nombre d'arètes de l'arbre"""
		compte = 0
		for node in self.Node_minimises:
			compte += len(node.edges)
		return compte

	def exporter(self, filename):
		"""routine d'export de l'arbre : on le met sous forme de liste de noeuds qu'on exporte dans un fichier txt"""
		with open(filename, 'w') as file:
			for node in self.Node_list:
				nodestr = str(node.id) + ',' + node.possibles + ','
				for (label, node_fils) in node.edges.items():
					nodestr += label + str(node_fils) + ','
				file.write(nodestr[:-1] + '\n')
		return('Fichier créé')

	def display(self):
		"""routine d'affichage de l'arbre; Éviter d'utiliser sur un arbre gros..."""
		pile = [self.root]
		finis = set()
		while pile:
			node = pile.pop()
			if node.id in finis:
				continue
			finis.add(node.id)
			print("{}: {}".format(node.id, node))
			if len(node.possibles)>0:
				print('    ('+node.possibles+')')
			for label, fils in node.edges.items():
				print("    {} vers {}".format(label, fils.id))
				pile.append(fils)

def importer(self, filename):
	"""routine d'import d'un fichier de noeuds et de construction du gaddag résultant mis sous forme de liste"""
	dico = Gaddag()
	with open(filename) as file:
		for line in file:
			node_list = line.strip().split(',')
			new_node = GaddagNode(int(node_list.pop(0)))
			new_node.possibles = node_list.pop(0)
			new_node.edges = dict()
			if node_list:
				for elt in node_list:
					new_node.edges[elt[0]] = int(elt[1:])
			dico.Node_list.append(new_node)
	print('Fichier importé')
	return dico

def build_dic():
	"""routine de contruction du gaddag à partir d'un fichier txt de mots"""
	start = time.time()
	gaddag = Gaddag()
	mots = []
	with open('ods8.txt') as file:
		for ligne in file:
			mot = ligne.strip()
			mots.append(mot[::-1])
			for i in range(len(mot)-1):
				mots.append(mot[i::-1]+'!'+mot[i+1:])
		print("Liste terminée en {0}s".format(time.time()-start))
		for mot in sorted(mots):
			gaddag.inserer(mot)
		print("Mots insérés en {0}s".format(time.time()-start))
		gaddag.termine()
		print("Création du gaddag en {0}s".format(time.time()-start))
	return gaddag