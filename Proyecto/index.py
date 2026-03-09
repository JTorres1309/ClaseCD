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

# 3. Gestión de estados (Navegación)
if "vista" not in st.session_state:
    st.session_state.vista = "inicio"

def cambiar_vista(nueva_vista):
    st.session_state.vista = nueva_vista

# 4. Lógica de las páginas
if st.session_state.vista == "inicio":
    st.title("Inventario de la bodega", anchor="center")
    st.markdown("Proyecto de ciencia de datos para analizar tendencias y gestión de inventario, con el objetivo de optimizar la rotación de productos y mejorar la eficiencia operativa.")
    st.image("Bodega.jpg", width="stretch")

#elif st.session_state.vista == "categorias":
    #st.subheader("Productos disponibles por categoría")
    
    ## Filtro funcional
    #cat_seleccionada = st.selectbox("Seleccione la categoría", options=inventario["Category"].unique())
    #df_filtrado = inventario[inventario["Category"] == cat_seleccionada]
    
    # Gráfica corregida
    #fig = go.Figure()
    # Usamos el dataframe filtrado para que la gráfica cambie según el selectbox
    #fig.add_trace(go.Bar(
        #x=df_filtrado["Product_Name"], 
        #y=df_filtrado["Quantity_On_Hand"] # Verifica si lleva espacio o no
    #))
    
    #fig.update_layout(title=f"Stock en {cat_seleccionada}", xaxis_title="Producto", yaxis_title="Cantidad")
    #st.plotly_chart(fig)

elif st.session_state.vista == "ventas":
    st.subheader("Análisis de ventas por ubicación (Unidades)")
    df_sumaventas=inventario.groupby("Warehouse_Location")["Avg_Daily_Sales"].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sumaventas["Warehouse_Location"], 
        y=df_sumaventas["Avg_Daily_Sales"]
    ))
    fig.update_layout(title="Ventas diarias promedio por ubicación", xaxis_title="Ubicación", yaxis_title="Ventas Diarias Promedio")
    st.plotly_chart(fig)
    
    ubi_seleccionada = st.selectbox("Seleccione la ubicación", options=inventario["Warehouse_Location"].unique())
    df_filtrado_ubi = inventario[inventario["Warehouse_Location"] == ubi_seleccionada]
    df_filtrado_ubi_sum=df_filtrado_ubi.groupby("Category")["Avg_Daily_Sales"].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_filtrado_ubi_sum["Avg_Daily_Sales"], 
        y=df_filtrado_ubi_sum["Category"],
        orientation="h"
    ))
    fig.update_layout(title=f"Ventas diarias promedio en {ubi_seleccionada}", xaxis_title="Ventas Diarias Promedio", yaxis_title="Categoría")
    st.plotly_chart(fig)

elif st.session_state.vista == "analisis":
    st.subheader("Análisis de rotación de inventario")
    cat_seleccionada_analisis = st.selectbox("Seleccione la categoría para análisis", options=inventario["Category"].unique())
    bodega_seleccionada_analisis = st.selectbox("Seleccione la ubicación para análisis", options=inventario["Warehouse_Location"].unique())
    df_filtrado_analisis = inventario[(inventario["Category"] == cat_seleccionada_analisis) & (inventario["Warehouse_Location"] == bodega_seleccionada_analisis)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtrado_analisis["Days_of_Inventory"], 
        y=df_filtrado_analisis["Avg_Daily_Sales"],
        mode="markers",
        text=df_filtrado_analisis["Product_Name"]
    ))
    fig.update_layout(title="Rotación de Inventario vs Ventas Diarias Promedio", xaxis_title="Días de Inventario", yaxis_title="Ventas Diarias Promedio")
    st.plotly_chart(fig)

