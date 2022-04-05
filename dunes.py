
##################################################################
#                                                                #
#                   JEUX DES DUNES - PROGRAMME                   #
#                           UE PROJET                            #
#                                                                #             
##################################################################

# -*- coding: utf-8 -*-

""" IMPORT FONCTIONS """
#from dunes_test import * #import fichier de test 
import string
from colorama import Fore #gestion des couleurs
from colorama import Style
from random import randint
from random import sample #pour IA NAIVE
from math import sqrt

""" INITIALISATION """

nbr_lignes = 10 #on définit le nombre de lignes de la grille
nbr_colonnes = 10 # on définit le nombre de colonnes de la grille
grille = [[0 for _ in range(0, nbr_colonnes)] for _ in range(0,nbr_lignes)] #création de la grille initiale
tour_joueur=1  #on commence le jeu avec le joueur 1
joueur1 = 0
joueur2 = 0


"""DEFINITION DES FONCTIONS"""

def affichage_logo() :
    print("   ___ _____ _   _  ______ _____ _____  ______ _   _ _   _  _____ _____  ")
    print("  |_  |  ___| | | | |  _  \  ___/  ___| |  _  \ | | | \ | ||  ___/  ___| ")
    print("    | | |__ | | | | | | | | |__ \ `--.  | | | | | | |  \| || |__ \ `--.  ")
    print("    | |  __|| | | | | | | |  __| `--. \ | | | | | | | . ` ||  __| `--. \ ")
    print("/\__/ / |___| |_| | | |/ /| |___/\__/ / | |/ /| |_| | |\  || |___/\__/ / ")
    print("\____/\____/ \___/  |___/ \____/\____/  |___/  \___/\_| \_/\____/\____/ ")
    print("\n")


"""
afficher_grille() permet d'afficher la grille du jeu
elle est définit par le nombre de lignes et le nombres de colonnes
que l'on a définit au début du programme
"""
def afficher_grille(nbr_lignes, nbr_colonnes,demo) : 
    lettre_en_nbr = 65
    print()
    print(" ", end="")
    for i in range(1,nbr_lignes+1) :
        print("",i, end="  ")
    print()
    for ligne in range(0, nbr_lignes) :
        print(chr(lettre_en_nbr), end="")
        print("|", end="")
        for colonne in range(0, nbr_colonnes) :
            if grille[ligne][colonne] == 1 :
                print(" X ", end="")
            elif grille[ligne][colonne] == 2 :
                print(" O ", end="")
            else :
                print("   ", end="")
           
            print("|", end="")
        print("")
        lettre_en_nbr += 1
    print() 
    joueur1,joueur2 = nombre_pions_joueur()
    if demo==1 : #si demo = 1, on n'affiche pas le nombre de pions des joueurs
        pass
    else :
        if tour_joueur==1 :
            print(f'{Fore.GREEN}JOUEUR X : {Style.RESET_ALL}', "Il te reste", joueur1, "pion(s).") #affichage avec couleur
            print("JOUEUR O : ",joueur2)
        else :
            print("JOUEUR X : ",joueur1)
            print(f'{Fore.GREEN}JOUEUR O : {Style.RESET_ALL}', "Il te reste", joueur2, "pion(s).")
        

""" 
Fonction qui remet la grille à 0
"""
def init_grille() :
    for i in range(0,9) :
        for j in range(0,9) :
            grille[i][j] = 0


""" 
liste_pions() retourne une liste des pions du joueur demandé
"""
def liste_pion(joueur) :
    liste = []
    for i in range(0,nbr_lignes) :
        for j in range(0,nbr_colonnes) :
            if grille[i][j] == joueur :
                liste.append([(i,j)])
    return liste


"""
convertion_premier_caractere est utilisé dans la fonction convertir_coordonnees
elle permet de convertir A en 0, B en 1 ..., Z en 25
"""
def convertion_premier_caractere(lettre) : 
    liste_lettres = list(string.ascii_lowercase) #fonction qui crée une liste de toutes les lettres de l'alphabet (pour eviter de refaire un for)
    liste_chiffres = []
    for i in range(0,26) :
        liste_chiffres.append(i)
    indice = -1
    for i in liste_lettres :
        indice += 1
        if i == lettre :
            indice_lettre = indice
    return (liste_chiffres[indice_lettre])


