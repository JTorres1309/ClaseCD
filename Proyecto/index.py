import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import streamlit as st


imagen="Bodega.jpg"
imagen1=plt.imread(imagen)
plt.imshow(imagen1)
plt.axis("off")

# Configuracion página
st.set_page_config(page_title="Analisis de inventario actual", page_icon=":bar_chart:", layout="centered")
@st.cache_data

#Cargar datos
def cargar_datos():
    inventario = pd.read_csv("Inventario.csv")
    #Limpienza de columnas
    inventario.drop(columns=["Batch_ID","SKU_Churn_Rate","FIFO_FEFO","Count_Variance","Audit_Date","Notes","Demand_Forecast_Accuracy_Pct","Last_Purchase_Date","Expiry_Date"],inplace=True)
    inventario.drop(columns=["SKU_ID","Supplier_ID","Warehouse_ID","Last_Purchase_Price_USD","Received_Date","Supplier_OnTime_Pct"],inplace=True)
    inventario.rename(columns={"SKU_Name":"Product_Name"},inplace=True)
    inventario.rename(columns={"Audit_Variance_Pct":"%_Variance_Audit"},inplace=True)
    #Cambiar formatos y tipos de datos
    inventario["Days_of_Inventory"] = inventario["Days_of_Inventory"].astype(str).str.replace(",", ".")
    inventario["Days_of_Inventory"] = pd.to_numeric(inventario["Days_of_Inventory"], errors="coerce")
    inventario["Avg_Daily_Sales"]=inventario["Avg_Daily_Sales"].astype(str).str.replace(",", ".")
    inventario["Avg_Daily_Sales"] = pd.to_numeric(inventario["Avg_Daily_Sales"], errors="coerce")
    inventario["Unit_Cost_USD"] = inventario["Unit_Cost_USD"].astype(str).str.replace("$", "", regex=False)
    inventario["Unit_Cost_USD"] = inventario["Unit_Cost_USD"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    inventario["Unit_Cost_USD"] = pd.to_numeric(inventario["Unit_Cost_USD"], errors="coerce")
    inventario["Total_Inventory_Value_USD"] = inventario["Total_Inventory_Value_USD"].astype(str).str.replace("$", "", regex=False)
    inventario["Total_Inventory_Value_USD"] = inventario["Total_Inventory_Value_USD"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
    inventario["Total_Inventory_Value_USD"] = pd.to_numeric(inventario["Total_Inventory_Value_USD"], errors="coerce")
    inventario["Order_Frequency_per_month"] = inventario["Order_Frequency_per_month"].astype(str).str.replace(",", ".")
    inventario["Order_Frequency_per_month"] = pd.to_numeric(inventario["Order_Frequency_per_month"], errors="coerce")
    inventario["%_Variance_Audit"] = inventario["%_Variance_Audit"].astype(str).str.replace(",", ".")
    inventario["%_Variance_Audit"] = inventario["%_Variance_Audit"].str.replace("%", "", regex=False)
    inventario["%_Variance_Audit"] = pd.to_numeric(inventario["%_Variance_Audit"], errors="coerce")

    return inventario

# Cargar los datos al iniciar
inventario = cargar_datos()

#Cambiar de pantallas 
def cambiar_vista(vista_activa):
    estados=["inicio","categorias","proveedores","bodega","ventas","conclusiones"]
    for estado in estados:
        st.session_state[estado] = (estado == vista_activa)
#Titulo del proyecto y descripción
if "inicio" not in st.session_state:
    st.session_state.inicio = True
def inicio():
    cambiar_vista("inicio")
if st.session_state.inicio:
    st.title("Inventario de la bodega")
    st.markdown("Proyecto de ciencia de datos para analizar un datased con el inventario actual de una bodega, con el objetivo de analizar tendencias, patrones y posibles problemas en la gestión del inventario.")
    st.image(imagen1, caption="Bodega", width="stretch")

#Contenidos de las paginas 

if "categorias" not in st.session_state:
    st.session_state.por_categoria=False
def categoria():
    cambiar_vista("categorias")  
     
if st.session_state.por_categoria:
    #with st.container():
        st.subheader("Productos disponibles por categoría")
        st.selectbox("Seleccione la categoría de productos deseada",options=inventario["Category"].unique(), key="categoria_seleccionada")
        #fig = go.Figure()
        #fig.add_trace(go.Bar(x=inventario["Product_Name"].value_counts().index, y=inventario["Quantity_On_Hand "].value_counts().values))
        #fig.update_layout(title="Cantidad de productos por categoría", xaxis_title="Categoría", yaxis_title="Cantidad de productos")
        #st.plotly_chart(fig)
        
        
 #Barra de navegación 
 
sidebar=st.sidebar
with sidebar:
        st.title("Navegación")
        st.button("Inicio", on_click=inicio)
        st.button("Categorías", on_click=categoria)
        st.button("Proveedores")
        st.button("Bodega")
        st.button("Ventas")
        st.button("Conclusiones")       
        
        
print("Hello world")    