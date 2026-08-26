import os
import tempfile
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook
from google import genai
from google.genai import types
from models import NotebookFullResponse
from utils import extraer_contenido_notebook

def procesar_notebook(modo, file_obj, user_instructions, api_key):
    if modo == "Editar Notebook existente" and file_obj is None:
        return None, "⚠️ Por favor, sube un archivo .ipynb válido para editar."
    
    if not user_instructions.strip():
        return None, "⚠️ Por favor, escribe las instrucciones para la notebook."

    key_a_usar = api_key.strip() if api_key else os.environ.get("GEMINI_API_KEY", "")
    if not key_a_usar:
        return None, "⚠️ Por favor, ingresa tu API Key de Gemini."

    try:
        if modo == "Editar Notebook existente":
            _, contenido_cuaderno = extraer_contenido_notebook(file_obj)
            system_instruction = (
                "Eres un experto en Data Science y Python. "
                "Reestructura el cuaderno completo según las instrucciones del usuario."
            )
            prompt = f"""
Contenido original del notebook:
---
{contenido_cuaderno}
---

Instrucciones del usuario:
"{user_instructions}"
"""
            nombre_base = os.path.splitext(os.path.basename(file_obj.name))[0]
            output_filename = f"{nombre_base}_modificado.ipynb"

        else:
            system_instruction = (
                "Eres un experto en Data Science y Python. "
                "Crea un cuaderno desde cero con celdas Markdown y código."
            )
            prompt = f"""
Solicitud del usuario:
"{user_instructions}"
"""
            output_filename = "notebook_generado.ipynb"

        client = genai.Client(api_key=key_a_usar)
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=NotebookFullResponse,
                temperature=0.2,
            ),
        )

        resultado: NotebookFullResponse = response.parsed
        nuevo_nb = new_notebook()

        for cell_data in resultado.notebook_cells:
            if cell_data.cell_type.lower() == 'markdown':
                nuevo_nb.cells.append(new_markdown_cell(cell_data.content))
            elif cell_data.cell_type.lower() == 'code':
                nuevo_nb.cells.append(new_code_cell(cell_data.content))

        output_path = os.path.join(tempfile.gettempdir(), output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            nbformat.write(nuevo_nb, f)

        mensaje_exito = f"✅ Proceso completado.\n\n**Resumen:**\n{resultado.summary}"
        return output_path, mensaje_exito

    except Exception as e:
        return None, f"❌ Error: {str(e)}"
