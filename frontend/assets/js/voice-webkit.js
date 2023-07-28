window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition
    if ('SpeechRecognition' in window) {
        console.log("SpeechRecognition is Working");
    } else {
        console.log("SpeechRecognition is Not Working");
    }

    var inputSearchQuery = document.getElementById("search_query");
    const recognition = new window.SpeechRecognition();
    //recognition.continuous = true;

    micButton = document.getElementById("mic_search");

    micButton.addEventListener('click', function () {
        if (micButton.innerHTML == "mic") {
            recognition.start();
        } else if (micButton.innerHTML == "mic_off") {
            recognition.stop();
        }

        recognition.addEventListener("start", function () {
            micButton.innerHTML = "mic_off";
            console.log("Recording.....");
        });

        recognition.addEventListener("end", function () {
            console.log("Stopping recording.");
            micButton.innerHTML = "mic";
        });

        recognition.addEventListener("result", resultOfSpeechRecognition);
        function resultOfSpeechRecognition(event) {
            const current = event.resultIndex;
            transcript = event.results[current][0].transcript;
            inputSearchQuery.value = transcript;
            console.log("transcript : ", transcript)
        }
    });