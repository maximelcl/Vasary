"""
vasary.py est un programme qui produit des tableaux d’art optique.
Auteur : Maxime Leclerc
Date : 21 avril 2020
Description : Les tableaux créés par vasary.py sont composés d'un pavage d'hexagone tricolore déformé par une sphère
en 3 dimensions en utilisant le module turtle.
Entrées : coin inférieur gauche du pavage, coin supérieur droit du pavage, les trois couleurs des hexagnes, les
du centre de la sphère de déformation ainsi que son rayon.
Sortie : Le dessin du tableau et éventuellement, l'enregistrement de ce dessin dans un fichier pavage.eps
"""

import turtle
from math import pi, sin, cos, sqrt, acos, asin

def hexagone(point, longueur, col, centre, rayon):
    """
    Dessine avec turtle un pave hexagonal éventuellement déformé par la sphère
    :param point: le centre de l'hexagone (x, y, z)
    :param longueur: longueur des arrêtes
    :param col: triplet des couleurs de remplissage
    :param centre: centre de la sphère de déformation
    :param rayon: rayon de la sphère
    """
    x, y, z = point #décompose le tuple point en ses différentes coordonnées avant déformation
    xprime, yprime, zprime = deformation(point, centre, rayon) #change la position de point grace à la fonction déformation
    turtle.up() #lève la plume
    turtle.goto(xprime, yprime)
    turtle.down() #baisse la plume
    angle = 0 #initialisation de l'angle avec lequel est fait chaque losange
    """
    Ci-dessous la boucle itère 3 fois pour dessiner 3 losanges, de 3 couleurs différentes
    et décalés d'un angle de 2 * pi / 3 à chaque fois.
    """
    for i in col:
        turtle.color(i)
        turtle.begin_fill()
        """
        Ci-dessous, la boucle qui dessine un losange en partant du centre(xprime, yprime). 
        (x_next, y_next) sont les coordonnées du prochain point à dessiner.
        """
        for i in range(3):
            x_next, y_next, z_next = x + longueur * cos(i * pi / 3 + angle), y + longueur * sin(i * pi / 3 + angle), 0
            x_next, y_next, z_next = deformation((x_next, y_next, z_next), centre, rayon)
            turtle.goto(x_next, y_next)
        turtle.goto(xprime, yprime) #la plume revient au centre de l'hexagone
        turtle.end_fill() #le losange se rempli
        angle += 2 * pi / 3 #incrémentation de l'angle du prochain losange

def deformation(p, centre, rayon):
    """ Calcul des coordonnées d'un point suite à la déformation
        engendrée par la sphère émergeante
        Entrées :
          p : coordonnées (x, y, z) du point du dalage à tracer
             (z = 0) AVANT déformation
          centre : coordonnées (X0, Y0, Z0) du centre de la sphère
          rayon : rayon de la sphère
        Sorties : coordonnées (xprim, yprim, zprim) du point du dallage
             à tracer APRÈS déformation
    """
    x, y, z = p
    xprim, yprim, zprim = x, y, z
    xc, yc, zc = centre
    if rayon**2 > zc**2:
        zc = zc if zc <= 0 else -zc
        r = sqrt(
            (x - xc) ** 2 + (y - yc) ** 2)  # distance horizontale
            # depuis le point à dessiner jusqu'à l'axe de la sphère
        rayon_emerge = sqrt(rayon ** 2 - zc ** 2) # rayon de la partie
            # émergée de la sphère
        rprim = rayon * sin(acos(-zc / rayon) * r / rayon_emerge)
        if 0 < r <= rayon_emerge: # calcul de la déformation
            # dans les autres cas
            xprim = xc + (x - xc) * rprim / r # les nouvelles coordonnées
            # sont proportionnelles aux anciennes
            yprim = yc + (y - yc) * rprim / r
        if r <= rayon_emerge:
            beta = asin(rprim / rayon)
            zprim = zc + rayon * cos(beta)
            if centre[2] > 0:
                zprim = -zprim
    return (xprim, yprim, zprim)

def pavage(inf_gauche, sup_droit, longueur, col, centre, rayon):
    """
    Dessine le pavage d'hexagones complet avec la déformation de la sphère
    :param inf_gauche: coin inférieur gauche du pavage
    :param sup_droit: coin supérieur droit du pavage
    :param longueur: longueur des arrêtes
    :param col: triplet des couleurs de remplissage
    :param centre: centre de la sphère de déformation
    :param rayon: rayon de la sphère
    """
    # initialisation de la position du premier hexagone en bas à gauche
    x, y, z = inf_gauche + longueur * cos(pi / 3), inf_gauche + longueur * sin(pi / 3), 0
    n = 1 #compteur de ligne
    while y <= sup_droit: #boucle while qui va dessiner chaque ligne d'hexagone
        while x <= sup_droit: # boucle while qui va dessiner chaque hexagone d'une ligne
            hexagone((x, y, z), longueur, col, centre, rayon)
            x += 3 * longueur
        #ci-dessous initialisation des coordonnées du prochain hexagone à dessiner
        y += longueur * sin(pi / 3)
        if n % 2 == 1:
            x = inf_gauche + longueur * (1 + 2 * cos(pi / 3))
        else:
            x = inf_gauche + longueur * cos(pi / 3)
        n += 1

"""
Ci-dessous, le programme demande à l'utilisateur de rentrer les différents paramètres de la fonction pavage.
La fonction pavage est executée.
Puis, le dessin final est enregistré dans le fichier pavage.eps du même dossier s'il existe.
"""
inf_gauche = float(input("Coin inférieur gauche (val, val) : "))
sup_droit = float(input("Coin supérieur droit (val, val) : "))
longueur = float(input("Longueur d'une arrête d'hexagone :"))
col1 = input("Première couleur : ")
col2 = input("Deuxième couleur : ")
col3 = input("Troisième couleur : ")
col = (col1, col2, col3)
x_c = float(input("Abscisse du centre de la sphère :  "))
y_c = float(input("Ordonnée du centre de la sphère :  "))
z_c = float(input("Hauteur du centre de la sphère :  "))
centre = (x_c, y_c, z_c)
rayon = float(input("Rayon de la sphère : "))

pavage(inf_gauche, sup_droit, longueur, col, centre, rayon)
turtle.getcanvas().postscript(file="pavage.eps")
turtle.done()
