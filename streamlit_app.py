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
from reportlab.pdfgen import canvas
from io import BytesIO




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





    url = "https://docs.google.com/spreadsheets/d/1lAc6NDecdyt6p_r6KtfYQAZtOUV7hCiMA_6gBZCL868/edit#gid=1274041194"
    
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
    df = conn.read(spreadsheet=url, worksheet="BD_calculos", usecols=list(range(7)))
    
    
    
    
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

    
    
    col1, col2 = st.columns(2)
    col3, col5 = st.columns(2)
    col4 = st.columns(1)[0]
    col6, col7 = st.columns(2)
    col8, col9 = st.columns(2)
    col10, col11, col12 = st.columns(3)
    col13, col14 = st.columns(2)
    col15, col16 = st.columns(2)
    col17, col18 = st.columns(2)
    col19 = st.columns(1)[0]
    col20, col21 = st.columns(2)
    col22, col23 = st.columns(2)
    col24, col25 = st.columns(2)
    col26, col27 = st.columns(2)

 
    

    # Define the order of months
    months_order = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    
    # Group by 'MÊS' and 'EXECUCACAO_ORCAMENTARIA', summing up the 'CUSTO'
    chart_data = filtered_df.groupby(['MÊS', 'EXECUCACAO_ORCAMENTARIA'])['CUSTO'].sum().reset_index()
    
    # Filter only 'EXECUTADO' and 'PLANEJADO'
    chart_data = chart_data[chart_data['EXECUCACAO_ORCAMENTARIA'].isin(['EXECUTADO', 'PLANEJADO'])]
    
    # Reorder the 'MÊS' column based on the defined order
    chart_data['MÊS'] = pd.Categorical(chart_data['MÊS'], categories=months_order, ordered=True)
    
    # Sort the DataFrame by the ordered 'MÊS' column
    chart_data = chart_data.sort_values(by='MÊS')
    
    # Create a line chart using Plotly Express
    fig = px.line(chart_data, x='MÊS', y='CUSTO', color='EXECUCACAO_ORCAMENTARIA',
                  title='Execução vs Planejamento Orçamentário',
                  labels={'CUSTO': 'Total Custo'},
                  height=400)
    
    # Show the chart in col1
    col1.plotly_chart(fig)

    # Calculate the difference between "PLANEJADO" and "EXECUTADO" for each month
    diff_data = filtered_df.pivot_table(index='MÊS', columns='EXECUCACAO_ORCAMENTARIA', values='CUSTO', aggfunc='sum').fillna(0)
    diff_data['DIFERENÇA'] = diff_data['PLANEJADO'] - diff_data['EXECUTADO']
    
    # Reorder the 'MÊS' column based on the defined order
    diff_data = diff_data.reset_index()
    diff_data['MÊS'] = pd.Categorical(diff_data['MÊS'], categories=months_order, ordered=True)
    diff_data = diff_data.sort_values(by='MÊS')
    
    # Create a line chart using Plotly Express
    fig_diff = px.line(diff_data, x='MÊS', y='DIFERENÇA',
                       title='Diferença entre Planejado e Executado',
                       labels={'DIFERENÇA': 'Diferença (PLANEJADO - EXECUTADO)'},
                       height=400)


    
    # Show the chart in col2
    col2.plotly_chart(fig_diff)

    # Calculate the difference between "PLANEJADO" and "EXECUTADO" for each CLASSIFICAÇÃO
    classificacao_diff = filtered_df.groupby('CLASSIFICAÇÃO').agg({'CUSTO': lambda x: x[df['EXECUCACAO_ORCAMENTARIA'] == 'PLANEJADO'].sum() - x[df['EXECUCACAO_ORCAMENTARIA'] == 'EXECUTADO'].sum()}).reset_index()
    classificacao_diff = classificacao_diff.sort_values(by='CUSTO', ascending=False).head(10)
    
    # Create a bar chart using Plotly Express
    fig_classificacao_diff = px.bar(classificacao_diff, x='CLASSIFICAÇÃO', y='CUSTO',
                                    title='Top 10 Diferenças entre Planejado e Executado por Classificação',
                                    labels={'CUSTO': 'Diferença (PLANEJADO - EXECUTADO)'},
                                    height=400)
    
    # Show the chart in col3
    col3.plotly_chart(fig_classificacao_diff)



    # Calculate the difference between "EXECUTADO" and "PLANEJADO" for each CLASSIFICAÇÃO
    classificacao_diff_executado = filtered_df.groupby('CLASSIFICAÇÃO').agg({'CUSTO': lambda x: x[df['EXECUCACAO_ORCAMENTARIA'] == 'EXECUTADO'].sum() - x[df['EXECUCACAO_ORCAMENTARIA'] == 'PLANEJADO'].sum()}).reset_index()
    classificacao_diff_executado = classificacao_diff_executado.sort_values(by='CUSTO', ascending=False).head(16)
    
    # Create a bar chart using Plotly Express
    fig_classificacao_diff_executado = px.bar(classificacao_diff_executado, x='CLASSIFICAÇÃO', y='CUSTO',
                                              title='Top 16 Diferenças entre Executado e Planejado por Classificação',
                                              labels={'CUSTO': 'Diferença (EXECUTADO - PLANEJADO)'},
                                              height=400)
    
    # Show the chart in col4
    col4.plotly_chart(fig_classificacao_diff_executado)



    # Calculate the total difference between "PLANEJADO" and "EXECUTADO"
    saldo_geral = filtered_df.loc[filtered_df['EXECUCACAO_ORCAMENTARIA'] == 'PLANEJADO', 'CUSTO'].sum() - filtered_df.loc[filtered_df['EXECUCACAO_ORCAMENTARIA'] == 'EXECUTADO', 'CUSTO'].sum()
    
    # Format the total difference to display as Brazilian Real currency
    formatted_saldo_geral = "R${:,.2f}".format(saldo_geral)
    
    # Display the "Saldo Geral" in col5
    col5.subheader('💰 Saldo Geral: Planejado x Executado')
    col5.metric(label='', value=formatted_saldo_geral, delta=None)


    # Specify the constant value
    contrato_gestao_value = 33000000 * 12
    
    # Calculate the percentage of "EXECUTADO" relative to the constant value
    porcentagem_gasto_contrato_gestao = (filtered_df.loc[filtered_df['EXECUCACAO_ORCAMENTARIA'] == 'EXECUTADO', 'CUSTO'].sum() / contrato_gestao_value) * 100
    
    # Format the percentage to display with two decimal places
    formatted_porcentagem_gasto_contrato_gestao = "{:.2f}%".format(porcentagem_gasto_contrato_gestao)
    
    # Display the "Porcentagem de Gasto do Contrato de Gestão" in col6
    col6.subheader('Porcentagem de Gasto do Contrato de Gestão 📊')
    col6.metric(label='', value=formatted_porcentagem_gasto_contrato_gestao, delta=None)
    


    
    def generate_pdf():
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
    
        # Add content to the PDF (you can customize this based on your app's content)
        pdf.drawString(100, 800, "PDF Content - Your App Title")
        pdf.drawString(100, 780, "Some additional information...")
    
        # Save the PDF to the buffer
        pdf.save()
        buffer.seek(0)
        return buffer
    
    # Button to trigger PDF generation and download
    if st.button("Download PDF"):
        pdf_buffer = generate_pdf()
        st.download_button(label="Download PDF", data=pdf_buffer, file_name="your_app_report.pdf", mime="application/pdf", key="pdf-download")    

    
    


    
    
    
    
    
    
    # Display the filtered DataFrame
    #st.write("Dados Selecionados:")
    #st.dataframe(filtered_df)



    url2 = "https://docs.google.com/spreadsheets/d/1lAc6NDecdyt6p_r6KtfYQAZtOUV7hCiMA_6gBZCL868/edit#gid=1941536595"
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Specify the sheet name (Sheet2) using the sheet parameter
    df2 = conn.read(spreadsheet=url2, worksheet="Respostas_Organizado", usecols=list(range(15)))
    
    # Display the filtered DataFrame
    st.write("Executado:")
    st.dataframe(df2)
    


    url1 = "https://docs.google.com/spreadsheets/d/1lAc6NDecdyt6p_r6KtfYQAZtOUV7hCiMA_6gBZCL868/edit#gid=1812952933"
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Specify the sheet name (Sheet2) using the sheet parameter
    df1 = conn.read(spreadsheet=url1, worksheet="Planejado", usecols=list(range(15)))
    
    # Display the filtered DataFrame
    st.write("Planejado:")
    st.dataframe(df1)

    # Embedding the external link using an iframe
    #st.markdown("<iframe src='https://chatchris.pythonanywhere.com/' width='100%' height='600'></iframe>", unsafe_allow_html=True)

 

 

