import os
import re
from pathlib import Path
import streamlit as st
from form_handler import FormHandler

PROJECTS_PATH = "projets"

st.markdown("""
<style>
div[data-testid="stDialog"] div[role="dialog"] {
    width: 90vw;
    max-width: 90vw;
}
</style>
""", unsafe_allow_html=True)

def display_file_tree(relative_path):
    """Affiche le 1er niveau de l'arborescence fichiers dans la barre latérale."""
    path = os.path.join(os.getcwd(), relative_path)
    
    if not os.path.exists(path):
        st.sidebar.error(f"Le chemin suivant n'existe pas: {path}")
        return

    items = sorted(os.listdir(path))

    for item in items:
        icon = "📂"
        st.sidebar.markdown(f"{icon} {item}")

@st.dialog(title="Aperçu")
def display_markdown_file(file_path):

    def is_remote_image(image_path):
        return image_path.startswith("http://") or image_path.startswith("https://")

    with open(file_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Regex to find markdown image syntax ![alt text](image_path)
    pattern = r'!\[.*?\]\((.*?)\)'
    image_paths = re.findall(pattern, markdown_content)
    
    # Display text content while replacing local image markdown with Streamlit images
    text_blocks = re.split(pattern, markdown_content)
    
    for i, text_block in enumerate(text_blocks):
        st.markdown(text_block)  # Display the markdown text block
        if i < len(image_paths):
            # Display corresponding image if the path exists
            image_path = image_paths[i]
            if is_remote_image(image_path):
                st.image(image_path)
            else:
                local_image_path = Path(image_path)
                if local_image_path.exists():
                    st.image(image_path)  # Display the local image
                else:
                    st.warning(f"Image not found: {image_paths[i]}")

def main():
    st.title("Nom de l'outil")
    
    # Display file tree in the sidebar
    st.sidebar.header("Liste des projets")
    display_file_tree(PROJECTS_PATH)
    
    # Initialize form handler
    form_handler = FormHandler()
    
    # Initialize session state for folder selection if not exists
    if 'file_path' not in st.session_state:
        st.session_state.file_path = None
    
    # Create a form
    with st.form(key='my_form'):
        source = st.selectbox(
            'Type de source',
            options=['github', 'local'],
            key='source'
        )       
        
        text_input = st.text_input(
            'Saisie des informations',
            key='text_input'
        )
        
        submit_button = st.form_submit_button(label='Envoyer')

        if submit_button:
            with st.spinner("Traitement en cours..."):
                result = form_handler.handle_submission(
                    source, 
                    text_input
                )
                
            if result.success:
                st.success(result.message)

                st.session_state.download_file_ready = True

                st.session_state.zip_path = result.data["zip_path"]
                st.session_state.zip_name = result.data["zip_name"]
                st.session_state.file_path = result.data["file_path"]

            else:
                st.error(result.message)

    if 'download_file_ready' in st.session_state and st.session_state.download_file_ready:
        col1,col2 = st.columns(2)
        with col1:
            with open(st.session_state.zip_path, "rb") as f:
                st.download_button(
                    label="Télécharger le dossier (Zip)",
                    data=f,
                    file_name=st.session_state.zip_name,
                    mime="application/zip"
                )

        with col2:
            if st.button("Afficher le contenu"):
                display_markdown_file(st.session_state.file_path)
        
            
if __name__ == "__main__":
    main()
