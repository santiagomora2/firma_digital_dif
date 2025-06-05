import streamlit as st
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generar_llaves():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem, public_key

def cargar_llave_privada(uploaded_file):
    try:
        return serialization.load_pem_private_key(
            uploaded_file.read(),
            password=None,
            backend=default_backend()
        )
    except Exception as e:
        st.error("⚠️ Error al cargar la clave privada: " + str(e))
        return None

def cargar_llave_publica(uploaded_file):
    try:
        return serialization.load_pem_public_key(
            uploaded_file.read(),
            backend=default_backend()
        )
    except Exception as e:
        st.error("⚠️ Error al cargar la clave pública: " + str(e))
        return None
