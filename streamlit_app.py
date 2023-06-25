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
st.subheader("Tecnologias Utilizadas")
st.markdown("- SQL/MySQL - Manipulação de Dados")
st.markdown("- R Studio - Análise dos dados")
st.markdown("- Streamlit - Construção do Dashboard")
st.markdown("- Python - Construção do Dashboard e Visualização dos Dados")
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
df_old['Data'] = df_old['Data'].dt.date
df_old.sort_values("Data")
st.header("Dataframe")
st.dataframe(df_old.head(), hide_index = True)
st.dataframe(df_old.describe())

st.header("Problema nos Dados")
st.markdown("Como podemos observar pela tabela acima, os dados parecem incorretos, mostrando valores irreais a primeira vista, iremos passar por uma série de análises para verificar se essa afirmação está correta.")

st.subheader("Teste para verificar se os dados seguem distribuição Normal - Kolmogorov–Smirnov test")
df_initial_ks_test = pd.read_csv("Inicial_KSTest.csv")
st.markdown("Como pode ter sido observado os gráficos além de estarem aparentemente incorretos, não possuem uma distribuição Normal, porém iremos comprovar pelo teste K.S.")
st.markdown("Código Utilizado no R-Studio, considerando:")
st.markdown("- df1 = Dataframe dos dados iniciais")
st.markdown("- dk = Novo Dataframe com as informações Resultantes")
st.markdown("- stringAsFactors = Elimitando as colunas que não são numéricas")
codigo_r_inicial = ("""dk <- data.frame(Name=character(19), D=numeric(19), p=numeric(19), stringAsFactors=F)
for(j in 2:19){
  k <- ks.test(df1[,j],"pnorm")
  dk$Name[j] <- names(df1)[j]
  dk$D[j] <- k$statistic
  dk$p[j] <- k$p.value
}""")
st.code(codigo_r_inicial, language='r')
st.dataframe(df_initial_ks_test, hide_index = True)

st.markdown("Como pode ter sido observado, a hipótese nula do teste KS pode ser rejeitado com os dados apresentados, mostrando que não seguem distribuições Normal")

st.subheader("Histogramas")
st.markdown("Como a maioria dos dados são Quantitativos Contínuos, iremos criar Histogramas, para verificar a representação dos dados")

dist1_old = df_old.Precipitacao
dist2_old = df_old.PressaoAtm
dist3_old = df_old.PressaoAtmMax
dist4_old = df_old.PressaoAtmMin
dist5_old = df_old.RadiacaoGlobal
dist6_old = df_old.TemperaturaBulboSeco
dist7_old = df_old.TemperaturaPontoOrvalho
dist8_old = df_old.TemperaturaMax
dist9_old = df_old.TemperaturaMin
dist10_old = df_old.TemperaturaMaxOrvalho
dist11_old = df_old.TemperaturaMinOrvalho
dist12_old = df_old.UmidadeRelMax
dist13_old = df_old.UmidadeRelMin
dist14_old = df_old.UmidadeRel
dist15_old = df_old.VentoDirecao
dist16_old = df_old.VentoRajada
dist17_old = df_old.VentoVelocidade
dist18_old = df_old.Acidentes


fig_old, axs_old = plt.subplots(3, 3, sharey=True, tight_layout=True)
axs_old[0,0].hist(dist1_old)
axs_old[0,1].hist(dist2_old)
axs_old[0,2].hist(dist3_old)
axs_old[1,0].hist(dist4_old)
axs_old[1,1].hist(dist5_old)
axs_old[1,2].hist(dist6_old)
axs_old[2,0].hist(dist7_old)
axs_old[2,1].hist(dist8_old)
axs_old[2,2].hist(dist9_old)
axs_old[0,0].set(ylabel="Precipitacao", yticks=[])
axs_old[0,1].set(ylabel="PressaoAtm", yticks=[])
axs_old[0,2].set(ylabel="PressaoAtmMax", yticks=[])
axs_old[1,0].set(ylabel="PressaoAtmMin", yticks=[])
axs_old[1,1].set(ylabel="RadiacaoGlobal", yticks=[])
axs_old[1,2].set(ylabel="TemperaturaBulboSeco", yticks=[])
axs_old[2,0].set(ylabel="TemperaturaPontoOrvalho", yticks=[])
axs_old[2,1].set(ylabel="TemperaturaMax", yticks=[])
axs_old[2,2].set(ylabel="TemperaturaMin", yticks=[])
st.pyplot(fig_old)


