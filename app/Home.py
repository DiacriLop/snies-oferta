"""
Punto de entrada de la aplicación Streamlit.
Contiene el menú principal, navegación y presentación general.
No debe contener lógica de procesamiento, limpieza o filtros. 
Debe delegar esto a la capa de services.
"""
import streamlit as st

st.set_page_config(
    page_title="Dashboard SNIES",
    page_icon="🇨🇴",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Estilos personalizados (CSS)
st.markdown("""
<style>
.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: #1E3A8A;
    text-align: center;
    margin-bottom: 0px;
    padding-top: 2rem;
}
.subtitle {
    font-size: 1.2rem;
    color: #4B5563;
    text-align: center;
    margin-bottom: 3rem;
    margin-top: 10px;
}
.card {
    border-radius: 10px;
    padding: 20px;
    background-color: #F3F4F6;
    height: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Sistema de Análisis SNIES</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explora la Oferta y Demanda de la Educación Superior en Colombia</div>', unsafe_allow_html=True)

st.divider()

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 🎓 Oferta Académica")
    st.write(
        "Analiza los programas activos, acreditaciones, instituciones y el comportamiento "
        "de las maestrías y doctorados a nivel nacional y departamental."
    )
    st.write("") # Espacio
    # Botón nativo de Streamlit que redirige de forma elegante
    st.page_link("pages/1_oferta.py", label="Ir al Módulo de Oferta", icon="📊")

with col2:
    st.markdown("### 👥 Demanda Académica")
    st.write(
        "Explora las estadísticas de matrícula, inscritos, admitidos y graduados, "
        "segmentando por diferentes variables demográficas y niveles académicos."
    )
    st.write("") # Espacio
    # Botón nativo de Streamlit que redirige de forma elegante
    st.page_link("pages/2_demanda.py", label="Ir al Módulo de Demanda", icon="📈")

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

st.info("💡 **Tip:** También puedes usar el menú lateral a tu izquierda para navegar rápidamente entre los diferentes módulos.")
