import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
import altair as alt
from PIL import Image

st.title('Dashboard de Ciência de Dados')
st.header('Condições Climáticas afetam o número de acidentes?')
st.subheader('Trabalho para Ciência de Dados I - Mestrado Profissional em Inovação Tecnológica')
logo_unifesp = Image.open('Unifesp_logo.png')
st.image(logo_unifesp)
st.subheader("Grupo:")
st.markdown("- Álvaro Salles Santiago")
st.markdown("- Luís Gustavo Barbosa")
st.markdown("- Luiz Otavio Ibrahim")
st.markdown("- Marcus Vinicius Teodoro Silva")
st.divider()

st.title("Problema:")
st.markdown("""Foram registrados em rodovias federais em 2022, 64.447 acidentes, sendo que 52.948 tiveram vítimas (Mortos ou Feridos).
Além dos riscos à vida, o custo total estimado para contorno dos acidentes foi de 12,92 bilhões de reais, sendo que este valor é o dobro do investido na malha pública federal 
(6,51 bilhões) no mesmo período, e este valor representa um total de aumento de R$ 800 milhões em relação a 2021.""")
st.divider()

st.title("Objetivo:")
st.markdown("- Identificar se há relação do alto índice de acidentes com as condições climáticas (Precipitação, Pressão Atmosférica (Min-Max), Temperatura (Min-Max), Umidade (Min-Max) e Vento.")
st.markdown("- Verificar quais as condições climáticas que mais impactam nos acidentes.")
st.markdown("- Caso alguma variável seja expressiva, criar uma aplicação para alertar motoristas que há um aumento na chance de acidente.")
st.markdown("- Se houver tempo hábil, criar uma aplicação para predizer se haverá acidentes nas pistas em um determinado dia.")
st.divider()

st.title("Metodologia:")
st.markdown("- Extrair dados de fonte públicas")
st.markdown("- Análise Exploratória dos dados")
st.markdown("- Análise Comparativa dos dados com a Variável Alvo (Acidente)")
st.divider()

st.title("Extração de Dados")
st.markdown("Dois tipos de dados são necessários, dados meteorológicos e dados de acidêntes, ambos os dados foram extraídos de fontes públicas")
st.markdown("Dados Meteorológicos, extraídos do portal INMET (Instituto Nacional de Meteorologia): https://portal.inmet.gov.br/dadoshistoricos")
st.markdown("Dados de acidentes em rodovias, extraídos do portal ANTT (Agência Nacional de Transportes Terrestres): https://dados.antt.gov.br/dataset/acidentes-rodovias")
st.divider()

st.title("Análise Exploratória")
st.header("Verificando os datasets obtidos")
st.markdown("Primeira etapa é verificar quais são as variáveis que possuímos dados, para saber se podemos ou devemos descartar algum dado")
st.markdown("Para os dados meteorológicos")
dados_meteorologicos_fonte = {"Fonte":["Data","Horario","PRECIPITAÇÃO TOTAL. HORÁRIO (mm)","PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO. HORARIA (mB)","PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)",
                                       "PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)","RADIACAO GLOBAL (Kj/m²)","TEMPERATURA DO AR - BULBO SECO. HORARIA (°C)",
                                       "TEMPERATURA DO PONTO DE ORVALHO (°C)","TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)","TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)","TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)",
                                       "TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)","UMIDADE REL. MAX. NA HORA ANT. (AUT) (%)","UMIDADE REL. MIN. NA HORA ANT. (AUT) (%)",
                                       "UMIDADE RELATIVA DO AR. HORARIA (%)","VENTO. DIREÇÃO HORARIA (gr) (° (gr))","VENTO. RAJADA MAXIMA (m/s)","VENTO. VELOCIDADE HORARIA (m/s)"],
                            "Significado":["Dia da medição","Hora da medição","Quantidade de chuva (mm)","Pressão Atmosférica (mB)","Pressão Atmosférica Máxima (mB)","Pressão Atmosférica Mínima (mB)",
                                               "Propagação de Energia (Kj/m²)","Temperatura sem considerar a umidade (°C)","Temperatura levando em consideração a umidade (°C)",
                                               "Temperatura Máxima (°C)","Temperatura Mínima (°C)","Temperatura Máxima de Orvalho(°C)","Temperatura Mínima de Orvalho(°C)",
                                               "Umidade Relativa Máxima (%)","Umidade Relativa Mínima (%)","Umidade Relativa do Ar (%)","Angulação do Vento (° (gr))",
                                               "Velocidade Máxima da Rajada do vento (m/s)","Velocidade do Vento (m/s)"],
                            "Tipo de Variável":["Data","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo",
                                                "Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo",
                                                "Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo",
                                                "Quantitativo Contínuo","Quantitativo Contínuo","Quantitativo Contínuo"]}
