import streamlit as st
import numpy as np
import plotly.graph_objects as go
import asyncio
from coordinador import Coordinador

def analizar_requerimiento(requerimiento):
    try:
        modulo_coordinador = Coordinador()
        respuesta = asyncio.run(modulo_coordinador.procesar_requerimiento(requerimiento))
        if respuesta is None:
            # Retornar dict por defecto si la coroutine devuelve None
            return {
                "check_ambiguity": {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento},
                "reformulacion": "No se pudo procesar el requerimiento."
            }
        return respuesta
    except Exception as e:
        # Captura cualquier excepción y devuelve un dict válido
        return {
            "check_ambiguity": {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento, "mensaje": str(e)},
            "reformulacion": f"No se pudo procesar el requerimiento debido a un error: {e}"
        }

# Función recursiva para convertir todos los tipos no serializables
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

# Configuración de la página: Wide mode activado
st.set_page_config(
    page_title="Detector de Ambigüedad",
    layout="wide",
    initial_sidebar_state="auto"
)

# Título principal
st.title("🔍 Detector de Ambigüedad de Requerimientos")

# Input del usuario
requerimiento_usuario = st.text_area(
    "✍️ Ingresa tu requerimiento aquí:",
    placeholder="Ej: El sistema debe ser rápido y seguro"
)

# Botón para enviar el requerimiento
if st.button("📤 Analizar Requerimiento") and requerimiento_usuario:
    # Llamada a la función de análisis
    respuesta = analizar_requerimiento(requerimiento_usuario)
    respuesta_serializable = convertir_objeto(respuesta)

    # Crear dos columnas
    col1, col2 = st.columns(2)

    # -------- Columna 1: Requerimiento y Reformulación --------
    with col1:
        st.subheader("📌 Requerimiento original")
        st.write(respuesta_serializable["check_ambiguity"])

        st.subheader("✏️ Reformulación sugerida")
        st.markdown(respuesta_serializable["reformulacion"])

    # -------- Columna 2: Probabilidad de ambigüedad --------
    with col2:
        st.subheader("📊 Probabilidad de ambigüedad")

        pred_prob = respuesta_serializable["check_ambiguity"]["pred_prob"]  # valor entre 0 y 1
        porcentaje = round(pred_prob * 100, 2)

        # Crear gráfico circular tipo dona
        fig = go.Figure(go.Pie(
            values=[porcentaje, 100-porcentaje],
            labels=[f"Ambiguo {porcentaje}%", f"No ambiguo {100-porcentaje}%"],
            hole=0.6,
            marker_colors=["#EF553B", "#00CC96"]
        ))
        fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))

        st.plotly_chart(fig, use_container_width=True)

        st.write(f"Predicción de ambigüedad: **{respuesta['check_ambiguity']['resultado']}**")
