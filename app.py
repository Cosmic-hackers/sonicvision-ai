
import os
import torch
import gradio as gr
from diffusers import StableDiffusionPipeline
import whisper
from datetime import datetime
from PIL import Image

# Ensure 'generatedimages' folder exists
os.makedirs("generatedimages", exist_ok=True)

# Load AI Models
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda" if torch.cuda.is_available() else "cpu")
model = whisper.load_model("base")

# Function: Convert Text to Image & Save
def generate_image(prompt):
    with torch.inference_mode():
        image = pipe(prompt).images[0]

    filename = f"generatedimages/{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    image.save(filename)

    return image, filename

# Function: Convert Audio to Text
def audio_to_text(audio):
    result = model.transcribe(audio)
    return result["text"]

# Function: Convert Audio to Image & Save
def audio_to_image(audio):
    text = audio_to_text(audio)
    return text, text  # Return the transcribed text for both fields

# Function: Generate Image from Edited Prompt
def generate_from_edited_prompt(edited_prompt):
    image, filename = generate_image(edited_prompt)
    return image, filename

# Function: Clear Inputs & Outputs
def clear_all():
    return None, None, "", "", None, "", None, None

# Function: Crop Image
def crop_image(image, x1, y1, x2, y2):
    cropped_image = image.crop((x1, y1, x2, y2))
    return cropped_image

# Function: Resize Image
def resize_image(image, width, height):
    resized_image = image.resize((width, height))
    return resized_image

# Custom CSS for a Modern, 3D Look
custom_css = """
body {
    background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
    color: white;
    font-family: 'Poppins', sans-serif;
    margin: 0;
    padding: 0;
}
.gradio-container {
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
}
h1 {
    font-size: 3.5rem;
    font-weight: bold;
    color: #ff9800;
    text-shadow: 0px 0px 20px rgba(255,152,0,0.8);
}
p {
    font-size: 1.2rem;
    color: #bbb;
}
button {
    background: linear-gradient(45deg, #ff9800, #ff5722);
    color: white;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 1.2rem;
    box-shadow: 0px 5px 15px rgba(255,152,0,0.6);
    border: none;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}
button:hover {
    background: linear-gradient(45deg, #ff5722, #ff9800);
    transform: scale(1.05);
}
input, textarea {
    border-radius: 12px;
    padding: 14px;
    border: 2px solid #ff9800;
    background: rgba(255, 255, 255, 0.1);
    color: #00ff00; /* Change text color to green */
    transition: transform 0.3s;
}
input:focus, textarea:focus {
    transform: scale(1.02);
    outline: none;
}
.gradio-image {
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(255,152,0,0.5);
    transition: transform 0.3s;
}
.gradio-image:hover {
    transform: scale(1.05) rotateY(5deg);
}
.audio-player {
    background: rgba(255, 255, 255, 0.1);
    padding: 15px;
    border-radius: 15px;
    transform-style: preserve-3d;
    transition: transform 0.3s;
}
.audio-player:hover {
    transform: rotateY(10deg);
}
/* Header and Navbar Styles */
.header {
    background: rgba(0, 0, 0, 0.7);
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar {
    display: flex;
    gap: 20px;
}
.navbar a {
    color: #ff9800;
    text-decoration: none;
    font-size: 1.2rem;
    transition: color 0.3s;
}
.navbar a:hover {
    color: #ff5722;
}
.hero {
    background: linear-gradient(135deg, rgba(13, 13, 13, 0.8), rgba(26, 26, 26, 0.8)), url('https://via.placeholder.com/1200x400');
    background-size: cover;
    background-position: center;
    padding: 100px 20px;
    text-align: center;
    margin-bottom: 40px;
}
.hero h1 {
    font-size: 4rem;
    margin-bottom: 20px;
}
.hero p {
    font-size: 1.5rem;
    color: #bbb;
}
/* Full-width rows */
.full-width-row {
    width: 100%;
    padding: 20px;
    background: rgba(255, 255, 255, 0.05);
    margin-bottom: 20px;
}
/* Ensure text in textboxes is visible */
textarea, input[type="text"] {
    color: #00ff00 !important; /* Change text color to green */
}
/* Enhanced Logo Styles */
.logo {
    font-family: 'Montserrat', sans-serif; /* Use a modern sans-serif font */
    font-size: 2.5rem;
    font-weight: bold;
    color: #ff9800; /* Solid orange color */
    text-transform: uppercase; /* Uppercase text for a bold look */
    letter-spacing: 2px; /* Add spacing between letters */
    position: relative;
    display: inline-block;
}
.logo::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -5px;
    width: 100%;
    height: 3px;
    background: #ff9800; /* Underline effect */
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease-in-out;
}
.logo:hover::after {
    transform: scaleX(1);
    transform-origin: left;
}
/* Download Button Styles */
.download-btn {
    background: linear-gradient(45deg, #4CAF50, #81C784);
    color: white;
    border-radius: 12px;
    padding: 14px 20px;
    font-size: 1.2rem;
    box-shadow: 0px 5px 15px rgba(76, 175, 80, 0.6);
    border: none;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}
.download-btn:hover {
    background: linear-gradient(45deg, #81C784, #4CAF50);
    transform: scale(1.05);
}
/* Audio Player Controls */
.audio-controls {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-top: 10px;
}
.audio-controls button {
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid #ff9800;
    padding: 10px;
    border-radius: 8px;
    color: #ff9800;
    cursor: pointer;
    transition: background 0.3s, color 0.3s;
}
.audio-controls button:hover {
    background: #ff9800;
    color: white;
}
.audio-controls button i {
    font-size: 1.2rem;
}
"""

