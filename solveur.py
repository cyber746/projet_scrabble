from dico_gaddag import build_dic
from grille import grille_test

class Solveur:
	def __init__(self, dico, grille, chevalet):
		self.dico = dico
		self.grille = grille
		self.chevalet = chevalet
		self.pivot = [[dict() for _ in range(grille.taille)] for _ in range(grille.taille)]
		self.suff = [[dict() for _ in range(grille.taille)] for _ in range(grille.taille)]
		self.ancres = []
		self.trouves = []

	def avant(self, pos, direction):
		ligne, col = pos
		if direction == 'h':
			return ligne, col-1
		else:
			return ligne-1, col

	def apres(self, pos, direction):
		ligne, col = pos
		if direction == 'h':
			return ligne, col+1
		else:
			return ligne+1, col

	def shift(self, pos, shift, direction):
		ligne, col = pos
		if direction == 'h':
			return ligne, col+shift
		else:
			return ligne+shift, col

	def trouve_ancres(self):
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
					self.suff[ligne][col][direction] = suff

	def cherche(self):
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
		return self.trouves

	def autorises(self, pos, direction):
		ligne, col = pos
		try:
			return self.pivot[ligne][col][direction]
		except KeyError:
			return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

	def generer_coups(self, pos_ancre, shift, direction, mot, chevalet, node):
		pos_scan = self.shift(pos_ancre, shift, direction)
		if direction == 'h':
			direction_perp = 'v'
		else:
			direction_perp = 'h'
		if self.grille.est_occupe(pos_scan):
			lettre = self.grille.get_jeton(pos_scan)
			self.aller_a(pos_ancre, shift, direction, lettre, mot, chevalet, node)
		elif chevalet:
			for lettre in chevalet.copy():
				if lettre in self.autorises(pos_scan, direction_perp):
					chevalet.remove(lettre)
					self.aller_a(pos_ancre, shift, direction, lettre, mot, chevalet, node)
					chevalet.append(lettre)
			if '?' in chevalet:
				for lettre in self.autorises(pos_scan, direction_perp):
					chevalet.remove('?')
					self.aller_a(pos_ancre, shift, direction, lettre, mot, chevalet, node) #mettre lettre en minuscule ?
					chevalet.append('?')

	def aller_a(self, pos_ancre, shift, direction, lettre, mot, chevalet, node):
		pos_scan = self.shift(pos_ancre, shift, direction)
		if shift <= 0:
			mot = lettre + mot
			if node is not None and lettre in node.possibles and not self.grille.est_occupe(self.avant(pos_scan, direction)):
				self.enregistre(mot, pos_scan, direction)
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
			if node is not None and lettre in node.possibles and not self.grille.est_occupe(self.apres(pos_scan, direction)):
				self.enregistre(mot, self.shift(pos_scan, -len(mot)+1, direction), direction)
			node = self.dico.parcours(node, [lettre])
			if node is not None and self.grille.est_vide(self.apres(pos_scan, direction)):
				self.generer_coups(pos_ancre, shift+1, direction, mot, chevalet, node)

	def enregistre(self, mot, pos, direction):
		ref = chr(ord('A')+pos[0])
		if direction == 'h':
			ref += str(pos[1]+1)
		else:
			ref = str(pos[1]+1) + ref
		self.trouves.append((ref, mot))
