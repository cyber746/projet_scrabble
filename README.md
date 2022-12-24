# projet_scrabble
Création d'un logiciel de Scrabble

test_fenetre est un ancien fichier à adapter pour faire une interface graphique du solveur.

Pour le moment, c'est une version minimale, le solveur marche. À tester avec des tirages à joker pour confirmer qu'il marche dans toutes les conditions.

Le dictionnaire est construit comme un GADDAG (cf. https://ericsink.com/downloads/faster-scrabble-gordon.pdf)
pour un fichier de mot, build_dic() construit le graphe.

La grille fonctionne sans case bonus pour l'instant. Le défaut est une grille de taille 15 classique avec case centrale comme case de début.

Pour faire marcher la recherche :

dico = build_dic() (environ 1 mn avec mon ordi pour construire le dico depuis le fichier complet de l'ods8, à l'avenir on importera directement le fichier contenant le graphe)

g = grille_test()

s = Solveur(dico, g, tirage) où tirage est la liste des lettres sur le chevalet (lettres en majuscule)



TO DO:

Renuméroter les noeuds du gaddag et le simplifier en liste pour l'importer/exporter facilement (un peu plus de 400 000 noeuds donc ça devrait être gérable)
Implémenter une fonction de compte, ce qui implique de faire une fonction de basant sur fichier de paramètres, ce qui permettrait d'avoir une grille complètement paramétrable.
On inclura dans le fichier de paramètres les primes selon le nombre de lettres posées.
Ensuite, il faudra adapter le fichier test_fenetre pour pouvoir faire du topping.


NB :
Le GADDAG permet moyennant une petite modif de faire du crab.
Le GADDAG de l'ODS8 peut être amélioré pour faire du clabbers (idée : ne stocker que les tirages rangés par ordre alphabétique)
