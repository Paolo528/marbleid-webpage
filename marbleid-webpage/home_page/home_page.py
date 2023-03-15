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
# def add_bg_from_url():
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://raw.githubusercontent.com/Paolo528/marbleid-webpage/master/images/marble_background.jpg");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

#add_bg_from_url()

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

groups_sites = ['Carrara', 'Pentelikon', 'Paros', 'Dokimeion', 'Herakleia', 'Miletos', 'Prokonnesos', 'Thasos', 'Aphrodisias']

groups_sites_dict = {'Carrara': "Carrara or Luni as it was called in the Roman times is a marble district located Apuan Alps in the northwestern part of the Italian peninsula; it is a region renowned for its white marble used for high quality sculpture and for the public architecture of the city of Rome. Thequarrying district includes four large areas (Ital. bacini): Pescina-Boccanaglia, Torano, Miseglia and Colonnata that were exploited continuously from Antiquity to the present days. Lunensian marble is a particularly fine-grained white marble with a high proportion of accessory minerals (quartz, mica, dolomite), which leads to the comparatively frequent occurrence of banding.",
                     'Pentelikon': "The quarrying district Mount Pentelikon is located about 14 km northeast of Athens. Its exploitation probably began in 6th c. B.C., reached a peak in Classical period (5th c. BC), when the material was used for Pericles’ building program of the Athenian Acropolis, and continued throughout the Roman imperial period. The quality marble was exhausted already in late antiquity. The pentelic marble is fine-grained and of milk-white color with a tinge of yellow. Frequently occurring elongated mica layers and the high iron content are the main macroscopic characteristic for this marble. The iron content is responsible for the fact that the marble gets a golden brown patina during weathering.",
                     'Paros': "Paros. The extraction area is located in the center of the Cycladic Island of Paros and extends on the northeastern slope of Mount Marpissa in the plains of Marathi and Chorodaki. The most renowned variety of Parian marble, the lychnites (Paros Marathi Lychnites) was quarried in the valley of Marathi in underground pits (Grotto of the Nymphs and Pan). In antiquity several varieties of marble generically called Paria lithos were extracted. The lychnites variety (Paros Marathi Lichnytes) is a pure white translucent marble of a medium grain size. The Paros Chorodaki and Paros Marathi varieties – which can only be distinguished by their geologic features (isotopic values) exhibit a coarser grain size and a more grayish color.",
                     'Dokimeion': "Dokimion The ancient quarrying district is situated 23 km northeast of the Turkish city Afyon near the ancient city Dokimion (mod. Iscehisar) in central Anatolia, in the historical landscape of Phrygia. Archaeological research has identified several quarrying areas that has divided it into two large mining areas according to the main mining period: a 'Latin' one with seven quarries (I-VII)139 , which were mainly operated in the imperial period, and a 'Greek' one with eight quarries (A-H), which show mining traces from late antiquity and Byzantine times. A central role within the Latin quarries is played by Quarry I (also called Bacakale), from which the largest quantity of Latin quarry inscriptions - from the Trajanic to the Severanperiod - originates. They testify that the quarries of that time were under imperial administration.",
                     'Herakleia': "Herakleia The extraction area is located in the immediate vicinity of the town of Herakleia on Latmos, on a ridge of the Latmos massif on the eastern shore of Lake Bafa.",
                     'Miletos': "The quarries of Miletos are located in the proximity of the ancient homonymous Ionian city on the south shores of the ancient Latmian Golf, now the Bafa Lake in the western part of Turkey. They provide a white-grey marble variety used primarily on a local level.",
                     'Prokonnesos': "Prokonnesos. The Proconnesian marble is extracted on the Marmara Adas (Turkey); the quarrying area covers about 40 km2 of the northern half of the island. Prokonnesos was one ofthe most popular marble used for architecture in the Roman Imperial period. This material is a coarse-grained, white-gray marble. It is recognizable by the parallel dark gray banding (striations) and by the strong sulfur odor that develops when the crystals are ground.",
                     'Thasos': "Thasos. The Thasian marble was quarried on the island of the same name in the North Aegean. The marble deposit consists of two types of marble with different chemical composition, a dolomite marble in the north of the island and a calcitic one in its southern part. The extraction districts extend along the east coast of the island: in the north at Cape Phanari(I-V), Saliari and Cape Vathy are the quarrying areas of dolomite marble, in the south at Cape Babouras and Aliki those of calcite marble.",
                     'Aphrodisias': "Aphrodisias. The ancient district in located in the proximity of the homonymous Carian city of Aphrodisias in Anatolia (nowadays Turkey). The city was renowned in Antiquity for its artists that were active in Rome and different centers of the ancient world. "
                     }

