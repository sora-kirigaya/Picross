from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import Image

# Création de la fenêtre principale
fenetre = Tk()
fenetre.configure(bg = "lightgray")
fenetre.title("Picross")

# Création des différentes frames
frame_accueil = Frame(fenetre, bg="lightgreen")
frame_jeu = Frame(fenetre, bg="white")
frame_defaite = Frame(fenetre, bg="red")
frame_victoire = Frame(fenetre, bg="blue")
frame_demander_taille = Frame(fenetre, bg="white")
frame_creer_niveau = Frame(fenetre, bg="white")

def switch_to_frame_accueil():
    "passe à la frame accueil et cache les autres frames"
    frame_accueil.pack(fill="both", expand=True)
    frame_defaite.pack_forget()
    frame_victoire.pack_forget()
    frame_jeu.pack_forget()
    frame_creer_niveau.pack_forget()
    bouton_accueil.pack_forget()

def switch_to_frame_jeu(image):
    "passe à la frame jeu et cache les autres frames"
    frame_accueil.pack_forget() 
    frame_defaite.pack_forget()
    frame_creer_niveau.pack_forget()
    bouton_accueil.pack(side = "top")
    frame_jeu.pack()
    nouvelle_partie(image)

def switch_to_frame_defaite():
    "passe à la frame défaite et cache les autres frames"
    frame_jeu.pack_forget()  # Cache le jeu
    frame_creer_niveau.pack_forget()
    frame_defaite.pack(fill="both", expand=True)  # Affiche la défaite
    bouton_accueil.pack(side = "top")

def switch_to_frame_victoire():
    "passe à la frame victoire et cache les autres frames"
    frame_jeu.pack_forget()  # Cache le jeu
    frame_creer_niveau.pack_forget()
    frame_victoire.pack(fill='both', expand=True)  # Affiche la victoire
    bouton_accueil.pack(side = "top")
    
def switch_to_frame_creer_niveau():
    "passe à la frame pour créer son picross et cache les autres frames"
    frame_accueil.pack_forget()
    frame_creer_niveau.pack(side = "bottom")
    bouton_accueil.pack(side = "top")

def indications_lignes(solution, longueur):
    "Prend en entrée la solution et la taille de la ligne et renvoie les indices pour toutes les lignes sous forme de liste"
    indications = []
    for ligne in range(longueur):
        indication = []
        bloc = 0
        for cases in solution[ligne]:
            if cases == 1:
                bloc += 1
            elif bloc != 0:
                indication.append(bloc)
                bloc = 0
        if bloc != 0:
            indication.append(bloc)
        if indication == []:
            indication.append(0)
        indications.append(indication)
    return indications

def trouver_couleur_proche(couleur):
    "Prend en entrée le tuple de la couleur et renvoie 0 si la couleur est proche du blanc et 1 sinon"
    nouvelle_couleur = []
    superieur_125 = 0
    for rgb in couleur:
        if rgb > 185:
            nouvelle_couleur.append(250)
            superieur_125 += 1
        else:
            nouvelle_couleur.append(0)
    if superieur_125 < 2:
        return 1
    else:
        return 0

def transformer_image(nom_du_fichier):
    "Prend en entrée un nom de fichier et renvoie une liste de 0 et 1, associés à la couleur de chaque pixel"
    image_entree = Image.open(nom_du_fichier)
    code = []
    pixel_map = image_entree.load()
    width = image_entree.size[0]
    height = image_entree.size[1]
    for i in range(height):
        ligne = []
        for j in range(width):
            couleur = pixel_map[j, i]
            if couleur == (0, 0, 0):
                ligne.append(1)
            elif couleur == (250, 250, 250):
                ligne.append(0)
            else:
                ligne.append(trouver_couleur_proche(couleur))
        code.append(ligne)
    return code

def indications_colonnes(reponse, largeur):
    "Prend en entrée la solution et la taille de la colonne et renvoie les indices pour toutes les colonnes sous forme de liste"
    grille_tournee = []
    for colonne in range(largeur_grille):
        ligne = []
        for cellule in range(hauteur_grille):
            ligne.append(reponse[cellule][colonne])
        grille_tournee.append(ligne)
    return indications_lignes(grille_tournee, largeur) # utilise la fonction indications_lignes() pour obtenir les indices des colonnes (puisque la grille est tournée)

