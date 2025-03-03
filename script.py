import random
import unicodedata

def supprimer_accents(chaine):
    """Supprime les accents d'une chaîne de caractères."""
    return ''.join(
        caractere for caractere in unicodedata.normalize('NFD', chaine)
        if unicodedata.category(caractere) != 'Mn'
    )

def demander_mot():
    # Choix aléatoire entre demander d'abord l'anglais ou le français
    if random.choice([True, False]):
        mot_anglais = input("Entrez un mot en anglais (ou 'quit' pour quitter) : ")
        if mot_anglais.lower() == "quit":
            return None, None
        mot_francais = input("Entrez sa traduction en français : ")
    else:
        mot_francais = input("Entrez un mot en français (ou 'quit' pour quitter) : ")
        if mot_francais.lower() == "quit":
            return None, None
        mot_anglais = input("Entrez sa traduction en anglais : ")
    
    return mot_anglais, mot_francais

def enregistrer_mot(mot_anglais, mot_francais):
    with open("mots.txt", "a") as fichier:
        fichier.write(f"{mot_anglais}:{mot_francais}:0\n")  # Ajouter 0 points par défaut

def charger_mots():
    mots = []
    try:
        with open("mots.txt", "r") as fichier:
            for ligne in fichier:
                mot_anglais, mot_francais, points = ligne.strip().split(":")
                mots.append((mot_anglais, mot_francais, int(points)))
    except FileNotFoundError:
        print("Aucun mot n'a été enregistré pour le moment.")
    return mots

def sauvegarder_mots(mots):
    with open("mots.txt", "w") as fichier:
        for mot_anglais, mot_francais, points in mots:
            fichier.write(f"{mot_anglais}:{mot_francais}:{points}\n")

def afficher_mots():
    mots = charger_mots()
    if not mots:
        print("Aucun mot n'a été enregistré pour le moment.")
        return
    
    print("\nListe des mots enregistrés :")
    for i, (mot_anglais, mot_francais, points) in enumerate(mots, start=1):
        print(f"{i}. {mot_anglais} : {mot_francais} (Points : {points})")

def supprimer_mot():
    mots = charger_mots()
    if not mots:
        print("Aucun mot n'a été enregistré pour le moment.")
        return
    
    afficher_mots()
    try:
        choix = int(input("\nEntrez le numéro du mot à supprimer : "))
        if 1 <= choix <= len(mots):
            mot_supprime = mots.pop(choix - 1)
            sauvegarder_mots(mots)
            print(f"Le mot '{mot_supprime[0]} : {mot_supprime[1]}' a été supprimé.")
        else:
            print("Numéro invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")

def interroger():
    mots = charger_mots()
    if not mots:
        print("Aucun mot disponible pour l'interrogation. Ajoutez d'abord des mots.")
        return
    
    # Filtrer les tuples avec 0 points ou moins de 7 points
    mots_a_interroger = [(mot_anglais, mot_francais, points) for mot_anglais, mot_francais, points in mots if points < 7]
    
    if not mots_a_interroger:
        print("Tous les mots ont atteint le nombre maximum de points (7).")
        return
    
    # Choisir un mot aléatoire parmi ceux à interroger
    mot_anglais, mot_francais, points = random.choice(mots_a_interroger)
    
    # Choisir aléatoirement si on demande la traduction en français ou en anglais
    if random.choice([True, False]):
        question = f"Quelle est la traduction en français de '{mot_anglais}' ? "
        reponse_correcte = mot_francais
    else:
        question = f"Quelle est la traduction en anglais de '{mot_francais}' ? "
        reponse_correcte = mot_anglais
    
    # Poser la question
    reponse_utilisateur = input(question)
    
    # Ignorer les réponses vides
    if not reponse_utilisateur.strip():  # Vérifie si la réponse est vide ou contient uniquement des espaces
        print("Réponse vide ignorée.")
        return
    
    # Normaliser les réponses (supprimer les accents et mettre en minuscules)
    reponse_utilisateur_normalisee = supprimer_accents(reponse_utilisateur.lower())
    reponse_correcte_normalisee = supprimer_accents(reponse_correcte.lower())
    
    # Vérifier la réponse
    if reponse_utilisateur_normalisee == reponse_correcte_normalisee:
        print("Correct !")
        points += 1  # Ajouter 1 point
    else:
        print(f"Incorrect. La réponse correcte était : {reponse_correcte}")
    
    # Mettre à jour les points dans la liste des mots
    for i, (ma, mf, p) in enumerate(mots):
        if ma == mot_anglais and mf == mot_francais:
            mots[i] = (ma, mf, min(points, 7))  # Limiter à 4 points maximum
            break
    
    # Sauvegarder les mots mis à jour
    sauvegarder_mots(mots)

def main():
    while True:
        print("\n1. Ajouter un mot")
        print("2. S'interroger")
        print("3. Afficher la liste des mots")
        print("4. Supprimer un mot")
        print("5. Quitter")
        choix = input("Choisissez une option (1, 2, 3, 4 ou 5) : ")
        
        if choix == "1":
            mot_anglais, mot_francais = demander_mot()
            if mot_anglais is None or mot_francais is None:
                print("Merci d'avoir utilisé le programme. À bientôt !")
                break
            enregistrer_mot(mot_anglais, mot_francais)
            print("Mot enregistré avec succès !")
        
        elif choix == "2":
            interroger()
        
        elif choix == "3":
            afficher_mots()
        
        elif choix == "4":
            supprimer_mot()
        
        elif choix == "5":
            print("Merci d'avoir utilisé le programme. À bientôt !")
            break
        
        else:
            print("Option invalide. Veuillez choisir 1, 2, 3, 4 ou 5.")

if __name__ == "__main__":
    main()