dados_meteorologicos = pd.DataFrame(data=dados_meteorologicos_fonte)
st.dataframe(dados_meteorologicos, hide_index = True)
st.markdown("Para os dados meteorológicos, iremos utilizar todos, pois não sabemos quais ou se algum interfere no número de acidentes")
st.markdown("Porém os dados de acidentes na rodovia, iremos utilizar apenas o número de acidentes por dia, pois não estamos considerando a gravidade do acidente por exemplo")
st.markdown("Como os dados meteorológicos estão com hora de medição, iremos criar um novo Dataset, com os dados resumindo pelo dia, com algumas considerações")
st.markdown("- Precipitação será o somatório do dia")
st.markdown("- Como todas as variáveis, contém sub-variáveis de Máximas e Mínimas, iremos considerar os limites do dia")
st.markdown("- Iremos considerar dados de 2010 até os mais recentes, pois é o período que as fontes tem em comum")
st.markdown("Com isso, transformando os dados por hora, em dados pelo dia, podendo fazer as relações com o número de acidente do mesmo")
st.markdown("Foi criado um Dataset, utilizando as informações meteorológicas, o número de acidentes por dia, qual é o dia da semana, e se houve feriado")
st.markdown("Primeiro iremos avaliar as variáveis: Precipitação; Pressão Atmosférica; Temperatura e Umidade")
st.divider()

df_old = pd.read_csv("2010-2021.csv")
df_old['Data'] = pd.to_datetime(df_old['Data'])
df_old.sort_values("Data")
st.header("Dataframe")
st.dataframe(df_old.head(), hide_index = True)

st.subheader("Gráficos Temporais")
chart1 = alt.Chart(df_old).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('Precipitacao',scale=alt.Scale(domain=[np.min(df_old.Precipitacao), np.max(df_old.Precipitacao)])), 
).properties(width=250, height=300)


chart2 = alt.Chart(df_old).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('PressaoAtmMin',scale=alt.Scale(domain=[np.min(df_old.PressaoAtmMin), np.max(df_old.PressaoAtmMin)])), 
).properties(width=250, height=300)

st.altair_chart(chart1 | chart2)

chart3 = alt.Chart(df_old).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('TemperaturaMin',scale=alt.Scale(domain=[np.min(df_old.TemperaturaMin), np.max(df_old.TemperaturaMin)])),
).properties(width=250, height=300)


chart4 = alt.Chart(df_old).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('UmidadeRelMin',scale=alt.Scale(domain=[np.min(df_old.UmidadeRelMin), np.max(df_old.UmidadeRelMin)])),
).properties(width=250, height=300)

st.altair_chart(chart3 | chart4)

st.markdown("Como pode ser observados pelos gráficos em questão, estão falhos pois:")
st.markdown("""- A Precipitação chegou a valores de -179,960.8 mm, o que não é possível, a precipitação média no Brasil varia de 1.250 a 2.000 mm, 
                    esses números significaria uma seca catastrófica""")
