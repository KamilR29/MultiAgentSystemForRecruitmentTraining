import streamlit as st
from pages import recruitment_process_page, analyze_cv_page, main_page

hide_menu_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;} /* Ukrywa domyślną nawigację */
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)


logo_path = "images/logo.png"

# Dodanie logo w pasku bocznym
st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.title("Menu")
page = st.sidebar.selectbox(
    "Select a page",
    ("Home","Analyze CV", "Technical Review")
)

if page == "Home":
    main_page.show()
elif page == "Analyze CV":
    analyze_cv_page.show()
elif page == "Technical Review":
    recruitment_process_page.show()