fig2_old, axs2_old = plt.subplots(3, 3, sharey=True, tight_layout=True)
axs2_old[0,0].hist(dist10_old)
axs2_old[0,1].hist(dist11_old)
axs2_old[0,2].hist(dist12_old)
axs2_old[1,0].hist(dist13_old)
axs2_old[1,1].hist(dist14_old)
axs2_old[1,2].hist(dist15_old)
axs2_old[2,0].hist(dist16_old)
axs2_old[2,1].hist(dist17_old)
axs2_old[2,2].hist(dist18_old)
axs2_old[0,0].set(ylabel="TemperaturaMaxOrvalho", yticks=[])
axs2_old[0,1].set(ylabel="TemperaturaMinOrvalho", yticks=[])
axs2_old[0,2].set(ylabel="UmidadeRelMax", yticks=[])
axs2_old[1,0].set(ylabel="UmidadeRelMin", yticks=[])
axs2_old[1,1].set(ylabel="UmidadeRel", yticks=[])
axs2_old[1,2].set(ylabel="VentoDirecao", yticks=[])
axs2_old[2,0].set(ylabel="VentoRajada", yticks=[])
axs2_old[2,1].set(ylabel="VentoVelocidade", yticks=[])
axs2_old[2,2].set(ylabel="Acidentes", yticks=[])

st.pyplot(fig2_old)

