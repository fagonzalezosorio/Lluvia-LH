import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

############## Imagenes ########################

paragua = Image.open('images/paragua.jfif')
lluvia = Image.open('images/lluvia.jfif')
pluviometro = Image.open('images/pluviometro2.jfif')

############## Titulo ###########################3
col1, col2, col3 = st.columns((4,1,1))
col1.markdown('<p style="font-family:Calibri Light; color:Black; font-size: 40px; font-weight:bold; text-shadow: 2px 2px 4px #000000;">Acumulación de Lluvia en Los Hornos de Huaquen </p>', unsafe_allow_html=True)
col1.markdown("         ")
col1.markdown("         ")

col2.image(lluvia,width=90)
col3.image(pluviometro, width=70)
######################### menu lateral ####################


col1,col2 = st.sidebar.columns(2)
col1.image(lluvia, width=90)
col2.image(paragua, width=94)
st.sidebar.title("Filtros")


########################################## RESUMEN MENSUAL-ANUAL ##################################3
## cargamos los datos

df=pd.read_excel("Datos/Lluvia (1).xlsx")
df = df.dropna(how='all')

cols = df.columns.tolist()
df = df.rename(columns = dict(zip(cols,[str(col).strip() for col in cols])) )
df["Fecha"] = pd.to_datetime(dict(year=df["Año"], month=df["Mes"], day=df["Dia"]))
df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d')
df['Año'] = df['Año'].astype(int)
df = df[df.Mes.notna()]
df['Mes'] = df['Mes'].astype(int)

mes = range(1,12)
nombre = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
mes_nombre = dict(zip(mes,nombre))
nombre_mes = dict(zip(nombre,mes))
df['mes_nombre'] = df.Mes.apply(lambda x: mes_nombre[x])


## creamos columnas
col1,col2,col3 = st.columns((3,1,3))
col1.markdown('<p style="font-family:Calibri Light; color:Black; font-size: 20px; font-weight:bold;"> Lluvias en el periodo seleccionado: </p>', unsafe_allow_html=True)

filtro_año=col2.selectbox("Año",df["Año"].unique())
df_filtered= df.query('Año == @filtro_año')

filtro_meses = col3.multiselect('Meses',df_filtered['mes_nombre'].unique())



col1, col2 = st.columns((5,2))


##### df filtrado
#
filtro_meses_str = ', '.join([f'"{mes}"' for mes in filtro_meses])

# Filtrar el DataFrame usando query
if filtro_meses_str:
    query_str = f'mes_nombre in [{filtro_meses_str}]'
    df_filtered = df_filtered.query(query_str)
else:
    df_filtered = df_filtered




col2.dataframe(df_filtered[['Fecha','mm']],  height=360)

### grafico mensual

# Crear el gráfico de barras
fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(df_filtered['Fecha'], df_filtered['mm'])
ax.set_ylabel('Lluvia acumulada [mm]')
ax.grid(True)
plt.xticks(rotation=45)

# Mostrar el gráfico en Streamlit
col1.pyplot(fig)



########################################## RESUMEN HISTORICO ##################################3
col1.markdown("         ")
col2.markdown("         ")
st.markdown('<p style="font-family:Calibri Light; color:Black; font-size: 20px; font-weight:bold;">Resumen historico de  lluvias </p>', unsafe_allow_html=True)
col1, col2 = st.columns((5,2))
col1.markdown("         ")
col2.markdown("         ")


df2 = pd.pivot_table(df,index = 'Año', columns='mes_nombre', values='mm', aggfunc='sum', fill_value=0)

order_cols = sorted([nombre_mes[col] for col in df2.columns])
df2 = df2[[mes_nombre[col] for col in order_cols]]

df2.loc['Total'] = df2.sum(numeric_only=True)
df2['Total'] = df2.sum(axis=1, numeric_only=True)

col1.dataframe(df2.replace(0,""))
col1.write('Fuente: Casa')

## historico conaf


conaf=pd.read_excel("Datos/Lluvia (1).xlsx", sheet_name= 'conaf')
conaf['Año'] = conaf['Año'].astype(int).astype(str)
conaf = conaf.dropna(how='all')


col2.dataframe(conaf,height=250)
col2.write('Fuente: Conaf')


