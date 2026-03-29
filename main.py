from fonction import *

def main():

    # choix du fichier au début
    nom_fichier = input("Veuillez séléctionner un fichier : ")
    fichier_automate = lire_automate_sur_fichier(nom_fichier)

    while True:
        print("\n===== MENU =====")
        print("1 - Afficher l'automate")
        print("2 - Recharger un fichier")
        print("3 - Standardiser l'automate")
        print("4 - Obtenir l'automate déterministe complet")
        print("5 - Reconnaître des mots")
        print("6 - Automate complémentaire")
        print("7 - Minimiser l'automate")
        print("0 - Quitter")

        choix = input("Choix : ")

        if choix == "1":
            afficher_automate(fichier_automate)

        elif choix == "2":
            nom_fichier = input("Nouveau fichier : ")
            fichier_automate = lire_automate_sur_fichier(nom_fichier)

        elif choix == "3":
            if non_standard(fichier_automate):
                print("L'automate n'est pas standard.")

                rep = input("Voulez-vous le standardiser ? (o/n) : ")

                if rep == "o":
                    fichier_automate = standardisation(fichier_automate)
                    print("Automate standardisé ")
                else:
                    print("Standardisation annulée")

            else:
                print("L'automate est déjà standard️")

        elif choix == "4":
            if est_un_automate_deterministe(fichier_automate):
                if est_un_automate_complet(fichier_automate):
                    afdc = fichier_automate
                else:
                    afdc = completion(fichier_automate)
            else:
                afdc = determinisation_et_completion_automate(fichier_automate)

            print("Automate déterministe complet :")
            afficher_automate_deterministe_complet(afdc)

        elif choix == "5":
            mot = lire_mot()

            while mot != "stop":
                reconnaitre_mot(mot, fichier_automate)
                mot = lire_mot()

        elif choix == "6":
            AComp = automate_complementaire(fichier_automate)
            print("Automate complémentaire :")
            afficher_automate(AComp)

        elif choix =="7":
            if est_un_automate_deterministe(fichier_automate):
                if est_un_automate_complet(fichier_automate):
                    afdc = fichier_automate
                else:
                    afdc = completion(fichier_automate)
            else:
                afdc = determinisation_et_completion_automate(fichier_automate)

            print("\nAutomate déterministe complet  :")
            afficher_automate(afdc)

            AFDCM = minimisation(afdc)

            if AFDCM is not None:
                print("\nAutomate minimal :")
                afficher_automate(AFDCM)

        elif choix == "0":

            print("Fin")
            break

        else:
            print("Choix invalide")

main()