# Encoder AI Model

This project is part of Encoder.ai's initiative to revolutionize call centers through the integration of AI technology. Encoder AI Model demonstrates how AI can be utilized to automate call center operations, specifically in understanding customer queries through voice and instantly classifying them into predefined categories. This simplifies the process of navigating through menu options and allows for direct connection to the appropriate service or agent, significantly reducing wait times and improving customer experience.

## Description

The Encoder AI Model is a Flask-based web application that integrates advanced AI models for speech recognition and text classification. Utilizing OpenAI's Whisper for speech-to-text conversion and a pre-trained BERT model for classification, this demo showcases the potential of AI in streamlining call center operations by providing immediate classification of customer queries into specific labels.

## Getting Started

### Dependencies

- Python 3.8+
- Flask
- Flask-Cors
- librosa
- transformers
- Pre-trained models from Hugging Face (Whisper large v3, BERT)

### Installing

Clone the repository and install the required Python packages:

git clone https://github.com/demetredevidze/encoda-ai-model.git
cd encoda-ai-model
pip install -r requirements.txt


### Executing Program

To run the application, use the following command:

python3 server.py

### Interacting with the model

After starting the server, open your web browser and navigate to the location specified by Flask, typically http://127.0.0.1:5000/, to interact with the application. You can start a recording, articulate your query, and upon stopping the recording, the system will process and display both the transcription and the identified label. 


### Project Structure

- `model.py`: Contains the logic for loading the AI models (Whisper and BERT), performing speech-to-text conversion, and classifying the transcribed text into predefined labels.
- `server.py`: The Flask application server. It defines the web routes and handles the interaction between the frontend and the AI processing in `model.py`.
- files used by the web application `script.js` and `style.css`
- The main file is `index.html`, which provides the UI for recording audio and displaying results.
- `requirements.txt`: Lists all Python dependencies required to run the application, ensuring easy setup in different environments.


### Contributing

```markdown
Your contributions are welcome! Please follow the standard process for contributing to open-source projects:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourAmazingFeature`).
3. Commit your changes (`git commit -m 'Add some YourAmazingFeature'`).
4. Push to the branch (`git push origin feature/YourAmazingFeature`).
5. Create a new Pull Request.


### Support

For support, feedback, or issues, please email me at [demetredevidze2000@gmail.com](mailto:demetredevidze2000@gmail.com).

### Licence

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

### Contact

- **GitHub**: [demetredevidze](https://github.com/demetredevidze)
- **LinkedIn**: [Demetre Devidze](https://www.linkedin.com/in/demetre-devidze/)
