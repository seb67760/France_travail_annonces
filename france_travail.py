import pandas as pd  
import streamlit as st
from bs4 import BeautifulSoup
import requests

import io

buffer = io.BytesIO()

st.sidebar.title("Sommaire")

pages = ["Contexte du projet", "Recherche du code de la commune", "Recherche emploi"]

page = st.sidebar.radio("Aller vers la page :", pages)

if page == pages[0] : 
    
    st.title('Contexte du projet')
    
    st.write("Cet outil va vous permettre de faire des recherches d'emploi et de les sauvegarder dans un tableau excel.")
    
    st.write("La recherche se fait par mots clés, lieu, distance de ce lieu")
    
    st.write("Cet outil n'est pas officiel, mais une aide possible pour lister les propositions de postes présentes sur le site **candidat.francetravail.fr** qui peuvent vous intéresser")
    
    file_image = r'logo.png'
    st.image(file_image, caption= "logo France Travail")
    
if page == pages[1] :
   
    st.title('Recherche du code de la commune')
 
    st.write("Pour effectuer cette recherche, l'outil fonctionne avec le code INSEE de la commune.")
    
    st.write("Faites votre recherche de code INSEE ci-dessous.")
    
    
    path_import     = "./data/"
    filename_import = "v_commune_2023.csv"
    
    commune = pd.read_csv(path_import + filename_import)
    commune = commune[['COM','NCC','LIBELLE']]
    
    commune = commune.rename(columns={"COM": "code INSEE"})
    
    val_BuildingType = st.text_input('Saisir le nom de la commune 👇', 'Stras')
    
    resultat = commune[commune["NCC"].str.contains(val_BuildingType.upper())]
    st.dataframe(resultat[['code INSEE','LIBELLE']], hide_index= True)
    
    

if page == pages[2] :
    
    st.title('Recherche emploi')
    
    st.write("Vous avez votre code INSEE ? Parfait, vous pouvez à présent effectuer votre recherche.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        val_code_insee = st.text_input('Code Insee', '67482')
        val_mot_cle_1 = st.text_input('Mot clé 1')
        val_mot_cle_4 = st.text_input('Mot clé 4')
        
    with col2:
        val_distance = st.text_input('Distance maximum', '30')
        val_mot_cle_2 = st.text_input('Mot clé 2')
        val_mot_cle_5 = st.text_input('Mot clé 5')
        
    with col3:
        empty_space = st.text_input('', label_visibility= "hidden", disabled= True)
        val_mot_cle_3 = st.text_input('Mot clé 3')
        val_mot_cle_6 = st.text_input('Mot clé 6')
        
    liste_entree = [val_mot_cle_1, val_mot_cle_2, val_mot_cle_3,
                    val_mot_cle_4, val_mot_cle_5, val_mot_cle_6]
    
    
    liste_mots_cles = []
    for liste_mots in liste_entree:
            if liste_mots != "":
                liste_mots_cles.append(liste_mots)
    
    liste_mots_cles = ",".join(liste_mots_cles)
    
    st.write(liste_mots_cles)
    
    def getData(domaine, rayon, code_insee):
        r = requests.get(
            "https://candidat.francetravail.fr/offres/recherche?lieux="+code_insee+"&motsCles="+domaine+"&offresPartenaires=true&range=0-200&rayon="+rayon+"&tri=0")
        data = r.text
        soup = BeautifulSoup(data)
        return soup
   
    postes = []

    soup = getData(liste_mots_cles, val_distance, val_code_insee)
    if soup:
        for link in soup.find_all('li', {'class':'result'}) :
            publication = link.find('p', {'class':'date'}).text
            #offre = link.find('h2 data-intitule-offre', {'class':'t4 media-heading'}).text
            titre = link.find('h2', {'class':'media-heading'}).text
            contrat = link.find('p', {'class':'contrat'}).text
            description = link.find('p', {'class':'description'}).text
            origine = link.find('img').get('alt')
    
            annonces = [titre,contrat,description,origine,publication]
            postes.append(annonces)

    postes = pd.DataFrame(postes, columns=('titre', 'contrat', 'description','origine','publication'))
    
    st.dataframe(postes, hide_index= True)
    

    
    #st.download_button(label='📥 Exporter sur Excel', data=df_xlsx ,file_name= 'postes.xlsx')

    csv = postes.to_csv(encoding='utf-16', sep='\t', index=False)
    
    
    st.write("**Pensez à sauvegarder vos résultats dans un fichier CSV.**")
    
    st.download_button("Cliquez pour télécharger", csv, "postes.csv","text/csv",key='download-csv')














 