locations_sites_dict = {
'Carrara': {'lat': 44.031458, 'lon': 10.033776},
'Miletos': {'lat': 37.314884, 'lon': 27.164213},
'Pentelikon': {'lat': 38.026000, 'lon': 23.2001},
'Herakleia': {'lat': 37.5028, 'lon': 27.5264},
'Aphrodisias': {'lat': 37.423227, 'lon': 28.432040},
'Dokimeion': {'lat': 38.7569, 'lon': 30.5387},
'Thasos': {'lat': 40.6845, 'lon': 24.6484},
'Paros': {'lat': 37.0854, 'lon': 25.1515},
'Prokonnesos': {'lat': 40.591686, 'lon': 27.55568}
}

latitudes_dict = [44.031458, 38.026000, 37.0854, 38.7569, 37.5028, 37.314884, 40.591686, 40.6845, 37.423227]
longitudes_dict = [10.033776, 23.2001, 25.1515, 30.5387, 27.5264, 27.164213, 27.55568, 24.6484, 28.432040]

locations_dict = {'Aphrodisias I': {'lat': 37.725556, 'lon': 28.741667}, 'Aphrodisias II': {'lat': 37.725556, 'lon': 28.741667}, 'Carrara': {'lat': 44.092500, 'lon': 10.126667}, 'Dokimeion': {'lat': 38.837222, 'lon': 30.783889}, 'Herakleia': {'lat':37.472222, 'lon': 27.490000}, 'Miletos': {'lat': 38.0914428, 'lon': 25.8589538}, 'Paros (Chorodaki)': {'lat': 37.082500, 'lon': 25.200278}, 'Paros (Lychnites)': {'lat': 37.082500, 'lon': 25.200278}, 'Paros (Marathi)': {'lat': 37.082500, 'lon': 25.200278}, 'Penteli': {'lat': 38.073889, 'lon': 23.881944}, 'Prokonnesos': {'lat': 40.6214922, 'lon': 27.4940853}, 'Prokonnesos III': {'lat': 40.6214922, 'lon': 27.4940853}, 'Thasos Aliki': {'lat': 40.603056, 'lon': 24.741667}}

locations_dict_all = {"Marble-Site": groups_sites, "lat": latitudes_dict, "lon": longitudes_dict}

groups_sites_dict = {
'Aphrodisias I': 'Aphrodisias',
'Aphrodisias II': 'Aphrodisias',
'Carrara': 'Carrara',
'Dokimeion': 'Dokimeion',
'Herakleia': 'Herakleia',
'Miletos': 'Miletos',
'Paros (Chorodaki)': 'Paros',
'Paros (Lychnites)': 'Paros',
'Paros (Marathi)': 'Paros',
'Pentelikon': 'Pentelikon',
'Prokonnesos': 'Prokonnesos',
'Prokonnesos III': 'Prokonnesos',
'Thasos Aliki': 'Thasos'
}
#Introduction about MarbleID
if selected == "About MarbleID":
    st.subheader("What is MarbleID?")

    st.subheader("General description:")
    st.write("Like no other material, marble, especially in its white variety, has significantly shaped the appearance of ancient art and architecture, so that modern references to the materiality of this historical period often speak of a marble-white antiquity. Materiality is therefore a relevant factor for understanding ancient societies in their complexity, for interpreting cultural interactions and art movements, but also for tracing economic contexts. Beyond its specific relevance for archaeological or art historical research, the materiality of ancient art has another practical application in the field of art provenance and authenticity, i.e., it is of importance for art managing institutions or private entrepreneurs active in the art trade.")

    st.subheader("The motivation.")
    st.write("The project is intended as a long-term scientific approach to investigate the provenance of white marble and decorative stones used in Antiquity, by focusing on the main, interregional active quarry districts of the Mediterranean. Its primary goal is to determine the marble origin of art works, by assigning them to one of the predefined ancient quarry districts.")

    st.subheader("Project description:")
    st.write("MarbleID is a ML-based tool for classifying lithic material based on its geologic conditioned features. Depending on the chromatics of the material two different approaches can be distinguished:")
    st.write("an image-based recognition for the colored stones and a statistical analysis of the geologic features expressed as numerical values in the case of the white marbles.")
    st.write("The first phase of the project focused on white marble resources from the main ancient districts of the Mediterranean and used a set of 25 numerical parameters for their classification. Despite their relative high number, the parameters required for the analysis result from three different standard laboratory measurements (stabile isotopes, trace elements by ICP MS and micro-inclusions). Supervised learning and an SCV kernel were used to train a model performing classification with 85% accuracy.The application: Our interface offers the possibility to upload a file including the numerical parameters necessary for the model to perform the classification and offers a prediction regarding the origin of the marble of object of interest. ")

