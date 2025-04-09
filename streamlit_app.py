import streamlit as st
import joblib
from cryptography.fernet import Fernet
import pandas as pd
import hashlib
from datetime import datetime

# Chargement du modèle
model = joblib.load("model.pkl")

# Chargement des secrets
fernet_key = st.secrets["fernet_key"]
access_token = st.secrets["access_token"]  # Le token secret
cipher = Fernet(fernet_key)

def authenticate():
    """Fonction pour vérifier le token d'accès de l'utilisateur"""
    st.title("🔐 Interface sécurisée SentimentCorp")
    token_utilisateur = st.text_input("Entrez votre token d'accès", type="password")
    if token_utilisateur == access_token:
        return True
    st.error("Accès refusé. Token incorrect.")
    return False

def log_access(action):
    """Fonction pour loguer les actions d'accès dans un fichier log"""
    with open("log_access.txt", "a") as f:
        f.write(f"[{datetime.now()}] WebUser - {action}\n")

def predict_and_encrypt(text, vectorizer):
    """Fonction pour prédire et chiffrer la prédiction"""
    vect = vectorizer.transform([text])
    pred = model.predict(vect)[0]
    label = "Toxique" if pred == 1 else "Positif"
    encrypted = cipher.encrypt(label.encode()).decode()  # Chiffrement du résultat
    return encrypted, label

# Interface
if authenticate():
    log_access("Connexion réussie")
    
    # Chargement du vectorizer
    vectorizer = joblib.load("vectorizer.pkl")  # Charger le vectorizer pour transformer les commentaires
    
    msg = st.text_area("💬 Entrez un commentaire à analyser :")
    
    if st.button("🔎 Prédire"):
        if msg:
            encrypted, label = predict_and_encrypt(msg, vectorizer)
            st.success("🔐 Résultat chiffré :")
            st.code(encrypted)  # Afficher la prédiction chiffrée
            if st.checkbox("🔓 Voir le résultat déchiffré"):
                st.write("Prédiction :", label)  # Afficher la prédiction en clair
            log_access("Prédiction faite")
