import streamlit as st
import os
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
    st.header('Firma de Documentos')

    # ------- Empieza sidebar --------
    with st.sidebar:
        st.page_link("main.py", label="Regresar a Inicio", icon="🏠")

    # ------- Termina sidebar --------

    st.markdown("### 🔑 Sube tus llaves")

    clave_privada_file = st.file_uploader("📤 Sube tu **clave privada** (.pem)", type=["pem"])

    private_key = cargar_llave_privada(clave_privada_file) if clave_privada_file else None

    if private_key:
        st.success("✔ Llave cargadas correctamente.")

        st.markdown("### 📄 Sube un PDF para firmar/verificar")
        uploaded_pdf = st.file_uploader("PDF a firmar/verificar", type="pdf")

        if uploaded_pdf:
            texto = extraer_texto_pdf(uploaded_pdf)
            # st.text_area("📝 Texto extraído del PDF:", texto, height=200)

            hash_pdf = generar_hash(texto)
            # st.write("🔢 Hash SHA-256 generado:", hash_pdf)

            st.success("✔ PDF leído correctamente.")

            if st.button("✍️ Firmar PDF"):
                firma = firmar_hash(hash_pdf, private_key)
                st.code(f"Firma generada: {firma}", language="python")
                st.session_state['firma'] = firma
                st.session_state['hash'] = hash_pdf

                num_bytes = (firma.bit_length() + 7) // 8

                firma_bytes = firma.to_bytes(num_bytes, byteorder='big')
                
                filename = os.path.splitext(uploaded_pdf.name)[0]

                # Crear un archivo descargable
                st.download_button(
                    label="⬇️ Descargar firma",
                    data=firma_bytes,
                    file_name="firma_"+filename+".sig",
                    mime="application/octet-stream"
                )

if __name__ == '__main__':
    main()