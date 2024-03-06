let mediaRecorder;
let audioChunks = [];

document.getElementById("startRecordBtn").onclick = () => {
    // Clear highlights from all labels at the start of a new recording
    document.querySelectorAll('.label').forEach(label => {
        label.classList.remove('highlight');
    });

    // Clear transcription text at the start of a new recording
    document.getElementById("transcription").textContent = ""; // or "Preparing transcription..." as a placeholder

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];

                const formData = new FormData();
                formData.append("audio", audioBlob, "input.wav");
                
                fetch("http://127.0.0.1:5000/classify", {
                    method: "POST",
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) { 
                        document.getElementById("transcription").textContent = data.transcription;
                        
                        // Highlight the correct label based on the server's response
                        let labelToHighlight = Array.from(document.querySelectorAll('.label')).find(label => label.textContent === data.label);
                        if (labelToHighlight) {
                            labelToHighlight.classList.add('highlight');
                        }
                    } else {
                        document.getElementById("transcription").textContent = "Error processing audio."; 
                        // Handle error case appropriately
                    }
                })
                .catch(error => console.error("Error:", error));
            };

            document.getElementById("stopRecordBtn").disabled = false;
        });
};

document.getElementById("stopRecordBtn").onclick = () => {
    mediaRecorder.stop();
    document.getElementById("stopRecordBtn").disabled = true;
};