"""
convertir_coordonnes permet de convertir la position entrée en coordonnees
exemple : A1 > (0,0) , A2 > (0,1)
"""
def convertir_coordonnees(code) :  #l'appel de la fonction convertion_premier_caractere permet de ne pas faire plusieurs if (if premier_caractere == "a" alors premier_caractere_conv == 0)
    premier_caractere = code[0]
    premier_caractere = premier_caractere.lower()
    deuxieme_caractere = code[1]
    liste_lettres = list(string.ascii_lowercase)
    if premier_caractere in liste_lettres :
        premier_caractere_conv = convertion_premier_caractere(premier_caractere)   
    deuxieme_caractere_conv = int(deuxieme_caractere)-1
    return (premier_caractere_conv,deuxieme_caractere_conv)


"""
est_dans_grille permet de vérifier si la case existe selon la taille de la grille
Sur une grille 5x5, A1 existe mais G9 n'existe pas
Sur une grille 10x10, G9 existe mais N23 n'existe pas
La fonction est donc adapté pour le changement de taille de grille
La condition code[1].isdigit() == True vérifie si code[1] (chaine de caractere) est aussi un entier
"""
def est_dans_grille(code) : 
    liste_ord_lignes = []
    liste_colonnes = []
    for ord_lettre in range(97,97+nbr_lignes) :
        liste_ord_lignes.append(ord_lettre) 
    for chiffre in range(1,1+nbr_colonnes) :
        liste_colonnes.append(chiffre)
    if ord(code[0].lower()) in liste_ord_lignes and code[1].isdigit() == True and int(code[1]) in liste_colonnes :
        erreur = 0 
    else :
        print("Le pion n'est pas dans la grille !")
        erreur = 1
    return erreur


"""
verif_joueur_sur_case permet de verifier que le joueur qui veut 
déplacer son pion à bien un pion sur cette case
Exemple : si le joueur 1 veut déplacer le pion B3 mais que le pion n'est pas à lui
il ne pourra pas.
"""
def verif_joueur_sur_case(code, numero_joueur) : #fct pour vérifier que le joueur qui veut déplacer son pion est bien sur cette case
    code_conv = convertir_coordonnees(code)
    if grille[code_conv[0]][code_conv[1]] == numero_joueur :
        return True #le joueur 1 est sur cette case
    else :
        print("Vous n'êtes pas sur cette case !")
        return False
  
    
"""
déplacer_pion() permet de déplacer un pion sur la grille
"""     
def deplacer_pion(code_avant,code_apres) :
    grille[code_avant[0]][code_avant[1]]=0
    grille[code_apres[0]][code_apres[1]]=2


"""
verifications_completes_avant permet de vérifier toutes les conditions nécessaires du pion à déplacer :
- on vérifie que le pion que le joueur veut déplacer existe (est_dans_grille)
- on vérifie que le pion que le joueur veut déplacer est le sien (verif_joueur_sur_case)

"""
def verifications_completes_avant(code, tour_joueur) :
    if est_dans_grille(code) == 1 :
        return False
    if verif_joueur_sur_case(code, tour_joueur) == False :
       return False
    return True
    
   
"""
verif_droit_deplacement permet de vérifier les conditions nécessaires pour avoir le droit déplacer le pion :
- on verifie que la case où on va poser le pion est bien vide
- on verifie qu'il fait bien un déplacement horizontal ou vertical de 1
"""
def verif_droit_deplacement(code_avant_conv, code) :
    code_apres_conv = convertir_coordonnees(code)
    if grille[code_apres_conv[0]][code_apres_conv[1]] != 0 : #si le déplacement demandé n'est pas vide
        print("Il y a un pion déjà sur cette case !")
        return False
    if (code_apres_conv[0],code_apres_conv[1]) != (code_avant_conv[0]+1,code_avant_conv[1]) and (code_apres_conv[0],code_apres_conv[1]) != (code_avant_conv[0],code_avant_conv[1]+1) and (code_apres_conv[0],code_apres_conv[1]) != (code_avant_conv[0]-1,code_avant_conv[1]) and (code_apres_conv[0],code_apres_conv[1]) != (code_avant_conv[0],code_avant_conv[1]-1) :
        print("Déplacement non autorise !")
        return False
    return True
        
