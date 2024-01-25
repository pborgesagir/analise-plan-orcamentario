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
    "sales_dashboard", "abcdef", cookie_expiry_days=0.00694)

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
    df = conn.read(spreadsheet=url, usecols=list(range(13)))
    
    def custom_sort(value):
        if isinstance(value, (int, float)):
            return value  # Return numbers as they are for sorting
        else:
            return -np.inf  # Assign -np.inf for non-numeric entries to place them at the end
    
    # Apply custom sorting to the DataFrame
    df['Sort_Values'] = df['VALOR TOTAL DO INVESTIMENTO'].apply(lambda x: custom_sort(x))
    df = df.sort_values(by='Sort_Values', ascending=False).drop(columns='Sort_Values')
    
    
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

 

   
    
    
    
    
    
    # Convert 'VALOR TOTAL DO INVESTIMENTO' column to numeric values, ignoring non-numeric values
    filtered_df['VALOR TOTAL DO INVESTIMENTO'] = pd.to_numeric(filtered_df['VALOR TOTAL DO INVESTIMENTO'], errors='coerce')
    
    # Filter out NaN (non-numeric) values
    numeric_values = filtered_df['VALOR TOTAL DO INVESTIMENTO'].dropna()
    
    # Calculate the sum of the numeric values in the "VALOR TOTAL DO INVESTIMENTO" column
    sum_valor_total = numeric_values.sum()
    
    # Format the sum to display as Brazilian Real currency
    formatted_sum = "R${:,.2f}".format(sum_valor_total)
    
    # Display the sum of "VALOR TOTAL DO INVESTIMENTO" with a border
    col2.markdown("""
        <div style='border: 2px solid #1f77b4; border-radius: 5px; padding: 10px;'>
            <h3 style='text-align: center;'>Valor Prospectado 💰</h3>
            <div style='display: flex; justify-content: center;'>
                <h2 style='color: #1f77b4;'>{}</h2>
            </div>
        </div>
    """.format(formatted_sum), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    
    # Count the number of rows in the "UNIDADE" column
    num_pedidos = filtered_df["UNIDADE"].count()
    
    # Display the number of rows in a centered metric display in col2 with a centered subheader
    col6.markdown("<h3 style='text-align: center;'>Número de Pedidos 📊</h3>", unsafe_allow_html=True)
    col6.markdown("<div style='display: flex; justify-content: center;'>"
                  "<h2 style='color: #1f77b4;'>{}</h2></div>".format(num_pedidos), unsafe_allow_html=True)
    
    # Sum the values in the "QUANTITATIVO SOLICITADO" column
    total_quantidade_solicitada = int(filtered_df["QUANTITATIVO SOLICITADO"].sum())
    
    # Display the total quantity in a centered metric display in col3 with a subheader
    col4.markdown("<h3 style='text-align: center;'>Qtd de Equipamentos 🔬</h3>", unsafe_allow_html=True)
    col4.markdown("<div style='display: flex; justify-content: center;'>"
                  "<h2 style='color: #1f77b4;'>{}</h2></div>".format(total_quantidade_solicitada), unsafe_allow_html=True)
    
    
    
    
    # Calculate the average value
    avg_value = sum_valor_total / num_pedidos
    
    # Format the average value to display as Brazilian Real currency
    formatted_avg = "R${:,.2f}".format(avg_value)
    
    # Display the average value in a metric display in col4 with a subheader and emoji
    col9.subheader('Média por Pedido ➗')
    col9.metric(label='', value=formatted_avg, delta=None)
    
    
    
    # Define a color map for the "NÍVEL DE PRIORIDADE" categories
    color_map = {
        "NÃO URGENTE": "blue",
        "POUCO URGENTE": "lightblue",
        "URGENTE": "lightcoral",
        "EMERGÊNCIA": "red"
    }
    
    #def styled_title(title):
        #return f"<div style='text-align: center; font-size: 36px; font-weight: bold;'>{title}</div>"
    
    
    # Create a bar chart using Plotly Express with the specified color order
    fig = px.bar(filtered_df, x="UNIDADE", color="NÍVEL DE PRIORIDADE", title="Quantidade por UNIDADE e NÍVEL DE PRIORIDADE",
                 color_discrete_map=color_map)
    
    # Specify the order of bars in descending order based on the total quantity within each "UNIDADE"
    fig.update_layout(barmode='stack', xaxis_categoryorder='total descending')
    
    # Display the bar chart in col8
    col14.plotly_chart(fig)
    
    
    # Create a bar chart using Plotly Express for Quantity by UNIDADE and CLASSIFICAÇÃO
    fig2 = px.bar(filtered_df, x="UNIDADE", color="CLASSIFICAÇÃO", title="Quantidade por UNIDADE e CLASSIFICAÇÃO")
    
    # Specify the order of bars in descending order based on the total quantity within each "UNIDADE"
    fig2.update_layout(barmode='stack', xaxis_categoryorder='total descending')
    
    # Display the bar chart in col6
    col17.plotly_chart(fig2)
    
    
    # Create a bar chart using Plotly Express for Quantity by UNIDADE and FAIXA DE VALOR
    fig3 = px.bar(filtered_df, x="UNIDADE", color="FAIXA DE VALOR", title="Quantidade por UNIDADE e FAIXA DE VALOR")
    
    # Specify the order of bars in descending order based on the total quantity within each "UNIDADE"
    fig3.update_layout(barmode='stack', xaxis_categoryorder='total descending')
    
    # Display the bar chart in col7
    col18.plotly_chart(fig3)
    
    
    
    
    
    
    # Group by CLASSIFICAÇÃO and calculate the sum of "VALOR TOTAL DO INVESTIMENTO"
    investment_sum_by_class = filtered_df.groupby("CLASSIFICAÇÃO")["VALOR TOTAL DO INVESTIMENTO"].sum().reset_index()
    
    # Create a bar chart using Plotly Express for the sum of "VALOR TOTAL DO INVESTIMENTO" by CLASSIFICAÇÃO
    fig4 = px.bar(investment_sum_by_class, x="CLASSIFICAÇÃO", y="VALOR TOTAL DO INVESTIMENTO",
                  title="Soma do Valor Total do Investimento por CLASSIFICAÇÃO")
    
    # Specify the order of bars in descending order based on the sum of "VALOR TOTAL DO INVESTIMENTO"
    fig4.update_layout(xaxis_categoryorder='total descending')
    
    # Display the bar chart in col8
    col12.plotly_chart(fig4)
    
    
    
    # Group by SETOR DE APLICACAO and calculate the sum of "VALOR TOTAL DO INVESTIMENTO"
    investment_sum_by_setor = filtered_df.groupby("SETOR DE APLICACAO")["VALOR TOTAL DO INVESTIMENTO"].sum().reset_index()
    
    # Select the top 10 values based on the sum of "VALOR TOTAL DO INVESTIMENTO"
    top_10_setores = investment_sum_by_setor.nlargest(10, "VALOR TOTAL DO INVESTIMENTO")
    
    # Create a bar chart using Plotly Express for the sum of "VALOR TOTAL DO INVESTIMENTO" by SETOR DE APLICACAO
    fig5 = px.bar(top_10_setores, x="SETOR DE APLICACAO", y="VALOR TOTAL DO INVESTIMENTO",
                  title="Top 10 Valor do Investimento por SETOR DE APLICACAO")
    
    # Specify the order of bars in descending order based on the sum of "VALOR TOTAL DO INVESTIMENTO"
    fig5.update_layout(xaxis_categoryorder='total descending')
    
    # Display the bar chart in col9
    col19.plotly_chart(fig5)
    
    
    
    
    color_map = {
        "NÃO URGENTE": "blue",
        "POUCO URGENTE": "lightblue",
        "URGENTE": "lightcoral",
        "EMERGÊNCIA": "red"
    }
    
    # Calculate the count of each "NÍVEL DE PRIORIDADE"
    prioridade_counts = filtered_df["NÍVEL DE PRIORIDADE"].value_counts().reset_index()
    
    # Rename the columns for clarity
    prioridade_counts.columns = ["NÍVEL DE PRIORIDADE", "Count"]
    
    # Create a pie chart using Plotly Express for the distribution of "NÍVEL DE PRIORIDADE"
    fig6 = px.pie(prioridade_counts, names="NÍVEL DE PRIORIDADE", values="Count",
                  title="Distribuição de Nível de Prioridade",
                  color="NÍVEL DE PRIORIDADE",  # Specify the color parameter
                  color_discrete_map=color_map)  # Use the color map
    
    # Display the pie chart
    col15.plotly_chart(fig6)
    
    
    # Create a scatter plot using Plotly Express for "VALOR TOTAL DO INVESTIMENTO" vs "UNIDADE"
    fig7 = px.scatter(filtered_df, x="UNIDADE", y="VALOR TOTAL DO INVESTIMENTO", color="UNIDADE",
                      title="Distribuição de investimento dos itens por UNIDADE",
                      labels={"VALOR TOTAL DO INVESTIMENTO": "Valor Total do Investimento"})
    
    # Adjust the size of the dots
    fig7.update_traces(marker=dict(size=20))  # Replace YOUR_DESIRED_SIZE with the desired size for all dots.
    
    # Display the scatter plot in col11 with full width
    col16.plotly_chart(fig7, use_container_width=True)
    
    
    
    # Calculate CAPEX as a percentage
    #current_capital = 200000000  # Replace with your actual current capital value
    #capex_percentage = (filtered_df["VALOR TOTAL DO INVESTIMENTO"].sum() / current_capital) * 100
    
    # Format CAPEX percentage
    #formatted_capex = "{:.2f}%".format(capex_percentage)
    
    # Display CAPEX percentage
    #st.markdown("<h2 style='text-align: center;'>CAPEX</h2>", unsafe_allow_html=True)
    #st.markdown("<div style='display: flex; justify-content: center;'>"
                #"<h1 style='color: #1f77b4;'>{}</h1></div>".format(formatted_capex), unsafe_allow_html=True)
    
    
    
    
    csv_file_path = "agir_capex.csv"
    df1 = pd.read_csv(csv_file_path)
    
    # Sort the DataFrame by the "VL. AQUISICAO" column in descending order
    df1 = df1.sort_values(by="VL. AQUISICAO", ascending=False)
    
    
    # Group by CLASSIFICAÇÃO and calculate the sum of "VALOR TOTAL DO INVESTIMENTO"
    investment_sum_by_class = filtered_df.groupby("UNIDADE")["VALOR TOTAL DO INVESTIMENTO"].sum().reset_index()
    
    # Create a bar chart using Plotly Express for the sum of "VALOR TOTAL DO INVESTIMENTO" by CLASSIFICAÇÃO
    fig4 = px.bar(investment_sum_by_class, x="UNIDADE", y="VALOR TOTAL DO INVESTIMENTO",
                  title="Soma do Valor Total do Investimento por UNIDADE")
    
    # Specify the order of bars in descending order based on the sum of "VALOR TOTAL DO INVESTIMENTO"
    fig4.update_layout(xaxis_categoryorder='total descending')
    
    # Display the bar chart in col8
    col10.plotly_chart(fig4)
    
    
    
    # ... (previous code remains unchanged)
    
    
    # ... (previous code remains unchanged)
    
    
    
    # Calculate the sum of "VL. AQUISICAO" by "UNIDADE" in the filtered_df1
    sum_valor_atual = df1.groupby("UNIDADE")["VL. AQUISICAO"].sum().reset_index()
    
    # Second request: Calculate the sum of "VALOR TOTAL DO INVESTIMENTO" by "UNIDADE" in the filtered_df
    sum_valor_pedido = filtered_df.groupby("UNIDADE")["VALOR TOTAL DO INVESTIMENTO"].sum().reset_index()
    
    # Sort dataframes in descending order by the sum values
    sum_valor_pedido = sum_valor_pedido.sort_values(by="VALOR TOTAL DO INVESTIMENTO", ascending=False)
    sum_valor_atual = sum_valor_atual.sort_values(by="VL. AQUISICAO", ascending=False)
    
    # Create a bar chart to display the values with color mapping
    fig_combined_colored = go.Figure()
    
    # Add "Valor Pedido" bar
    fig_combined_colored.add_trace(go.Bar(
        x=sum_valor_pedido["UNIDADE"],
        y=sum_valor_pedido["VALOR TOTAL DO INVESTIMENTO"],
        name="Valor Pedido",
        marker_color='blue'
    ))
    
    # Add "Valor Atual" bar
    fig_combined_colored.add_trace(go.Bar(
        x=sum_valor_atual["UNIDADE"],
        y=sum_valor_atual["VL. AQUISICAO"],
        name="Valor Atual",
        marker_color='pink'
    ))
    
    # Update layout for better visualization
    fig_combined_colored.update_layout(
        barmode='stack',
        title="Soma do Valor Total do Investimento por UNIDADE",
        xaxis_title="UNIDADE",
        yaxis_title="Valor",
    )
    
    # Display the combined bar chart with color mapping
    col20.plotly_chart(fig_combined_colored)
    
    
    # Group by UNIDADE and calculate the average of "Anos desde a instalação"
    investment_avg_by_class = df1.groupby("UNIDADE")["Anos desde a instalação"].mean().reset_index()
    
    # Create a bar chart using Plotly Express for the average of "Anos desde a instalação" by UNIDADE
    fig4 = px.bar(investment_avg_by_class, x="UNIDADE", y="Anos desde a instalação",
                  title="Média de anos dos itens por UNIDADE")
    
    # Specify the order of bars in descending order based on the average "Anos desde a instalação"
    fig4.update_layout(xaxis_categoryorder='total descending')
    
    # Display the bar chart
    col21.plotly_chart(fig4)
    
    
    
    
    # Group by SETOR and calculate the average of "Anos desde a instalação"
    investment_avg_by_class = df1.groupby("SETOR")["Anos desde a instalação"].mean().reset_index()
    
    # Sort the DataFrame based on the average "Anos desde a instalação" in descending order
    investment_avg_by_class = investment_avg_by_class.sort_values(by="Anos desde a instalação", ascending=False)
    
    # Select the top 10 rows
    top_10_investments = investment_avg_by_class.head(10)
    
    # Create a bar chart using Plotly Express for the average of "Anos desde a instalação" by SETOR
    fig4 = px.bar(top_10_investments, x="SETOR", y="Anos desde a instalação",
                  title="Média de anos dos itens por SETOR - Top10 + antigos")
    
    # Display the bar chart
    col22.plotly_chart(fig4)
    
    
    
    
    
    # Calculate the percentage of "SOLICITAÇÃO REALIZADA" values by "VALOR TOTAL DO INVESTIMENTO"
    solicitacao_percentage = filtered_df.groupby("SOLICITAÇÃO REALIZADA")["VALOR TOTAL DO INVESTIMENTO"].sum() / filtered_df["VALOR TOTAL DO INVESTIMENTO"].sum() * 100
    
    # Create a donut chart using Plotly Express for "SOLICITAÇÃO REALIZADA"
    fig_donut_solicitacao = px.pie(names=solicitacao_percentage.index, values=solicitacao_percentage,
                                   title="Porcentagem do valor total do investimento POR SOLICITAÇÃO REALIZADA",
                                   hole=0.4)
    
    # Display the donut chart in col16
    col23.plotly_chart(fig_donut_solicitacao)
    
    
    # Calculate the percentage of "UNIDADE" values by "VALOR TOTAL DO INVESTIMENTO"
    unidade_percentage = filtered_df.groupby("UNIDADE")["VALOR TOTAL DO INVESTIMENTO"].sum() / filtered_df["VALOR TOTAL DO INVESTIMENTO"].sum() * 100
    
    # Create a donut chart using Plotly Express for "UNIDADE"
    fig_donut_unidade = px.pie(names=unidade_percentage.index, values=unidade_percentage,
                               title="Porcentagem do valor total do investimento POR UNIDADE",
                               hole=0.4)
    
    # Display the donut chart in col17
    col11.plotly_chart(fig_donut_unidade)
    
    
    # Calculate the percentage of "CLASSIFICAÇÃO" values by "VALOR TOTAL DO INVESTIMENTO"
    classificacao_percentage = filtered_df.groupby("CLASSIFICAÇÃO")["VALOR TOTAL DO INVESTIMENTO"].sum() / filtered_df["VALOR TOTAL DO INVESTIMENTO"].sum() * 100
    
    # Create a donut chart using Plotly Express for "CLASSIFICAÇÃO"
    fig_donut_classificacao = px.pie(names=classificacao_percentage.index, values=classificacao_percentage,
                                    title="Porcentagem do valor total do investimento POR CLASSIFICAÇÃO",
                                    hole=0.4)
    
    # Display the donut chart with no col
    col13.plotly_chart(fig_donut_classificacao)
    
    
    # Count the number of rows where "CLASSIFICAÇÃO" is equal to "OBRAS"
    quantidade_obras = filtered_df[filtered_df["CLASSIFICAÇÃO"] == "OBRAS"].shape[0]
    
    # Display the "Quantidade de Obras" in col19
    col5.subheader('Quantidade de Obras 🏗️')
    col5.metric(label='', value=quantidade_obras, delta=None)
    
    # Sum the values in the "VALOR TOTAL DO INVESTIMENTO" column where "CLASSIFICAÇÃO" is equal to "OBRAS"
    valor_das_obras = filtered_df.loc[filtered_df["CLASSIFICAÇÃO"] == "OBRAS", "VALOR TOTAL DO INVESTIMENTO"].sum()
    
    # Format the sum to display as Brazilian Real currency
    formatted_valor_das_obras = "R${:,.2f}".format(valor_das_obras)
    
    # Display the "Valor das Obras" in col20
    col8.subheader('Valor das Obras 💰🏗️')
    col8.metric(label='', value=formatted_valor_das_obras, delta=None)
    
    
    # Sum the values in the "VALOR TOTAL DO INVESTIMENTO" column where "CLASSIFICAÇÃO" is not equal to "OBRAS"
    valor_dos_equipamentos = filtered_df.loc[filtered_df["CLASSIFICAÇÃO"] != "OBRAS", "VALOR TOTAL DO INVESTIMENTO"].sum()
    
    # Format the sum to display as Brazilian Real currency
    formatted_valor_dos_equipamentos = "R${:,.2f}".format(valor_dos_equipamentos)
    
    # Display the "Valor dos Equipamentos" in col21
    col7.subheader('Valor dos Equipamentos 💰🔬')
    col7.metric(label='', value=formatted_valor_dos_equipamentos, delta=None)
    
    
    
    
    
    
    
    
    
    
    
    # Display the filtered DataFrame
    st.write("Dados Selecionados:")
    st.dataframe(filtered_df)
