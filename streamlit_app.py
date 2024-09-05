import streamlit as st
from lab1 import lab1
from lab2 import lab2

pg = st.navigation([
    st.Pages(lab2, title = "Lab 2"),
    st.Pages(lab1, title = "Lab 1")
])