st.markdown("Com os Histogramas apresentados, e as análises anteriores podemos perceber que há algum problema com os dados, vamos traçar algumas series temporais para entender melhor")

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
st.markdown("""- A Precipitação chegou a valores de -179,960.8 mm, o que não é possível, a precipitação média no Brasil varia de 1.250 a 2.000 mm por ano, 
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


st.header("Análise dos dados após Limpeza")
st.markdown("Primeiramente iremos plotar os mesmos gráficos da situação anterior para verificar a limpeza dos dados")

df = pd.read_csv("Geral_Limpo_Corrigido.csv")
df['Data'] = pd.to_datetime(df['Data'])
df['Data'] = df['Data'].dt.date
df.sort_values("Data")
st.header("Novo Dataframe")
st.dataframe(df.head(), hide_index = True)
st.dataframe(df.describe())

st.markdown(""""Como pode ser observado, os dados seguem uma melhor distribuição, em sua maioria, std (standard deviation), 
ou desvio padrão estão baixo (75% dos dados estão dentro da média +- o desvio), exceto Radiação Global.
Conforme falado anteriormente iremos trabalhar com os valores Maxímos e Mínimos, pois eles trazem os menores erros (Comprovado pela tabela acima) e pelos Histogramas que serão mostrados abaixo.""")

st.subheader("Teste para verificar se os dados seguem distribuição Normal - Kolmogorov–Smirnov test")

st.markdown("Algumas variáveis, possuem um comportamente que pode simbolizar uma distribuição normal, iremos comprovar pelo K.S. Test")
st.markdown("Código Utilizado no R-Studio, considerando:")
st.markdown("- df2 = Dataframe dos dados após limpeza")
st.markdown("- dk2 = Novo Dataframe com as informações Resultantes")
st.markdown("- stringAsFactors = Elimitando as colunas que não são numéricas")
codigo_r_final = ("""dk2 <- data.frame(Name=character(19), D=numeric(19), p=numeric(19), stringAsFactors=F)
for(j in 2:19){
  k <- ks.test(df2[,j],"pnorm")
  dk$Name[j] <- names(df2)[j]
  dk$D[j] <- k$statistic
  dk$p[j] <- k$p.value
}""")
st.code(codigo_r_final, language='r')
df_final_ks_test = pd.read_csv("Final_KSTest.csv")
st.dataframe(df_final_ks_test, hide_index = True)

st.markdown("Como pode ter sido observado e esperado, a hipótese nula do teste KS pode ser rejeitado com os dados apresentados, iremos analisar melhor observando os Histogramas")

st.subheader("Histogramas")

dist1 = df.Precipitacao
dist2 = df.PressaoAtm
dist3 = df.PressaoAtmMax
dist4 = df.PressaoAtmMin
dist5 = df.RadiacaoGlobal
dist6 = df.TemperaturaBulboSeco
dist7 = df.TemperaturaPontoOrvalho
dist8 = df.TemperaturaMax
dist9 = df.TemperaturaMin
dist10 = df.TemperaturaMaxOrvalho
dist11 = df.TemperaturaMinOrvalho
dist12 = df.UmidadeRelMax
dist13 = df.UmidadeRelMin
dist14 = df.UmidadeRel
dist15 = df.VentoDirecao
dist16 = df.VentoRajada
dist17 = df.VentoVelocidade
dist18 = df.Acidentes


fig, axs = plt.subplots(3, 3, sharey=True, tight_layout=True)
axs[0,0].hist(dist1)
axs[0,1].hist(dist2)
axs[0,2].hist(dist3)
axs[1,0].hist(dist4)
axs[1,1].hist(dist5)
axs[1,2].hist(dist6)
axs[2,0].hist(dist7)
axs[2,1].hist(dist8)
axs[2,2].hist(dist9)
axs[0,0].set(ylabel="Precipitacao", yticks=[])
axs[0,1].set(ylabel="PressaoAtm", yticks=[])
axs[0,2].set(ylabel="PressaoAtmMax", yticks=[])
axs[1,0].set(ylabel="PressaoAtmMin", yticks=[])
axs[1,1].set(ylabel="RadiacaoGlobal", yticks=[])
axs[1,2].set(ylabel="TemperaturaBulboSeco", yticks=[])
axs[2,0].set(ylabel="TemperaturaPontoOrvalho", yticks=[])
axs[2,1].set(ylabel="TemperaturaMax", yticks=[])
axs[2,2].set(ylabel="TemperaturaMin", yticks=[])
st.pyplot(fig)


fig2, axs2 = plt.subplots(3, 3, sharey=True, tight_layout=True)
axs2[0,0].hist(dist10)
axs2[0,1].hist(dist11)
axs2[0,2].hist(dist12)
axs2[1,0].hist(dist13)
axs2[1,1].hist(dist14)
axs2[1,2].hist(dist15)
axs2[2,0].hist(dist16)
axs2[2,1].hist(dist17)
axs2[2,2].hist(dist18)
axs2[0,0].set(ylabel="TemperaturaMaxOrvalho", yticks=[])
axs2[0,1].set(ylabel="TemperaturaMinOrvalho", yticks=[])
axs2[0,2].set(ylabel="UmidadeRelMax", yticks=[])
axs2[1,0].set(ylabel="UmidadeRelMin", yticks=[])
axs2[1,1].set(ylabel="UmidadeRel", yticks=[])
axs2[1,2].set(ylabel="VentoDirecao", yticks=[])
axs2[2,0].set(ylabel="VentoRajada", yticks=[])
axs2[2,1].set(ylabel="VentoVelocidade", yticks=[])
axs2[2,2].set(ylabel="Acidentes", yticks=[])

st.pyplot(fig2)

st.markdown("Algumas distribuições aparentam distribuição normal, porém em nenhum dos testes K.S. isso foi comprovado, isso se da que para testes maiores de 1,000 entries, não é recomendado a utilização do K.S. Test")
st.markdown("Iremos criar Boxplots das variáveis Precipitação, Acidentes, Maximas e Mínimas para verificar visualmente a sua Normalidade")

st.subheader("BoxPlots")

fig_prep, axs_prep = plt.subplots()
axs_prep.boxplot(dist1)
axs_prep.set(ylabel="Precipitação",yticks=[])
st.pyplot(fig_prep)

fig_pressao, axs_pressao = plt.subplots(1, 2, sharey=True)
axs_pressao[0].boxplot(dist3)
axs_pressao[1].boxplot(dist4)
axs_pressao[0].set(ylabel="PressaoAtmMax", yticks=[])
axs_pressao[1].set(ylabel="PressaoAtmMin", yticks=[])

st.pyplot(fig_pressao)

fig_temp, axs_temp = plt.subplots(1, 2, sharey=True)
axs_temp[0].boxplot(dist8)
axs_temp[1].boxplot(dist9)
axs_temp[0].set(ylabel="TemperaturamMax", yticks=[])
axs_temp[1].set(ylabel="TemperaturaMin", yticks=[])
st.pyplot(fig_temp)

fig_temp_or, axs_temp_or = plt.subplots(1, 2, sharey=True)
axs_temp_or[0].boxplot(dist10)
axs_temp_or[1].boxplot(dist11)
axs_temp_or[0].set(ylabel="TemperaturamMax", yticks=[])
axs_temp_or[1].set(ylabel="TemperaturaMin", yticks=[])
st.pyplot(fig_temp_or)

fig_umi, axs_umi = plt.subplots(1, 2, sharey=True)
axs_umi[0].boxplot(dist12)
axs_umi[1].boxplot(dist13)
axs_umi[0].set(ylabel="TemperaturamMax", yticks=[])
axs_umi[1].set(ylabel="TemperaturaMin", yticks=[])
st.pyplot(fig_temp_or)

fig_aci, axs_aci = plt.subplots()
axs_aci.boxplot(dist18)
axs_aci.set(ylabel="Acidentes",yticks=[])
st.pyplot(fig_aci)
st.markdown("Como podemos visualizar as variáveis Max e Min, possuem uma Normalidade, sendo ")

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

st.markdown("Como podemos verificar, agora os valores fazem mais sentido com a realidade, embora temos períodos sem dados, neste caso não há ação a ser feita")

st.title("Correlação das variáveis")
st.markdown("Agora que comprovamos que os dados estão melhorados, e foi feita uma análise exploratória, vamos verificar se há correlação entre alguma variável e o número de acidentes")

correlacao = ("""
library(readr)
trabalho <- read_csv("Geral_Limpo_Corrigido.csv")
head(trabalho)
library(tidyverse)
dat <- trabalho %>%
  select(-Data,-DiaSemana)
head(dat)

round(cor(dat, use = "complete.obs"),
      digits = 2
      )
mydf = round(cor(dat, use = "complete.obs"), digits = 2)

write.csv(mydf, "CorrRStudio_new.csv")
}

