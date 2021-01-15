# Description de l'outil
Ce **moteur de recherche** constitue une base de connaissances  ouverte de l'IGA; les [bonnes feuilles](https://www.interieur.gouv.fr/Publications/Rapports-de-l-IGA/Bonnes-Feuilles).

⚠️ **Attention** ⚠️, il s'agit ici d'une démo, la barre de recherche ainsi que les résultats sont configurables.
Il peut aussi être utilisé pour des documents sous d'autres formats, avec des champs texte, date ou mots-clefs.
Pour des questions relatives à son installation ou utilisation, vous pouvez nous contacter [✉️](datalab@interieur.gouv.fr).
---
# Notice d'utilisation

## Un onglet [recherche](search)

Dans la barre de recherche, on peut effectuer une recherche par mots-clefs avec des **opérateurs spéciaux**:
La recherche : ("Des Sargasses" -algues) OR (Martinique +plage) retournera les documents avec la séquence "Des Sargasses" sans algues OU les documents avec Martinique et absolument plages.

On peut aussi mettre un filtre par tag.

Les documents sont présentés par ordre de pertinence. En mode **admin**, il est possible de le supprimer ou de changer des méta-données.
Une limite est indiquée pour les documents jugés non pertinents.

## Un onglet [glossaire](glossary)

La liste des **acronymes** avec une barre de recherche. En mode **admin**, possibilité de supprimer, modifier ou ajouter des éléments. Les "\_" sont ajoutés automatiquement, les accents et les mots de liaison sont supprimés.

## Un onglet [expression](expression)

Idem que pour les acronymes.

## Un onglet [admin 👤](admin)

Il est visible uniquement en mode **admin**. On peut ajouter un nouveau document, lancer la réindexation, ajouter des pièces-jointes ou changer les seuils d'affichage et de pertinence.

##  Une icône de connexion
Un clic ouvre ou ferme la **fenêtre d'identification**. Pour devenir admin, rentrez user1 et abcxyz pour tester.

---
# Briques technologiques

## Le moteur de recherche
Le coeur du moteur s'appuie sur la technologie ouverte [**elasticsearch**](https://elasticsearch.com).

## L'interface utilisateur
ELle est développée en [Svelte](https://svelte.dev), un language récent et très rapide qui compile du javascript, html et css.
Le site est servi avec Nginx, pour contrôler les connexions et gérer le routage des services appelés par l'interface.

## Le serveur
Le serveur qui répond aux requêtes de l’interface est développée en **Python**, avec la bibliothèque Flask.

## Autres outils
Pour mieux cloisonner les différents services, nous utilisons **Docker**.
