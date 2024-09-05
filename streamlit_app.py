import streamlit as st

pg = st.navigation([
    st.Page(lab1, title = "Lab 1"),
    st.Page(lab2, title = "Lab 2")
], position = "top")


pg.run()
