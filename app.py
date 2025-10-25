import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página (opcional pero buena práctica)
st.set_page_config(
    page_title="Análisis de Anuncios de Venta de Coches",
    page_icon="🚗",
    layout="wide"
)

# --- Encabezado y Descripción ---
st.header('Análisis Interactivo de Anuncios de Venta de Coches Usados')
st.markdown(
    """
    Esta aplicación te permite explorar visualizaciones de datos del conjunto 
    de anuncios de venta de vehículos en EE. UU.
    
    Selecciona las casillas de verificación a continuación para generar 
    histogramas y diagramas de dispersión interactivos.
    """
)

# Cargar los datos
# Nota: Asume que el archivo 'vehicles_us_clean.csv' está en el mismo directorio.
try:
    car_data = pd.read_csv('./data/vehicles_us_clean.csv')
except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'vehicles_us_clean.csv'. Asegúrate de que esté en el mismo directorio.")
    st.stop()

# Rellenar valores nulos para 'odometer' y 'cylinders' para permitir la graficación
# (una estrategia simple para este ejercicio, en un caso real se necesitaría un análisis más profundo)
car_data['odometer'] = car_data['odometer'].fillna(
    car_data['odometer'].median())
car_data['cylinders'] = car_data['cylinders'].fillna(0).astype(
    int)  # Usar 0 o imputar con modo/mediana si es apropiado

# --- Opciones de Casillas de Verificación ---

st.subheader('Selecciona las visualizaciones a mostrar:')
col1, col2 = st.columns(2)

with col1:
    build_histogram = st.checkbox(
        'Construir Histograma de Kilometraje (Odómetro)')

with col2:
    build_scatter = st.checkbox(
        'Construir Diagrama de Dispersión de Precio vs. Kilometraje')


# --- Generación de Gráficos basada en Checkbox ---

if build_histogram:  # Si la casilla de verificación del histograma está seleccionada
    st.markdown('### Histograma de Kilometraje')
    st.write(
        'Distribución de la columna `odometer` (kilometraje) en el conjunto de datos.')

    # Crear un histograma
    fig = px.histogram(
        car_data,
        x="odometer",
        title="Distribución del Kilometraje (Odómetro)",
        labels={'odometer': 'Kilometraje'},
        color_discrete_sequence=['#42A5F5']
    )

    # Mostrar el gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)

if build_scatter:  # Si la casilla de verificación del diagrama de dispersión está seleccionada
    st.markdown('### Diagrama de Dispersión: Precio vs. Kilometraje')
    st.write('Relación entre el `price` (precio) y el `odometer` (kilometraje).')

    # Crear un diagrama de dispersión
    fig = px.scatter(
        car_data,
        x="odometer",
        y="price",
        title="Precio vs. Kilometraje",
        labels={'odometer': 'Kilometraje', 'price': 'Precio ($)'},
        color="condition",  # Colorear por la condición del coche para más contexto
        hover_data=['model_year', 'model']
    )

    # Mostrar el gráfico Plotly interactivo
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.info(
    "¡Gracias por usar la aplicación de análisis de datos de coches!")
