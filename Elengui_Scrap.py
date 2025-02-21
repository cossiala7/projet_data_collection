import streamlit as st
import pandas as pd
import numpy as np
from requests import get 
import streamlit.components.v1 as components
from bs4 import BeautifulSoup as bs
# Contenu de la sidebar
st.sidebar.title("📌 Menu")
option = st.sidebar.selectbox("🎯 Choisissez une option", ["Accueil","Scraper avec Beautifoulsoup","Scraper avec web scraper" ,"Evaluer l'app"],index = 0, )
# Ajout de styles CSS personnalisés
st.markdown("""
    <style>
        /* Fond blanc pour l'application */
        .stApp {
            background-color: white;
            color: #333;
            font-family: 'Arial', sans-serif;
        }

        /* Fond blanc pour la sidebar */
        .css-1d391kg {
            background-color: white !important;
            color: #333 !important;
            border-right: 2px solid #ddd !important;  /* Légère séparation */
        }

        /* Titres et sous-titres en bleu foncé */
        h1, h2, h3 {
            color: #005580;
            text-align: center;
        }

        /* Boutons et sélections */
        .stSelectbox label {
            font-weight: bold;
            color: #005580;
        }

        /* Cartes et blocs de contenu */
        .css-1lcbmhc {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)
# Titre principal
# Contenu principal
if option == "Accueil":
    st.title("✨ Bienvenue sur Elengui scrap")
    st.header(" ")
    st.write("""
    Elengui scrap est une application de Web Scraping ! 
    Grâce à cet outil puissant, vous pouvez facilement extraire, télécharger et analyser les données des annonces immobilières en ligne.  
    Notre application vous offre **trois principales fonctionnalités** :

    🔍 **1. Scraper les données en temps réel**  
    Vous pouvez récupérer les données des annonces en fonction du **nombre de pages** que vous souhaitez explorer.  
    Les informations collectées incluent : la superficie, le prix, l'adresse, et bien plus encore.

    📥 **2. Télécharger les données brutes**  
    Une fois le scraping terminé, vous avez la possibilité de **télécharger** les données brutes extraites pour les analyser ultérieurement.

    📝 **3. Évaluer l’application**  
    Nous vous donnons la possibilité de nous faire un retour sur votre expérience via **Google Forms** ou **Kobo Toolbox**.  
    Vos retours sont essentiels pour améliorer notre service !

    💡 **Facile d'utilisation, rapide et efficace !** Sélectionnez simplement une option dans le menu et profitez de la puissance du Web Scraping. 🚀
    """)

elif option == "Scraper avec Beautifoulsoup":
    st.title("Beautifoulsoup Elengui")
    st.write("Avec l'option Scrapper avec Beautifoulsoup d'Elengui Scrap, scrapez facilement les données de deux catégories distinctes du site [Coin Afrique Sénégal](https://sn.coinafrique.com) et définissez vous-même le nombre de pages à extraire !")
    nbre_page = st.number_input("Entrez le nombre de page que vous voulez scraper", min_value=1, max_value=100)
    data = st.radio("Quelles données voulez vous scraper",["Terrains","Appartement"])
    if data == "Appartement":
        gdf = pd.DataFrame()
        for i in range(nbre_page):
            url = 'https://sn.coinafrique.com/categorie/appartements?page={i}'
            res = get(url)
            soup = bs(res.text, 'html.parser')
            containers = soup.find_all("div",class_ = "col s6 m4 l3")        
            #Scraper plusieurs containers 
            df = []
            for container in containers:
                try:
                    img_link = container.find("img",class_ = "ad__card-img")["src"]
                    prix = int(container.find("p", class_="ad__card-price").text.replace(" ", "").replace("CFA", ""))
                    adresse = container.find("p", class_="ad__card-location").text.replace("location_on","")
                    href = container.find("a",class_ = "card-image ad__card-image waves-block waves-light")["href"]
                    urll = 'https://sn.coinafrique.com' + str(href)
                    resa = get(urll)
                    soup = bs(resa.text, 'html.parser')
                    containerr = soup.find("div",class_ = "ad__info")
                    nbre_piece = int(containerr.find("span",class_ = "qt").text)
                    dict_appart ={
                            "Nombre_pieces":nbre_piece,
                            "prix":prix,
                            "adresse":adresse,
                            "img_link":img_link,
                    }
                    df.append(dict_appart)
                except:
                    pass
            DF = pd.DataFrame(df)
            gdf = pd.concat([gdf,DF],axis=0).reset_index(drop = True)
            # Standardiser la colonne "prix" et remplacer "prixsurdemande" par NaN
            gdf["prix"] = gdf["prix"].replace("Prixsurdemande", np.nan).astype(float)
            # Remplacer les NaN par la moyenne des prix et convertir en int
            gdf.fillna({"prix": gdf["prix"].mean()}, inplace = True)  
            #gdf["prix"] = gdf["prix"].astype(int)
        st.write(f"Dimension du jeu de données: {gdf.shape[0]} lignes et {gdf.shape[1]} colonnes")      
        st.write(gdf)
        # Convertir le DataFrame en CSV (sans index)
        csv = gdf.to_csv(index=False).encode('utf-8')
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv,
            file_name="donnees_terrain.csv",
            mime="text/csv")
    else:
        #Faire un scraping sur toutes les pages 
        Gdf = pd.DataFrame()
        for i in range(nbre_page):
            url = 'https://sn.coinafrique.com/categorie/terrains?page={i}'
            res = get(url)
            soup = bs(res.text, 'html.parser')
            containers = soup.find_all("div",class_ = "col s6 m4 l3")
            pdf = []
            for container in containers:
                try:
                    img_link = container.find("img", class_="ad__card-img")["src"]
                    prix = int(container.find("p", class_="ad__card-price").text.replace(" ", "").replace("CFA", ""))
                    adresse = container.find("p", class_="ad__card-location").text.replace("location_on","")
                    href = container.find("a", class_="card-image ad__card-image waves-block waves-light")["href"]
                    urll = 'https://sn.coinafrique.com' + str(href)
                    resa = get(urll)
                    soup = bs(resa.text, 'html.parser')
                    containerr = soup.find("div", class_="ad__info") 
                    superficie = int(containerr.find("span", class_="qt").text.replace(" ", "").replace("m2", ""))
                    dict_terrain_infos = {
                        "superficie": superficie,
                        "prix": prix,
                        "adresse": adresse,
                        "img_link": img_link,
                    }
                    pdf.append(dict_terrain_infos)
                except:
                    pass    
            DF = pd.DataFrame(pdf)
            Gdf = pd.concat([Gdf,DF],axis=0).reset_index(drop = True)
            # Standardiser la colonne "prix" et remplacer "prixsurdemande" par NaN
            Gdf["prix"] = Gdf["prix"].replace("Prixsurdemande", np.nan).astype(float)
            # Remplacer les NaN par la moyenne des prix et convertir en int
            Gdf.fillna({"prix": Gdf["prix"].mean()}, inplace = True)  
            #Gdf["prix"] = Gdf["prix"].astype(int)
        st.write(f"Dimension du jeu de données: {Gdf.shape[0]} lignes et {Gdf.shape[1]} colonnes")  
        st.write(Gdf)      
        # Convertir le DataFrame en CSV (sans index)
        csv2 = Gdf.to_csv(index=False).encode('utf-8')
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv2,
            file_name="donnees_terrain.csv",
            mime="text/csv")    
elif option == "Scraper avec web scraper":
    st.title("Web scraper Elengui")
    st.write("web scraper automatise l'extraction de données d'un site en suivant un sitemap et en utilisant des sélecteurs pour cibler les éléments spécifiques à récupérer.")
    terrain_scrap = st.button("Terrains a vendre")
    appartements_scrap = st.button("Appartements a louer")
    if terrain_scrap:
        terrain = pd.read_csv("./data/coinafrique_terrain_scrap (2).csv")
        st.write(f"Dimension du jeu de données: {terrain.shape[0]} lignes et {terrain.shape[1]} colonnes")
        st.write(terrain)
        dwld = terrain.to_csv(index=False).encode('utf-8')
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger les données en CSV",
            data=dwld,
            file_name="donnee_terrain.csv",
            mime="text/csv")
    elif appartements_scrap:
        file = pd.read_csv("./data/coinafrique_appartement_scrap.csv")
        st.write(f"Dimension du jeu de données: {file.shape[0]} lignes et {file.shape[1]} colonnes")
        st.write(file)
        csv = file.to_csv(index=False).encode('utf-8')
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger les données en CSV",
            data=csv,
            file_name="donnees_terrain.csv",
            mime="text/csv")
elif option == "Evaluer l'app":
    eval_app = st.radio("Sur quelle plateforme souhaitez-vous évaluer l'application ?",["Koboo Toolbox","Google Forms"])
    if eval_app == "Koboo Toolbox":
        components.iframe("https://ee.kobotoolbox.org/i/d1fEvstv",width=800, height=600)
    elif eval_app == "Google Forms":
        components.iframe("https://forms.gle/gvzAHKs9L5MprPHn8",width=750,height=1200)    
    
           