elif st.session_state.vista =="proveedores":
    st.subheader("Tiempos de entrega por proveedor")
    ubi_seleccionada=st.selectbox("Seleccione ubicación para análisis", options=inventario["Warehouse_Location"].unique())
    cat_seleccionada_proveedores=st.selectbox("Seleccione categoría para análisis", options=inventario["Category"].unique())
    df_filtrado_proveedores = inventario[(inventario["Warehouse_Location"] == ubi_seleccionada) & (inventario["Category"] == cat_seleccionada_proveedores)]
    df_agrupado_proveedores = df_filtrado_proveedores.groupby("Supplier_Name")["Lead_Time_Days"].mean().reset_index()
    fig = px.bar(df_agrupado_proveedores, x="Supplier_Name", y="Lead_Time_Days", title=f"Tiempos de entrega en {ubi_seleccionada} para {cat_seleccionada_proveedores}", labels={"Supplier_Name": "Proveedor", "Lead_Time_Days": "Días de entrega"})
    st.plotly_chart(fig)

elif st.session_state.vista == "bodega":
    st.subheader("Tabla de gestión de la bodega")

    ubicaciones_sel = st.selectbox(
        "Seleccione la ubicación de la bodega:", 
        options=inventario["Warehouse_Location"].unique())
    categorias_sel = st.selectbox(
        "Seleccione las categorías:", 
        options=inventario["Category"].unique())
    df_filtrado_bodega = inventario[
        (inventario["Warehouse_Location"] == ubicaciones_sel) & 
        (inventario["Category"] == categorias_sel)
    ]
    st.dataframe(df_filtrado_bodega[["Product_Name", "Quantity_On_Hand", "Days_of_Inventory", "Inventory_Status","%_Variance_Audit"]])
    
    #Gestion del inventario en bodega
    st.subheader("Auditoria de inventario")
    variacion_promedio=df_filtrado_bodega["%_Variance_Audit"].mean()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Variación promedio de auditoría", 
                  value=f"{variacion_promedio:.2f}%",
                  delta=f"{variacion_promedio:.2f}%",
        )
    with col2:
        valor_total_inventario = df_filtrado_bodega["Total_Inventory_Value_USD"].sum()
        st.metric("Valor total del inventario",
                    value=f"${valor_total_inventario:,.2f}",
            )
      #Grafica de distribución de inventario por categoria
    df_filtrado_ubi = inventario[inventario["Warehouse_Location"] == ubicaciones_sel]
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=df_filtrado_ubi["Category"], 
        values=df_filtrado_ubi["Quantity_On_Hand"],
        hole=0.4
    ))
    fig.update_layout(title=f"Distribución de inventario en {ubicaciones_sel}", xaxis_title="Categoría", yaxis_title="Cantidad")
    st.plotly_chart(fig)

elif st.session_state.vista == "conclusiones":
    st.subheader("Conclusiones y recomendaciones")
    st.markdown("**1)** **Optimización de inventario**: Se recomienda implementar un sistema de gestión de inventario basado en la rotación de productos, priorizando aquellos con mayor demanda y menor tiempo de almacenamiento.")
    st.markdown("**2)** **Revisión de proveedores**: Es crucial evaluar el desempeño de los proveedores en términos de tiempos de entrega y calidad, para asegurar una cadena de suministro eficiente.")
    st.markdown("**3)** **Análisis continuo**: Se sugiere realizar análisis periódicos del inventario y las ventas para identificar tendencias y ajustar las estrategias de compra y almacenamiento.")
    st.markdown("**4)** **Capacitación del personal**: Es importante capacitar al personal de la bodega en prácticas de gestión de inventario y auditoría para reducir las variaciones y mejorar la precisión de los registros.")
    st.markdown("**5)** **Implementación de tecnología**: Considerar la implementación de tecnologías como sistemas de gestión de inventario (IMS) o software de análisis para mejorar la visibilidad y el control del inventario en tiempo real.")
# 5. Barra lateral
with st.sidebar:    
    st.title("Navegación")
    st.button("Inicio", on_click=cambiar_vista, args=("inicio",))
    st.button("Bodega", on_click=cambiar_vista, args=("bodega",))
    #st.button("Categorías", on_click=cambiar_vista, args=("categorias",))
    st.button("Ventas", on_click=cambiar_vista, args=("ventas",))
    st.button("Análisis", on_click=cambiar_vista, args=("analisis",))
    st.button("Proveedores", on_click=cambiar_vista, args=("proveedores",))
    st.button("Conclusiones", on_click=cambiar_vista, args=("conclusiones",))