"""
nombre_pions_joueur permet de compter le nombre de pions qu'il reste à chaque joueur
"""
def nombre_pions_joueur() :
    joueur1=0
    joueur2 = 0
    for i in grille :
        for j in i :
            if j==1 :
                joueur1 += 1
            elif j==2 :
                joueur2 += 1
    return joueur1,joueur2

"""
fin_de_partie vérifie si il reste encore des pions pour le joueur 1 et pour le joueur 2.
Si il n'y a plus de pion du joueur 1 alors le joueur 2 remporte la partie et inversement. 
"""
def fin_de_partie() :
    joueur1,joueur2 = nombre_pions_joueur()
    if joueur1 == 0 :
        print("Bravo ! Le joueur O a remporté la partie")
        return True
    elif joueur2 == 0 :
        print("Bravo ! Le joueur X a remporté la partie")
        return True
    else :
        return False
    
"""
placement_pions_init permet de placer les pions de départ suivant le type de grille
"""
def placement_pions_init(type_grille) :
    if type_grille == "1" : #INITIALISATION GRILLE 1
        for n in range(0,nbr_colonnes) :
            grille[1][n] = 1
            grille[3][n] = 2
            grille[nbr_colonnes-2][n] = 2
            grille[nbr_colonnes-4][n] = 1
    elif type_grille == "2" : #INITIALISATION AU HASARD DE LA GRILLE 2
        grille[0][0] = 1
        grille[0][3] = 2
        grille[6][1] = 1
        grille[0][8] = 1
        grille[3][8] = 2
        grille[5][6] = 2
        grille[1][9] = 1
        grille[9][9] = 2
        grille[9][7] = 1
    else : #INITIALISATION GRILLE 3
        grille[1][0] = 2
        grille[0][1] = 2
        grille[1][2] = 2
        grille[1][3] = 1
        grille[2][1] = 1
    
        
        
"""
choix_type_grille permet de demander à l'utilisateur quel type de grille il souhaite
"""
def choix_type_grille() :
    choix = "a" #on force l'entree dans la boucle
    print("\nSur quelle grille souhaitez-vous jouer ?")
    print("Grille de départ = 1")
    print("Grille de milieu = 2")
    print("Grille de fin = 3")
    while choix != "1" and choix!= "2" and choix != "3" : #on fait en str pour pouvoir traiter le cas où l'utilisateur entre des lettres.
        choix = input("Votre choix : ")
    return choix


"""
bord_grille() vérifie si la coordonnée est sur le bord de la grille (droite,gauche,haut,bas)
"""
def bord_grille(colonne,ligne) :
     return colonne<0 or colonne>=nbr_colonnes or ligne<0 or ligne>=nbr_lignes
 

"""
Verifie que l'on n'accede pas à une case hors de la grille (pour fct verif_manger_pion)
"""
def est_dans_intervalle(valeur,maxi) :
    return valeur>=0 and valeur<maxi
    
        
"""
on verifie si le joueur mange le pion adverse et on retourne la coordonnée du pion que l'on supprime
"""
def verif_manger_pion(code_avant_conv,code_apres_conv,tour_joueur) :
    pion_a_manger = []
    tour_joueur_adverse = tour_joueur%2+1
    ligne = code_apres_conv[0]
    colonne = code_apres_conv[1]
    if est_dans_intervalle(ligne+1,nbr_lignes) and grille[ligne+1][colonne] == tour_joueur_adverse : #si il y a un pion adverse au dessus
        if bord_grille(colonne,ligne+2) or (est_dans_intervalle(ligne+2,nbr_lignes) and grille[ligne+2][colonne] == tour_joueur) :
            pion_a_manger.append([ligne+1,colonne])
    if est_dans_intervalle(ligne-1,nbr_lignes) and grille[ligne-1][colonne] == tour_joueur_adverse : # si il y a un pion en dessous
        if bord_grille(colonne,ligne-2) or (est_dans_intervalle(ligne-2,nbr_lignes) and grille[ligne-2][colonne] == tour_joueur) :
            pion_a_manger.append([ligne-1,colonne])
    if est_dans_intervalle(colonne+1,nbr_colonnes) and grille[ligne][colonne+1] == tour_joueur_adverse : #si il y a un pion à droite
        if bord_grille(colonne+2,ligne) or (est_dans_intervalle(colonne+2,nbr_colonnes) and grille[ligne][colonne+2] == tour_joueur) :
            pion_a_manger.append([ligne,colonne+1])
    if est_dans_intervalle(colonne-1,nbr_colonnes) and grille[ligne][colonne-1] == tour_joueur_adverse : #si il y a un pion à gauche
        if bord_grille(colonne-2,ligne) or (est_dans_intervalle(colonne-2,nbr_colonnes) and grille[ligne][colonne-2] == tour_joueur) :
            pion_a_manger.append([ligne,colonne-1])
    return pion_a_manger


