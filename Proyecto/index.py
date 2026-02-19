import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import streamlit as st

url="Inventario.csv"
invet=pd.read_csv(url)
imagen="Bodega.jpg"
imagen1=plt.imread(imagen)
plt.imshow(imagen1)
plt.axis("off")

# Configuracion página
st.set_page_config(page_title="Inventario", page_icon=":bar_chart:", layout="centered")
st.title("Inventario de Bodega")
st.markdown("El siguiente dashboard muestra el inventario de la bodega, con información sobre los productos, cantidades y categorías.")
st.image(imagen1, caption="Bodega", use_column_width=True)



print("Hello world")