import streamlit as st
import requests
import json
import pandas as pd
from streamlit_option_menu import option_menu


#Title

st.title("MarbleID")
st.subheader("Analysis results")

#hide Streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

#getting the prediction
url = "http://127.0.0.1:8000/data"
response = requests.get(url).text
site1 = json.loads(response)
site = site1["prediction"]

# for loop for getting correct site displayed
groups = ['Aphrodisias I', 'Aphrodisias II', 'Carrara', 'Dokimeion', 'Herakleia', 'Miletos', 'Paros (Chorodaki)', 'Paros (Lychnites)', 'Paros (Marathi)', 'Penteli', 'Prokonnesos', 'Prokonnesos III', 'Thasos Aliki']
#aphrodisias 1 is also aphrodisias 2
groups_dict = {'Aphrodisias I': 'bla1', 'Aphrodisias II': 'bla1', 'Carrara': 'bla3', 'Dokimeion': 'bla4', 'Herakleia': 'bla5', 'Miletos': 'bla6', 'Paros (Chorodaki)': 'bla7', 'Paros (Lychnites)': 'bla8', 'Paros (Marathi)': 'bla9', 'Penteli': 'bla10', 'Prokonnesos': 'bla11', 'Prokonnesos III': 'bla12', 'Thasos Aliki': 'bla13'}

#pictures_dict = {'Aphrodisias I': 'bla1', 'Aphrodisias II': 'bla1', 'Carrara': 'bla3', 'Dokimeion': 'bla4', 'Herakleia': 'bla5', 'Miletos': 'bla6', 'Paros (Chorodaki)': 'bla7', 'Paros (Lychnites)': 'bla8', 'Paros (Marathi)': 'bla9', 'Penteli': 'bla10', 'Prokonnesos': 'bla11', 'Prokonnesos III': 'bla12', 'Thasos Aliki': 'bla13'}
#SITES:
# LatituteLongitude
# Carrara 44.092500 10.126667
# Miletos546537.6805061999475584145692.119173400569707
# Penteli38.073889 23.881944
# Herakleia37.472222 27.490000
# Aphrodisi
# as
# 37.725556 28.741667
# Dokimion38.837222 30.783889
# Thasos40.603056 24.741667
# Paros37.082500 25.200278
# Prokonnes




locations_dict = {'Aphrodisias I': {'lat': 37.725556, 'lon': 28.741667}, 'Aphrodisias II': {'lat': 37.725556, 'lon': 28.741667}, 'Carrara': {'lat': 44.092500, 'lon': 10.126667}, 'Dokimeion': {'lat': 38.837222, 'lon': 30.783889}, 'Herakleia': {'lat':37.472222, 'lon': 27.490000}, 'Miletos': {'lat': 38.0914428, 'lon': 25.8589538}, 'Paros (Chorodaki)': {'lat': 37.082500, 'lon': 25.200278}, 'Paros (Lychnites)': {'lat': 37.082500, 'lon': 25.200278}, 'Paros (Marathi)': {'lat': 37.082500, 'lon': 25.200278}, 'Penteli': {'lat': 38.073889, 'lon': 23.881944}, 'Prokonnesos': {'lat': 40.6214922, 'lon': 27.4940853}, 'Prokonnesos III': {'lat': 40.6214922, 'lon': 27.4940853}, 'Thasos Aliki': {'lat': 40.603056, 'lon': 24.741667}}


locations_df = pd.DataFrame(locations_dict[site], index=[0])

for i in groups:
    if site == i:
        text_group = groups_dict[i]
        #pictures = pictures_dict[i]

#Site
st.subheader(f"{site}")


#map the site
st.map(locations_df)


#about the site
st.subheader(f"About {site}")
st.write(text_group)

#maybe for more picture or catalogue
with st.expander("Click here for more pictures"):
    st.write("Pictures...")

#response to api if uploaded file arrived
if response is not None:
    json_data={"page_status": "allowed"}
    url = "http://127.0.0.1:8000/reverse_c"
    response = requests.post(url, json=json_data)
