import nbformat
import gradio as gr

def extraer_contenido_notebook(file_obj):
    if file_obj is None:
        return None, None
    
    with open(file_obj.name, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
        
    codigo_y_texto = []
    for idx, cell in enumerate(nb.cells):
        prefix = f"[Celda {idx+1} - {cell.cell_type.upper()}]"
        codigo_y_texto.append(f"{prefix}\n{cell.source}")

    contenido_cuaderno = "\n\n".join(codigo_y_texto)
    return nb, contenido_cuaderno


def estimar_tokens_notebook(file_obj):
    if file_obj is None:
        return "⚠️ Por favor, sube un archivo .ipynb primero."

    _, contenido_cuaderno = extraer_contenido_notebook(file_obj)
    total_caracteres = len(contenido_cuaderno)
    estimacion_tokens = total_caracteres // 4
    return f"~{estimacion_tokens:,} tokens"


def cambiar_modo(modo):
    es_editar = (modo == "Editar Notebook existente")
    return gr.update(visible=es_editar), gr.update(visible=es_editar), gr.update(visible=es_editar)
