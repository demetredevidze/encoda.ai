from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import librosa
import torch
import os
import logging

# Load BERT model for text classification
bert_tokenizer = AutoTokenizer.from_pretrained("a-b-a/bert_qiib_v0")
bert_model = AutoModelForSequenceClassification.from_pretrained("a-b-a/bert_qiib_v0")

# Load Whisper model for speech-to-text
whisper_processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
whisper_model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3")

# Define your label names based on the model's training
label_names = [
    "Phone Banking Services",
    "Lost or Stolen Card",
    "Offers/General Information",
    "Suggestions/Complaints",
    "New Customer",
    "Card Activation & Pin Services",
    "Working Hours",
    "Speak to an Agent",
    "Special Offers"
]

logger = logging.getLogger(__name__)  # Configure as per your logging setup


import subprocess
import os

def convert_audio_to_wav(input_path, output_path, sample_rate=16000):
    """
    Converts an audio file to WAV format with a specific sample rate,
    ensuring compatibility with audio processing libraries.
    """
    try:
        # Build the ffmpeg command for converting the audio
        command = [
            'ffmpeg',
            '-y',  # Overwrite output file if it exists
            '-i', input_path,  # Input file
            '-acodec', 'pcm_s16le',  # Output codec (PCM 16-bit signed little-endian)
            '-ar', str(sample_rate),  # Output sample rate
            '-ac', '1',  # Output to mono channel
            output_path  # Output file
        ]
        # Execute the ffmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Audio converted and saved to {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert audio: {e.stderr}")
        return False


def transcribe_and_classify():
    audio_path0 = os.path.join(os.getcwd(), 'hello.wav')

    audio_path0 = os.path.join(os.getcwd(), 'input.wav')
    audio_path = os.path.join(os.getcwd(), 'converted_input.wav')

    if not convert_audio_to_wav(audio_path0, audio_path):
        return {    
            "success": False,
            "error": "Failed to convert audio file to compatible format."
        }
    try:
        logger.debug("Loading and resampling the audio file.")
        audio_input, sample_rate = librosa.load(audio_path, sr=16000)

        logger.debug("Preprocessing input for Whisper.")
        whisper_inputs = whisper_processor(audio_input, sampling_rate=sample_rate, return_tensors="pt")

        logger.debug("Generating transcript with Whisper.")
        generated_ids = whisper_model.generate(**whisper_inputs)

        logger.debug("Decoding the generated ids to get the transcript.")
        transcription = whisper_processor.decode(generated_ids[0], skip_special_tokens=True)

        logger.debug("Processing the transcription with BERT tokenizer.")
        inputs = bert_tokenizer(transcription, return_tensors="pt")

        logger.debug("Predicting with BERT model.")
        with torch.no_grad():
            outputs = bert_model(**inputs)

        logger.debug("Extracting the logits and converting to probabilities.")
        probabilities = torch.softmax(outputs.logits, dim=1)

        logger.debug("Getting the predicted label index.")
        predicted_label_index = probabilities.argmax()
        predicted_label = label_names[predicted_label_index.item()]

        return {
            "success": True,
            "transcription": transcription,
            "label_index": predicted_label_index.item(),
            "label": predicted_label
        }
    except Exception as e:
        logger.error("An error occurred in transcribe_and_classify: %s", e, exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }
