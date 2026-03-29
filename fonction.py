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
    with open(nom_du_fichier, "r") as f:
        lignes = f.readlines()

    # alphabet
    n = int(lignes[0])
    for i in range(n):
        automate.alphabet.append(chr(ord('a') + i))

    # états initiaux
    parties = lignes[2].split()
    for i in range(1, len(parties)):
        automate.etats_initiaux.append(parties[i].strip())

    # états finaux
    parties = lignes[3].split()
    for i in range(1, len(parties)):
        automate.etats_finaux.append(parties[i].strip())

    # transitions
    n = int(lignes[4])
    for i in range(n):
        parties = lignes[5 + i].split()
        depart = parties[0].strip()
        symbole = parties[1].strip()
        arrivee = parties[2].strip()
        automate.transitions.append((depart, symbole, arrivee))


        if depart not in automate.etats:
            automate.etats.append(depart)
        if arrivee not in automate.etats:
            automate.etats.append(arrivee)

    return automate

def afficher_automate(automate):
    ligne = "    "
    for symbole in automate.alphabet:
        ligne += symbole + "   "
    print(ligne)

    for etat in automate.etats:
        ligne = ""
        if etat in automate.etats_initiaux:
            ligne += "E "
        elif etat in automate.etats_finaux:
            ligne += "S "
        else:
            ligne += "  "
        ligne += str(etat) + "   "

        for symbole in automate.alphabet:
            arrivees = [t[2] for t in automate.transitions if t[0] == etat and t[1] == symbole]
            if not arrivees:
                ligne += "--   "
            else:
                ligne += ",".join(arrivees) + "   "
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

    floats = [float(e) for e in std.etats if str(e).replace('.', '', 1).isdigit()]
    i0 = str(int(max(floats)) + 1) if floats else "I0"
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

    nom_fichier = input("Nom du fichier pour le nouvel automate standardisé : ") + ".txt"
    with open(nom_fichier, "w") as f:
        # alphabet
        f.write(f"{len(std.alphabet)}\n")
        # états
        f.write(f"{len(std.etats)}\n")
        # états initiaux
        f.write(f"{len(std.etats_initiaux)} {' '.join(map(str, std.etats_initiaux))}\n")
        # états finaux
        f.write(f"{len(std.etats_finaux)} {' '.join(map(str, std.etats_finaux))}\n")
        # transitions
        f.write(f"{len(std.transitions)}\n")
        for (dep, sym, arr) in std.transitions:
            f.write(f"{dep} {sym} {arr}\n")

    print(f"Automate standardisé sauvegardé dans '{nom_fichier}'")

    return std

def est_un_automate_deterministe(automate):
    print("\n--- Vérification du déterminisme ---")
    raisons = []
    if len(automate.etats_initiaux) != 1:
        raisons.append(f"Il y a {len(automate.etats_initiaux)} états initiaux (il en faut exactement 1).")
    for etat in automate.etats:
        for symbole in automate.alphabet:
            cibles = [t[2] for t in automate.transitions if t[0] == etat and t[1] == symbole]
            if len(cibles) > 1:
                raisons.append(f"L'état {etat} possède plusieurs transitions pour '{symbole}' vers {cibles}")
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
            if not any(t[0] == etat and t[1] == symbole for t in automate.transitions):
                manquants.append(f"({etat},{symbole})")
    if manquants:
        print("Transitions manquantes :", ", ".join(manquants))
        return False
    print("L'automate est complet.")
    return True

def completion(automate):
    import copy

    afdc = copy.deepcopy(automate)
    deja_presents = {(t[0], t[1]) for t in afdc.transitions}
    puits_utilise = False

    for etat in afdc.etats:
        for symbole in afdc.alphabet:
            if (etat, symbole) not in deja_presents:
                afdc.transitions.append((etat, symbole, "P"))
                puits_utilise = True

    if puits_utilise:
        if "P" not in afdc.etats:
            afdc.etats.append("P")
        for symbole in afdc.alphabet:
            afdc.transitions.append(("P", symbole, "P"))

    # --- Sauvegarde fichier ---
    nom_fichier = input("Nom du fichier pour l'automate complété  : ") + ".txt"

    with open(nom_fichier, "w") as f:
        # alphabet
        f.write(f"{len(afdc.alphabet)}\n")

        # états
        f.write(f"{len(afdc.etats)}\n")

        # états initiaux
        f.write(f"{len(afdc.etats_initiaux)} {' '.join(map(str, afdc.etats_initiaux))}\n")

        # états finaux
        f.write(f"{len(afdc.etats_finaux)} {' '.join(map(str, afdc.etats_finaux))}\n")

        # transitions
        f.write(f"{len(afdc.transitions)}\n")
        for (dep, sym, arr) in afdc.transitions:
            f.write(f"{dep} {sym} {arr}\n")

    print(f"Automate complété sauvegardé dans '{nom_fichier}'")

    return afdc

def determinisation_et_completion_automate(automate):
    print("\n--- Déterminisation et Complétion ---")
    AFDC = Automate()
    AFDC.alphabet = automate.alphabet[:]
    AFDC.mapping = {}

    etat_init = tuple(sorted(set(automate.etats_initiaux)))
    file_a_traiter = [etat_init]
    groupes_vus = [etat_init]

    while file_a_traiter:
        groupe_courant = file_a_traiter.pop(0)
        nom_courant = "P" if len(groupe_courant) == 0 else ".".join(groupe_courant)
        if nom_courant not in AFDC.etats:
            AFDC.etats.append(nom_courant)
            AFDC.mapping[nom_courant] = list(groupe_courant)
            if groupe_courant == etat_init:
                AFDC.etats_initiaux.append(nom_courant)
            for e in groupe_courant:
                if e in automate.etats_finaux:
                    AFDC.etats_finaux.append(nom_courant)
                    break
        for lettre in AFDC.alphabet:
            union_destinations = []
            for e in groupe_courant:
                for t in automate.transitions:
                    if t[0] == e and t[1] == lettre:
                        if t[2] not in union_destinations:
                            union_destinations.append(t[2])
            groupe_suivant = tuple(sorted(union_destinations))
            nom_suivant = "P" if len(groupe_suivant) == 0 else ".".join(groupe_suivant)
            AFDC.transitions.append((nom_courant, lettre, nom_suivant))
            if groupe_suivant not in groupes_vus:
                groupes_vus.append(groupe_suivant)
                file_a_traiter.append(groupe_suivant)

    nom_fichier = input("Nom du fichier de sauvegarde deterministe : ") + ".txt"
    with open(nom_fichier, "w") as f:
        f.write(f"{len(AFDC.alphabet)}\n")
        f.write(f"{len(AFDC.etats)}\n")
        f.write(f"{len(AFDC.etats_initiaux)} {' '.join(AFDC.etats_initiaux)}\n")
        f.write(f"{len(AFDC.etats_finaux)} {' '.join(AFDC.etats_finaux)}\n")
        f.write(f"{len(AFDC.transitions)}\n")
        for dep, sym, arr in AFDC.transitions:
            f.write(f"{dep} {sym} {arr}\n")
    print(f"Automate déterministe complet sauvegardé dans '{nom_fichier}'")
    return AFDC


def afficher_automate_deterministe_complet(automate):
    afficher_automate(automate)

def reconnaitre_mot(mot, automate):
    if not automate.etats_initiaux:
        print("non")
        return
    etats_courants = set(automate.etats_initiaux)
    for char in mot:
        prochains = set()
        for etat in etats_courants:
            for depart, symbole, arrivee in automate.transitions:
                if depart == etat and symbole == char:
                    prochains.add(arrivee)
        etats_courants = prochains
        if not etats_courants:
            print("non")
            return
    for etat in etats_courants:
        if etat in automate.etats_finaux:
            print("oui")
            return
    print("non")

def lire_mot():
    return input("Saisissez un mot (ou tapez 'stop' pour terminer) : ")


def automate_complementaire(automate):
    if not est_un_automate_deterministe(automate):
        print("L'automate n'est pas déterministe.")
        return None
    if not est_un_automate_complet(automate):
        print("L'automate n'est pas complet.")
        return None

    complement = copy.deepcopy(automate)
    complement.etats_finaux = [etat for etat in automate.etats if etat not in automate.etats_finaux or etat in automate.etats_initiaux]
    complement.etats_initiaux = [etat for etat in automate.etats_initiaux if etat not in automate.etats_finaux]
    complement.etats_initiaux = [etat for etat in complement.etats_initiaux if etat not in complement.etats_finaux]
    return complement

def minimisation(automate):

    if not est_un_automate_deterministe(automate):
        print("L'automate n'est pas déterministe.")
        return None

    if not est_un_automate_complet(automate):
        print("L'automate n'est pas complet.")
        return None

    if not automate.etats:
        return automate

    print("\n--- Minimisation de l'automate ---")

    def get_dest(etat, symbole):
        for (d, s, a) in automate.transitions:
            if d == etat and s == symbole:
                return a
        return None


    partition = {}
    for etat in automate.etats:
        partition[etat] = 1 if etat in automate.etats_finaux else 0

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
        signatures = {}
        next_id = 0

        for etat in automate.etats:
            signature = [partition[etat]]
            for symbole in automate.alphabet:
                dest = get_dest(etat, symbole)
                signature.append(partition[dest])
            signature = tuple(signature)
            if signature not in signatures:
                signatures[signature] = next_id
                next_id += 1
            nouvelle_partition[etat] = signatures[signature]

        afficher_partition(nouvelle_partition, etape)

        if len(set(nouvelle_partition.values())) == len(set(partition.values())):
            stable = True
            for e1 in automate.etats:
                for e2 in automate.etats:
                    if (partition[e1] == partition[e2]) != (nouvelle_partition[e1] == nouvelle_partition[e2]):
                        stable = False
                        break
                if not stable:
                    break
            if stable:
                break

        partition = nouvelle_partition


    print("\nConstruction de l'automate minimal...")
    min_auto = Automate()
    min_auto.alphabet = automate.alphabet[:]

    groupes_finaux = {}
    for e, g in partition.items():
        groupes_finaux.setdefault(g, []).append(e)

    mapping_nom = {g: ".".join(map(str, sorted(groupes_finaux[g]))) for g in groupes_finaux}

    min_auto.etats = list(mapping_nom.values())

    for g, nom_fusionne in mapping_nom.items():
        etat_representant = groupes_finaux[g][0]

        if etat_representant in automate.etats_initiaux:
            min_auto.etats_initiaux.append(nom_fusionne)
        if etat_representant in automate.etats_finaux:
            min_auto.etats_finaux.append(nom_fusionne)

        for symbole in automate.alphabet:
            dest_origine = get_dest(etat_representant, symbole)
            groupe_dest = partition[dest_origine]
            min_auto.transitions.append(
                (nom_fusionne, symbole, mapping_nom[groupe_dest]))

    return min_auto
def afficher_automate_minimal(automate):
    afficher_automate(automate)