from clasificador_ambiguedad import Clasificador_ambiguedad
from reformulación_requerimiento import Reformulación_requerimiento

class Coordinador:
    def __init__(self):
        self.clasificador = Clasificador_ambiguedad()
        self.reformulador = Reformulación_requerimiento()
    
    async def procesar_requerimiento(self, requerimiento):
        try:
            res_ambiguedad = self.clasificador.analizar_ambiguedad(requerimiento)

            # Si no es ambiguo
            if res_ambiguedad.get("resultado") != "Ambiguo":
                return {
                    "check_ambiguity": res_ambiguedad,
                    "reformulacion": f"El requerimiento '{res_ambiguedad.get('requerimiento', requerimiento)}' es no ambiguo"
                }
            else:
                final_response = await self.reformulador.realizar_reescritura(requerimiento)
                return {
                    "check_ambiguity": res_ambiguedad,
                    "reformulacion": final_response
                }
        except Exception as e:
            return {
                "check_ambiguity": {"resultado": "Error", "pred_prob": 0, "requerimiento": requerimiento, "mensaje": str(e)},
                "reformulacion": f"No se pudo procesar el requerimiento: {e}"
            }
