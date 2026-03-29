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

    print("\n--- Complétion de l'automate ---")
    afdc = copy.deepcopy(automate)
    deja_presents = {(t[0], t[1]) for t in afdc.transitions}
    puits_utilise = False

    # On cherche les manques
    for etat in afdc.etats:
        for symbole in afdc.alphabet:
            if (etat, symbole) not in deja_presents:
                afdc.transitions.append((etat, symbole, "P"))
                puits_utilise = True

    # Si on a envoyé vers "P", on l'ajoute aux états et on crée ses boucles
    if puits_utilise:
        afdc.etats.append("P")
        for symbole in afdc.alphabet:
            afdc.transitions.append(("P", symbole, "P"))

    return afdc

def determinisation_et_completion_automate(automate):
    pass

def afficher_automate_deterministe_complet(automate):
    afficher_automate(automate)

def minimisation(automate):

    if not est_un_automate_deterministe(automate):
        print("L'automate n'est pas déterministe.")
        return None

    if not est_un_automate_complet(automate):
        print("L'automate n'est pas complet.")
        return None


    if not automate.liste_etats:
        return automate

    print("\n--- Minimisation de l'automate ---")

    # 1. Partition initiale P0 : Séparer Terminaux (T) et Non-Terminaux (NT)
    partition = {}
    for etat in automate.liste_etats:
        partition[etat] = 1 if etat in automate.etats_terminaux else 0

    def afficher_partition(p, etape):
        groupes = {}
        for e, g in p.items():
            groupes.setdefault(g, []).append(e)
        print(f"P{etape} : ", end="")
        print(" ; ".join([f"{{{','.join(map(str, sorted(groupes[g])))}}}" for g in sorted(groupes)]))

    etape = 0
    afficher_partition(partition, etape)

    while True:
        etape += 1
        nouvelle_partition = {}
        signatures = {} # (Groupe_actuel, Groupe_dest_a, Groupe_dest_b...) -> Nouvel_ID
        next_id = 0

        for etat in automate.liste_etats:
            # La signature d'un état est son groupe actuel + les groupes de ses destinations
            signature = [partition[etat]]
            for symbole in automate.alphabet:
                dest = automate.transitions[etat][symbole][0]
                signature.append(partition[dest])

            signature = tuple(signature)
            if signature not in signatures:
                signatures[signature] = next_id
                next_id += 1
            nouvelle_partition[etat] = signatures[signature]

        afficher_partition(nouvelle_partition, etape)

        # Si la partition est identique à la précédente (même nombre de groupes et répartition)
        # On compare si les états qui étaient ensemble le restent
        if len(set(nouvelle_partition.values())) == len(set(partition.values())):
            # Vérification plus profonde : les groupes sont-ils identiques ?
            stable = True
            for e1 in automate.liste_etats:
                for e2 in automate.liste_etats:
                    if (partition[e1] == partition[e2]) != (nouvelle_partition[e1] == nouvelle_partition[e2]):
                        stable = False
                        break
            if stable: break

        partition = nouvelle_partition

    # 2. Construction de l'automate minimal
    print("\nConstruction de l'automate minimal...")
    min_auto = Automate()
    min_auto.nb_symboles = automate.nb_symboles
    min_auto.alphabet = automate.alphabet.copy()

    # Création des nouveaux noms d'états basés sur les groupes finaux
    groupes_finaux = {}
    for e, g in partition.items():
        groupes_finaux.setdefault(g, []).append(e)

    mapping_nom = {g: ".".join(map(str, sorted(groupes_finaux[g]))) for g in groupes_finaux}

    min_auto.liste_etats = list(mapping_nom.values())
    min_auto.nb_etats = len(min_auto.liste_etats)

    for g, nom_fusionne in mapping_nom.items():
        etat_representant = groupes_finaux[g][0]

        # Initiales / Terminales
        if etat_representant in automate.etats_initiaux:
            min_auto.etats_initiaux.add(nom_fusionne)
        if etat_representant in automate.etats_terminaux:
            min_auto.etats_terminaux.add(nom_fusionne)

        # Transitions
        min_auto.transitions[nom_fusionne] = {}
        for symbole in automate.alphabet:
            dest_origine = automate.transitions[etat_representant][symbole][0]
            groupe_dest = partition[dest_origine]
            min_auto.transitions[nom_fusionne][symbole] = [mapping_nom[groupe_dest]]

    return min_auto

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