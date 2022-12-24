import time

class GaddagNode:
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

class Gaddag:
	compteurNodes = 0
	def __init__(self):
		self.root = GaddagNode(Gaddag.compteurNodes)
		self.mot_precedent = ""
		self.a_verifier = []
		self.Node_minimises = {}
		self.Node_list = []
		Gaddag.compteurNodes += 1

	def inserer(self, mot):
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
		self.minimize(0)
		#self.Node_minimises[self.root] = self.root
		#self.renumber()

	def renumber(self):
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
			node = node_list[i]
			for label, fils in node.edges.items():
				node.edges[label] = id_map[str(fils.id)]
			node_list[i] = node
		for i in range(len(node_list)):
			node_list[i].id = id_map[str(node_list[i].id)]
		self.Node_list = node_list

	def minimize(self, ind_reduc): #ajouter root à Node_minimises ? Vérifier si c'est fait, sinon ajouter à termine.
		for i in range(len(self.a_verifier)-1, ind_reduc-1, -1):
			(parent, lettre, fils) = self.a_verifier[i]
			if fils in self.Node_minimises:
				parent.edges[lettre] = self.Node_minimises[fils]
			else:
				self.Node_minimises[fils] = fils
			self.a_verifier.pop()

	def parcours(self, node, pile):
		while pile:
			lettre = pile.pop()
			try:
				node = node.edges[lettre]
			except KeyError:
				return None
		return node			

	def cherche(self, mot):
		node = self.root
		pile = list(mot)
		lettre1 = pile.pop(0)
		node = self.parcours(node, pile)
		return lettre1 in node.possibles

	def pivot(self, pref, suff):
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


	def pivot2(self, pref, suff): #simple mais pas opti
		pivot_possible = ""
		for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if self.cherche(pref+char+suff):
				pivot_possible += char
		return pivot_possible


	def nb_nodes(self):
		return len(self.Node_minimises)

	def nb_aretes(self):
		compte = 0
		for node in self.Node_minimises:
			compte += len(node.edges)
		return compte

	def display(self):
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


def build_dic():
	start = time.time()
	gaddag = Gaddag()
	mots = []
	with open('ods8.txt') as file:
		for ligne in file:
			mot = ligne.strip()
			mots.append(mot[::-1])
			for i in range(len(mot)-1):
				mots.append(mot[i::-1]+'!'+mot[i+1:])
		for mot in sorted(mots):
			gaddag.inserer(mot)
		gaddag.termine()
		print("Création du gaddag en {0}s".format(time.time()-start))
	return gaddag