"""
manger_pion() permet de supprimer le/les pions qui ont été mangés
"""
def manger_pion(pion_a_manger) :
    for coordonnees in pion_a_manger :
        grille[coordonnees[0]][coordonnees[1]] = 0
        

"""
saisir_coordonnees_avant permet de saisir les coordonnées du pion à déplacer (vérifications incluses)
"""
def saisir_coordonnees_avant() :
    code = input("Quel pion souhaitez-vous déplacer ? ")
    while len(code)<2 :
        print("Vos coordonnées doivent être de la forme 'A1' !")
        code = input("Quel pion souhaitez-vous déplacer ? ")
    code = code[0],code[1:]
    while (verifications_completes_avant(code,tour_joueur) == False ) :
        code = input("Quel pion souhaitez-vous déplacer ? ") 
        while len(code)<2 :
            print("Vos coordonnées doivent être de la forme 'A1' !")
            code = input("Quel pion souhaitez-vous déplacer ? ")
        code = code[0],code[1:]
    code_conv = convertir_coordonnees(code)
    grille[code_conv[0]][code_conv[1]] = 0
    return code_conv

            

"""
saisir_coordonnees_avant permet de saisir les coordonnees de l'emplacement où l'on souhaite placer le pion (vérifications incluses)
"""
def saisir_coordonnees_apres(tour_joueur) :
    code = input("Où souhaitez-vous déplacer le pion ? ")
    while len(code)<2 :
        print("Vos coordonnées doivent être de la forme 'A1' !")
        code = input("Où souhaitez-vous déplacer le pion ? ")
    code = code[0],code[1:]
    while (est_dans_grille(code) == 1 or verif_droit_deplacement(code_avant_conv, code) == False) :
        code = input("Où souhaitez-vous déplacer le pion ? ")
        while len(code)<2 :
            print("Vos coordonnées doivent être de la forme 'A1' !")
            code = input("Où souhaitez-vous déplacer le pion ? ")
        code = code[0],code[1:]
    code_conv = convertir_coordonnees(code)
    if tour_joueur == 1 :
        grille[code_conv[0]][code_conv[1]] = 1
    else :
        grille[code_conv[0]][code_conv[1]] = 2
    return code_conv
 
    
"""
Fonction pour choisir le mode de jeu (1 VS 1, 1 VS IA)
"""
def choix_mode() :
    choix = "a" #on force à rentrer dans la boucle
    print("Quel mode de jeu souhaitez-vous utiliser ?\n1 = Joueur 1 VS joueur 2\n2 = Joueur 1 VS IA")
    while choix != "1" and choix != "2" : #on traite en str pour les cas où l'utilisateur tape des lettres
        choix = input("Veuillez choisir un mode entre 1 ou 2 : ")
    return choix
    
#"""FONCTIONS POUR IA NAIVE"""
#Les fonctions de l'IA NAIVE sont commentées pour ne pas alourdir le code 
#   
#def creation_liste_hasard() :#création d'une liste pour générer aléatoirement les déplacements possibles du pion
#    liste1 = [1,2,3,4]
#    liste = sample(liste1, 4)
#    return liste
#
#def selection_pion_hasard() : #on sélectionne un pion au hasard
#    ligne_hasard = 0
#    colonne_hasard = 0
#    while grille[ligne_hasard][colonne_hasard] != 2 :
#        ligne_hasard = randint(0,9)
#        colonne_hasard = randint(0,9)
#    selection_pion = ligne_hasard,colonne_hasard
#    return (selection_pion)


