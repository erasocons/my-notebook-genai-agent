
"""
Punto de entrada principal del proyecto Notebook GenAI Agent.
Lanza la interfaz gráfica construida con Gradio.
"""

from src.interface import demo

if __name__ == "__main__":
    # Ejecuta la aplicación Gradio
    demo.launch(share=True)
