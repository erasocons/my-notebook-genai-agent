import gradio as gr
from .utils import estimar_tokens_notebook
from .processor import procesar_notebook


def abrir_tarea(modo, api_key):
    if not api_key or not api_key.strip():
        return (
            modo,
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(
                value="⚠️ Ingresa tu API key de Gemini para continuar.",
                visible=True,
            ),
        )

    es_edicion = modo == "Editar Notebook existente"
    return (
        modo,
        gr.update(visible=False),
        gr.update(visible=True),
        gr.update(visible=es_edicion),
        gr.update(visible=es_edicion),
        gr.update(visible=es_edicion),
        "## Modificar una notebook existente" if es_edicion else "## Crear una notebook desde cero",
        gr.update(value="", visible=False),
    )


def abrir_creacion(api_key):
    return abrir_tarea("Crear Notebook desde cero", api_key)


def abrir_edicion(api_key):
    return abrir_tarea("Editar Notebook existente", api_key)


def limpiar_error_api_key():
    return gr.update(value="", visible=False)


def volver_a_inicio():
    return gr.update(visible=True), gr.update(visible=False)


with gr.Blocks(title="Agente de Automatización para Jupyter Notebooks") as demo:
    modo_state = gr.State("Crear Notebook desde cero")

    with gr.Column(visible=True) as pantalla_inicio:
        gr.Markdown("# 🤖 Agente de Automatización para Jupyter Notebooks")
        gr.Markdown(
            """
            ### Crea y mejora notebooks con ayuda de inteligencia artificial

            Esta herramienta convierte tus instrucciones en notebooks de Jupyter
            con contenido Markdown y código Python. Puedes empezar desde una idea
            o cargar una notebook para modificarla.
            """
        )
        api_key_input = gr.Textbox(
            label="Gemini API Key",
            type="password",
            placeholder="Pega tu API Key aquí...",
        )
        api_key_error = gr.Markdown(visible=False)

        with gr.Row(equal_height=True):
            with gr.Column(scale=2):
                gr.Markdown("**¿Qué quieres hacer hoy?**")
            with gr.Column(scale=1, min_width=280):
                btn_crear = gr.Button("✨ Crear Notebook desde cero", variant="primary")
                btn_editar = gr.Button("📝 Modificar Notebook existente", variant="secondary")

    with gr.Column(visible=False) as pantalla_trabajo:
        with gr.Row():
            btn_volver = gr.Button("← Volver al inicio", scale=0, min_width=150)
            titulo_modo = gr.Markdown("## Crear una notebook desde cero")

        with gr.Row():
            with gr.Column():
                file_input = gr.File(
                    label="Sube tu archivo .ipynb",
                    file_types=[".ipynb"],
                    visible=False,
                )
                btn_tokens = gr.Button("📊 Calcular Tokens", variant="secondary", visible=False)
                tokens_output = gr.Textbox(
                    label="Estimación de Tokens",
                    interactive=False,
                    lines=1,
                    visible=False,
                )
                prompt_input = gr.Textbox(label="Instrucciones", lines=5)
                btn_procesar = gr.Button("🚀 Procesar Notebook", variant="primary")

            with gr.Column():
                status_output = gr.Markdown(label="Estado del Proceso")
                file_output = gr.File(label="Descargar Notebook Resultado")

    api_key_input.input(fn=limpiar_error_api_key, outputs=[api_key_error])
    btn_crear.click(
        fn=abrir_creacion,
        inputs=[api_key_input],
        outputs=[modo_state, pantalla_inicio, pantalla_trabajo, file_input, btn_tokens, tokens_output, titulo_modo, api_key_error],
    )
    btn_editar.click(
        fn=abrir_edicion,
        inputs=[api_key_input],
        outputs=[modo_state, pantalla_inicio, pantalla_trabajo, file_input, btn_tokens, tokens_output, titulo_modo, api_key_error],
    )
    btn_volver.click(fn=volver_a_inicio, outputs=[pantalla_inicio, pantalla_trabajo])
    btn_tokens.click(fn=estimar_tokens_notebook, inputs=[file_input], outputs=[tokens_output])
    btn_procesar.click(
        fn=procesar_notebook,
        inputs=[modo_state, file_input, prompt_input, api_key_input],
        outputs=[file_output, status_output],
    )

if __name__ == "__main__":
    demo.launch(share=True)
