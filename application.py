"""
Instructions :
- Installez toutes les bibliothèques nécessaires en fonction des imports présents dans le code, utilisez la commande suivante :
  conda create -n projet python pandas numpy matplotlib seaborn streamlit plotly scikit-learn
  conda activate projet
- Complétez les sections en écrivant votre code où c'est indiqué.
- Ajoutez des commentaires clairs pour expliquer vos choix.
- Interprétez les résultats de vos visualisations (quelques phrases).
"""


### 1. Importation des librairies et chargement des données
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px


# Chargement des données
df = pd.read_csv("ds_salaries.csv")


### 2. Exploration visuelle des données
st.title("Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")

# Affichage d'un aperçu des données
if st.checkbox("Afficher un aperçu des données"):
    st.write(df.head(10))  # Affiche les 10 premières lignes pour avoir un aperçu rapide

# Statistiques générales avec describe pandas 
st.subheader("Statistiques générales")
st.write(df.describe())  # Statistiques descriptives (moyenne, médiane, écart-type, etc.)


### 3. Distribution des salaires en France par rôle et niveau d'expérience, utilisant px.box et st.plotly_chart
st.subheader("Distribution des salaires en France")

# Filtrer les données pour la France uniquement
df_france = df[df['company_location'] == 'FR']

if len(df_france) > 0:
    # Box plot pour visualiser la distribution des salaires par niveau d'expérience
    fig = px.box(df_france, x='experience_level', y='salary_in_usd', 
                 color='experience_level',
                 title="Distribution des salaires en France par niveau d'expérience",
                 labels={'salary_in_usd': 'Salaire (USD)', 'experience_level': 'Niveau d\'expérience'})
    st.plotly_chart(fig)
    st.markdown("**Interprétation** : Les salaires en France augmentent avec le niveau d'expérience, avec une forte dispersion pour les profils seniors (SE/EX).")
else:
    st.warning("Aucune donnée disponible pour la France dans ce dataset.")


### 4. Analyse des tendances de salaires :
#### Salaire moyen par catégorie : en choisissant une des : ['experience_level', 'employment_type', 'job_title', 'company_location'], utilisant px.bar et st.selectbox 

st.subheader("Salaire moyen par catégorie")

# Sélecteur pour choisir la catégorie d'analyse
category = st.selectbox("Choisissez une catégorie", ['experience_level', 'employment_type', 'job_title', 'company_location'])

# Calcul du salaire moyen par catégorie
avg_salary = df.groupby(category)['salary_in_usd'].mean().sort_values(ascending=False).reset_index()

# Affichage d'un graphique en barres
fig = px.bar(avg_salary, x=category, y='salary_in_usd', 
             title=f"Salaire moyen par {category}",
             labels={'salary_in_usd': 'Salaire moyen (USD)', category: category.replace('_', ' ').title()},
             color='salary_in_usd', color_continuous_scale='Blues')
st.plotly_chart(fig)
st.markdown(f"**Interprétation** : Le salaire moyen varie fortement selon le **{category}**, avec des écarts importants entre les catégories.")


### 5. Corrélation entre variables
# Sélectionner uniquement les colonnes numériques pour la corrélation
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

# Calcul de la matrice de corrélation
corr_matrix = df[numeric_cols].corr()

# Affichage du heatmap avec sns.heatmap
st.subheader("Corrélations entre variables numériques")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', ax=ax, linewidths=0.5)
st.pyplot(fig)
st.markdown("**Interprétation** : Le heatmap montre les corrélations entre les variables numériques. Une forte corrélation positive indique que deux variables évoluent ensemble.")


### 6. Analyse interactive des variations de salaire
# Une évolution des salaires pour les 10 postes les plus courants
st.subheader("Évolution des salaires pour les postes les plus courants")

# Identifier les 10 postes les plus courants
top_jobs = df['job_title'].value_counts().head(10).index.tolist()

# Filtrer les données pour ces postes
df_top_jobs = df[df['job_title'].isin(top_jobs)]

# Calcul du salaire moyen par année pour chaque poste
salary_evolution = df_top_jobs.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()