st.markdown("- A Pressão Atmosférica chegou -9,999mB, outro número que simbolizaria situações catastróficas, pois a medição não é relativa")
st.markdown("- Foi registrado uma Temperatura de -9,999ºC, o que é fisicamente impossível na física tradicional, já que o Zero absoluto é em -273,15ºC")
st.markdown("""- A Umidade Relativa do Ar foi registrada em -9,999%, o menor número registrado foi 0,3% no Irã em 2017, como é uma relação
                    é um número impossível de ser atingido na física tradicional e em condições naturais.""")

st.header("Qualidade dos dados")
st.markdown("Com as informações acima, podemos perceber que a qualidade dos dados públicos, devem ser sempre checadas e analisadas antes de chegar a qualquer afirmação")
st.markdown("""Foi feita uma limpeza dos dados, pois foi registrado que em certos momentos os dados registravam -9.999, para quaisquer valores e valores vazios (não zero, vazios).
                    Após a limpeza dos dados constatamos que:""")
st.markdown("""- 47.86% dos dados, possuem informação falsa""")
st.markdown("""- Não há registros válidos do ano de 2014""")
st.markdown("""- Apenas 15.62% dos dados de 2021 podem ser utilizados""")
st.markdown("""Nós iremos utilizar os dados após a limpeza, porém caso eles sejam utilizados para futuros projetos em aplicações reais
                é necessário a revisar e averiguar a qualidade dos dados novamente""")
st.divider()


st.header("Análise de Gráficos")
st.markdown("Primeiramente iremos plotar os mesmos gráficos da situação anterior para verificar a limpeza dos dados")

df = pd.read_csv("Geral_Limpo_Corrigido.csv")
df['Data'] = pd.to_datetime(df['Data'])
df.sort_values("Data")
st.header("Novo Dataframe")
st.dataframe(df.head(), hide_index = True)

st.subheader("Gráficos Temporais")

chart1_2 = alt.Chart(df).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('Precipitacao',scale=alt.Scale(domain=[np.min(df.Precipitacao), np.max(df.Precipitacao)])), 
).properties(width=250, height=300)


chart2_2 = alt.Chart(df).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('PressaoAtmMin',scale=alt.Scale(domain=[np.min(df.PressaoAtmMin), np.max(df.PressaoAtmMin)])), 
).properties(width=250, height=300)

st.altair_chart(chart1_2 | chart2_2)

chart3_2 = alt.Chart(df).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('TemperaturaMin',scale=alt.Scale(domain=[np.min(df.TemperaturaMin), np.max(df.TemperaturaMin)])),
).properties(width=250, height=300)


chart4_2 = alt.Chart(df).mark_line().encode(
    x=alt.X('Data',axis=alt.Axis(format='%Y-%m',labelAngle=-20)),
    y=alt.Y('UmidadeRelMin',scale=alt.Scale(domain=[np.min(df.UmidadeRelMin), np.max(df.UmidadeRelMin)])),
).properties(width=250, height=300)

st.altair_chart(chart3_2 | chart4_2)

st.markdown("Como podemos verificar, agora os valores fazem mais sentido com a realidade")

st.title("TODO")
st.markdown("Criar pares de gráficos para análises de Max e Min das variáveis, depois fazer as correlações")

Corre_matrix_r = pd.read_csv("CorrRStudio.csv")

st.dataframe(Corre_matrix_r, hide_index = True)


