import streamlit as st
import pandas as pd #web scrapping ke lie
import base64
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np 
from PIL import Image



#Now we are creating our web app
st.title("Project3:Basketball data webapp")
st.header(" **Hello Visitors This website will display Basketball team statistics ** Heat map  ")
st.sidebar.header("User Input")
selected_year=st.sidebar.selectbox('Year',list(reversed(range(1950,2021))))

def load_data(year):
    url="https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html=pd.read_html(url,header=0)
    df=html[0]
    raw=df.drop(df[df.Age=='Age'].index)
    raw.fillna(0)
    pic_selected=raw.drop(['Rk'],axis=1)
    return pic_selected
pic_selected=load_data(selected_year)
st.header("THE TABLE FOR THE YEAR IS BELOW")
st.write("""This table will show the content related to your selection
>Tables   Are  """)
pic_selected
sorted_unique_team = sorted(pic_selected.Tm.unique())
selected_team= st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)
unique_pos = ['C','PF','SF','PG','SG']
pos_selected=st.sidebar.multiselect('Team_pos',unique_pos,unique_pos)
#This is filtering data
st.slider('Times',14,25,20)
df_selected_team= pic_selected[(pic_selected.Tm.isin(selected_team)) & (pic_selected.Pos.isin(pos_selected))]

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot()


