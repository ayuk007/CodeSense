import streamlit as st
from src.chain import Chain

chain = Chain()
st.set_page_config(page_title = "CodeSense")

st.header("CodeSense: Your code analyst!!..")
st.subheader("Root path of project")
root_dir = st.text_input("Path")
if root_dir:
    final_output = chain.process(root_dir)
    st.components.v1.html(final_output, height = 600, scrolling = True)