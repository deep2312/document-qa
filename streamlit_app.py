import streamlit as st
import pandas as pd
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from lab10 import lab10
# import math
# from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Lab Manager'
)

pages = [
    st.Page(lab3, title="Lab 3"),  # Lab 3 is now the default
    st.Page(lab2, title="Lab 2"),  
    st.Page(lab1, title="Lab 1"),
    st.Page(lab4, title="Lab 4"),
    st.Page(lab5, title="Lab 5"),
    st.Page(lab6, title="Lab 6"),
    st.Page(lab7, title="Lab 7"),
    st.Page(lab8, title="Lab 8"),
    st.Page(lab9, title="Lab 9"),
    st.Page(lab10, title="Lab 10")
]

pg = st.navigation(pages, position="top")

# Run the current page
pg.run()           