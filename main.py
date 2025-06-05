import streamlit as st
import streamlit.components.v1 as components

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

    # Custom HTML with inline styling
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <style>
            /* Full-screen animated background */
            body {
                background-image: url('https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmE0djE4Z3F0YngyN2ZwZW15YTU2emtoMm83Z3c5MTBmNGU2bWEyMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ohONS2y8GTDoI/giphy.gif');
                background-size: cover;
                background-attachment: fixed;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }

            /* Container for the title and divider */
            .container {
                position: relative;
                text-align: center;
                color: white;
                max-width: 1000px;
                width: 100%;
            }

            /* Horizontal divider line */
            .line {
                border-top: 2px solid white;
                width: 80%; /* Adjust width as needed */
                margin: 20px auto; /* Adds spacing above and below */
            }

            /* Big title text on top */
            .big-title {
                font-size: 50px;
                font-weight: bold;
                margin-bottom: 20px; /* Adds spacing below the title */
            }

            /* Small title text below */
            .small-title {
                font-size: 20px;
                margin-top: 20px; /* Adds spacing above the subtitle */
            }

        </style>
    </head>
    <body>
        <div class="container">
            <div class="big-title">DIFacto</div>
            <div class="line"></div>
            <div class="small-title">Firma y autenticación de documentos PDF.</div>
        </div>
    </body>
    </html>

        """

    # Display the custom HTML in Streamlit
    components.html(html_code, height=350)

    cols = st.columns(3)
    with cols[0]:
        st.page_link("pages/dif.py", label="Firmar documentos", icon="✍️")
        st.page_link("pages/dif_admin.py", label="Generar Llaves (ADMIN)", icon="🔐")
    with cols[2]:
        st.page_link("pages/rc.py", label="Verificar documentos", icon="🔍")

if __name__ == '__main__':
    main()