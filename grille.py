class Grille:
	"""Classe construisant la grille de jeu"""
	def __init__(self, taille, bonus):
		self.taille = taille
		self.jetons = []
		self.bonus = bonus
		self.mult_mot = get_multiplicateur('M')
		self.mult_lettre = get_multiplicateur('L')
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
		resultat = Grille(self.taille, self.bonus)
		for pos in self.coord_cases():
			resultat.set_jeton(pos, self.get_jeton(pos))
		return resultat

	def get_multiplicateur(self, char):
		g = []
		for ligne in self.bonus:
			l = []
			for case in ligne:
				if char in case:
					l.append(int(case[1:]))
				else:
					l.append(1)
			g.append(l)
		return g

def grille_test(src):
	"""routine de construction de la grille à partir d'un fichier de paramètres comme celui fourni"""
	bonus = []
	with open(src, 'r') as g_txt:
			taille = int(g_txt.readline().strip())
			for line in g_txt:
				ligne = line.strip().split(',')
				if len(ligne) != taille:
					return('Erreur dans le fichier de paramètres de la grille')
				else:
					bonus.append(ligne)
	return(Grille(taille, bonus))