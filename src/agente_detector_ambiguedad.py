import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # fuerza CPU para TF/Keras

from sentence_transformers import SentenceTransformer
from keras.models import load_model

class Agente_detector_ambiguedad:
    def __init__(self):
        print("Agente detector de ambiguedad iniciado")
        self.embedder = SentenceTransformer("/home/maximiliano-gm/Documentos/proyecto_jai_detector_ambiguedad/src/modelo_embeddings", device="cpu")
        self.model = load_model("/home/maximiliano-gm/Documentos/proyecto_jai_detector_ambiguedad/src/modelo_nn_requerimientos")


    def ejecutar(self, requerimiento):
        try:
            texto = requerimiento
            vec = self.embedder.encode([texto])
            pred_prob = self.model.predict(vec)[0][0]
            pred_label = 1 if pred_prob > 0.5 else 0
            resultado = "Ambiguo" if pred_label == 1 else "No ambiguo"

            return {
                "requerimiento": texto,
                "pred_prob": pred_prob,
                "resultado": resultado,
            }
        except Exception as e:
            return {
                "requerimiento": requerimiento,
                "pred_prob": 0,
                "resultado": "Error",
                "mensaje": str(e)
            }