#def deplacement_pions(code_avant) : #on effectue le déplacement du pion
#   code_apres = code_avant
#    compteur = 0
#    liste = creation_liste_hasard()
#    while compteur<len(liste) and verif_droit_deplacement_hasard(code_avant,code_apres) == False :
#        if liste[compteur] == 1 :
#            code_apres = (code_avant[0]+1,code_avant[1])
#        elif liste[compteur] == 2 :
#            code_apres = (code_avant[0]-1,code_avant[1])
#        elif liste[compteur] == 3 :
#            code_apres = (code_avant[0],code_avant[1]+1)
#        else :
#            code_apres = (code_avant[0],code_avant[1]-1)
#        compteur+=1
#    if compteur>len(liste) or verif_droit_deplacement_hasard(code_avant,code_apres) == False:
#        code_avant = selection_pion_hasard()
#        return deplacement_pions(code_avant)
#    grille[code_avant[0]][code_avant[1]] = 0
#    grille[code_apres[0]][code_apres[1]] = 2
#    return code_apres
        
#def verif_droit_deplacement_hasard(code_avant, code_apres) : #on vérifie si le déplacement est autorisé
#    if est_dans_grille_hasard(code_apres) == 1 :
#        return False
#    if grille[code_apres[0]][code_apres[1]] != 0 : #si le déplacement demandé n'est pas vide
#        return False
#    if (code_apres[0],code_apres[1]) != (code_avant[0]+1,code_avant[1]) and (code_apres[0],code_apres[1]) != (code_avant[0],code_avant[1]+1) and (code_apres[0],code_apres[1]) != (code_avant[0]-1,code_avant[1]) and (code_apres[0],code_apres[1]) != (code_avant[0],code_avant[1]-1) :
#        return False
#    return True

#def est_dans_grille_hasard(code) : #on vérifie que le code est dans la grille (fct est_dans_grille_hasard() != est_dans_grille() car traitement sur tuple)
#    liste = []
#    for chiffre in range(0,nbr_colonnes) :
#        liste.append(chiffre)
#    if code[0] in liste and code[1] in liste :
#        erreur = 0 
#    else :
#        erreur = 1
#    return erreur

""" FONCTIONS POUR IA AVANCEE"""


def verif_droit_deplacement_ia(code_avant, code_apres,pas) : #on vérifie si le déplacement est autorisé + gestion du pas pour vérifier si les déplacement+2,+3, etc sont autorisés (conditions et code != de la fonction verif_droit_deplacement)
    code_avant=code_avant[0]
    if est_dans_grille_ia(code_apres) == 1 :
        return False
    if grille[code_apres[0]][code_apres[1]] != 0 : #si le déplacement demandé n'est pas vide
        return False
    if (code_apres[0],code_apres[1]) != (code_avant[0]+pas,code_avant[1]) and (code_apres[0],code_apres[1]) != (code_avant[0],code_avant[1]+pas) and (code_apres[0],code_apres[1]) != (code_avant[0]-pas,code_avant[1]) and (code_apres[0],code_apres[1]) != (code_avant[0],code_avant[1]-pas) :
        return False
    return True
    

def est_dans_grille_ia(code) : #on vérifie que le code est dans la grille (fct est_dans_grille_ia() != est_dans_grille() car traitement sur tuple)
    liste = []
    for chiffre in range(0,nbr_colonnes) :
        liste.append(chiffre)
    if code[0] in liste and code[1] in liste :
        erreur = 0 
    else :
        erreur = 1
    return erreur


def liste_coups_possibles(liste_init,pas) : #on fait une liste des coups possibles pour chaque pion
    compteur=0
    for i in liste_init :
        code = liste_init[compteur]
        if verif_droit_deplacement_ia(code,(code[0][0]+pas,code[0][1]),pas) == True: #BAS
            liste_init[compteur].append((code[0][0]+pas,code[0][1]))
        if verif_droit_deplacement_ia(code,(code[0][0],code[0][1]+pas),pas) == True :#DROITE
            liste_init[compteur].append((code[0][0],code[0][1]+pas))
        if verif_droit_deplacement_ia(code,(code[0][0]-pas,code[0][1]),pas) == True :#HAUT
            liste_init[compteur].append((code[0][0]-pas,code[0][1]))
        if verif_droit_deplacement_ia(code,(code[0][0],code[0][1]-pas),pas) == True :#GAUCHE
            liste_init[compteur].append((code[0][0],code[0][1]-pas))
        compteur+=1
    return liste_init
      

