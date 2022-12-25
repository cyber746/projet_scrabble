class Grille:
	def __init__(self, taille):
		#à adapter pour inclure cases bonus
		self.jetons = []
		self.taille = taille
		for i in range(taille):
			ligne = []
			for j in range(taille):
				ligne.append(None)
			self.jetons.append(ligne)

	def __str__(self):
		return '\n'.join(''.join(x if x is not None else '_' for x in ligne) for ligne in self.jetons)

	def coord_cases(self):
		liste_coord = []
		for ligne in range(self.taille):
			for col in range(self.taille):
				liste_coord.append((ligne, col))
		return liste_coord

	def get_jeton(self, pos):
		ligne, col = pos
		return self.jetons[ligne][col]

	def set_jeton(self, pos, jeton):
		ligne, col = pos
		self.jetons[ligne][col] = jeton
	
	def check_limites(self, pos):
		ligne, col = pos
		return ligne >= 0 and ligne < self.taille and col >= 0 and col < self.taille

	def est_vide(self, pos):
		return self.check_limites(pos) and self.get_jeton(pos) is None

	def est_occupe(self, pos):
		return self.check_limites(pos) and self.get_jeton(pos) is not None

	def copy(self):
		#à adapter pour cases bonus
		resultat = Grille(self.size)
		for pos in self.coord_cases():
			resultat.set_jeton(pos, self.get_jeton(pos))
		return resultat

def grille_test():
	g = Grille(15)
	return g
