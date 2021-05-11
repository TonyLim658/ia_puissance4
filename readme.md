# Puissance 5
## Description 

Ce projet à été réalisé suite a un cours d'intelligence artificielle.
Le jeu permet de jouer contre un robot ou contre un autre joueur sur le même système. 
Le but principale n'était pas de permettre le jeu entre deux joueurs donc aucun websocket ne permet à deux joueur de se confronter via 2 systèmes différents.

## Algorithmes Utilisés

La décision du bot est prinicipalement prise grâce à un arbre de décision basé sur un minimax de profondeur 5. Pour les noeuds non terminaux dans la dernière profondeur une euristique qui imite la logique humaine permet de choisir un score pour que le noeud non terminal devienne temporairement une feuille. Pour diminuer le temps de calcul un élagage "alpha beta" est réalisé sur l'arbre de décision.

## Technologie

Les algorithmes ont été implémentés en python. On a donc inclu ces algos dans un framework django pour pouvoir facilement y ajouter un IHM web intuitive.

## Utilisation 

Vous pouvez découvrir l'application [ici](https://nicolas-bourneuf.fr/puissance5) : [https://nicolas-bourneuf.fr/puissance5](https://nicolas-bourneuf.fr/puissance5)