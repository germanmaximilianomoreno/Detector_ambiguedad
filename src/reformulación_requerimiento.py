import os
import asyncio
import warnings
import logging
from dotenv import load_dotenv

# Ignorar warnings para que no se llene la salida
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

# Importar módulos de GenAI
from google.genai import types
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

class Reformulación_requerimiento:
    def __init__(self, USER_ID="user_1", SESSION_ID="session_001"):
        load_dotenv()  # carga las variables del .env
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        self.APP_NAME = "ambiguity_detector_app"
        self.USER_ID = USER_ID
        self.SESSION_ID = SESSION_ID
        self.MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

        # Crear subagente reformulador
        self.agente_reformulador = Agent(
            name="agente_reformulador",
            model=self.MODEL_GEMINI_2_0_FLASH,
            description="Explica por qué el requerimiento es ambiguo y sugiere una reformulación clara de requerimientos ambiguos.",
            instruction=(
                "Recibe un requerimiento ambiguo y reescríbelo con métricas cuantificables, "
                "criterios objetivos y sin términos vagos, "
                "La respuesta debe tener un máximo de 200 palabras"
            ),
            tools=[]
        )

        # Crear sesión y runner
        self.session_service = InMemorySessionService()
        self.session = asyncio.run(
            self.session_service.create_session(
                app_name=self.APP_NAME,
                user_id=self.USER_ID,
                session_id=self.SESSION_ID
            )
        )

        self.runner = Runner(
            agent=self.agente_reformulador,
            app_name=self.APP_NAME,
            session_service=self.session_service
        )

        print(f"✅ Runner listo para agente '{self.agente_reformulador.name}'.")

    async def realizar_reescritura(self, requerimiento):
            try:
                content = types.Content(
                    role="user",
                    parts=[types.Part(text=requerimiento)]
                )

                final_response = None
                async for event in self.runner.run_async(
                    user_id=self.USER_ID,
                    session_id=self.SESSION_ID,
                    new_message=content
                ):
                    if event.is_final_response():
                        if event.content and event.content.parts:
                            final_response = event.content.parts[0].text
                        break

                if final_response is None:
                    # Si no se obtuvo respuesta, retornar mensaje de error
                    final_response = "No se pudo generar la reformulación. Intenta nuevamente."

                return final_response

            except Exception as e:
                # Retornar mensaje de error en caso de excepción
                return f"No se pudo generar la reformulación debido a un error: {e}"