library(corrplot)
corrplot(cor(dat, use = "complete.obs"),
         method = "number",
         type = "upper", shade.col=NA,)"""
)
st.code(correlacao, language='r')

Corre_matrix_r = pd.read_csv("CorrRStudio_new.csv")
r_plot_corr = Image.open('Rplot.png')
st.image(r_plot_corr, caption="CorrelacaodePearson_Total")

st.dataframe(Corre_matrix_r, hide_index = True)


st.markdown("Com isso podemos chegar as seguintes observações com os dados atuais")
st.markdown("Podemos observar que nenhuma das variáveis presentes possui um impacto expressivo no número de acidentes")
st.markdown("Variáveis que possuem maior correlação positiva")
st.markdown("- Umidade Relativa Mínima - 0.1")
st.markdown("- Precipitação - 0.1")
st.markdown("- Temperatura Mínima de Orvalho - 0.07")
st.markdown("- Umidade Relativa Máxima - 0.06")
st.markdown("- Temperatura Mínima - 0.06")
st.markdown("Variáveis que possuem maior correlação negativa")
st.markdown("- Pressão Atmosférica - -0.11")
st.markdown("- Pressão Atmosférica Máxima - -0.1")
st.markdown("- Pressão Atmosférica Mínima - -0.09")
st.markdown("- Radiação Global - -0.08")
st.markdown("- Rajada de Vento - -0.05")
st.divider()


st.title("Análises de distribuição")
st.markdown("Como as análises retornaram poucas evidências, iremos traçar a distribuição das variáveis e correlação visualmente.")
st.header('Relação entre Acidentes e Precipitação')
dfPre = pd.DataFrame(df[['Acidentes',"Precipitacao"]])
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
st.markdown("É possível verificar que a análise de correlação, foi feita corretamente, pois visualmente nenhuma das variáveis apresenta correlação com o número de acidentes visualmente")



st.markdown("Após o resultado dos dados, decidimos observador por outro lado, e levantamos algumas possibilidades")
st.markdown("- Será que o dia da semana interfere no número de acidentes?")
st.markdown("- Será que a Data é um fator que influencia o número de acidentes?")
st.divider()


st.subheader("Dia da semana")
correlacao_semana = ("""
trabalho2 <- read_csv("Geral2_Limpo.csv")
dat2 <- trabalho2 %>%
  select(-Data)
