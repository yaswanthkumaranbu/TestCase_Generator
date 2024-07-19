from main import generate_test_cases
import gradio as gr
import os

# Global variable to store the content
global_content = None

# Ensure the output folder exists
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def read_file_and_convert(file, output_filename):
    global global_content
    
    if file is None:
        return "No file uploaded", None
    try:
        with open(file.name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Store content in global variable
        global_content = content
        
        # Generate testcases
        Result = generate_test_cases(global_content)
        
        # Ensure the filename ends with .json
        if not output_filename.lower().endswith('.json'):
            output_filename += '.json'
        
        # Create the full path for the output file
        output_path = os.path.join(output_folder, output_filename)
        
        # Write the Result directly to the JSON file
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json_file.write(Result)

        return content, output_path
      
    except Exception as e:
        return f"Error processing file: {str(e)}", None
    
interface = gr.Interface(
    fn=read_file_and_convert,
    inputs=[
        gr.File(file_count="single", label="Upload a text file"),
        gr.Textbox(label="Output JSON filename", placeholder="e.g., output.json")
    ],
    outputs=[
        gr.Textbox(label="File Content"),
        gr.File(label="Download JSON")
    ],
    title="Functional Testcase Generator",
)

interface.launch()