from dico_gaddag import build_dic
from grille import grille_test

import time

class Solveur:
	"""Classe qui calcule le meilleur coup sur une grille donnée selon un tirage et un dico donnés"""
	def __init__(self, dico, grille, chevalet, valeurs, primes):
		self.dico = dico
		self.grille = grille
		self.chevalet = chevalet
		self.valeurs = valeurs
		self.primes = primes
		self.pivot = [[dict() for _ in range(grille.taille)] for _ in range(grille.taille)]
		self.pref = [[dict() for _ in range(grille.taille)] for _ in range(grille.taille)]
		self.suff = [[dict() for _ in range(grille.taille)] for _ in range(grille.taille)]
		self.score_pivot = [[dict() for _ in range(grille.taille)] for _ in range(grille.taille)]
		self.ancres = []
		self.trouves = []

	def avant(self, pos, direction):
		"""retourne la case avant pos dans une direction donnée"""
		ligne, col = pos
		if direction == 'h':
			return ligne, col-1
		else:
			return ligne-1, col

	def apres(self, pos, direction):
		"""retourne la case après pos dans une direction donnée"""
		ligne, col = pos
		if direction == 'h':
			return ligne, col+1
		else:
			return ligne+1, col

	def shift(self, pos, shift, direction):
		"""retourne la case shiftée de shift cases par rapport à pos dans une direction donnée"""
		ligne, col = pos
		if direction == 'h':
			return ligne, col+shift
		else:
			return ligne+shift, col

	def trouve_ancres(self):
		"""retourne les ancres (cases adjacentes à des jetons déjà sur la grille ou case centrale si grille vide)"""
		ancres = []
		for pos in self.grille.coord_cases():
			vide = self.grille.est_vide(pos)
			voisins_occupes = self.grille.est_occupe(self.avant(pos,'h')) or self.grille.est_occupe(self.apres(pos,'h')) or self.grille.est_occupe(self.avant(pos,'v')) or self.grille.est_occupe(self.apres(pos,'v')) 
			if vide and voisins_occupes:
				ancres.append(pos)
		if not ancres:
			ancres.append((7,7)) #à adapter plus tard
		self.ancres = ancres

	def update_pivot(self):
		"""Calcule les pivots suivant la grille donnée"""
		for pos in self.ancres:
			for direction in ['h', 'v']:
				pref, suff = "", ""
				pos_test = self.avant(pos, direction)
				while self.grille.est_occupe(pos_test):
					pref = self.grille.get_jeton(pos_test) + pref
					pos_test = self.avant(pos_test, direction)

				pos_test = self.apres(pos, direction)
				while self.grille.est_occupe(pos_test):
					suff = suff + self.grille.get_jeton(pos_test)
					pos_test = self.apres(pos_test, direction)

				ligne, col = pos
				if pref or suff:
					self.pivot[ligne][col][direction] = self.dico.pivot(pref, suff)
					self.pref[ligne][col][direction] = pref
					self.suff[ligne][col][direction] = suff
					self.score_pivot[ligne][col][direction] = self.compte_pivot(ligne, col, direction, pref+suff)

	def compte_pivot(self, ligne, col, direction, seq):
		"""Compte les mots en pivot"""
		compte = 0
		for lettre in seq:
			try:
				compte += self.valeurs[lettre]
			except KeyError:
				pass
		return compte

	def get_valeur(self, lettre):
		"""Retourne la valeur d'une lettre"""
		try:
			return self.valeurs[lettre]
		except KeyError:
			return 0

	def cherche(self):
		"""Cherche tous les coups possibles en parcourant toutes les ancres"""
		start = time.time()
		self.trouve_ancres()
		self.update_pivot()
		for ancre in self.ancres:
			for direction in ['h','v']:
				try:
					suff = self.suff[ancre[0]][ancre[1]][direction]
					node = self.dico.parcours(self.dico.root, list(suff))
				except KeyError:
					suff = ''
					node = self.dico.root
				chevalet = [x for x in self.chevalet]
				self.generer_coups(ancre, 0, direction, suff, chevalet, node)
		print("Recherche faite en {0}s".format(time.time()-start))

	def autorises(self, pos, direction):
		"""Retourne toutes les lettres autorisées sur une case pos"""
		ligne, col = pos
		try:
			return self.pivot[ligne][col][direction]
		except KeyError:
			return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	def generer_coups(self, pos_ancre, shift, direction, mot, chevalet, node):
		"""Pour une ancre donnée, essaye toutes les lettres possibles selon le dico (première routine de l'article)"""
		pos_scan = self.shift(pos_ancre, shift, direction)
		if direction == 'h':
			direction_perp = 'v'
		else:
			direction_perp = 'h'
		if self.grille.est_occupe(pos_scan):
			lettre = self.grille.get_jeton(pos_scan)
			self.aller_a(pos_ancre, shift, direction, lettre, mot, chevalet, node, False)
		elif chevalet:
			for lettre in set(chevalet.copy()):
				if lettre in self.autorises(pos_scan, direction_perp):
					chevalet.remove(lettre)
					self.aller_a(pos_ancre, shift, direction, lettre, mot, chevalet, node, False)
					chevalet.append(lettre)
			if '?' in chevalet:
				for lettre in self.autorises(pos_scan, direction_perp):
					chevalet.remove('?')
					self.aller_a(pos_ancre, shift, direction, lettre, mot, chevalet, node, True)
					chevalet.append('?')

	def aller_a(self, pos_ancre, shift, direction, lettre, mot, chevalet, node, est_jok):
		"""Une fois la lettre posée, teste toutes les cases sur lesquelles on peut continuer la recherche (deuxième routine de l'article)"""
		pos_scan = self.shift(pos_ancre, shift, direction)
		if shift <= 0:
			mot = lettre + mot
			if est_jok:
				mot = mot[:1].lower() + mot[1:]
			if node is not None and lettre in node.possibles and not self.grille.est_occupe(self.avant(pos_scan, direction)):
				self.enregistre(pos_scan, direction, mot)
			node = self.dico.parcours(node, [lettre])
			if node is not None:
				pos_scan = self.avant(pos_scan, direction)
				if pos_scan not in self.ancres:
					self.generer_coups(pos_ancre, shift-1, direction, mot, chevalet, node)
				node = self.dico.parcours(node, ['!'])
				try:
					shift_apres = len(self.suff[pos_ancre[0]][pos_ancre[1]][direction]) + 1
				except KeyError:
					shift_apres = 1
				if node is not None and not self.grille.est_occupe(pos_scan):
					self.generer_coups(pos_ancre, shift_apres, direction, mot, chevalet, node)
		else:
			mot = mot + lettre
			if est_jok:
				mot = mot[:-1] + mot[-1].lower()
			if node is not None and lettre in node.possibles and not self.grille.est_occupe(self.apres(pos_scan, direction)):
				self.enregistre(self.shift(pos_scan, -len(mot)+1, direction), direction, mot)
			node = self.dico.parcours(node, [lettre])
			if node is not None and self.grille.est_vide(self.apres(pos_scan, direction)):
				self.generer_coups(pos_ancre, shift+1, direction, mot, chevalet, node)

	def compte(self, pos, direction, mot):
		"""Compte le mot trouvé"""
		c = 0
		nb_lettres_posees = 0
		mult_mot = 1
		pos_scan = pos
		compte_pivot = 0
		if direction == 'h':
			direction_perp = 'v'
		else:
			direction_perp = 'h'
		for lettre in mot:
			valeur_lettre = self.get_valeur(lettre)
			if self.grille.est_occupe(pos_scan):
				c += valeur_lettre
			else:
				nb_lettres_posees += 1
				mult_lettre = self.grille.mult_lettre[pos_scan[0]][pos_scan[1]]
				mult_mot_pivot = self.grille.mult_mot[pos_scan[0]][pos_scan[1]]
				mult_mot *= mult_mot_pivot
				c += valeur_lettre*mult_lettre
				compte_pivot_case = self.score_pivot[pos_scan[0]][pos_scan[1]][direction_perp] #à tester pour voir si ça marche avec le None
				if compte_pivot_case > 0:
					compte_pivot_case += valeur_lettre*mult_lettre
				compte_pivot += mult_mot_pivot*compte_pivot_case
			pos_scan = self.apres(pos_scan, direction)
		return(mult_mot*c + compte_pivot + self.primes[nb_lettres_posees])

	def enregistre(self, pos, direction, mot):
		"""Enregistre un mot trouvé"""
		ref = chr(ord('A')+pos[0])
		if direction == 'h':
			ref += str(pos[1]+1)
		else:
			ref = str(pos[1]+1) + ref
		score = self.compte(pos, direction, mot)
		self.trouves.append((ref, mot, score))

	def tri_solutions(self): #à voir si cette fonction a sa place ici (peut-être dans un futur partie.py ?)
		self.trouves.sort(key = lambda a: (-a[2], a[1]))