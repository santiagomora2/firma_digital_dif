import streamlit as st
from functions import *

# página principal
def main():

    # Esconder menú de streamlit
    st.set_page_config(page_title="Portal DIF-RC")
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # Título
    st.header('Verificación de Firma de Documentos')

    df = pd.read_csv('users_keys.csv')

    # ------- Empieza sidebar --------
    with st.sidebar:
        st.page_link("main.py", label="Regresar a Inicio", icon="🏠")

    # ------- Termina sidebar --------


    st.markdown("### 📄 Sube un PDF para verificar")
    uploaded_pdf = st.file_uploader("PDF a verificar", type="pdf")

    st.markdown("### 📄 Introduce el nombre del funcionario que firmó")

    nombre_firmante = st.text_input('Nombre del funcionario: (Presiona enter para aplicar)')

    if nombre_firmante:

        try:

            public_key = extract_key_from_df(nombre_firmante, df)

        except:
    
            st.error('Funcionario no existe en la base de datos.')

    st.markdown("### 📄 Sube la firma del PDF")

    uploaded_file_signature = st.file_uploader("Sube un archivo .sig", type="sig")

    if uploaded_pdf and uploaded_file_signature is not None and public_key is not None:

        texto = extraer_texto_pdf(uploaded_pdf)
        # st.text_area("📝 Texto extraído del PDF:", texto, height=200)

        hash_pdf = generar_hash(texto)
        # st.write("🔢 Hash SHA-256 generado:", hash_pdf)

        st.success("✔ PDF leído correctamente.")

        firma_bytes = uploaded_file_signature.read()
        firma_cargada = int.from_bytes(firma_bytes, byteorder='big')

        st.success("✔ Llave leída correctamente.")

        st.session_state['firma'] = firma_cargada
        st.session_state['hash'] = hash_pdf


        if st.button("✅ Verificar firma"):

            es_valida = verificar_firma(st.session_state['firma'], st.session_state['hash'], public_key)
            if es_valida:
                st.success("✔ Firma válida")
            else:
                st.error("❌ Firma inválida")

if __name__ == '__main__':
    main()
