import streamlit as st
import pandas as pd
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
# import math
# from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Lab Manager'
)

pages = [
    st.Page(lab3, title="Lab3"),  # Lab 3 is now the default
    st.Page(lab2, title="Lab 2"),  
    st.Page(lab1, title="Lab 1")
]

pg = st.navigation(pages, position="top")

# Run the current page
pg.run()           