#-----------------------------------MAP--------------------------------------
    #map all
    location_df_all = pd.DataFrame(locations_dict_all)
    #location_df_all = location_df_all.set_index("marble_groups")
    #st.map(location_df_all, zoom=None, use_container_width=True)

    fig = px.scatter_geo(location_df_all, lat=locations_dict_all["lat"], lon=locations_dict_all["lon"],
                     #color="continent", # which column to use to set the color of markers
                     hover_name="Marble-Site"
                     ) # column added to hover information
                     #size="pop", # size of markers
                     #projection="natural earth")
    st.plotly_chart(fig, use_container_width=True)




#-----------------------------------MAP--------------------------------------

#setup file upload
if selected == "Upload File":
    #st.subheader("?header?")
    #st.write("info")
    with st.expander("expand to upload your file"):
        uploaded_file = st.file_uploader(
            label="Upload your CSV or Excel file.",
                                             type=["csv", "xlsx", "xls"],
                                             accept_multiple_files=False
                                             )

    if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            time.sleep(5)


        url = "https://prod-ql7u7a2o3q-ew.a.run.app//uploaded_file"
        response=requests.post(url, files={"file": uploaded_file})



        #getting the prediction

        url = "https://prod-ql7u7a2o3q-ew.a.run.app/data"
        response = requests.get(url).text
        json_data = json.loads(response)
        site1 = pd.DataFrame(json_data, index=[0])
        site2 = site1.iloc[0]["prediction"]

        for i in groups:
            if site2 == i:
                site = groups_sites_dict[i]


        #show results
        if response is not None:
             st.success("Sample analysed successfully!")
             if st.button("see results"):

                # for loop for getting correct site displayed
                #groups = ['Aphrodisias I', 'Aphrodisias II', 'Carrara', 'Dokimeion', 'Herakleia', 'Miletos', 'Paros (Chorodaki)', 'Paros (Lychnites)', 'Paros (Marathi)', 'Penteli', 'Prokonnesos', 'Prokonnesos III', 'Thasos Aliki']
                #aphrodisias 1 is also aphrodisias 2


                locations_df = pd.DataFrame(locations_sites_dict[site], index=[0])

                for i in groups_sites:
                    if site == i:
                        text_group = groups_sites_dict[i]


                #Site
                st.subheader(f"Result of the analysis: {site}")


                #map the site
                st.map(locations_df, zoom=None, use_container_width=True)

#more sites page
if selected == "more sites":
    st.subheader("About what ite do you want to learn more about?")
    #what site
    option = st.selectbox("Select",
        ('Carrara', 'Pentelikon', 'Paros', 'Dokimeion', 'Herakleia', 'Miletos', 'Prokonnesos', 'Thasos', 'Aphrodisias'))

    #select bar group
    if option:
        for i in groups_sites:
            if option == i:
                text_group = groups_sites_dict[i]

    #about the group
    st.subheader(f"About {option}")
    st.write(text_group)



    #maybe for more picture or catalogue
    st.subheader(f"Location of {option}")
    locations_df = pd.DataFrame(locations_sites_dict[option], index=[0])
    st.map(locations_df, zoom=None, use_container_width=True)
