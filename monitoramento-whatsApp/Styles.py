import streamlit as st

def apply_styles():
    st.markdown(
        """
        <style>
        .title {
            text-align: center;
            font-size: 60px; /* Ajuste o tamanho do título conforme necessário */
            font-weight: bold;
            
        }
        </style>
        """, unsafe_allow_html=True
    )
