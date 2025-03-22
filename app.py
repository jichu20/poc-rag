import gradio as gr
import os
from commons.binaries import process_document

theme = gr.themes.Base()
demo = gr.Blocks(theme=theme)

with demo:
    gr.Markdown("# Prueba de concepto RAG + ChromaDB")
    with gr.Row():
        with gr.Column():
            gr.Markdown("## Seleciona un documento para poder hacer preguntas")
            upload_file = gr.File(label="Upload new document.", interactive=True)
    with gr.Row():
        with gr.Column():
            vertex_chatbot = gr.Chatbot(
                [[None, "Welcome!"]],
                label="cahtbot - IPA - cachivache",
                avatar_images=["assets/chat.png", "assets/googleAvatar.png"],
            )
        with gr.Column():
            gr.Markdown("## Introduce tu pregunta")
            question = gr.Textbox(label="Preguntame")

    # Funciones
    upload_file.change(
        process_document,
        inputs=[upload_file],
        # outputs=status,
    )

demo.load(show_progress=True)
demo.queue().launch(
    server_name=os.getenv("SERVER_ADDRESS", "localhost"),
    server_port=int(os.getenv("GRADIO_PORT", 7860)),
)
