import streamlit as st
import requests
import pandas as pd
from streamlit_option_menu import option_menu
import json
from fastapi import File, UploadFile
import webbrowser
import time
import plotly.express as px


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
    options=["About MarbleID", "Upload File", "more sites"],
    icons=[],
    orientation="horizontal")

# for loop for getting correct site displayed
groups = ['Aphrodisias I', 'Aphrodisias II', 'Carrara', 'Dokimeion', 'Herakleia', 'Miletos', 'Paros (Chorodaki)', 'Paros (Lychnites)', 'Paros (Marathi)', 'Penteli', 'Prokonnesos', 'Prokonnesos III', 'Thasos Aliki']

groups_dict = {'Aphrodisias I': 'bla1', 'Aphrodisias II': 'bla1', 'Carrara': 'bla3', 'Dokimeion': 'bla4', 'Herakleia': 'bla5', 'Miletos': 'bla6', 'Paros (Chorodaki)': 'bla7', 'Paros (Lychnites)': 'bla8', 'Paros (Marathi)': 'bla9', 'Penteli': 'bla10', 'Prokonnesos': 'bla11', 'Prokonnesos III': 'bla12', 'Thasos Aliki': 'bla13'}

locations_dict = {'Aphrodisias I': {'lat': 37.725556, 'lon': 28.741667}, 'Aphrodisias II': {'lat': 37.725556, 'lon': 28.741667}, 'Carrara': {'lat': 44.092500, 'lon': 10.126667}, 'Dokimeion': {'lat': 38.837222, 'lon': 30.783889}, 'Herakleia': {'lat':37.472222, 'lon': 27.490000}, 'Miletos': {'lat': 38.0914428, 'lon': 25.8589538}, 'Paros (Chorodaki)': {'lat': 37.082500, 'lon': 25.200278}, 'Paros (Lychnites)': {'lat': 37.082500, 'lon': 25.200278}, 'Paros (Marathi)': {'lat': 37.082500, 'lon': 25.200278}, 'Penteli': {'lat': 38.073889, 'lon': 23.881944}, 'Prokonnesos': {'lat': 40.6214922, 'lon': 27.4940853}, 'Prokonnesos III': {'lat': 40.6214922, 'lon': 27.4940853}, 'Thasos Aliki': {'lat': 40.603056, 'lon': 24.741667}}

locations_dict_all = {"marble_groups": groups, "lat": [37.725556, 37.725556, 44.092500, 38.837222, 37.472222, 38.0914428, 37.082500, 37.082500, 37.082500, 38.073889, 40.6214922, 40.6214922, 40.603056], "lon": [28.741667, 28.741667, 10.126667, 30.783889, 27.49000, 25.8589538, 25.200278, 25.200278, 25.200278, 23.881944, 27.4940853, 27.4940853, 24.741667]}
#Introduction about MarbleID
if selected == "About MarbleID":
    st.subheader("What does MarbleID do???")
    st.write("blablabla")
#-----------------------------------MAP--------------------------------------
    #map all
    location_df_all = pd.DataFrame(locations_dict_all)
    #location_df_all = location_df_all.set_index("marble_groups")
    #st.map(location_df_all, zoom=None, use_container_width=True)

    # compute the center of the map as the average latitude and longitude
    center_lat = location_df_all['lat'].mean()
    center_lon = location_df_all['lon'].mean()

    fig = px.scatter_geo(location_df_all, lat="lat", lon="lon",
                     #color="continent", # which column to use to set the color of markers
                     hover_name="marble_groups",
                     center={'lat': center_lat, 'lon': center_lon}
                     ) # column added to hover information
                     #size="pop", # size of markers
                     #projection="natural earth")
    st.plotly_chart(fig, zoom=7, use_container_width=True)




#-----------------------------------MAP--------------------------------------

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


        url = "https://prod-ql7u7a2o3q-ew.a.run.app/uploaded_file"
        response=requests.post(url, files={"file": uploaded_file})



        #getting the prediction

        url = "https://prod-ql7u7a2o3q-ew.a.run.app/data"
        response = requests.get(url).text
        site1 = json.loads(response)
        site = site1["prediction"]

        #show results
        if response is not None:
             st.success("Sample analysed successfully!")
             if st.button("see results"):

                # for loop for getting correct site displayed
                #groups = ['Aphrodisias I', 'Aphrodisias II', 'Carrara', 'Dokimeion', 'Herakleia', 'Miletos', 'Paros (Chorodaki)', 'Paros (Lychnites)', 'Paros (Marathi)', 'Penteli', 'Prokonnesos', 'Prokonnesos III', 'Thasos Aliki']
                #aphrodisias 1 is also aphrodisias 2


                locations_df = pd.DataFrame(locations_dict[site], index=[0])

                for i in groups:
                    if site == i:
                        text_group = groups_dict[i]


                #Site
                st.subheader(f"{site}")


                #map the site
                st.map(locations_df, zoom=None, use_container_width=True)

#more sites page
if selected == "more sites":
    #what site
    option = st.selectbox(
        'Of what site do you want to learn more?',
        ('Aphrodisias I', 'Aphrodisias II', 'Carrara', 'Dokimeion', 'Herakleia', 'Miletos', 'Paros (Chorodaki)', 'Paros (Lychnites)', 'Paros (Marathi)', 'Penteli', 'Prokonnesos', 'Prokonnesos III', 'Thasos Aliki'))

    #select bar group
    if option:
        for i in groups:
            if option == i:
                text_group = groups_dict[i]

    #about the group
    st.subheader(f"About {option}")
    st.write(text_group)



    #maybe for more picture or catalogue
    with st.expander("See map"):
        locations_df = pd.DataFrame(locations_dict[option], index=[0])
        st.map(locations_df, zoom=None, use_container_width=True)



        # #response to api if uploaded file arrived
        # if response is not None:
        #     json_data={"page_status": "allowed"}
        #     url = "http://127.0.0.1:8000/reverse_c"
        #     response = requests.post(url, json=json_data)
