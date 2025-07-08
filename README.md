# 🎧 SonicVision AI — Turn Sound into Stunning Visuals 🌌  
### by Cosmoss Innovations

**SonicVision AI** is an advanced, interactive web app that transforms **audio into AI-generated images** using OpenAI's Whisper and Stable Diffusion.

> Speak it. See it. Feel it.

---

## 🚀 Features

- 🎤 Convert **voice/audio recordings** into text using Whisper
- 🎨 Generate **images from text prompts** using Stable Diffusion (v1.5)
- ✂️ Built-in image editing: crop and resize
- 🌐 Web UI powered by Gradio with immersive 3D design
- 🧠 Edit your prompt before generation
- 📥 Download generated images directly
- ⚙️ Full compatibility with CPU or GPU

---

## 🧠 Tech Stack

| Component      | Tool/Model                                 |
|----------------|---------------------------------------------|
| Audio-to-Text  | [OpenAI Whisper](https://github.com/openai/whisper) |
| Text-to-Image  | [Stable Diffusion v1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5) |
| UI             | [Gradio](https://gradio.app)               |
| Backend        | Python, Torch, Diffusers, Transformers     |
| Styling        | Custom CSS (3D, glowing buttons, animations) |

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/sonicvision-ai.git
cd sonicvision-ai

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
