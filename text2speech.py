import os
import base64
from dotenv import load_dotenv
import openai

# Step 3.1: Load environment variables from your .env file
load_dotenv()

# Step 3.2: Retrieve configuration values
endpoint = os.getenv("AZURE_GPT_ENDPOINT")        # e.g., "https://avina-m7vw4icv-eastus2.cognitiveservices.azure.com"
api_key = os.getenv("AZURE_GPT_API_KEY")            # your Azure OpenAI key
deployment = os.getenv("AZURE_GPT_DEPLOYMENT_NAME")      # e.g., "gpt-4o-audio-preview"

# Validate that required variables are set
if not endpoint or not api_key or not deployment:
    print("One or more environment variables are missing. Please check your .env file.")
    exit(1)

# Step 3.3: Configure the OpenAI library for Azure
openai.api_type = "azure"
openai.api_base = endpoint                # Base endpoint (do not include extra path segments)
openai.api_version = "2025-01-01-preview"  # Use the preview API version that supports audio
openai.api_key = api_key

def generate_conversational_response(prompt):
    """
    Generate a conversational response with both text and audio using the GPT‑4o preview audio model.
    """
    try:
        response = openai.ChatCompletion.create(
            deployment_id=deployment,          # Use deployment_id to specify your Azure deployment
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": prompt}
            ],
            modalities=["text", "audio"],       # Request both text and audio outputs
            audio={"voice": "alloy", "format": "wav"}   # Specify desired voice and audio file format
        )

        # Extract text response
        assistant_message = response['choices'][0]['message']
        text_reply = assistant_message.get("content")
        print("Assistant reply (text):", text_reply)

        # Extract the audio response (base64 encoded)
        audio_data_base64 = assistant_message.get("audio", {}).get("data")
        if audio_data_base64:
            with open("response.wav", "wb") as f:
                f.write(base64.b64decode(audio_data_base64))
            print("Audio saved to response.wav")
        else:
            print("No audio data was returned.")

        return text_reply

    except Exception as e:
        print("An error occurred while generating the response:", e)
        return None

if __name__ == "__main__":
    test_prompt = "Hello! I'm your voice assistant. Let's fill in this form together."
    generate_conversational_response(test_prompt)
