from fonction import *

def main():

    # choix du fichier au début
    nom_fichier = input("Veuillez séléctionner un fichier : ")
    A = lire_automate_sur_fichier(nom_fichier)

    while True:
        print("\n===== MENU =====")
        print("1 - Afficher l'automate")
        print("2 - Recharger un fichier")
        print("0 - Quitter")

        choix = input("Choix : ")

        if choix == "1":
            afficher_automate(A)

        elif choix == "2":
            nom_fichier = input("Nouveau fichier : ")
            A = lire_automate_sur_fichier(nom_fichier)

        elif choix == "0":
            print("Fin")
            break

        else:
            print("Choix invalide")

main()