def souris_cliquee(event):
    "Prend en entrée l'événement et appelle la fonction creer_case pour colorier/cocher les cases"
    # calcule la case dans laquelle on a cliqué
    x = (event.x - espace_avant_grille_lignes) // largeur_case 
    y = (event.y - espace_avant_grille_colonnes) // largeur_case

    if (x >= 0 and y >= 0) and (x <= largeur_grille and y <= hauteur_grille): # vérifie qu'on a cliqué dans la grille
        if tableau_joueur[y][x] == 0 or tableau_joueur[y][x] == "croix": # vérifie que la case est vide, ou qu'il y a une croix, sinon il ne se passe rien
            if mode == "colorier":
                tableau_joueur[y][x] = 1 
            elif mode == "barrer" and tableau_joueur[y][x] == "croix":
                tableau_joueur[y][x] = 0
            else:
                tableau_joueur[y][x] = "croix"
        
            global nombre_cases_coloriees
            if tableau_joueur[y][x] == reponse[y][x] or tableau_joueur[y][x] == "croix" or tableau_joueur[y][x] == 0: # vérifie que c'est correct si on a colorié ou qu'on a mis une croix (n'entraine pas d'erreurs)
                creer_case(y, x, tableau_joueur[y][x], False)
                if tableau_joueur[y][x] == 1:
                    nombre_cases_coloriees -= 1 
            
            else: # si on s'est trompé
                global nombre_de_vies
                nombre_de_vies -= 1
                afficher_vies() # appelle la fonction pour retirer un coeur de l'affichage
                if nombre_de_vies != 0:
                    creer_case(y, x, "croix_erreur")
                else:
                    switch_to_frame_defaite()
                    
            if nombre_cases_coloriees == 0:
                switch_to_frame_victoire()

def souris_cliquee_creer(event):
    "Prend en entrée l'événement et colorie la case"
    x = (event.x - marge) // largeur_case
    y = (event.y - marge) // largeur_case
    if (x >= 0 and y >= 0) and (x <= largeur_image_cree and y <= hauteur_image_cree): # vérifie qu'on a cliqué dans la grille
        if image_cree[y][x] == 0:
            image_cree[y][x] = 1
        else:
            image_cree[y][x] = 0
        creer_case(y, x, image_cree[y][x], True)

