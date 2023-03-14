import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import json
from fastapi import File, UploadFile
import webbrowser
import time





#configuration
st.set_option("deprecation.showfileUploaderEncoding", False)

#Title
st.set_page_config(page_title="MarbleID", layout="wide")

#st.image(image, use_column_width=True)
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://raw.githubusercontent.com/Paolo528/marbleid-webpage/master/images/marble_background.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

st.title("MarbleID")

#hide Streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

#nacvigation menu
selected = option_menu(
    menu_title=None,
    options=["About MarbleID", "Upload File"],
    icons=[],
    orientation="horizontal")

#Introduction about MarbleID
if selected == "About MarbleID":
    with st.container():
        st.subheader("What does MarbleID do???")
        st.write("blablabla")

#setup file upload
if selected == "Upload File":
    st.subheader("?header?")
    st.write("info")
    with st.expander("expand to upload your file"):
        uploaded_file = st.file_uploader(
            label="Upload your CSV or Excel file.",
                                             type=["csv", "xlsx", "xls"],
                                             accept_multiple_files=False
                                             )

    if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            time.sleep(5)


        url = "http://127.0.0.1:8000/uploaded_file"
        response=requests.post(url, files={"file": uploaded_file})

#get result page access
        url = "http://127.0.0.1:8000/reverse_r"
        response=requests.get(url)

        if response is not None:
            st.success("Sample analysed successfully!")
            if st.button("see results"):
                webbrowser.open_new_tab("https://paolo528-marbleid-marbleid-webpageresult-pageresult-page-nk878y.streamlit.app/")
