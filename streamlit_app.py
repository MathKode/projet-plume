import streamlit as st
import tempfile
import os
from pathlib import Path
import docx 
import pymupdf

st.warning(st.secrets["API_KEY_OPENAI"])

# ─────────────────────────────────────────────
# Interface Streamlit
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Détection d'annales",
    page_icon="📄",
    layout="centered"
)

# Créer un bouton pour déclencher l'upload

st.title("📄 Détection d'annales dans un ronéo")
st.caption("Importe tes fichiers, réponds aux questions, récupère le résultat.")

# ── Étape 1 : Upload des fichiers ──────────────────────────────────────────

st.header("1 · Fichiers sources")

col1, col2 = st.columns(2)

with col1:
    roneo_file = st.file_uploader(
        "Ronéo source",
        type=["pdf", "docx"],
        help="Le ronéo dans lequel détecter les annales"
    )

with col2:
    annales_file = st.file_uploader(
        "Fichier annales",
        type=["pdf", "docx"],
        help="Le fichier annales à enrichir / compléter"
    )

# ── Étape 2 : Analyse + questions dynamiques ──────────────────────────────

# Initialiser la variable de session pour le bouton
if "bt_demarrage" not in st.session_state:
    st.session_state.bt_demarrage = False

# Afficher le bouton seulement si les deux fichiers sont chargés
if roneo_file and annales_file:
    #st.divider()
    if st.button("Démarrer le script"):
        st.session_state.bt_demarrage = True
else:
    st.info("⬆️ Importe les deux fichiers pour démarrer l'analyse.", icon="ℹ️")


if st.session_state.bt_demarrage:
    st.caption("Le Script est en cours de fonctionnement, cela peut prendre 2/3min")
    #st.header("2 · Questions")

    # Sauvegarde temporaire des fichiers uploadés
    with tempfile.TemporaryDirectory() as tmpdir:
        roneo_path = os.path.join(tmpdir, roneo_file.name)
        annales_path = os.path.join(tmpdir, annales_file.name)
        with open(roneo_path, "wb") as f:
            f.write(roneo_file.getbuffer())
        with open(annales_path, "wb") as f:
            f.write(annales_file.getbuffer())

        # Lance l'analyse (mise en cache pour éviter de ré-analyser à chaque interaction)
        @st.cache_data(show_spinner="Analyse en cours…")
        
        # --- Transformer le cours docx en cours txt ---
        def remove_espace(txt):
            #supprime les trucs en trop
            t = txt.split('\n')
            r=[]
            for i in t:
                if i!="":
                    r.append(i)
            return "\n".join(r)
        
        def docx_to_txt(source_path,result_name):
            fichier_cours = docx.Document(source_path)
            cours_txt = ""
            for p in fichier_cours.paragraphs:
                cours_txt+="\n" 
                cours_txt += p.text
            for t in fichier_cours.tables:
                for r in t.rows:
                    for cell in r.cells:
                        cours_txt+="\n" 
                        cours_txt += cell.text
            cours_txt = remove_espace(cours_txt)
            #print(cours_txt)
            result_path = os.path.join(tmpdir, result_name)
            with open(result_path, "w", encoding="utf-8") as f2:
                f2.write(cours_txt)
            return result_path

        roneo_txt_path = docx_to_txt(roneo_path,"roneo_txt.txt")
        print(roneo_txt_path)

        # --- Transformer les annales pdf en annales txt ---
        def pdf_to_txt(source_path,result_name):
            doc = pymupdf.open(source_path) # open a document
            txt_annales = ""
            for page in doc: # iterate the document pages
                text = page.get_text() #recupere le text format utf8
                txt_annales += text
            #print(txt_annales)
            result_path = os.path.join(tmpdir, result_name)
            with open(result_path, "w", encoding="utf-8") as f2:
                f2.write(txt_annales)
            return result_path
        
        annales_txt_path = pdf_to_txt(annales_path,"oki")
        print(annales_txt_path)