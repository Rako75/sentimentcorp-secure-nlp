# SentimentCorp - Pipeline NLP Sécurisé 🛡️

**SentimentCorp** propose une solution de modération automatique de commentaires en ligne, classifiant les commentaires en **positifs** ou **négatifs**. Ce pipeline est conçu avec un fort accent sur la **cybersécurité**.

## 🚀 Description du projet

Ce projet permet de classer les commentaires en utilisant un modèle NLP (Logistic Regression) en intégrant plusieurs aspects de cybersécurité :
- **Chiffrement des données** d’entrée et de sortie à l'aide de la bibliothèque `cryptography` (clé Fernet).
- **Authentification par mot de passe** : seulement les utilisateurs authentifiés peuvent accéder aux prédictions.
- **Journalisation des accès** pour traquer les actions effectuées sur l’application.
- **Séparation des rôles** : accès complet pour les Data Scientists, accès en lecture pour les Analystes.

Le modèle et le transformateur TF-IDF sont enregistrés dans des fichiers `model.pkl` et `vectorizer.pkl` respectivement.

## 🔐 Sécurité et gestion des accès

### Authentification
- Un mot de passe hashé est utilisé pour garantir l’accès sécurisé à l’interface.
- Le mot de passe est vérifié avant d’afficher les résultats des prédictions.

### Chiffrement des prédictions
- Les résultats des prédictions sont **chiffrés** avant d’être envoyés à l’utilisateur.
- L’utilisateur peut choisir de les **déchiffrer** pour voir la prédiction originale.

### Journalisation des accès
- Un fichier `log_access.txt` garde une trace de toutes les actions importantes : chargement des données et génération de prédictions.