st.line_chart(df, x='Data',y="Acidentes", use_container_width=True)
st.line_chart(df, x='Data',y="Precipitacao", use_container_width=True)
st.line_chart(df, x='Data',y="PressaoAtm", use_container_width=True)
st.line_chart(df, x='Data',y="PressaoAtmMin", use_container_width=True)
st.line_chart(df, x='Data',y="RadiacaoGlobal", use_container_width=True)
st.line_chart(df, x='Data',y="TemperaturaBulboSeco", use_container_width=True)
st.line_chart(df, x='Data',y="TemperaturaPontoOrvalho", use_container_width=True)
st.line_chart(df, x='Data',y="TemperaturaMax", use_container_width=True)
st.line_chart(df, x='Data',y="TemperaturaMin", use_container_width=True)
st.line_chart(df, x='Data',y="TemperaturaMaxOrvalho", use_container_width=True)
st.line_chart(df, x='Data',y="TemperaturaMinOrvalho", use_container_width=True)
st.line_chart(df, x='Data',y="UmidadeRelMax", use_container_width=True)
st.line_chart(df, x='Data',y="UmidadeRelMin", use_container_width=True)
st.line_chart(df, x='Data',y="UmidadeRel", use_container_width=True)
st.line_chart(df, x='Data',y="VentoDirecao", use_container_width=True)
st.line_chart(df, x='Data',y="VentoRajada", use_container_width=True)
st.line_chart(df, x='Data',y="VentoVelocidade", use_container_width=True)
st.line_chart(df, x='Data',y=["Precipitacao","TemperaturaMax"], use_container_width=True)
st.line_chart(df['Precipitacao'], use_container_width=True)


df = pd.read_csv("Geral_Limpo_Corrigido.csv")
df['Data'] = pd.to_datetime(df['Data'])
df.sort_values("Data")
st.dataframe(df.head(), hide_index = True)

# outliers = df.value_counts()
# st.dataframe(outliers)
Corre_matrix_r = pd.read_csv("CorrRStudio.csv")

st.dataframe(Corre_matrix_r, hide_index = True)

fig = px.box(df, y="Precipitação")
st.plotly_chart(fig, use_container_width=True)

st.header('Relação entre Acidentes e Precipitação')
dfPre = pd.DataFrame(df[['Acidentes',"Precipitação"]])
figPre = px.scatter_matrix(dfPre)
st.plotly_chart(figPre, use_container_width=True)

st.header('Relação entre Acidentes e Pressão e Radiação')
dfPressao = pd.DataFrame(df[['Acidentes',"PressaoAtm","PressaoAtmMax","PressaoAtmMin", "RadiacaoGlobal"]])
figPressao = px.scatter_matrix(dfPressao)
st.plotly_chart(figPressao, use_container_width=True)

st.header('Relação entre Acidentes e Temperatura')
dfTemp = pd.DataFrame(df[['Acidentes',"TemperaturaBulboSeco","TemperaturaMax", "TemperaturaMin"]])
figTemp = px.scatter_matrix(dfTemp)
st.plotly_chart(figTemp, use_container_width=True)

st.header('Relação entre Acidentes e Temperatura Ponto de Orvalho')
dfTempOR = pd.DataFrame(df[['Acidentes',"TemperaturaPontoOrvalho","TemperaturaMaxOrvalho", "TemperaturaMinOrvalho"]])
figTempOR = px.scatter_matrix(dfTempOR)
st.plotly_chart(figTempOR, use_container_width=True)

st.header('Relação entre Acidentes e Umidade')
dfUmidade = pd.DataFrame(df[['Acidentes',"UmidadeRel","UmidadeRelMin","UmidadeRelMax"]])
figUmidade = px.scatter_matrix(dfUmidade)
st.plotly_chart(figUmidade, use_container_width=True)

st.header('Relação entre Acidentes e Vento')
dfVento = pd.DataFrame(df[['Acidentes',"VentoDirecao","VentoRajada","VentoVelocidade"]])
figVento = px.scatter_matrix(dfVento)
st.plotly_chart(figVento, use_container_width=True)


# st.line_chart(df['Data'], use_container_width=True)
# fig = ff.create_distplot(df[['Acidentes']], df[['Day of The Week']])

st.line_chart(df['Acidentes'], use_container_width=True)

st.plotly_chart(fig, use_container_width=True)


image = Image.open('Pearson_Corr.png')
st.image(image, caption="CorrelacaodePearson_Feita em R")
