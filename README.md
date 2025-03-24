# LoshFinder

**LoshFinder** est un outil gratuit et simple à utiliser qui permet de rechercher rapidement des mots, caractères ou phrases dans un ensemble de fichiers. Il prend en charge plusieurs formats de fichiers tels que `.txt`, `.sql`, `.html`, etc. Il permet de faire une recherche avancée à la manière de la fonction `CTRL + F` sur un ensemble de fichiers sans avoir à ouvrir chaque fichier manuellement.

## Fonctionnalités

- Rechercher des mots, phrases ou caractères dans plusieurs fichiers à la fois.
- Prise en charge de différents formats de fichiers comme `.txt`, `.sql`, `.html`, et plus.
- Recherche rapide et efficace pour gagner du temps.
- Interface simple et facile à utiliser.

## Technologies

- **Langage principal** : Python

## Installation

Pour installer **LoshFinder**, assurez-vous d'avoir Python 3.x installé sur votre machine. Ensuite, clonez ce dépôt et installez les dépendances requises.

1. Clonez ce dépôt :
    ```bash
    git clone https://github.com/ton-utilisateur/LoshFinder.git
    cd LoshFinder
    ```

2. Installez les dépendances (si nécessaire) :
    ```bash
    pip install -r requirements.txt
    ```

3. Si vous n'avez pas encore un fichier `requirements.txt`, vous pouvez installer directement les bibliothèques nécessaires (si besoin) avec :
    ```bash
    pip install os re
    ```

## Utilisation

1. Lancez le script principal en ligne de commande :
    ```bash
    python loshfinder.py
    ```

2. Ensuite, fournissez le dossier contenant les fichiers que vous souhaitez rechercher ainsi que le terme de recherche (mot, phrase, etc.).

Exemple de commande :
```bash
python loshfinder.py --dossier "chemin/vers/dossier" --terme "mot_de_recherche"
