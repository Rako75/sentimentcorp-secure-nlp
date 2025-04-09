import streamlit as st
import joblib
from cryptography.fernet import Fernet
import pandas as pd
import hashlib
from datetime import datetime

# Chargement du modèle
model = joblib.load("model.pkl")

# Chargement des secrets
fernet_key = st.secrets["general"]["fernet_key"]
password_hash = st.secrets["general"]["password_hash"]

cipher = Fernet(fernet_key)

def authenticate():
    st.title("🔐 Interface sécurisée SentimentCorp")
    pwd = st.text_input("Mot de passe", type="password")
    if hashlib.sha256(pwd.encode()).hexdigest() == password_hash:
        return True
    st.error("Mot de passe incorrect.")
    return False

def log_access(action):
    with open("log_access.txt", "a") as f:
        f.write(f"[{datetime.now()}] WebUser - {action}\n")

def predict_and_encrypt(text, vectorizer):
    vect = vectorizer.transform([text])
    pred = model.predict(vect)[0]
    label = "Toxique" if pred == 1 else "Positif"
    encrypted = cipher.encrypt(label.encode()).decode()
    return encrypted, label

# Interface
if authenticate():
    log_access("Connexion réussie")
    
    vectorizer = joblib.load("vectorizer.pkl")  # à ajouter à ton entraînement
    
    msg = st.text_area("💬 Entrez un commentaire à analyser :")
    if st.button("🔎 Prédire"):
        if msg:
            encrypted, label = predict_and_encrypt(msg, vectorizer)
            st.success("🔐 Résultat chiffré :")
            st.code(encrypted)
            if st.checkbox("🔓 Voir le résultat déchiffré"):
                st.write("Prédiction :", label)
            log_access("Prédiction faite")