# Custom HTML for the Header with Enhanced Logo
header_html = """
<header class="header">
    <div class="logo">cosmoss AI</div>
    <nav class="navbar">
        <a href="#features">Features</a>
        <a href="#about">About</a>
        <a href="#contact">Contact</a>
    </nav>
</header>
"""

hero_html = """
<section class="hero">
    <h1>Welcome to cosmoss AI</h1>
    <p>Transform your ideas into stunning visuals with the power of AI.</p>
</section>
"""

# Gradio UI with Enhanced Features
with gr.Blocks(css=custom_css, theme="soft") as demo:
    # Inject Header and Hero Section
    gr.HTML(header_html)
    gr.HTML(hero_html)

    gr.Markdown("### Convert *Text or Audio* into AI-generated *Stunning Images*")

    with gr.Row(elem_classes="full-width-row"):
        with gr.Column():
            gr.Markdown("### 🎤 Upload, Record & Play Audio")
            audio_input = gr.Audio(type="filepath", label="🎧 Upload or Record Audio", interactive=True, elem_classes="audio-player")
            transcribed_text = gr.Textbox(label="📝 Transcribed Text", interactive=False)
            edit_prompt = gr.Textbox(label="✏ Edit Prompt", placeholder="Edit the transcribed text here...", interactive=True)
            image_output_audio = gr.Image(label="🎨 Generated Image from Audio", elem_classes="gradio-image")
            file_path_audio = gr.Textbox(label="📂 Saved File Path", interactive=False)
            download_btn_audio = gr.Button("📥 Download Image", elem_classes="download-btn")
            convert_btn = gr.Button("🎵 Convert Audio to Image")
            generate_from_edit_btn = gr.Button("🖌 Generate Image from Edited Prompt")

        with gr.Column():
            gr.Markdown("### 🖼 Generate AI Image from Text")
            text_input = gr.Textbox(label="📜 Enter Prompt", placeholder="Describe an image...", interactive=True)
            image_output_text = gr.Image(label="🎨 Generated Image", elem_classes="gradio-image")
            file_path_text = gr.Textbox(label="📂 Saved File Path", interactive=False)
            download_btn_text = gr.Button("📥 Download Image", elem_classes="download-btn")
            generate_btn = gr.Button("🖌 Generate Image")

    # Audio Player Controls with Icons
    with gr.Row(elem_classes="full-width-row"):
        gr.Markdown("## 🎧 *Audio Player Controls*")
        with gr.Column():
            audio_controls_html = """
            <div class="audio-controls">
                <button onclick="recordAudio()"><i class="fas fa-microphone"></i> Record</button>
                <button onclick="stopAudio()"><i class="fas fa-stop"></i> Stop</button>
                <button onclick="resumeAudio()"><i class="fas fa-play"></i> Resume</button>
                <button onclick="playAudio()"><i class="fas fa-play"></i> Play</button>
                <button onclick="pauseAudio()"><i class="fas fa-pause"></i> Pause</button>
                <button onclick="forwardAudio()"><i class="fas fa-forward"></i> Forward</button>
                <button onclick="rewindAudio()"><i class="fas fa-backward"></i> Rewind</button>
                <button onclick="trimAudio()"><i class="fas fa-cut"></i> Trim</button>
            </div>
            """
            gr.HTML(audio_controls_html)

    # Image Editing Tools
    with gr.Row(elem_classes="full-width-row"):
        gr.Markdown("## 🖼 *Image Editing Tools*")
        x1 = gr.Number(label="X1", value=0)
        y1 = gr.Number(label="Y1", value=0)
        x2 = gr.Number(label="X2", value=512)
        y2 = gr.Number(label="Y2", value=512)
        crop_btn = gr.Button("✂ Crop Image")
        width = gr.Number(label="Width", value=512)
        height = gr.Number(label="Height", value=512)
        resize_btn = gr.Button("🖼 Resize Image")

    with gr.Row(elem_classes="full-width-row"):
        clear_btn = gr.Button("🧹 Clear All")

    # Button Actions
    convert_btn.click(
        audio_to_image,
        inputs=audio_input,
        outputs=[transcribed_text, edit_prompt]
    ).then(
        generate_image,
        inputs=transcribed_text,
        outputs=[image_output_audio, file_path_audio]
    )

    generate_from_edit_btn.click(
        generate_from_edited_prompt,
        inputs=edit_prompt,
        outputs=[image_output_audio, file_path_audio]
    )

    generate_btn.click(
        generate_image,
        inputs=text_input,
        outputs=[image_output_text, file_path_text]
    )

    crop_btn.click(
        crop_image,
        inputs=[image_output_audio, x1, y1, x2, y2],
        outputs=image_output_audio
    )

    resize_btn.click(
        resize_image,
        inputs=[image_output_audio, width, height],
        outputs=image_output_audio
    )

    clear_btn.click(
        clear_all,
        outputs=[audio_input, image_output_audio, transcribed_text, file_path_audio, text_input, image_output_text, file_path_text, edit_prompt]
    )

    # Download Button Actions
    download_btn_audio.click(
        lambda file_path: file_path,
        inputs=file_path_audio,
        outputs=file_path_audio
    )

    download_btn_text.click(
        lambda file_path: file_path,
        inputs=file_path_text,
        outputs=file_path_text
    )
# ... your Gradio UI definition above ...

# ✅ Launch app
if __name__ == "__main__":
    demo.launch()
