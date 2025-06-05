import hashlib
from PyPDF2 import PdfReader
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from key_functions import *
import pandas as pd

def agregar_usr_csv(nombre, clave_pub, modulo, df, filename = 'users_keys.csv'):
    df.loc[len(df)] = [nombre, clave_pub, modulo]
    df.to_csv(filename, index = False)

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def extract_key_from_df(nombre, df):
    # Buscar la fila correspondiente al usuario
    row = df[df['nombre'] == nombre]

    if row.empty:
        raise ValueError(f"No se encontró al usuario '{nombre}' en el DataFrame")

    e = int(row.iloc[0]['llave_publica'])  # Asegurarse que esté en formato int
    n = int(row.iloc[0]['modulo'])

    # Reconstruir clave pública
    public_numbers = rsa.RSAPublicNumbers(e, n)
    clave_publica = public_numbers.public_key(backend=default_backend())

    return clave_publica


def extraer_texto_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

def generar_hash(texto):
    sha256 = hashlib.sha256()
    sha256.update(texto.encode('utf-8'))
    return int.from_bytes(sha256.digest(), byteorder='big')

def firmar_hash(hash_int, clave_privada):
    private_numbers = clave_privada.private_numbers()
    d = private_numbers.d
    n = private_numbers.public_numbers.n
    return pow(hash_int, d, n)

def verificar_firma(firma, hash_original, clave_publica):
    public_numbers = clave_publica.public_numbers()
    e = public_numbers.e
    n = public_numbers.n
    hash_verificado = pow(firma, e, n)
    return hash_verificado == hash_original

def interfaz_streamlit():
    st.title("🔐 Firma y Verificación de PDFs con RSA")

    st.markdown("## 1. 🔄 Generar nuevas llaves (opcional)")
    if st.button("Generar par de llaves"):
        private_pem, public_pem = generar_llaves()
        st.download_button("⬇️ Descargar clave privada", private_pem, file_name="clave_privada.pem")
        st.download_button("⬇️ Descargar clave pública", public_pem, file_name="clave_publica.pem")
        st.success("¡Llaves generadas con éxito!")

    st.markdown("## 2. 🔑 Sube tus llaves")

    clave_privada_file = st.file_uploader("📤 Sube tu **clave privada** (.pem)", type=["pem"])
    clave_publica_file = st.file_uploader("📤 Sube tu **clave pública** (.pem)", type=["pem"])

    private_key = cargar_llave_privada(clave_privada_file) if clave_privada_file else None
    public_key = cargar_llave_publica(clave_publica_file) if clave_publica_file else None

    if private_key and public_key:
        st.success("✔ Llaves cargadas correctamente.")

        st.markdown("## 3. 📄 Sube un PDF para firmar/verificar")
        uploaded_pdf = st.file_uploader("PDF a firmar/verificar", type="pdf")

        if uploaded_pdf:
            texto = extraer_texto_pdf(uploaded_pdf)
            st.text_area("📝 Texto extraído del PDF:", texto, height=200)

            hash_pdf = generar_hash(texto)
            st.write("🔢 Hash SHA-256 generado:", hash_pdf)

            if st.button("✍️ Firmar PDF"):
                firma = firmar_hash(hash_pdf, private_key)
                st.code(f"Firma generada: {firma}", language="python")
                st.session_state['firma'] = firma
                st.session_state['hash'] = hash_pdf

            if 'firma' in st.session_state and st.button("✅ Verificar firma"):
                es_valida = verificar_firma(st.session_state['firma'], st.session_state['hash'], public_key)
                if es_valida:
                    st.success("✔ Firma válida")
                else:
                    st.error("❌ Firma inválida")
    else:
        st.info("Para continuar, por favor sube ambas llaves.")

if __name__ == '__main__':
    interfaz_streamlit()
