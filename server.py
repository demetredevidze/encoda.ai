from flask import Flask, request, jsonify
import os
from model import transcribe_and_classify  # Assuming this is your custom function
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

app.logger.setLevel(logging.DEBUG)  # Log more information

@app.route('/classify', methods=['POST'])
def classify_audio():
    if 'audio' not in request.files:
        return jsonify(success=False, error="No audio part in the request")

    audio_file = request.files['audio']
    audio_path = os.path.join(os.getcwd(), 'input.wav')

    try:
        audio_file.save(audio_path)  # Save the audio file once
        app.logger.debug("Audio file received: %s", audio_file.filename)
        app.logger.debug("Saving audio file to: %s", audio_path)
        app.logger.debug("Audio file saved successfully")
        
        # Note: If you want to check the file size after saving, use the os.path.getsize() function
        file_size = os.path.getsize(audio_path)
        app.logger.debug("Audio file size (bytes): %s", file_size)

        result = transcribe_and_classify()  # Process the saved audio file
        return jsonify(result)
    except Exception as e:
        app.logger.error("Error processing audio file: %s", e)
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)






