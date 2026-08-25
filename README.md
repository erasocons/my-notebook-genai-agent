# 🤖 Notebook GenAI Agent

Un agente interactivo para **crear y editar Jupyter Notebooks automáticamente** usando la API de **Gemini (Google GenAI)** y una interfaz gráfica con **Gradio**.

---

## 🚀 Características
- **Editar notebooks existentes**: reestructura, corrige y mejora un `.ipynb` según instrucciones del usuario.
- **Generar notebooks desde cero**: crea un cuaderno completo con celdas Markdown y código Python.
- **Estimación de tokens**: calcula el tamaño aproximado del notebook en tokens.
- **Interfaz amigable**: construida con Gradio para facilitar la interacción.

---

## 📦 Requisitos
- Python 3.9+
- Paquetes:
  - `nbformat`
  - `pydantic`
  - `google-genai`
  - `gradio`

Instalación rápida:

```bash
pip install nbformat pydantic google-genai gradio
