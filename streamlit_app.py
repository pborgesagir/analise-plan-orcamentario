import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
import streamlit_authenticator as stauth 
import pickle
from pathlib import Path




st.set_page_config(
    page_title='Planejamento Orçamentário - GCINFRA',
    layout='wide',
    page_icon='🏗️',
    initial_sidebar_state='auto'
)
#testing authentication
# --- USER AUTHENTICATION ---

names = ["Peter Parker", "Rebecca Miller", "Pedro Borges", "Arthur Pires", "Kaio Razotto", "Vitor Peixoto", "Claudemiro Dourado", "Izabela Lopes", "Fernando Souza", "Michelle Bonfim"]
usernames = ["pparker", "rmiller", "pborges", "arthur.pires", "kaio.razotto", "vitor.peixoto", "claudemiro.dourado", "izabela.lopes", "fernando.souza", "michelle.bonfim"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login de acesso: Planejamento Orçamentário - GCINFRA", "main")

if authentication_status == False:
    st.error("Usuário/senha está incorreto")

if authentication_status == None:
    st.warning("Por favor, insira usuário e senha")

if authentication_status:

#ending authetincation 





    url = "https://docs.google.com/spreadsheets/d/1lAc6NDecdyt6p_r6KtfYQAZtOUV7hCiMA_6gBZCL868/edit#gid=0"
    
    # Centered title using HTML tags
    st.markdown("<h1 style='text-align: center;'>PLANEJAMENTO E ACOMPANHAMENTO ORÇAMENTÁRIO - GCINFRA</h1>", unsafe_allow_html=True)
    
    
    # Adding a centered subtitle with larger font size using HTML
    st.markdown("""
        <div style='text-align: center; font-size: 36px;'>
            <b>SOF - DCOL - GCINFRA</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.sidebar.image('index.png', width=150)
    st.sidebar.title(f"Bem-vindo, {name}")
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, usecols=list(range(7)))
    
    
    
    
    # Define the list of "UNIDADE" values and add "Todos" as an option
    desired_unidade = df["UNIDADE"].unique().tolist()
    desired_unidade.insert(0, "Todos")
    
    unidade = st.sidebar.multiselect("UNIDADE", desired_unidade, default=desired_unidade[0])
    
    # Define the list of "CLASSIFICAÇÃO" values and add "Todos" as an option
    desired_classificacao = df["CLASSIFICAÇÃO"].unique().tolist()
    desired_classificacao.insert(0, "Todos")
    
    # Create a filter for selecting "CLASSIFICAÇÃO"
    classificacao = st.sidebar.multiselect("CLASSIFICAÇÃO", desired_classificacao, default=desired_classificacao[0])
    
    # Define the list of "MÊS" values and add "Todos" as an option
    desired_mes = df["MÊS"].unique().tolist()
    desired_mes.insert(0, "Todos")
    
    # Create a filter for selecting "MÊS"
    mes = st.sidebar.multiselect("MÊS", desired_mes, default=desired_mes[0])
    
    # Filter the DataFrame based on user selections
    filtered_df = df.copy()
    
    if unidade and unidade != ["Todos"]:
        filtered_df = filtered_df[filtered_df["UNIDADE"].isin(unidade)]
    
    if classificacao and classificacao != ["Todos"]:
        filtered_df = filtered_df[filtered_df["CLASSIFICAÇÃO"].isin(classificacao)]
    
    if mes and mes != ["Todos"]:
        filtered_df = filtered_df[filtered_df["MÊS"].isin(mes)]
    
    st.markdown("<br>", unsafe_allow_html=True)
    authenticator.logout("Logout", "sidebar")

    
    
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col10, col11 = st.columns(2)
    col12, col13 = st.columns(2)
    col14, col15 = st.columns(2)
    col16 = st.columns(1)[0]
    col17, col18 = st.columns(2)
    col19, col20 = st.columns(2)
    col21, col22 = st.columns(2)
    col23, col24 = st.columns(2)

 

   
    
    
    
 
    
   
    



    
    
    
    
    
    
    
    
    
    # Display the filtered DataFrame
    st.write("Dados Selecionados:")
    st.dataframe(filtered_df)


    url1 = "https://docs.google.com/spreadsheets/d/1lAc6NDecdyt6p_r6KtfYQAZtOUV7hCiMA_6gBZCL868/edit#gid=1812952933"
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Specify the sheet name (Sheet2) using the sheet parameter
    df1 = conn.read(spreadsheet=url1, worksheet="Planejado", usecols=list(range(15)))
    
    # Display the filtered DataFrame
    st.write("Dados Selecionados2:")
    st.dataframe(df1)


 

