import streamlit as st
from datetime import datetime

def calculer_mois_assurance(date_permis, date_infraction, date_recuperation, mois_supplementaires):
    # Convertir les chaînes de texte en objets datetime
    date_permis = datetime.strptime(date_permis, "%d-%m-%Y")
    date_infraction = datetime.strptime(date_infraction, "%d-%m-%Y")
    
    # Vérifier si une date de récupération est spécifiée
    if date_recuperation:
        date_recuperation = datetime.strptime(date_recuperation, "%d-%m-%Y")
    else:
        date_recuperation = date_infraction  # Utiliser la date de l'infraction si aucune date de récupération n'est spécifiée
    
    # Calculer la différence entre la date de récupération et la date du permis en jours
    difference_permis_recuperation = date_recuperation - date_permis
    
    # Calculer la différence entre la date de l'infraction et la date du permis en jours
    difference_permis_infraction = date_infraction - date_permis
    
    # Calculer la différence entre la date de récupération et la date de l'infraction en jours
    difference_infraction_recuperation = date_recuperation - date_infraction
    
    # Calculer le nombre de mois exact entre la date du permis et la date de récupération
    nombre_mois_permis_recuperation = difference_permis_recuperation.days / 30.4367
    
    # Vérifier si la date de récupération est après la date de l'infraction
    if difference_infraction_recuperation.days < 0:
        st.warning("La date de récupération du permis est avant la date de l'infraction. Veuillez vérifier les dates.")
        return None
    
    # Calculer le nombre de mois exact entre la date du permis et la date de l'infraction
    nombre_mois_permis_infraction = difference_permis_infraction.days / 30.4367
    
    # Calculer le nombre total de mois en excluant la période entre la récupération et l'infraction
    nombre_mois_total = nombre_mois_permis_infraction + mois_supplementaires
    
    return nombre_mois_total

# Titre de l'application
st.title("Calculateur de mois d'assurance")

# Champ de saisie pour la date du permis avec le format jour-mois-année
date_permis = st.date_input("Date du permis", format="DD-MM-YYYY")

# Champ de saisie pour la date de l'infraction avec le format jour-mois-année
date_infraction = st.date_input("Date de l'infraction", format="DD-MM-YYYY")

# Vérifier si le permis a été récupéré après l'infraction
recuperation_permis = st.checkbox("Le permis a été récupéré après l'infraction ?")

# Champ de saisie pour la date de récupération si sélectionnée
if recuperation_permis:
    date_recuperation = st.date_input("Date de récupération du permis", format="DD-MM-YYYY")
    
    # Demander à l'utilisateur le nombre de mois supplémentaires pour l'assurance
    mois_supplementaires = st.number_input("Nombre de mois d'assurance après la récupération du permis", min_value=0, step=1)
else:
    date_recuperation = None
    mois_supplementaires = 0


# Bouton pour calculer le nombre de mois d'assurance
if st.button("Calculer"):
    if date_permis <= date_infraction:
        nombre_mois = calculer_mois_assurance(date_permis.strftime("%d-%m-%Y"), date_infraction.strftime("%d-%m-%Y"), date_recuperation.strftime("%d-%m-%Y") if date_recuperation else None, mois_supplementaires)
        if nombre_mois is not None:
            st.success(f"Le nombre de mois d'assurance est de : {nombre_mois:.2f} mois")
            if nombre_mois >= 9 and nombre_mois < 10:
               st.write("Le nombre de mois est entre 9 inclus et strictement inférieur à 10")
               st.write("Merci de placer le client chez COVERITY OU CARMINE")
                
            elif nombre_mois >= 10:
                 st.write("Le nombre de mois est supérieur ou égal à 10")
                 st.write("Merci de placer le client chez COVERITY OU CARMINE")
            else:
                st.write("Hors souscription")
                st.write("coonseil: Si l client  a moins de",  "23 ans" ,"et s'il n'a pas dinfraction alcoolemie ou stupefiant merci de tarifier sur MAXANCE")
               
            
    else:
        st.error("La date du permis doit être antérieure à la date de l'infraction.")