# Line chart pour visualiser l'évolution
fig = px.line(salary_evolution, x='work_year', y='salary_in_usd', color='job_title',
              title="Évolution des salaires pour les 10 postes les plus courants",
              labels={'salary_in_usd': 'Salaire moyen (USD)', 'work_year': 'Année'},
              markers=True)
st.plotly_chart(fig)
st.markdown("**Interprétation** : On observe une tendance à la hausse des salaires pour la plupart des postes entre 2020 et 2023, avec des variations selon les rôles.")


### 7. Salaire médian par expérience et taille d'entreprise
# utilisez median(), px.bar
st.subheader("Salaire médian par expérience et taille d'entreprise")

# Calcul du salaire médian par expérience et taille d'entreprise
median_salary = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()

# Barplot groupé
fig = px.bar(median_salary, x='experience_level', y='salary_in_usd', color='company_size',
             title="Salaire médian par niveau d'expérience et taille d'entreprise",
             labels={'salary_in_usd': 'Salaire médian (USD)', 'experience_level': 'Niveau d\'expérience', 'company_size': 'Taille d\'entreprise'},
             barmode='group')
st.plotly_chart(fig)
st.markdown("**Interprétation** : Les grandes entreprises (L) offrent généralement des salaires médians plus élevés que les petites (S) et moyennes (M), quel que soit le niveau d'expérience.")


### 8. Ajout de filtres dynamiques
# Filtrer les données par salaire utilisant st.slider pour sélectionner les plages 
st.subheader("Filtrage par plage de salaire")

# Définir les bornes du slider
min_salary = int(df['salary_in_usd'].min())
max_salary = int(df['salary_in_usd'].max())

# Slider pour sélectionner la plage de salaire
salary_range = st.slider("Sélectionnez la plage de salaire (USD)", min_salary, max_salary, (min_salary, max_salary))

# Filtrer le dataframe selon la plage sélectionnée
df_filtered = df[(df['salary_in_usd'] >= salary_range[0]) & (df['salary_in_usd'] <= salary_range[1])]

st.write(f"Nombre d'enregistrements : **{len(df_filtered)}**")
st.write(df_filtered.head(10))


### 9. Impact du télétravail sur le salaire selon le pays
st.subheader("Impact du télétravail sur le salaire")

# Sélectionner les 5 pays avec le plus de données
top_countries = df['company_location'].value_counts().head(5).index.tolist()
df_top_countries = df[df['company_location'].isin(top_countries)]

# Calcul du salaire moyen par remote_ratio et pays
remote_impact = df_top_countries.groupby(['company_location', 'remote_ratio'])['salary_in_usd'].mean().reset_index()

# Barplot pour comparer l'impact du télétravail
fig = px.bar(remote_impact, x='company_location', y='salary_in_usd', color='remote_ratio',
             title="Impact du télétravail sur le salaire selon le pays",
             labels={'salary_in_usd': 'Salaire moyen (USD)', 'company_location': 'Pays', 'remote_ratio': 'Taux de télétravail (%)'},
             barmode='group')
st.plotly_chart(fig)
st.markdown("**Interprétation** : Le télétravail à 100% est souvent associé à des salaires plus élevés, notamment dans les pays comme les USA où la culture du remote est bien établie.")


### 10. Filtrage avancé des données avec deux st.multiselect
st.subheader("Filtrage avancé des données")

# Multiselect pour le niveau d'expérience
experience_levels = st.multiselect("Sélectionnez le niveau d'expérience", 
                                    options=df['experience_level'].unique().tolist(),
                                    default=df['experience_level'].unique().tolist())

# Multiselect pour la taille d'entreprise
company_sizes = st.multiselect("Sélectionnez la taille d'entreprise", 
                                options=df['company_size'].unique().tolist(),
                                default=df['company_size'].unique().tolist())

# Filtrer le dataframe selon les sélections
df_advanced_filtered = df[(df['experience_level'].isin(experience_levels)) & (df['company_size'].isin(company_sizes))]

st.write(f"Nombre d'enregistrements filtrés : **{len(df_advanced_filtered)}**")
st.write(df_advanced_filtered.head(20))

st.markdown("**Interprétation** : Ce filtre avancé permet d'explorer les données selon des critères multiples pour des analyses plus ciblées.")
