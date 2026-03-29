import streamlit as st
from conversion import *
import tempfile
import os
from pathlib import Path
from IA.Anthropic_connection import *
from IA.OpenIA_connection import *
from prompt import *

def correction_orthographe_page():
    st.caption("Script pour corriger les fautes d'orthographe")
    st.title("📓 Détection d'annales dans un ronéo")
    st.caption("Importe le fichier, sélectionne les modifications orthographiques voulues, récupère le ronéo corrigé.")

    # ── Étape 1 : Upload du fichiers ───

    st.header("1 · Fichier source")

    col1, col2 = st.columns(2)

    with col1:
        roneo_file = st.file_uploader(
            "Ronéo source",
            type=["docx"],
            help="Le ronéo à corriger"
        )
    if roneo_file:
            
        # SAUVEGARDER LES NOMS DES FICHIERS
        if "roneo_file_name" not in st.session_state:
            st.session_state.roneo_file_name = roneo_file.name
            
        # SAUVEGARDER LE CONTENU DES FICHIERS
        if "roneo_file_bytes" not in st.session_state:
            st.session_state.roneo_file_bytes = roneo_file.getvalue()
        
        # ✅ VÉRIFIER QUE LES DONNÉES SONT EN SESSION
        if "roneo_file_bytes" not in st.session_state or "roneo_file_name" not in st.session_state:
            st.error("⚠️ Fichiers manquants. Recharge la page et réimporte-les.")
            st.session_state.bt_demarrage = False
            st.stop()

        with tempfile.TemporaryDirectory() as tmpdir:
            # ✅ UTILISER LES DONNÉES SAUVEGARDÉES
            roneo_path = os.path.join(tmpdir, st.session_state.roneo_file_name)
            with open(roneo_path, "wb") as f:
                f.write(st.session_state.roneo_file_bytes)
            # --- Transformer le cours docx en cours txt ---
            roneo_txt_path = docx_to_structured_txt(roneo_path, os.path.join(tmpdir, "roneo_txt.txt"))

            with open(roneo_txt_path, "rb") as f:
                data_ = f.read()

            # Bouton de téléchargement
            st.download_button(
                                label="💾 Télécharger le fichier Word TXT intermédiaire (log)",
                                data=data_,
                                file_name=f"roneo_txt.txt",
                                mime="text/plain",
                                use_container_width=True
            )


            # Connection à l'IA
            apikey_openia = st.secrets["API_KEY_OPENAI"]
            apikey_anthropic = st.secrets["API_KEY_ANTHROPIC"]

            st.title("⚙️ Configuration IA")

            # 1. Choix du provider
            provider = st.selectbox(
                "Choisis le type d'IA :",
                ["ChatGPT", "Anthropic (Claude)"]
            )

            # 2. Choix du modèle selon provider
            if provider == "ChatGPT":
                model = st.selectbox(
                    "Choisis le modèle ChatGPT :",
                    [
                            "gpt-5.4",
                            "gpt-5.4-mini",
                            "gpt-5.4-nano",
                            "gpt-5.2",
                            "gpt-5.2-pro",
                            "gpt-5.1",
                            "gpt-5",
                            "gpt-5-mini",
                            "gpt-5-nano",
                            "gpt-4.1",
                            "gpt-4.1-mini",
                            "gpt-4.1-nano"
                    ]
                )
            else:
                model = st.selectbox(
                    "Choisis le modèle Claude :",
                        [
                            "claude-opus-4-6",
                            "claude-opus-4-5",
                            "claude-opus-4-1",
                            "claude-opus-4",
                            "claude-sonnet-4-6",
                            "claude-sonnet-4",
                            "claude-sonnet-3-7",
                            "claude-haiku-4-5",
                            "claude-haiku-3-5",
                            "claude-haiku-3"
                    ]
                )

            pt_choix = st.selectbox(
                        "Sélectionne ton prompt",
                        [
                            "pt1",
                        ]
                    )
            if True:
                # 3. Zone de prompt (modifiable)
                if pt_choix=="pt1":
                    prompt = st.text_area(
                        "Prompt :",
                        value=PROMPT_ORTHO_V1,
                        height=300
                    )
                elif pt_choix=="pt2":
                    prompt = st.text_area(
                        "Prompt :",
                        value=PROMPT_UNIQUE_OKIII,
                        height=300
                    )
                elif pt_choix=="pt3":
                    prompt = st.text_area(
                        "Prompt :",
                        value=PROMPT_V2_ANTI_BRUIT,
                        height=300
                    )


                # PROMPT_V2_ANTI_BRUIT

                # 4. Bouton valider
                if st.button("🚀 Valider"):
                    st.write(f"[{model}]")
                    if provider == "ChatGPT":
                        #Upload file
                        roneo_txt_id = IA_upload_openIA(apikey_openia, roneo_txt_path)

                        #Ask IA
                        reponse_ia = IA_ask_openIA(apikey_openia,prompt,[roneo_txt_id],model)
                    else :
                        #Upload file
                        roneo_txt_id = IA_upload_anthropic(apikey_anthropic, "roneo.txt",roneo_txt_path)

                        #Ask IA
                        reponse_ia = IA_ask_anthropic(apikey_anthropic,prompt,[roneo_txt_id],model)

                    st.success("Configuration validée !")

                    st.write(reponse_ia)

                    #Traitement de la réponse de l'IA :
                    def creation_notion_ls(reponse_ia):
                        notions_ls_var = []
                        for i in reponse_ia.split("\n"):
                            j = i.split('[AN]')
                            if len(j)>1:
                                notion = j[1].split('[/AN]')[0]
                                #Découpe phrase de base/phrase modif
                                b0 = notion.split('[B0]')[1].split('[/B0]')[0].strip()
                                b1 = notion.split('[B1]')[1].split('[/B1]')[0].strip()
                                
                                n_result = [str(b0), str(b1)]
                                if n_result not in notions_ls_var:
                                    notions_ls_var.append(n_result)
                                    
                        return notions_ls_var
                    
                    notion_ls = creation_notion_ls(reponse_ia)
                    st.write(notion_ls)


                    # Stocker les données
                    st.session_state.notion_ls = notion_ls
                    st.session_state.index = 0
                    st.session_state.selection = []
                    st.session_state.ia_done = True  # Flag pour indiquer que l'IA a terminé
                
                # 🔹 SECTION DE TRI (en dehors du bouton Valider)
                
            
    else:
        st.info("Importe le fichier pour démarrer l'analyse.", icon="ℹ️")