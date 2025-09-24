from agente_detector_ambiguedad import Agente_detector_ambiguedad
from agente_reescritura import Agente_reescritura

class Main:
    def __init__(self):
        # Inicializar agentes una sola vez
        self.agente_ambiguo = Agente_detector_ambiguedad()
        self.agente_reescritura = Agente_reescritura()
    
    def check_ambiguity(self, requerimiento):
        try:
            return self.agente_ambiguo.ejecutar(requerimiento)
        except Exception as e:
            return {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento, "mensaje": str(e)}
    
    async def procesar_requerimiento(self, requerimiento):
        try:
            res_ambiguedad = self.check_ambiguity(requerimiento)

            # Si no es ambiguo
            if res_ambiguedad.get("resultado") != "Ambiguo":
                return {
                    "check_ambiguity": res_ambiguedad,
                    "reformulacion": f"El requerimiento '{res_ambiguedad.get('requerimiento', requerimiento)}' es no ambiguo"
                }
            else:
                final_response = await self.agente_reescritura.realizar_reescritura(requerimiento)
                return {
                    "check_ambiguity": res_ambiguedad,
                    "reformulacion": final_response
                }
        except Exception as e:
            return {
                "check_ambiguity": {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento, "mensaje": str(e)},
                "reformulacion": f"No se pudo procesar el requerimiento: {e}"
            }