""" 
On regarde quel pion mange le plus de pions.
Si aucun pion ne mange alors :
    - On regarde si il y a possibilité que l'on sa fasse manger par l'adversaire :
        si c'est le cas on change de case
        sinon on regarde le chemin pour manger le plus de pions dans les tours suivants (coups+2,coups+3, ...) et on se déplace en fonction
"""
def recup_pion_a_deplacer(liste_coups,joueur,etape) : 
    nbr_manger_pions = 0
    pion_a_deplacer = []
    for liste in liste_coups :
        nbr_pions = len(liste)
        for j in range(1,nbr_pions) :
            if len(verif_manger_pion(liste[0],liste[j],joueur)) > nbr_manger_pions :
                pion_a_deplacer = [liste[0],liste[j]]
                nbr_manger_pions = len(verif_manger_pion(liste[0],liste[j],joueur))
    if etape == 2 :
        if len(pion_a_deplacer) == 0 : #si on ne mange aucun pion 
            if adverse_va_me_manger(2,1) != False : #si le joueur peut nous manger un pion
                pion = [[tuple(adverse_va_me_manger(2,1)[0])]]
                pions_deplacements = liste_coups_possibles(pion,1)
                pions_deplacements = pions_deplacements[0]
                deplacement_random = randint(1,2)
                code_avant,code_apres = pions_deplacements[0],pions_deplacements[deplacement_random]
                pion_a_deplacer = [code_avant,code_apres]
            else : #on ne mange pas de pion, l'adversaire ne peut pas nous manger donc on regarde au coup+2,coups+3, etc ...
                pas = 2
                deplacement = []
                while len(deplacement) == 0 :
                    deplacement = pions_n_coups(pas)
                    pas += 1
                pion_a_deplacer = distance_dep(deplacement)
    return pion_a_deplacer
    
def distance_dep(deplacement) :
    dep, dep1 = [[deplacement[0]]],deplacement[1]
    liste = liste_coups_possibles(dep,1)
    liste = liste[0]
    distance_min = 100
    for i in range(1,len(liste)) :
        point = liste[i]
        xa,ya,xb,yb = point[0],point[1],dep1[0],dep1[1]
        if calcul_distance(xa,xb,ya,yb) < distance_min :
            distance_min = calcul_distance(xa,xb,ya,yb)
            point_min = point
    return [dep[0][0],point_min]

def calcul_distance(xa,xb,ya,yb) :
    return sqrt(abs(((xb-xa)**2)-((yb-ya)**2)))
    
def adverse_va_me_manger(joueur,pas) : #fonction pour savoir si l'adversaire peut nous manger ou pas
    pion_adverse = recup_pion_a_deplacer(liste_coups_possibles(liste_pion(joueur%2+1),pas),joueur%2+1,1) 
    if pion_adverse != [] :
        return verif_manger_pion(pion_adverse[0],pion_adverse[1],joueur%2+1) #retourne le pion que l'adversaire peut nous manger
    else :
        return False
    
def pions_n_coups(pas) :
    return recup_pion_a_deplacer(liste_coups_possibles(liste_pion(2),pas),2,1)
  
    
""" 
AFFICHAGE DES REGLES DU JEU
"""

def demo() : #choix si on affiche les règles ou pas
    choix_demo = input("Pour connaître les règles appuyer sur R, sinon appuyer sur n'importe quelle touche : ")
    if choix_demo == "R" or choix_demo == "r" :
        print("Bienvenue dans le jeu des Dunes. Voici les règles :\nVous pouvez choisir de jouer contre un autre joueur ou vous pouvez choisir de jouer contre une IA.\nChacun votre tour vous devrez déplacer un de vos pions de manière à manger les pions de votre adversaire. Le joueur qui n'a plus de pions à perdu la partie.\nVoici les différentes manières de manger un pion :\n")
        print("####################################################################/n")
        possibilite1()
        possibilite2()
        possibilite3()
        print("#####################################################################################\n")
    else :
        pass

