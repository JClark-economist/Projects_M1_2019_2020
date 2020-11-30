def convertisseur_de_caractere(liste):
    """Parcours d'une chaine de caractère en remplacant"""
    taille=len(liste)
    separateur_de_car=[i for i in liste]
    for j in range(0,taille):
        if separateur_de_car[j]=='-' or separateur_de_car[j]=='o':
            separateur_de_car[j]=0
        else:
            separateur_de_car[j]=1
    return separateur_de_car

def convertisseur_labyrinthe(liste_de_liste):
    """Parcours d'une liste de chaine de caractère en remplacant"""
    nombre_de_lignes=len(liste_de_liste)
    couche_labyrinthe=[]
    for ligne in range(0,nombre_de_lignes):
        couche_labyrinthe.append(convertisseur_de_caractere(liste_de_liste[ligne]))
    return couche_labyrinthe

def convertisseur_labyrinthe_3d(liste_de_matrices):
    """Nouveau"""
    nombre_de_matrices=len(liste_de_matrices)
    labyrinthe=[]
    for matrice in range(0,nombre_de_matrices):
        labyrinthe.append(convertisseur_labyrinthe(liste_de_matrices[matrice]))
    return labyrinthe

def exploration_des_cases_vides(corps):
    """Retourne les coordonnées des passages
    """
    #Modifiée
    c=len(corps)
    n=len(corps[0])
    m=len(corps[0][0])
    liste_cases_vides=[]
    for indice_couche in range(0,c):
        for indice_ligne in range(0,n):
            for indice_colonne in range(0,m):
                if corps[indice_couche][indice_ligne][indice_colonne] == 1:
                    liste_cases_vides.append((indice_couche,indice_ligne,indice_colonne))
    return liste_cases_vides  

def creation_des_aretes(corps):
    sommets=exploration_des_cases_vides(corps)
    liste_aretes=[]
    #Modifiée
    for sommet1 in sommets:
        for sommet2 in sommets:
            if sommet1[0]==sommet2[0] and sommet1[1]==sommet2[1]and sommet1[2]+1==sommet2[2] :
                liste_aretes.append((sommet1,sommet2)) 
            elif sommet1[0]==sommet2[0] and sommet1[1]==sommet2[1]and sommet1[2]==sommet2[2]+1 :      
                liste_aretes.append((sommet1,sommet2))
            elif sommet1[0]==sommet2[0] and sommet1[1]+1==sommet2[1]and sommet1[2]==sommet2[2] :    
                liste_aretes.append((sommet1,sommet2))
            elif sommet1[0]==sommet2[0] and sommet1[1]==sommet2[1]+1 and sommet1[2]==sommet2[2] :
                liste_aretes.append((sommet1,sommet2))
            elif sommet1[0]+1==sommet2[0] and sommet1[1]==sommet2[1]and sommet1[2]==sommet2[2] :    
                liste_aretes.append((sommet1,sommet2))
            elif sommet1[0]==sommet2[0]+1 and sommet1[1]==sommet2[1] and sommet1[2]==sommet2[2] :
                liste_aretes.append((sommet1,sommet2))and liste_aretes.append((sommet2,sommet1))
    return liste_aretes
    
def est_non_oriente(arretes):
    for sommet1, sommet2 in arretes:
        if not (sommet2, sommet1) in arretes:
            return False
    return True
    
def transformation_voisinage(sommets, arretes):
    resultat = dict()
    for sommet in sommets:
        resultat[sommet] = list()
    for sommet1, sommet2 in arretes:
        resultat[sommet1].append(sommet2)
    return resultat

def remonte_arbre(arbre, depart, arrivee):
    #Codage de la récursion
    resultat = list()
    noeud_courant = arrivee
    while noeud_courant in arbre:
        resultat.append(noeud_courant)
        if noeud_courant == depart:
            resultat.reverse()
            return resultat
        noeud_courant = arbre[noeud_courant]
    raise ValueError("Pas de chemin")

def coord_entree(entree):
    #Nouveau
    n=len(entree)
    m=len(entree[0])
    for i_ligne in range(0,n):
        for i_colonne in range(0,m):
            if entree[i_ligne][i_colonne]==1:
                return (0,i_ligne,i_colonne)
def coord_sortie(sortie,corps):
    n=len(sortie)
    m=len(sortie[0])
    c=len(corps)
    for i_ligne in range(0,n):
        for i_colonne in range(0,m):
            if sortie[i_ligne][i_colonne]==1:
                return (c-1,i_ligne,i_colonne)
def dfs(voisinage, entree, sortie,corps):
    #Codage de l'algorithme d'exploration en profondeur, lent mais qui permet l'exploration de tout les potentiels chemins
    #Modifiée
    coor_entree=coord_entree(entree)
    coor_sortie=coord_sortie(sortie,corps)
    visites = list()
    vus = list()
    vus.append(coor_entree)
    vus_part = dict()
    vus_part[coor_entree] = None
    while vus:
        noeud_courant = vus.pop()
        if not noeud_courant in visites:
            visites.append(noeud_courant)
            for voisin in voisinage[noeud_courant]:
                vus.append(voisin)
                if not voisin in vus_part:
                    vus_part[voisin] = noeud_courant
    return remonte_arbre(vus_part, coor_entree, coor_sortie)
    
def taille_de_l_interface(taille_de_ligne, hauteur_du_labyrinthe,nombre_de_couches):
    #Modifiée
    cellule='{}'
    nombre_de_cel_par_ligne=cellule*taille_de_ligne+'\n'
    taille_couche=nombre_de_cel_par_ligne*(hauteur_du_labyrinthe)+'\n'
    taille_labyrinthe=(nombre_de_couches+2)*taille_couche
    return taille_labyrinthe

def crea_interface(entree,corps,sortie,solveur):
    #Modifiée
    n=len(corps[0])
    m=len(corps[0][0])
    c=len(corps)
    for chemin in solveur:
        for p in range(0,c):
            for i in range(0,n):
                for j in range(0,m):
                    if chemin[0]==p and chemin[1]== i and chemin[2]==j:
                        corps[p][i][j]=2    
    #création de l'interface
    filtree = list()
    for l1 in range(0,n):
        for cel1 in entree[l1]:
            if cel1 == 0:
                filtree.append("-")
            else:
                filtree.append(" ")
    for couche in range(0,c):
        for ligne in range(0,n):
            for cel in corps[couche][ligne]:
                if cel == 0:
                    filtree.append("o")
                elif cel==1:
                    filtree.append("x")
                else:
                    filtree.append(" ")
    for l2 in range(0,n):
        for cel2 in sortie[l2]:
            if cel2 == 0:
                filtree.append("-")
            else:
                filtree.append(" ")
    return filtree

def resolution(entree,corps,sortie):
    #Modifiée
    #Formatage du labyrinthe
    
    entree=convertisseur_labyrinthe(entree)
    sortie=convertisseur_labyrinthe(sortie)
    corps=convertisseur_labyrinthe_3d(corps)
    
    n=len(corps[0])
    m=len(corps[0][0])
    c=len(corps)
    
    #trouver les sommets les arretes et lancer le solveur
    sommets=exploration_des_cases_vides(corps)
    aretes=creation_des_aretes(corps)
    voisinage=transformation_voisinage(sommets, aretes)
    solveur=dfs(voisinage, entree, sortie,corps)
    
    print (solveur)
    
    #parcourir les coordonnées du chemin le plus court les transformer en 2 afin de pouvoir facilement les transformer
    #Création de l'interface
    
    filtree=crea_interface(entree,corps,sortie,solveur)
    
    return taille_de_l_interface(m,n,c).format(*filtree)