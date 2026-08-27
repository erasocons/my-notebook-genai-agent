import gradio as gr
from .utils import estimar_tokens_notebook, cambiar_modo
from .processor import procesar_notebook

with gr.Blocks(title="Agente Generador de Notebooks") as demo:
    gr.Markdown("# 🤖 Agente de Automatización para Jupyter Notebooks")

    modo_input = gr.Radio(
        choices=["Editar Notebook existente", "Crear Notebook desde cero"],
        value="Editar Notebook existente",
        label="Selecciona el Modo",
        interactive=True
    )

    with gr.Row():
        with gr.Column():
            api_key_input = gr.Textbox(
                label="Gemini API Key", type="password",
                placeholder="Pega tu API Key aquí..."
            )
            file_input = gr.File(label="Sube tu archivo .ipynb", file_types=[".ipynb"])
            btn_tokens = gr.Button("📊 Calcular Tokens", variant="secondary")
            tokens_output = gr.Textbox(label="Estimación de Tokens", interactive=False, lines=1)
            prompt_input = gr.Textbox(label="Instrucciones", lines=5)
            btn_procesar = gr.Button("🚀 Procesar Notebook", variant="primary")

        with gr.Column():
            status_output = gr.Markdown(label="Estado del Proceso")
            file_output = gr.File(label="Descargar Notebook Resultado")

    modo_input.change(fn=cambiar_modo, inputs=[modo_input], outputs=[file_input, btn_tokens, tokens_output])
    btn_tokens.click(fn=estimar_tokens_notebook, inputs=[file_input], outputs=[tokens_output])
    btn_procesar.click(fn=procesar_notebook, inputs=[modo_input, file_input, prompt_input, api_key_input], outputs=[file_output, status_output])

if __name__ == "__main__":
    demo.launch(share=True)
