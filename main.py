"""
Main module for page routing and custom styling in the Streamlit application.

This module sets up custom CSS styles for the sidebar, displays the logo,
and routes to different pages ("Home", "Analyze CV", and "Technical Review")
based on user selection.

Pages imported:
    - recruitment_process_page
    - analyze_cv_page
    - main_page
"""
import streamlit as st
from pages import recruitment_process_page, analyze_cv_page, main_page
# --- Custom Styling ---
hide_menu_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;} /* Ukrywa domyślną nawigację */
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)
# Custom sidebar background styling
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
                background: rgb(108,53,222);
                background: linear-gradient(108deg, rgba(115,68,214,1) 0%, rgba(37,37,38,1) 100%);
        }
    </style>
    """,
    unsafe_allow_html=True
)

logo_path = "images/logo.png"


st.sidebar.image(logo_path, use_container_width=True)
# --- Sidebar Menu ---
st.sidebar.title("Menu")
page = st.sidebar.selectbox(
    "Select a page",
    ("Home","Analyze CV", "Technical Review")
)
# --- Page Routing ---
if page == "Home":
    main_page.show()
elif page == "Analyze CV":
    analyze_cv_page.show()
elif page == "Technical Review":
    recruitment_process_page.show()