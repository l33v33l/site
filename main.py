from website import create_app

# Seulement exécuter la ligne si on exécute le fichier directement (et ne pas le faire si l'importer)
# Car ça lance le serveur web.

app = create_app()

if __name__ == '__main__':
    # Debug = True c'est pour relancer le serveur après chaque modification du code.
    app.run(debug=True)
