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

    if len(automate.etats_initiaux) != 1:
        return True

    etat_initial = automate.etats_initiaux[0]

    for (depart, symbole, arrivee) in automate.transitions:
        if arrivee == etat_initial:
            return True


    return False

def standardisation(automate):

    std = copy.deepcopy(automate)

    i0 = max(std.etats) + 1
    std.etats.append(i0)


    anciens_initiaux = std.etats_initiaux
    std.etats_initiaux = [i0]

    nouvelles_transitions = []
    for (depart, symbole, arrivee) in std.transitions:
        if depart in anciens_initiaux:
            nouvelles_transitions.append((i0, symbole, arrivee))

    std.transitions += nouvelles_transitions

    for ancien in anciens_initiaux:
        if ancien in std.etats_finaux:
            std.etats_finaux.append(i0)
            break

    return std

def est_un_automate_deterministe(automate):
    print("\n--- Vérification du déterminisme ---")
    raisons = []

    # Vérification de l'état initial unique
    if len(automate.etats_initiaux) != 1:
        raisons.append(f"Il y a {len(automate.etats_initiaux)} états initiaux (il en faut exactement 1).")

    # Vérification de l'unicité des transitions (pas de transitions multiples pour un même symbole)
    for etat in automate.etats:
        for symbole in automate.alphabet:
            cibles = [t[2] for t in automate.transitions if t[0] == etat and t[1] == symbole]
            if len(cibles) > 1:
                raisons.append(f"L'état {etat} possède plusieurs transitions pour le symbole '{symbole}' vers {cibles}")

    if raisons:
        for r in raisons:
            print(f"Cause : {r}")
        return False

    print("L'automate est déterministe.")
    return True

def est_un_automate_complet(automate):
    print("\n--- Vérification de la complétude ---")
    manquants = []

    for etat in automate.etats:
        for symbole in automate.alphabet:
            # On cherche s'il existe au moins une transition
            trouve = any(t[0] == etat and t[1] == symbole for t in automate.transitions)
            if not trouve:
                manquants.append(f"({etat}, {symbole})")

    if manquants:
        print(f"L'automate n'est pas complet. Transitions manquantes : {', '.join(manquants)}")
        return False

    print("L'automate est complet.")
    return True

def completion(automate):
    pass

def determinisation_et_completion_automate(automate):
    pass

def afficher_automate_deterministe_complet(automate):
    afficher_automate(automate)

def minimisation(automate):
    pass

def afficher_automate_minimal(automate):
    afficher_automate(automate)

def lire_mot():
    return input("Saisissez un mot (ou tapez 'fin' pour terminer) : ")

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
    if not est_un_automate_deterministe(automate):
        print("L'automate n'est pas déterminisé.")
        return None

    if not est_un_automate_complet(automate):
        print("L'automate n'est pas complet.")
        return None

    complement = copy.deepcopy(automate)

    nouveaux_terminaux = set()
    for etat in automate.liste_etats:
        if etat not in automate.etats_terminaux:
            nouveaux_terminaux.add(etat)

    complement.etats_terminaux = nouveaux_terminaux
    return complement