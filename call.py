from openai import OpenAI
import base64 
import os
from dotenv import load_dotenv
from flask import jsonify 


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
async def call(base64_audio, contacts):

    binary_audio = base64.b64decode(base64_audio)
    audio_file_path = "temp_audio_file.mp3"
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(binary_audio)
    
    try:
        transcription_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=open(audio_file_path, "rb")
        )
        transcription_text = transcription_response['choices'][0]['text']
        
        # Prompt Sample
        # prompt = f"Given the following contact list:\n{contacts}\nand the recording: '{transcription_text}'"
        
        # Send the prompt to ChatGPT
        chat_response = client.completions.create(
            model="gpt-3.5-turbo-0125",  
            response_format={"type", "json_object"},
            messages=[
              {"role": "system", "content": "return me a json with a prop name and phone number. If this person is not in the list, return me empty string for both these props"},
              {"role": "user", "content": f"""Given the following contact list:\n{contacts}\nand the recording: {transcription_text}"""}
            ],
            temperature=0,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        
        response_text = chat_response['choices'][0]['text'].strip()
        name, number = response_text.split(', ')
        name = name.split(': ')[1]
        number = number.split(': ')[1]
        
        print(response_text)

        return jsonify({'name': name, 'number': number})

    except Exception as e:
        return jsonify({'error': str(e)})

