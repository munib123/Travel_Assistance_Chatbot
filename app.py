import gradio as gr
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key from .env
client = Groq(api_key=os.getenv("GROK_API_KEY"))

system_prompt = "You are a Travel Advisor. Provide helpful travel tips, recommend destinations, and suggest itineraries based on user queries."

def chatbot_response(user_message, history, output_length):
    # Initialize chat history if None
    if history is None:
        history = []
    
    # Build messages list
    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": user_message})
    
    # Adjust response length
    length_modifier = {
        "Concise": "Respond briefly.",
        "Moderate": "Respond with a balanced explanation.",
        "Explained": "Provide a detailed and thorough response."
    }
    messages.append({"role": "system", "content": length_modifier[output_length]})
    
    # Call Groq API
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    # Update history
    history.append((user_message, response.choices[0].message.content))
    return history, history, ""  # Return history for chatbot/state and "" to clear textbox

# Custom CSS for a travel-themed UI
custom_css = """
/* General container styling */
.gradio-container {
    background: linear-gradient(to bottom, #e6f3ff, #ffffff);
    font-family: 'Poppins', sans-serif;
    color: #333;
}

/* Header styling */
h1, h3 {
    color: #1a5f7a;
    text-align: center;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

/* Chatbot area */
.gr-chatbot {
    background: #ffffff;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 20px;
    max-height: 500px;
    overflow-y: auto;
    border: 2px solid #95c8d8;
}

/* Chat messages */
.gr-chatbot .message {
    border-radius: 10px;
    margin: 10px 0;
    padding: 10px 15px;
}
.gr-chatbot .user {
    background: #95c8d8;
    color: #fff;
    text-align: right;
}
.gr-chatbot .assistant {
    background: #e6f3ff;
    color: #333;
    text-align: left;
}

/* Textbox */
.gr-textbox input {
    border: 2px solid #95c8d8;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}
.gr-textbox input:focus {
    border-color: #1a5f7a;
    outline: none;
}

/* Radio buttons */
.gr-radio {
    background: #ffffff;
    border-radius: 10px;
    padding: 15px;
    border: 2px solid #95c8d8;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.gr-radio label {
    color: #1a5f7a;
    font-weight: 600;
}
.gr-radio input[type="radio"]:checked + label {
    color: #0a3d62;
}

/* Buttons */
.gr-button {
    background: #1a5f7a;
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 600;
    transition: background 0.3s ease, transform 0.2s ease;
}
.gr-button:hover {
    background: #0a3d62;
    transform: translateY(-2px);
}
.gr-button:active {
    transform: translateY(0);
}

/* Row layout */
.gr-row {
    gap: 20px;
}

/* Add a subtle background image */
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('https://www.transparenttextures.com/patterns/white-wave.png');
    opacity: 0.1;
    z-index: -1;
}
"""

# Create Gradio interface with Blocks
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🌍 My Travel Advisor Chatbot")
    gr.Markdown("Embark on your next adventure with personalized travel tips and itineraries!")
    
    # Chatbot display
    chatbot = gr.Chatbot(label="Travel Chat", height=500)
    
    # Input components
    with gr.Row():
        user_message = gr.Textbox(
            label="Your Travel Question",
            placeholder="Ask about destinations, tips, or itineraries...",
            lines=2
        )
        output_length = gr.Radio(
            choices=["Concise", "Moderate", "Explained"],
            value="Moderate",
            label="Response Length",
            info="Choose how detailed you
