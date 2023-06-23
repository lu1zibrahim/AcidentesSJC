import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
from PIL import Image

st.header('Dashboard de Ciencia de Dados')

df = pd.read_csv("Geral_Limpo_Corrigido.csv")
df['Data'] = pd.to_datetime(df['Data'])
df.sort_values("Data")
st.dataframe(df.head(), hide_index = True)

# outliers = df.value_counts()
# st.dataframe(outliers)
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

fig = px.box(df, y="Precipitacao")
st.plotly_chart(fig, use_container_width=True)

st.header('Relação entre Acidentes e Precipitacao')
dfPre = pd.DataFrame(df[['Acidentes',"Precipitacao"]])
figPre = px.scatter_matrix(dfPre)
st.plotly_chart(figPre, use_container_width=True)

st.header('Relação entre Acidentes e Pressao e Radiação')
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