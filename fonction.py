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
    """
    Vérifie si un automate fini (AF) n'est PAS standard.

    Un automate est STANDARD si et seulement si :
      1. Il possède exactement UN SEUL état initial.
      2. Aucune transition n'a pour destination l'état initial
         (l'état initial n'a aucune transition entrante).

    Retourne :
      True  -> l'automate N'EST PAS standard (standardisation nécessaire)
      False -> l'automate EST standard (rien à faire)
    """

    # Condition 1 : il faut exactement un état initial
    if len(automate.etats_initiaux) != 1:
        return True  # 0 ou plusieurs états initiaux → non standard

    etat_initial = automate.etats_initiaux[0]

    # Condition 2 : aucune transition ne doit arriver sur l'état initial
    for (depart, symbole, arrivee) in automate.transitions:
        if arrivee == etat_initial:
            return True  # une transition entre sur l'état initial → non standard

    # Les deux conditions sont satisfaites → l'automate est standard
    return False

def standardisation(automate):
    """
    Standardise un automate fini en créant un nouvel état initial i0
    qui hérite de toutes les transitions sortantes des anciens états initiaux.

    Retourne un nouvel automate standardisé (l'original n'est pas modifié).
    """

    # On travaille sur une copie pour ne pas modifier l'automate original
    std = copy.deepcopy(automate)

    # Étape 1 : créer un nouvel état initial i0 (numéro = max des états + 1)
    i0 = max(std.etats) + 1
    std.etats.append(i0)

    # Étape 2 : i0 devient le seul état initial
    anciens_initiaux = std.etats_initiaux
    std.etats_initiaux = [i0]

    # Étape 3 : i0 hérite des transitions sortantes de tous les anciens états initiaux
    nouvelles_transitions = []
    for (depart, symbole, arrivee) in std.transitions:
        if depart in anciens_initiaux:
            nouvelles_transitions.append((i0, symbole, arrivee))

    std.transitions += nouvelles_transitions

    # Étape 4 : si un ancien état initial était final, i0 devient aussi final
    for ancien in anciens_initiaux:
        if ancien in std.etats_finaux:
            std.etats_finaux.append(i0)
            break  # une seule fois suffit

    return std

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
    pass

def automate_complementaire(automate):
    pass