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
    st.header('Generación de Llaves')

    # Inicializar la variable de sesión solo si no existe
    if 'authenticaded_admin' not in st.session_state:
        st.session_state['authenticaded_admin'] = False

    if st.session_state['authenticaded_admin']:

        df = pd.read_csv('users_keys.csv')

        # ------- Empieza sidebar --------
        with st.sidebar:
            st.page_link("main.py", label="Regresar a Inicio", icon="🏠")
        # ------- Termina sidebar --------

        st.markdown("## 🔄 Generar nuevas llaves ")

        usuario_llaves = st.text_input('Nombre del funcionario que recibirá las llaves:')

        if usuario_llaves:
            if st.button("Generar par de llaves"):
                private_pem, public_pem, public_key = generar_llaves()
                st.download_button("⬇️ Descargar clave privada", private_pem, file_name="clave_privada_" + usuario_llaves.lower() + ".pem")
                st.success("¡Llaves generadas con éxito!")

                public_numbers = public_key.public_numbers()
                e = str(public_numbers.e)
                n = str(public_numbers.n)

                agregar_usr_csv(usuario_llaves, e, n, df, filename='users_keys.csv')

    else:
        pass_try = st.text_input('Ingresa la contraseña de administrador', type='password')

        if st.button('Ingresar'):
            if pass_try == 'password':
                st.session_state['authenticaded_admin'] = True
            else:
                st.error('Contraseña incorrecta. Por favor inténtelo de nuevo.')

if __name__ == '__main__':
    main()