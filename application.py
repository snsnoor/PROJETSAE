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
#import matplotlib.pyplot as plt
#import seaborn as sns
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide", page_title="Salaires Data Science", page_icon="📊")

# Chargement des données
df = pd.read_csv("datasets/ds_salaries.csv")


### 1. Titre et introduction
st.title("📊 Visualisation des Salaires en Data Science")
st.markdown("Explorez les tendances des salaires à travers différentes visualisations interactives.")


### 2. Exploration visuelle (seul sur toute la ligne)
st.subheader("🔍 Exploration visuelle des données")

nb_lignes = st.slider("Nombre de lignes à afficher", min_value=1, max_value=100, value=10)
st.write(df.head(nb_lignes))

st.write("**📌 Statistiques générales**")
st.write(df.drop(columns=['work_year']).describe())



### 3 et 4. Distribution France (3) et Salaire moyen par catégorie (4) côte à côte
col_3, col_4 = st.columns(2)

with col_3:
    st.subheader("📈 Distribution France")
    df_france = df[df['company_location'] == 'FR']
    
    if len(df_france) > 0:
        fig = px.box(df_france, x='experience_level', y='salary_in_usd', 
                     color='experience_level',
                     title="Salaires en France par expérience",
                     labels={'salary_in_usd': 'Salaire (USD)', 'experience_level': 'Expérience'})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("💡 **Interprétation** : Les salaires augmentent avec l'expérience, forte dispersion pour SE.")
    else:
        st.warning("⚠️ Aucune donnée pour la France.")

with col_4:
    st.subheader("💰 Salaire moyen par catégorie")
    category = st.selectbox("Choisissez une catégorie", 
                            ['experience_level', 'employment_type', 'job_title', 'company_location'])
    
    avg_salary = df.groupby(category)['salary_in_usd'].mean().sort_values(ascending=False).reset_index()
    
    fig = px.bar(avg_salary, x=category, y='salary_in_usd', 
                 title=f"Salaire moyen par {category}",
                 labels={'salary_in_usd': 'Salaire moyen (USD)', category: category.replace('_', ' ').title()},
                 color='salary_in_usd', color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"💡 **Interprétation** : Écarts importants selon **{category}**. Le salaire moyen varient énormément selon plein de critères")


### 5. Corrélation (seul sur toute la ligne)
### 5. Corrélation (seul sur toute la ligne)
st.subheader("🔗 Corrélations entre variables numériques")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr_matrix = df[numeric_cols].corr()

# Remplace seaborn par plotly (même résultat, sans matplotlib)
fig = px.imshow(corr_matrix, 
                text_auto=True, 
                aspect="auto",
                title="Matrice de corrélation",
                color_continuous_scale='RdBu_r',
                height=600)
st.plotly_chart(fig, use_container_width=True)
st.markdown("💡 **Interprétation** : Le heatmap révèle les relations entre variables numériques. Dans notre cas les liens entre les varibales sont très faibles , allant de -0.02 à 0.24 ce qui suggère que les variables numériques ne sont pas fortement corrélées entre elles.")


### 6 et 7. Évolution salaires (6) et Salaire médian (7) côte à côte
col_6, col_7 = st.columns(2)

with col_6:
    st.subheader("📉 Évolution des salaires")
    top_jobs = df['job_title'].value_counts().head(10).index.tolist()
    df_top_jobs = df[df['job_title'].isin(top_jobs)]
    salary_evolution = df_top_jobs.groupby(['work_year', 'job_title'])['salary_in_usd'].mean().reset_index()
    
    fig = px.line(salary_evolution, x='work_year', y='salary_in_usd', color='job_title',
                  title="Évolution des salaires (top 10 postes)",
                  labels={'salary_in_usd': 'Salaire moyen (USD)', 'work_year': 'Année'},
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : En 2021 on a une chute soudain des salaires, ce qui est surement du aux confinements qui ont eu lieu. Et la plupart de ces métiers tournaient entre 50k et 100k")

with col_7:
    st.subheader("🏢 Salaire médian")
    median_salary = df.groupby(['experience_level', 'company_size'])['salary_in_usd'].median().reset_index()
    
    fig = px.bar(median_salary, x='experience_level', y='salary_in_usd', color='company_size',
                 title="Salaire médian par expérience et taille",
                 labels={'salary_in_usd': 'Salaire médian (USD)', 'experience_level': 'Expérience', 'company_size': 'Taille'},
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : Les entreprises à taille moyenne (M) sont celles qui paient le mieux.")


### 8 et 9. Filtrage salaire (8) et Impact télétravail (9) côte à côte
col_8, col_9 = st.columns(2)

with col_8:
    st.subheader("🎚️ Filtrage par salaire")
    min_salary = int(df['salary_in_usd'].min())
    max_salary = int(df['salary_in_usd'].max())
    
    salary_range = st.slider("Plage de salaire (USD)", min_salary, max_salary, (min_salary, max_salary))
    df_filtered = df[(df['salary_in_usd'] >= salary_range[0]) & (df['salary_in_usd'] <= salary_range[1])]
    
    st.write(f"📊 Nombre d'enregistrements : **{len(df_filtered)}**")
    st.write(df_filtered.head(10))

with col_9:
    st.subheader("🏠 Impact du télétravail")
    top_countries = df['company_location'].value_counts().head(5).index.tolist()
    df_top_countries = df[df['company_location'].isin(top_countries)]
    
    remote_impact = df_top_countries.groupby(['company_location', 'remote_ratio'])['salary_in_usd'].mean().reset_index()
    
    fig = px.bar(remote_impact, x='company_location', y='salary_in_usd', color='remote_ratio',
                 title="Impact du télétravail par pays",
                 labels={'salary_in_usd': 'Salaire moyen (USD)', 'company_location': 'Pays', 'remote_ratio': 'Taux télétravail (%)'},
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("💡 **Interprétation** : Le télétravail 100% est associé à des salaires plus élevés dans certains pays.")


### 10. Filtrage avancé (seul sur toute la ligne)
st.subheader("🔍 Filtrage avancé des données")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    experience_levels = st.multiselect("Sélectionnez le niveau d'expérience", 
                                        options=df['experience_level'].unique().tolist(),
                                        default=df['experience_level'].unique().tolist())

with col_filter2:
    company_sizes = st.multiselect("Sélectionnez la taille d'entreprise", 
                                    options=df['company_size'].unique().tolist(),
                                    default=df['company_size'].unique().tolist())

df_advanced_filtered = df[(df['experience_level'].isin(experience_levels)) & 
                          (df['company_size'].isin(company_sizes))]

st.write(f"📊 Nombre d'enregistrements filtrés : **{len(df_advanced_filtered)}**")
st.write(df_advanced_filtered.head(20))
st.markdown("💡 **Interprétation** : Filtrage multicritères pour analyses ciblées.")


