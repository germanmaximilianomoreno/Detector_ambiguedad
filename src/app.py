import streamlit as st
import numpy as np
import plotly.graph_objects as go
import asyncio
from coordinador import Coordinador
import os

# ---------------- FUNCIONES PRINCIPALES ---------------- #

def analizar_requerimiento(requerimiento):
    try:
        modulo_coordinador = Coordinador()
        respuesta = asyncio.run(modulo_coordinador.procesar_requerimiento(requerimiento))
        if respuesta is None:
            return {
                "check_ambiguity": {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento},
                "reformulacion": "No se pudo procesar el requerimiento."
            }
        return respuesta
    except Exception as e:
        return {
            "check_ambiguity": {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento, "mensaje": str(e)},
            "reformulacion": f"No se pudo procesar el requerimiento debido a un error: {e}"
        }

def convertir_objeto(obj):
    if isinstance(obj, dict):
        return {k: convertir_objeto(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_objeto(x) for x in obj]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    else:
        return obj


# ---------------- CONFIGURACIÓN DE PÁGINA ---------------- #

st.set_page_config(
    page_title="Detector de Ambigüedad",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- ESTILO CSS ---------------- #

# Ruta absoluta al archivo CSS (siempre relativa al archivo actual)
css_path = os.path.join(os.path.dirname(__file__), "style.css")

with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- INTERFAZ ---------------- #

st.markdown("<h2 font-size:1.6rem; font-weight:600; color:#222;'>Detector de Ambigüedad de Requerimientos</h2>", unsafe_allow_html=True)

st.markdown("Analiza tus requerimientos y detecta posibles ambigüedades en su redacción.")

requerimiento_usuario = st.text_area(
    "Ingresa tu requerimiento:",
    placeholder="Ejemplo: El sistema debe ser rápido y seguro",
    height=120
)

if st.button("Analizar Requerimiento") and requerimiento_usuario:
    respuesta = analizar_requerimiento(requerimiento_usuario)
    respuesta_serializable = convertir_objeto(respuesta)

    st.markdown("---")

    # Crear dos columnas equilibradas
    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        st.subheader("Resultado del análisis")

        probabilidad = respuesta_serializable["check_ambiguity"]["pred_prob"]
        texto = (
            f"**Requerimiento:** {respuesta_serializable['check_ambiguity']['requerimiento']}  \n"
            f"**Probabilidad de ambigüedad:** {probabilidad:.2%}  \n"
            f"**Etiqueta:** {respuesta_serializable['check_ambiguity']['resultado']}"
        )
        st.markdown(texto)

        st.subheader("Reformulación sugerida")
        st.markdown(f"<div class='reformulacion'>{respuesta_serializable['reformulacion']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='text-align:center;'>Probabilidad</h3>", unsafe_allow_html=True)
        pred_prob = respuesta_serializable["check_ambiguity"]["pred_prob"]
        porcentaje = round(pred_prob * 100, 2)

        fig = go.Figure(go.Pie(
            values=[porcentaje, 100-porcentaje],
            labels=[f"Ambiguo {porcentaje}%", f"No ambiguo {100-porcentaje}%"],
            hole=0.7,
            marker_colors=["#FF6B6B", "#A0E7A0"]
        ))
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=250,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)
