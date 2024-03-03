from openai import OpenAI
import base64 
import os
from dotenv import load_dotenv
from flask import jsonify 
import whisper
import json
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
async def call(base64_audio, contacts):

    binary_audio = base64.b64decode(base64_audio)
    audio_file_path = "temp_audio_file.mp3"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(binary_audio)
    
    try:
        model = whisper.load_model("base")
        result = model.transcribe("temp_audio_file.mp3")
        print(result["text"])
        # with open(audio_file_path, "rb") as audio_file:
        #     transcription_response = client.audio.transcriptions.create(
        #         model="whisper-1",
        #         file=(audio_file)
        # )
        # transcription_text = transcription_response.text
        # print(transcription_text)
        
        # Prompt Sample
        # prompt = f"Given the following contact list:\n{contacts}\nand the recording: '{transcription_text}'"
        
        # Send the prompt to ChatGPT
        chat_response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": """Given a contact list and a recording, return a JSON object with a 'name', 'mode', and 'phone number'. If the person is not in the list, return an empty string for all properties.
                 Example: 
                 {
                        "name": "John Doe",
                        "phone number": "123-456-7890",
                        "mode": "call" | "text"
                        "message": only if mode is "text"
                 }
                 """},
                {"role": "user", "content": f"Given the following contact list:\n{contacts}\nand the recording: '{result['text']}'"}
            ]
        )

        # Assuming the chat_response['choices'][0]['message']['content'] contains the JSON string with 'name' and 'phone number'
        response_content = chat_response.choices[0].message.content
        print(response_content)

    
        # Extract ```json``` from the response
        if response_content.startswith("```json"):
            response_content = response_content.split("```json")[1]
        if response_content.endswith("```"):
            response_content = response_content.split("```")[0]
        obj = json.loads(response_content)
        print(obj)
        return jsonify(obj)

    except Exception as e:
        return jsonify({'error': str(e)})