library(ggstatsplot)
ggcorrmat(
  data = dat2[, c("Acidentes", "Monday","Tuesday","Wednesday","Thursday","Friday", "Saturday","Sunday")],
  type = "nonparametric", # parametric for Pearson, nonparametric for Spearman's correlation
  colors = c("darkred", "white", "steelblue") # change default colors
)
         """
)
st.code(correlacao_semana, language='r')
dia_semana = Image.open('CorrDiaSemana.png')
st.image(dia_semana, caption="Correlação do dia da Semana")
st.markdown("Com os dados atuais podemos chegar a conclusão que")
st.markdown("- Sexta-feira é o dia que possui maior correlação positiva - 0.15")
st.markdown("- Terça-feira é o dia que possui maior correlação negativa - -0.11")
st.markdown("- Finais de semana são mais tendenciosos a ter acidente")
st.markdown("- Dias de semana são menos tendenciosos a ter acidente")
st.divider()
st.subheader("Será que a data influencia o número de acidentes?")
st.markdown("Primeiramente iremos traçar o número de acidentes em relação ao tempo")
st.line_chart(df, x='Data',y="Acidentes", use_container_width=True)

st.markdown("É possível verificar que há certos períodos de aumento e decrécimo de acidentes (Também a falta de dados, que pode influenciar os resultados)")
st.markdown("Para melhor visualização ao longo do tempo vamos traçar duas variáveis que variam em relação a data (Estações do ano), que são Precipitação e Temperatura")
st.line_chart(df, x='Data',y=["Precipitacao","TemperaturaMax","TemperaturaMin"], use_container_width=True)

st.markdown("Agora iremos traçar o número de Acidentes e Precipitação")
st.line_chart(df, x='Data',y=["Acidentes", "Precipitacao"], use_container_width=True)
st.markdown("Agora iremos traçar o número de Acidentes e Umidade Relativa Mínima")
st.line_chart(df, x='Data',y=["Acidentes","UmidadeRelMin"], use_container_width=True)
# st.line_chart(df, x='Data',y="Precipitacao", use_container_width=True)
# st.line_chart(df, x='Data',y="PressaoAtm", use_container_width=True)
# st.line_chart(df, x='Data',y="PressaoAtmMin", use_container_width=True)
# st.line_chart(df, x='Data',y="RadiacaoGlobal", use_container_width=True)
# st.line_chart(df, x='Data',y="TemperaturaBulboSeco", use_container_width=True)
# st.line_chart(df, x='Data',y="TemperaturaPontoOrvalho", use_container_width=True)
# st.line_chart(df, x='Data',y="TemperaturaMax", use_container_width=True)
# st.line_chart(df, x='Data',y="TemperaturaMin", use_container_width=True)
# st.line_chart(df, x='Data',y="TemperaturaMaxOrvalho", use_container_width=True)
# st.line_chart(df, x='Data',y="TemperaturaMinOrvalho", use_container_width=True)
# st.line_chart(df, x='Data',y="UmidadeRelMax", use_container_width=True)
# st.line_chart(df, x='Data',y="UmidadeRelMin", use_container_width=True)
# st.line_chart(df, x='Data',y="UmidadeRel", use_container_width=True)
# st.line_chart(df, x='Data',y="VentoDirecao", use_container_width=True)
# st.line_chart(df, x='Data',y="VentoRajada", use_container_width=True)
# st.line_chart(df, x='Data',y="VentoVelocidade", use_container_width=True)
# st.line_chart(df, x='Data',y=["Precipitacao","TemperaturaMax"], use_container_width=True)
# st.line_chart(df['Precipitacao'], use_container_width=True)

st.markdown("Visualmente é possível identificar que a Data, pode ser um fator que influencia o número de acidentes, porém pelos métodos tradicionais não é possível averiguar")
st.markdown("Por isso optamos por trazer um outro método de análise a de Regressão Linear")
st.markdown("Através de modelos matemáticos, verifica o 'peso', de uma variável em função da variável alvo, no nosso caso a de acidente")
st.markdown("Para isso foi utilizado o Vertex AI, que é uma plataforma da Google que permite treinar modelos de M.L., e com isso obtivemos os seguintes resultados:")
st.markdown("- Data tem 43,76% de Importância")
st.markdown("- O Dia da Semana tem 11,2% de Importância")
st.markdown("- Precipitação Possui 6,89% de Importância")
st.markdown("- A Temperatura Possui 6,69% de Importância")
st.markdown("- A Umidade Relativa Mínima Possui 6,55% de Importância")
st.markdown("Podemos ver um pouco mais no gráfico abaixo:")

vertex = Image.open('imagem_VertexAI.png')
st.image(vertex, caption="Imagem do Vertex")

st.title("Conclusões")
st.markdown("Com relação a primeira parte da análise, conseguimos chegar a conclusão com os dados apresentados que:")
st.markdown("- As condições climáticas não possuem tanto impacto no número de acidêntes")
st.markdown("- Os dias da semana, possui uma correlação com o número de Acidentes")
st.markdown("- Os dados disponíveis, encontra-se com muitas informações faltas, chegando a quase 50%, isso impacta diretamente na qualidade da pesquisa")
st.markdown("- Como são dados históricos, existe a possibilidade dos dados não poderem ser recuperados")
st.markdown("- Caso, a partir deste trabalho, há o interesse de continua-lo, é necessário melhor base de dados")
st.markdown("Agora em relação ao uso de Machine Learning podemos visualizar:")
st.markdown("""- A Data é um fator impactante no número de acidentes. Feriados Nacionais, Feriados Locais, Dias 'Emendados' Férias de Verão, Férias de Inverno, Eventos Periódicos, são alguns fatores que podem impactar""")
st.markdown("Tanto o modelo de M.L. quanto o feito neste trabalho, possuem resultados semelhantes na atribuição de correlação das variáveis")
st.markdown("""Com isso concluimos o objetivo deste Dashboard, mostramos que com os dados atuais não é possível verificar um alta correlação entre condições climáticas e acidentes, porém, podemos identificar
Uma relação entre o número de acidentes e as datas do ano.""")