def possibilite1() : #affichage capture1
    grille[2][2] = 2
    grille[2][3] = 1
    grille[2][4] = 2
    afficher_grille(nbr_lignes,nbr_colonnes,1) 
    print("Bloquer le pion adverse entre 2 de vos pions : le pion X est mangé par les pions O.\n")
    
def possibilite2() : #affichage capture2
    init_grille()
    grille[2][0] = 1
    grille[2][1] = 2
    afficher_grille(nbr_lignes,nbr_colonnes,1) 
    print("Bloquer le pion adverse entre la bordure et un de vos pions : le pion X est mangé par le pion O.\n")
    
def possibilite3() : #affichage capture3
    init_grille()
    grille[0][1] = 2
    grille[1][1] = 1
    grille[2][0] = 1
    grille[2][2] = 1
    grille[2][3] = 2
    grille[3][1] = 2
    afficher_grille(nbr_lignes,nbr_colonnes,1) 
    print("Bloquer plusieurs pions adverses entre vos pions et les bordures : les pions O mangent tous les pions X.\n")


"""
Fonction qui affiche le tour en cours
"""
def joueur_est_ia(choix_jeu,tour_joueur) :
    if choix_jeu == "1" : #JOUEUR 1 VS 1
        if tour_joueur == 1 : #si c'est au joueur1 de jouer 
            print("C'est au joueur X de jouer !")
            return False
        else : 
            print("C'est au joueur O de jouer !")
            return False
    else :
        if tour_joueur == 1 : #JOUEUR VS MACHINE
            print("C'est au joueur X de jouer !")
            return False
        else :
            print("\nL'ordinateur vient de jouer !")
            return True
        

def conv_chiffre_lettre(code) :
    lettres = list(string.ascii_lowercase)
    code0 = code[0]
    code1 = code[1]
    return (str(lettres[code0].upper())+str(code1+1))

"""TESTS"""
#print("Lancement des tests :")
#verif_tests_complets() #fonctions qui appelle les tests
#print("Tous les tests ont été validés")
        
    
"""PROGRAMME PRINCIPAL"""

affichage_logo() #affichage "Jeu des Dunes"
demo() #affichage des règles si l'utilisateur le souhaite
choix_jeu = choix_mode() #on choisit le mode de jeux (1vs1, 1vsIA)
placement_pions_init(choix_type_grille()) #on place les pions de départ en fonction de la grille choisit
afficher_grille(nbr_lignes,nbr_colonnes,0) #affichage de la grille

while fin_de_partie() == False : #tant que la partie n'est pas terminée
    if joueur_est_ia(choix_jeu,tour_joueur) == False : #si ce n'est pas une IA qui joue
        code_avant_conv = saisir_coordonnees_avant() #pion à déplacer
        code_apres_conv = saisir_coordonnees_apres(tour_joueur)#emplacement du pion à placer
    else :
        code_avant_conv = (recup_pion_a_deplacer(liste_coups_possibles(liste_pion(2),1),2,2))[0] #pion à déplacer IA  AVANCEE
        code_apres_conv = (recup_pion_a_deplacer(liste_coups_possibles(liste_pion(2),1),2,2))[1] #déplacement du pion de l'IA  AVANCEE
        #code_avant_conv = selection_pion_hasard() #sélection du pion de l'IA NAIVE
        #code_apres_conv = deplacement_pions(code_avant_conv) #déplacement du pion de l'IA NAIVE
        deplacer_pion(code_avant_conv,code_apres_conv) #on déplace le pion
    print("Pion déplacé : ", conv_chiffre_lettre(code_avant_conv), "->", conv_chiffre_lettre(code_apres_conv))
    liste_pions = verif_manger_pion(code_avant_conv,code_apres_conv,tour_joueur) #on vérifie si il y a un pion à manger
    manger_pion(liste_pions) #on mange le/les pions
    tour_joueur = tour_joueur%2+1 #changement de tour du joueur (variation entre 1 et 2)
    afficher_grille(nbr_lignes,nbr_colonnes,0)
    

