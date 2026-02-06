"""
Instructions :
- Installez toutes les bibliothèques nécessaires :
  conda create -n projet python pandas numpy matplotlib seaborn streamlit plotly scikit-learn
  conda activate projet
- Lancez l'application avec : streamlit run application.py
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_title="Salaires Data Science", page_icon="📊")

# Chargement des données
df = pd.read_csv("datasets/ds_salaries.csv")




### 1. Titre et introduction
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")

# Bloc description dataset 
with st.expander("📋 Description du dataset", expanded=True):
    col_desc1, col_desc2 = st.columns([1, 3])
    
    with col_desc1:
        st.markdown("**Dataset : Data Science Salaries**")
        st.markdown("**11 colonnes :**")
    
    with col_desc2:
        st.info("""
        **work_year** : Année du salaire  
        **experience_level** : Niveau d'expérience  
        **employment_type** : Type de contrat  
        **job_title** : Poste occupé  
        **salary** : Salaire brut  
        **salary_currency** : Devise  
        **salary_in_usd** : Salaire USD  
        **employee_residence** : Pays résidence  
        **remote_ratio** : % télétravail  
        **company_location** : Pays entreprise  
        **company_size** : Taille entreprise
        """)
      
st.markdown("---")  # Séparateur visuel

### 2. Exploration visuelle (seul sur toute la ligne)
with st.container():
    st.subheader("🔍 Exploration visuelle des données")
    
    nb_lignes = st.slider("Nombre de lignes à afficher", min_value=1, max_value=100, value=10)
    st.dataframe(df.head(nb_lignes), use_container_width=True)
    
    st.markdown("**📌 Statistiques générales**")
    st.dataframe(df.drop(columns=['work_year']).describe(), use_container_width=True)

st.markdown("Le salaire minimum à 6000 € (5132 USD) et maximum à 30 400 000 € (450 000 USD) révèlent probablement des erreurs de saisie ou des valeurs aberrantes extrêmes. Les quartiles révèlent une répartition intéressante : 75% des postes n'offrent aucun télétravail (Q1, Q2, Q3 = 0%), tandis que 25% proposent du full remote (75e percentile = 100%)."
st.markdown("---")

### 3. Distribution France (seule ligne)
with st.container():
    st.subheader("📈 Distribution des salaires en France")
    
    df_france = df[df['company_location'] == 'FR']
    
    if len(df_france) > 0:
        fig = px.box(df_france, x='experience_level', y='salary_in_usd', 
                     color='experience_level',
                     title="Salaires en France par niveau d'expérience",
                     labels={'salary_in_usd': 'Salaire (USD)', 'experience_level': 'Niveau d\'expérience'})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("💡 **Interprétation** : Les salaires augmentent avec l'expérience, forte dispersion pour SE. Quelques valeurs aberrantes apparaissent chez les MI et SE (dépassant 105-110k USD), reflétant des positions exceptionnelles dans certaines régions ou dans des entreprises tech spécialisées")
    else:
        st.warning("⚠️ Aucune donnée pour la France.")

st.markdown("---")

### 4. Salaire moyen par catégorie (seule ligne)
with st.container():
    st.subheader("💰 Salaire moyen par catégorie")
    
    category = st.selectbox("Choisissez une catégorie", 
                            ['experience_level', 'employment_type', 'job_title', 'company_location'])
    
    avg_salary = df.groupby(category)['salary_in_usd'].mean().sort_values(ascending=False).reset_index()
    
    fig = px.bar(avg_salary, x=category, y='salary_in_usd', 
                 title=f"Salaire moyen par {category}",
                 labels={'salary_in_usd': 'Salaire moyen (USD)', category: category.replace('_', ' ').title()},
                 color='salary_in_usd', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"💡 **Interprétation** : Écarts importants selon **{category}**. Le salaire moyen varie énormément selon les critères.")

st.markdown("---")

### 5. Corrélation (seule ligne)
with st.container():
    st.subheader("🔗 Corrélations entre variables numériques")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(corr_matrix, 
                    text_auto=True, 
                    aspect="auto",
                    title="Matrice de corrélation",
                    color_continuous_scale='RdBu_r',
                    height=600)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : Les liens entre variables sont faibles (-0.02 à 0.24). Les variables numériques ne sont pas fortement corrélées.")

st.markdown("---")

### 6. Évolution des salaires (seule ligne)
with st.container():
    st.subheader("📉 Évolution des salaires")
    
    top_jobs = df['job_title'].value_counts().head(10).index.tolist()
    df_top_jobs = df[df['job_title'].isin(top_jobs)]
    salary_evolution = df_top_jobs.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
    
    fig = px.line(salary_evolution, x='work_year', y='salary_in_usd', color='job_title',
                  title="Évolution des salaires (top 10 postes)",
                  labels={'salary_in_usd': 'Salaire moyen (USD)', 'work_year': 'Année'},
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : Chute en 2021 due aux confinements. La plupart des métiers tournent entre 50k et 100k.")

st.markdown("---")

### 7. Salaire médian (seule ligne)
with st.container():
    st.subheader("🏢 Salaire médian par expérience et taille d'entreprise")
    
    median_salary = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()
    
    fig = px.bar(median_salary, x='experience_level', y='salary_in_usd', color='company_size',
                 title="Salaire médian par niveau d'expérience et taille d'entreprise",
                 labels={'salary_in_usd': 'Salaire médian (USD)', 'experience_level': 'Expérience', 'company_size': 'Taille d\'entreprise'},
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : Les entreprises de taille moyenne (M) paient généralement le mieux.")

st.markdown("---")

### 8. Filtrage par salaire (seule ligne)
with st.container():
    st.subheader("🎚️ Filtrage par plage de salaire")
    
    min_salary = int(df['salary_in_usd'].min())
    max_salary = int(df['salary_in_usd'].max())
    
    salary_range = st.slider("Plage de salaire (USD)", min_salary, max_salary, (min_salary, max_salary))
    df_filtered = df[(df['salary_in_usd'] >= salary_range[0]) & (df['salary_in_usd'] <= salary_range[1])]
    
    st.metric("Nombre d'enregistrements", len(df_filtered))
    st.dataframe(df_filtered[['job_title', 'experience_level', 'salary_in_usd', 'company_location']].head(10), use_container_width=True)

st.markdown("---")

### 9. Impact du télétravail (seule ligne)
with st.container():
    st.subheader("🏠 Impact du télétravail sur le salaire")
    
    top_countries = df['company_location'].value_counts().head(5).index.tolist()
    df_top_countries = df[df['company_location'].isin(top_countries)]
    
    remote_impact = df_top_countries.groupby(['company_location', 'remote_ratio'])['salary_in_usd'].mean().reset_index()
    
    fig = px.bar(remote_impact, x='company_location', y='salary_in_usd', color='remote_ratio',
                 title="Impact du télétravail par pays (top 5)",
                 labels={'salary_in_usd': 'Salaire moyen (USD)', 'company_location': 'Pays', 'remote_ratio': 'Taux télétravail (%)'},
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : Le télétravail à 100% est souvent associé à des salaires plus élevés.")

st.markdown("---")

### 10. Filtrage avancé (seule ligne)
with st.container():
    st.subheader("🔍 Filtrage avancé des données")
    
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        experience_levels = st.multiselect("Niveau d'expérience", 
                                            options=df['experience_level'].unique().tolist(),
                                            default=df['experience_level'].unique().tolist())
    
    with col_filter2:
        company_sizes = st.multiselect("Taille d'entreprise", 
                                        options=df['company_size'].unique().tolist(),
                                        default=df['company_size'].unique().tolist())
    
    df_advanced_filtered = df[(df['experience_level'].isin(experience_levels)) & 
                              (df['company_size'].isin(company_sizes))]
    
    st.metric("Nombre d'enregistrements filtrés", len(df_advanced_filtered))
    st.dataframe(df_advanced_filtered[['job_title', 'salary_in_usd', 'experience_level', 'company_size']].head(20), use_container_width=True)
    st.markdown("💡 **Interprétation** : Filtrage multicritères pour analyses ciblées.")





