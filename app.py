import gradio as gr

def read_file(file):
    with open(file.name, 'r') as f:
        content = f.read()
    return content

interface = gr.Interface(
    fn=read_file,
    inputs=gr.inputs.File(file_count="single", label="Upload a text file"),
    outputs=gr.outputs.Textbox(label="File Content"),
    title="Text File Reader"
)

interface.launch()
