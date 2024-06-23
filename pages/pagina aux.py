import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st

df=pd.read_excel("Datos/Lluvia (1).xlsx")
cols = df.columns.tolist()
cols2 = [str(col).strip() for col in cols]
df = df.rename(columns = dict(zip(cols,[str(col).strip() for col in cols])) )
df["Fecha"] = pd.to_datetime(dict(year=df["Año"], month=df["Mes"], day=df["Dia"]))



fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Fecha'], df['mm'], marker='o', linestyle='-', color='b', label='Valores de mm')


ax.set_xlabel('Fecha')
ax.set_ylabel('Valor de mm')
ax.set_title('Gráfico de línea: Valores de mm a lo largo del tiempo')
plt.xticks(rotation=45)
ax.legend()

# Mostrar el gráfico en Streamlit
st.pyplot(fig)



# histograma N(0,1)
fig, ax = plt.subplots()
ax.hist(np.random.normal(0, 1, 500))

st.pyplot(fig)


