import copy

class Automate:
    def __init__(self):
        self.alphabet = []
        self.etats = []
        self.etats_initiaux = []
        self.etats_finaux = []
        self.transitions = []
def lire_automate_sur_fichier(nom_du_fichier):
    automate = Automate()

    f = open(nom_du_fichier, "r")
    lignes = f.readlines()
    f.close()

    # alphabet
    n = int(lignes[0])
    for i in range(n):
        automate.alphabet.append(chr(ord('a') + i))

    # états
    n = int(lignes[1])
    for i in range(n):
        automate.etats.append(i)

    # états initiaux
    parties = lignes[2].split()
    for i in range(1, len(parties)):
        automate.etats_initiaux.append(int(parties[i]))

    # états finaux
    parties = lignes[3].split()
    for i in range(1, len(parties)):
        automate.etats_finaux.append(int(parties[i]))

    # transitions
    n = int(lignes[4])
    for i in range(n):
        parties = lignes[5 + i].split()
        depart = int(parties[0])
        symbole = parties[1]
        arrivee = int(parties[2])

        automate.transitions.append((depart, symbole, arrivee))

    return automate
def afficher_automate(automate):

    # entête
    ligne = "    "
    for symbole in automate.alphabet:
        ligne += symbole + "   "
    print(ligne)

    # lignes
    for etat in automate.etats:

        ligne = ""

        # on affiche les entrées et les sorties
        if etat in automate.etats_initiaux:
            ligne += "E "
        elif etat in automate.etats_finaux:
            ligne += "S "
        else:
            ligne += "  "

        # numéro état
        ligne += str(etat) + "   "

        # transitions
        for symbole in automate.alphabet:

            arrivees = []

            for t in automate.transitions:
                if t[0] == etat and t[1] == symbole:
                    arrivees.append(t[2])

            if len(arrivees) == 0:
                ligne += "--   "
            else:
                texte = ""
                for i in range(len(arrivees)):
                    texte += str(arrivees[i])
                    if i < len(arrivees) - 1:
                        texte += ","
                ligne += texte + "   "

        print(ligne)

def non_standard(automate):
    pass

def standardisation(automate):
    pass

def est_un_automate_deterministe(automate):
    pass

def est_un_automate_complet(automate):
    pass

def completion(automate):
    pass

def determinisation_et_completion_automate(automate):
    pass

def afficher_automate_deterministe_complet(automate):
    pass

def minimisation(automate):
    pass

def afficher_automate_minimal(automate):
    pass

def lire_mot(mot):
    pass

def reconnaitre_mot(mot, automate):
    etat_courant = automate["initial"]

    for char in mot:
        if char in automate["transitions"].get(etat_courant, {}):
            etat_courant = automate["transitions"][etat_courant][char]
        else:
            print("non")
            return

    if etat_courant in automate["finaux"]:
        print("oui")
    else:
        print("non")

def automate_complementaire(automate):
    pass