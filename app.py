import pandas as pd
import plotly.express as px
import streamlit as st

# Cargar los datos
data = pd.read_csv('vehicles_us.csv')

# Reemplazo de valores ausentes
data['model'] = data['model'].str.lower()
data['type'] = data['type'].str.lower()
data['is_4wd'] = data['is_4wd'].fillna(0)
data['model_year'] = data.groupby('model')['model_year'].transform(
    lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.mean()))
data['odometer'] = data['odometer'].fillna(data['odometer'].median())
data['cylinders'] = data['cylinders'].fillna(data['cylinders'].median())
data['paint_color'] = data['paint_color'].fillna(data['paint_color'].mode()[0])

# Convertir columnas numéricas a enteros
data['model_year'] = data['model_year'].astype(int)
data['is_4wd'] = data['is_4wd'].astype(int)
data['cylinders'] = data['cylinders'].astype(int)
data['odometer'] = data['odometer'].astype(int)

# **Corrección: Extraer fabricante desde modelo**
data['manufacturer'] = data['model'].str.split().str[0].str.lower()

# Mostrar datos en la web
st.write('# Conjunto de datos de venta de coches')
st.dataframe(data, use_container_width=True)

# **Botón para generar histograma**
hist_button = st.button("Generar histograma de odometer")

if hist_button:
    st.write("Creación de un histograma para el conjunto de datos de anuncios de venta de coches")
    fig = px.histogram(data, x="odometer", title="Distribución del kilometraje")
    st.plotly_chart(fig, use_container_width=True)

# **Botón para generar gráfica de barras apiladas**
bar_chart_button = st.button("Generar gráfica de barras apiladas por modelo")

if bar_chart_button:
    st.write("Distribución de vehículos por modelo y condición")

    # Contar cantidad de vehículos por modelo y condición
    model_counts = data.groupby(['model', 'condition']).size().reset_index(name='count')

    # Crear la gráfica de barras apiladas
    fig = px.bar(model_counts, x='model', y='count', color='condition',
                 title="Número de vehículos por modelo y condición",
                 labels={'model': 'Modelo', 'count': 'Cantidad', 'condition': 'Condición'},
                 barmode='stack')

    # Rotar etiquetas del eje X para mejor visibilidad
    fig.update_layout(xaxis={'tickangle': -45})

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)

# **Corrección: Crear lista de fabricantes sin error**
manufacturers = sorted(data['manufacturer'].unique())



# Mostrar título
st.write("# Gráfico de Burbujas: Relación entre Precio y Kilometraje")

# Crear el gráfico de burbujas
fig = px.scatter(data, x="odometer", y="price", 
                 size="cylinders", color="type", 
                 title="Distribución de precios según kilometraje",
                 labels={'odometer': 'Kilometraje', 'price': 'Precio', 'cylinders': 'Cilindros', 'type': 'Tipo de vehículo'},
                 hover_data=["model"])

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig, use_container_width=True)



# Convertir valores a minúsculas para mayor uniformidad
data['paint_color'] = data['paint_color'].str.lower()
data['condition'] = data['condition'].str.lower()



# **Checkbox para gráfico de cilindros**
show_cylinders_pie = st.checkbox("Mostrar gráfico de cilindros")

if show_cylinders_pie:
    st.write("Distribución de vehículos por número de cilindros")
    fig_cylinders = px.pie(data, names="cylinders", title="Distribución por Número de Cilindros", 
                           labels={'cylinders': 'Cilindros'}, hole=0.3)
    st.plotly_chart(fig_cylinders, use_container_width=True)

# **Checkbox para gráfico de condición**
show_condition_pie = st.checkbox("Mostrar gráfico de condición del vehículo")

if show_condition_pie:
    st.write("Distribución de vehículos por condición")
    fig_condition = px.pie(data, names="condition", title="Distribución por Condición del Vehículo", 
                           labels={'condition': 'Condición'}, hole=0.3)
    st.plotly_chart(fig_condition, use_container_width=True)
    