# Mouvement de souris
cases_a_creer = []
test_mouvement = []
def souris_maintenir(event):
    "Prend en entrée les événements du clic maintenue et colorie/coche les cases"
    if mode == "colorier":
        souris_cliquee(event)
    elif mode == "barrer":
        global cases_a_creer
        global test_mouvement
        x = ((event.x - espace_avant_grille_lignes) // largeur_case)
        y = ((event.y - espace_avant_grille_colonnes) // largeur_case)
        test_mouvement.append([event.x , event.y]) # ajout des coordonnées de l'événement
        cases_a_creer.append([x,y]) # ajout des coordonnées dans la grille
        if len(cases_a_creer) > 1:
            if (event.x-test_mouvement[-2][0]<largeur_case and event.x-test_mouvement[-2][0]>-largeur_case) and (
                event.y-test_mouvement[-2][1]<largeur_case and event.y-test_mouvement[-2][1]>-largeur_case) : # vérifie que le mouvement ne bug pas (problème de tkinter)
                if cases_a_creer[-2]!=[x,y]: # vérifie que la case ne soit coloriée qu'une seule fois quand la souris est maintenue dessus
                    souris_cliquee(event)

def souris_maintenir_creer(event):
        "Prend en entrée les événements du clic maintenue et colorie les cases"
        global cases_a_creer
        global test_mouvement
        x = ((event.x - marge) // largeur_case) * largeur_case + marge
        y = ((event.y - marge) // largeur_case) * largeur_case + marge
        test_mouvement.append([event.x , event.y]) # ajout des coordonnées de l'événement
        cases_a_creer.append([x,y]) # ajout des coordonnées dans la grille
        if len(cases_a_creer)>1:
            if (event.x-test_mouvement[-2][0]<largeur_case and event.x-test_mouvement[-2][0]>-largeur_case) and (
                event.y-test_mouvement[-2][1]<largeur_case and event.y-test_mouvement[-2][1]>-largeur_case) : # vérifie que le mouvement ne bug pas (problème de tkinter)
                if cases_a_creer[-2]!=[x,y]: # vérifie que la case ne soit coloriée qu'une seule fois quand la souris est maintenue dessus
                    souris_cliquee_creer(event)

def souris_relacher(event):
    "reset les coordonnées et le test lors du relachement du clic"
    del cases_a_creer[:]
    del test_mouvement[:]


def creer_case(y, x, couleur, creer = False):
    "crée les cases et les colorie/coche selon l'action de l'utilisateur"
    if couleur == 0:
        couleur = "white"
    elif couleur == 1:
        couleur = "black"
    elif couleur == "croix":
        couleur_croix = "black"
    else:
        couleur_croix = "red"
        
    if not creer:
        x0 = x * largeur_case + espace_avant_grille_lignes
        y0 = y * largeur_case + espace_avant_grille_colonnes
        if couleur == "white" or couleur == "black":
            canvas_jeu.create_rectangle(x0, y0, x0 + largeur_case, y0 + largeur_case, fill=couleur, outline='black', width = 3)
        else:
            canvas_jeu.create_line(x0, y0, x0 + largeur_case, y0 + largeur_case, fill=couleur_croix, width=2)
            canvas_jeu.create_line(x0 + largeur_case, y0, x0, y0 + largeur_case, fill=couleur_croix, width=2)
    else:
        x0 = x * largeur_case + marge
        y0 = y * largeur_case + marge
        canvas_creer_son_picross.create_rectangle(x0, y0, x0 + largeur_case, y0 + largeur_case, fill=couleur, outline='black', width = 3)

def creer_case_indice(x0, y0, valeur):
    "crée les cases pour les indices"
    canvas_jeu.create_rectangle(x0, y0, x0 + largeur_case, y0 + largeur_case, fill="yellow", outline='gray', width = 3)
    canvas_jeu.create_text(x0 + 0.5*largeur_case, y0 + 0.5*largeur_case, text = valeur, fill="black")

def colorier_choisi():
    "active le mode : colorier"
    global mode
    mode = "colorier"

def barrer_choisi():
    "active le mode : barrer"
    global mode
    mode = "barrer"

def calculer_nombre_max_indices(liste_indices):
    "prend en entrée la liste des indices et renvoie le nombre max d'indices"
    nombre_max = 0 
    for indices in liste_indices:
        if len(indices) > nombre_max:
            nombre_max = len(indices)
    return nombre_max

def reessayer():
    "change la frame pour réessayer"
    switch_to_frame_jeu(image_reponse)

def calculer_largeur_case(largeur, hauteur, creer = False):
    "Prend en entrée la largeur et la hauteur de la grille, et en facultatif si on est en mode 'creer' ou non, et renvoie la largeur des cases pour les modes de jeux"
    if not creer:
        largeur_c = (600 - marge) //(len(reponse) + max(nombre_max_indices_colonnes, nombre_max_indices_lignes))
    else:
        largeur_c = (600 - marge) // max(largeur, hauteur)
    if largeur_c > 50:
        return 50
    else:
        return largeur_c
    
def changement_ligne_creer(ligne_colonne):
    "Prend en entrée la ligne ou la colonne à ajouter/supprimer et l'ajoute/la supprime"
    global largeur_image_cree, hauteur_image_cree, image_cree, canvas_creer_son_picross, largeur_case
    if ligne_colonne == "ligne+1":
        hauteur_image_cree += 1
        nouvelle_colonne = []
        for _ in range(largeur_image_cree):
            nouvelle_colonne.append(0)
        image_cree.append(nouvelle_colonne)
    elif ligne_colonne == "colonne+1":
        largeur_image_cree += 1
        for j in range(hauteur_image_cree):
            image_cree[j].append(0)

    if ligne_colonne == "ligne-1" and hauteur_image_cree>3:
        hauteur_image_cree -= 1
        del image_cree[-1]
    elif ligne_colonne == "colonne-1" and largeur_image_cree>3:
        largeur_image_cree -= 1
        for j in range(hauteur_image_cree):
            del image_cree[j][-1]

    largeur_case = calculer_largeur_case(largeur_image_cree, hauteur_image_cree, True)
    canvas_creer_son_picross.destroy()
    canvas_creer_son_picross = Canvas(frame_creer_niveau, width=largeur_image_cree*largeur_case + 2*marge, height=hauteur_image_cree*largeur_case + 2*marge, background = "white")
    canvas_creer_son_picross.bind("<Button-1>", souris_cliquee_creer)
    canvas_creer_son_picross.bind("<B1-Motion>", souris_maintenir_creer)
    canvas_creer_son_picross.bind("<ButtonRelease-1>", souris_relacher)
    canvas_creer_son_picross.pack()
    for y in range(hauteur_image_cree):
        for x in range(largeur_image_cree):
            creer_case(y, x, image_cree[y][x], True)
    
    if hauteur_image_cree==3 and largeur_image_cree==3:
        showinfo(";-;", "Le niveau est pas un peu trop facile là?") # limite minimale atteinte

def afficher_vies():
    "cache les coeurs lorsqu'on perd une vie"
    if nombre_de_vies<2:
        canvas_jeu.itemconfigure(coeur2, state='hidden')
    else:
        canvas_jeu.itemconfigure(coeur3, state='hidden')

def secret():
    "affiche le bouton du niveau secret"
    bouton_niveau_secret.pack(side = "top")

def nouvelle_partie(image):
    "prend en entrée le chemin d'accès pour l'image et crée une nouvelle partie (les niveaux)"
    global reponse, largeur_grille, hauteur_grille, tableau_joueur, nombre_de_vies, mode, espace_avant_grille_colonnes
    global espace_avant_grille_lignes, coeur1, coeur2, coeur3, nombre_cases_coloriees, largeur_case, canvas_jeu, largeur_case, image_reponse
    canvas_jeu.destroy()
    canvas_jeu = Canvas(frame_jeu, background='white', highlightthickness=0)
    canvas_jeu.bind("<Button-1>", souris_cliquee)
    canvas_jeu.bind("<B1-Motion>", souris_maintenir)
    canvas_jeu.bind("<ButtonRelease-1>", souris_relacher)
    canvas_jeu.pack(side = "bottom")
    global image_reponse
    image_reponse = image
    reponse = transformer_image(image)
    largeur_grille = len(reponse[0])
    hauteur_grille = len(reponse)
    nombre_cases_coloriees = 0
    
    for x in range(largeur_grille):
        for y in range(hauteur_grille):
            if reponse[y][x] == 1:
                nombre_cases_coloriees += 1
    
    tableau_joueur = [[0 for _ in range(largeur_grille)] for _ in range(hauteur_grille)]
    nombre_de_vies = 3
    mode = "colorier"
    
    indices_lignes = indications_lignes(reponse, hauteur_grille)
    indices_colonnes = indications_colonnes(reponse, largeur_grille)
    
    global nombre_max_indices_colonnes, nombre_max_indices_lignes

    nombre_max_indices_colonnes = calculer_nombre_max_indices(indices_colonnes)
    nombre_max_indices_lignes = calculer_nombre_max_indices(indices_lignes)
    
    largeur_case = calculer_largeur_case(largeur_grille, hauteur_grille)

    espace_avant_grille_colonnes = nombre_max_indices_colonnes * largeur_case + marge
    espace_avant_grille_lignes = nombre_max_indices_lignes * largeur_case + marge

    largeur_canvas_jeu = largeur_case*largeur_grille + espace_avant_grille_lignes + marge
    hauteur_canvas_jeu = largeur_case*hauteur_grille + espace_avant_grille_colonnes + marge
    
    canvas_jeu.configure(width = largeur_canvas_jeu, height = hauteur_canvas_jeu)

    coeur1 = canvas_jeu.create_text(35, 20, text = "❤️", fill="red", font = 16)
    coeur2 = canvas_jeu.create_text(55, 20, text = "❤️", fill="red", font = 16)
    coeur3 = canvas_jeu.create_text(75, 20, text = "❤️", fill="red", font = 16)

    # création des indices
    for y in range(hauteur_grille):
        for x in range(nombre_max_indices_lignes):
            if x < len(indices_lignes[y]):
                creer_case_indice(x*largeur_case+marge, y*largeur_case+espace_avant_grille_colonnes, indices_lignes[y][x])
            else:
                creer_case_indice(x*largeur_case+marge, y*largeur_case+espace_avant_grille_colonnes, " ")

    for x in range(largeur_grille):
        for y in range(nombre_max_indices_colonnes):
            if y < len(indices_colonnes[x]):
                creer_case_indice(x*largeur_case+espace_avant_grille_lignes, y*largeur_case+marge, indices_colonnes[x][y])
            else:
                creer_case_indice(x*largeur_case+espace_avant_grille_lignes, y*largeur_case+marge, " ")
                
    # création de la grille
    for y in range(hauteur_grille):
        for x in range(largeur_grille):
            couleur = tableau_joueur[y][x]
            creer_case(y, x, couleur)
        
def creer_picross():
    "crée un nouveau niveau avec son propre dessin"
    global largeur_case, canvas_creer_son_picross, image_cree, largeur_image_cree, hauteur_image_cree
    switch_to_frame_creer_niveau()
    largeur_image_cree = 5
    hauteur_image_cree = 5
    image_cree = [[0 for _ in range(hauteur_image_cree)] for _ in range(largeur_image_cree)]
    largeur_case = calculer_largeur_case(largeur_image_cree, hauteur_image_cree, True)
    canvas_creer_son_picross.destroy()
    canvas_creer_son_picross = Canvas(frame_creer_niveau, width=largeur_image_cree*largeur_case + 2*marge, height=hauteur_image_cree*largeur_case + 2*marge, background = "white")
    canvas_creer_son_picross.bind("<Button-1>", souris_cliquee_creer)
    canvas_creer_son_picross.bind("<B1-Motion>", souris_maintenir_creer)
    canvas_creer_son_picross.bind("<ButtonRelease-1>", souris_relacher)
    canvas_creer_son_picross.pack()
    for y in range(hauteur_image_cree):
        for x in range(largeur_image_cree): 
            creer_case(y, x, 0, True)
        
def sauvegarder_image_cree():
    "sauvegarder son dessin pour l'avoir dans ses fichiers et pouvoir le réutiliser après"
    image = Image.new('RGB', (largeur_image_cree, hauteur_image_cree))
    for y in range(len(image_cree)):
        for x in range(len(image_cree[0])):
            if image_cree[y][x] == 0:
                couleur = (250, 250, 250)
            else:
                couleur = (0, 0, 0)
            image.putpixel((x, y), couleur)
    chemin_image = "Asset/Mes_images/" + nom_du_fichier.get()
    image.save(chemin_image)
    showinfo("Image sauvegardée", "Votre image a bien été enregistrée dans le dossier Mes_images")
    

def importer_image():
    "Permet d'importer une image : demande à l'utilisateur de choisir une image dans ses fichiers puis lance la partie avec cette image"
    showinfo("Information", "C'est mieux de choisir une image en noir et blanc")
    chemin_du_fichier = askopenfilename(title="Ouvrir une image en noir et blanc", initialdir='Asset/Mes_images', filetypes=[('png files','.png')]) 
    switch_to_frame_jeu(chemin_du_fichier)
        
marge = 10

# création de l'accueil
image_accueil = PhotoImage(file="Asset/picross_image.png")
affichage_image_accueil = Button(frame_accueil, image=image_accueil, command = secret)
affichage_image_accueil.pack()

# création du Canvas pour le jeu

canvas_jeu = Canvas(frame_jeu, background='white')
canvas_jeu.bind("<Button-1>", souris_cliquee)
canvas_jeu.bind("<B1-Motion>",souris_maintenir)
canvas_jeu.bind("<ButtonRelease-1>", souris_relacher)
canvas_jeu.pack()

# création des boutons pour choisir le mode (colorier ou barrer)

frame_boutons_jeux = Frame(frame_jeu) 
frame_boutons_jeux.pack()
bouton_colorier = Button(frame_boutons_jeux, text="Colorier", command = colorier_choisi)
bouton_colorier.pack(side = "left")
bouton_barrer = Button(frame_boutons_jeux, text="Barrer", command = barrer_choisi)
bouton_barrer.pack(side = "right")

# création des Canvas gagné et perdu

canvas_gagné = Canvas(frame_victoire, width = 250, height = 250, background="blue")
canvas_gagné.create_text(125, 125, text = "Bravo! Vous avez gagné !!!")
canvas_gagné.pack()

canvas_perdu = Canvas(frame_defaite, width = 250, height = 250, background = "red")
canvas_perdu.create_text(125, 125, text = "Dommage, vous avez perdu...")
canvas_perdu.pack()
bouton_reessayer = Button(frame_defaite, text = "Réessayer", command = reessayer).pack()

# création du bouton accueil
pixel = PhotoImage(width=1, height=1)
bouton_accueil = Button(fenetre, image=pixel, text = "Accueil", compound="c", command = switch_to_frame_accueil, bg="lightgreen")
bouton_accueil.pack(side = "top")

# création des widgets qui servent pour dessiner son picross
canvas_creer_son_picross = Canvas(frame_creer_niveau, width=510, height=510, background = "white")
canvas_creer_son_picross.pack()

bouton_creer_son_picross = Button(frame_accueil, image = pixel, width = 389, height = 20, text = "Créer son niveau", compound="c", command = creer_picross)
bouton_creer_son_picross.pack()

frame_boutons_création = Frame(frame_creer_niveau, bg="white")

bouton_rajouter_ligne = Button(frame_boutons_création, text = "ajouter une ligne", command = lambda : changement_ligne_creer("ligne+1"))
bouton_rajouter_colonne = Button(frame_boutons_création, text = "ajouter une colonne", command = lambda : changement_ligne_creer("colonne+1"))
bouton_enlever_ligne = Button(frame_boutons_création, text = "enlever une ligne", command = lambda : changement_ligne_creer("ligne-1"))
bouton_enlever_colonne = Button(frame_boutons_création, text = "enlever une colonne", command = lambda : changement_ligne_creer("colonne-1"))
bouton_rajouter_ligne.grid(row=0,column=0)
bouton_rajouter_colonne.grid(row=1,column=0)
bouton_enlever_ligne.grid(row=0,column=1)
bouton_enlever_colonne.grid(row=1,column=1)
frame_boutons_création.pack()

bouton_sauvegarder_image = Button(frame_creer_niveau, text = "Sauvegarder l'image", command = sauvegarder_image_cree)
bouton_sauvegarder_image.pack()

# création de l'espace pour écrire le nom du fichier quand on veut sauvegarder l'image dessinée
nom_du_fichier = StringVar() 
nom_du_fichier.set("mon_image.png")
entree = Entry(frame_creer_niveau, textvariable=nom_du_fichier, width=30)
entree.pack(side = BOTTOM)

# création du bouton pour importer une image
bouton_importer_image = Button(frame_accueil, image=pixel, width = 389, height = 20, text="Importer une image", compound="c", command = importer_image)
bouton_importer_image.pack()

# création des boutons de niveau

frame_boutons_niveaux = Frame(frame_accueil, bg="lightgrey")
bouton_niveau1 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 1", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Tour.png"))
bouton_niveau2 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 2", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Horloge.png"))
bouton_niveau3 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 3", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Feuille.png"))
bouton_niveau4 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 4", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Montgolfiere.png"))
bouton_niveau5 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 5", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Note_musique.png"))
bouton_niveau6 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 6", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Canard.png"))
bouton_niveau7 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 7", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/yin-yang.png"))
bouton_niveau8 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 8", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Dauphin.png"))
bouton_niveau9 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 9", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Bougie.png"))
bouton_niveau10 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 10", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Cygne.png"))
bouton_niveau11 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 11", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Partition.png"))
bouton_niveau12 = Button(frame_boutons_niveaux, image = pixel, width = 97.5, height = 20, text = "Niveau 12", compound = "c", command = lambda : switch_to_frame_jeu("Asset/Solutions/Souris.png"))

bouton_niveau1.grid(row=0,column=0)
bouton_niveau2.grid(row=0,column=1)
bouton_niveau3.grid(row=0,column=2)
bouton_niveau4.grid(row=0,column=3)
bouton_niveau5.grid(row=1,column=0)
bouton_niveau6.grid(row=1,column=1)
bouton_niveau7.grid(row=1,column=2)
bouton_niveau8.grid(row=1,column=3)
bouton_niveau9.grid(row=2,column=0)
bouton_niveau10.grid(row=2,column=1)
bouton_niveau11.grid(row=2,column=2)
bouton_niveau12.grid(row=2,column=3)

frame_boutons_niveaux.pack()

bouton_niveau_secret = Button(frame_accueil, image = pixel, width = 389, height = 20, text = "Niveau secret", compound = "c", bg="blue", command = lambda : switch_to_frame_jeu("Asset/Solutions/Perroquet.png"))


# Affiche initialement le premier cadre
switch_to_frame_accueil()

# Boucle principale de l'application
fenetre.mainloop()
