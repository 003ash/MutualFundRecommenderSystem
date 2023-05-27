let timerObj = {
    minutes: 0,
    seconds: 0,
    timerId: 0
};

function soundAlarm() {
    let amount = 3;
    let audio = new Audio("Timer_Sound_Effect.mp3");

    function playSound() {
        audio.pause();
        audio.currentTime = 0;
        audio.play();
    }

    for (let i = 0; i < amount; i++) {
        setTimeout(playSound, 1000 * i);
    }
}

function updateValue(key, value) {
    let secondsInput = document.getElementById("seconds-input");
    let minutesInput = document.getElementById("minutes-input");
    if (secondsInput.value > 59) {
        secondsInput.value = 59;
    }
    if (minutesInput.value > 300) {
        minutesInput.value = 300;
    }
    if (value < 0) {
        value = 0;
        console.log("Positive values only!");
    }
    if (value > 300 && key == "minutes") {
        value = 300;
    }
    if (value > 59 && key == "seconds") {
        value = 59;
    }
    if (key == "seconds" && value < 10) {
        value = "0" + value;
    }

    $("#" + key).html(value || 0);
    timerObj[key] = value;
}

(function detectChanges(key) {
    let input = "#" + key + "-input";
    $(input).change(function() {
        updateValue(key, $(input).val());
    });
    $(input).keyup(function() {
        updateValue(key, $(input).val());
    });

    return arguments.callee;
})("minutes")("seconds");

function startTimer() {
    let startButton = document.getElementById("start-button");
    let stopButton = document.getElementById("stop-button");
    let pauseButton = document.getElementById("pause-button");
    startButton.disabled = true;
    stopButton.disabled = false;
    pauseButton.disabled = false;
    let secondsInput = document.getElementById("seconds-input");
    let minutesInput = document.getElementById("minutes-input");
    secondsInput.disabled = true;
    minutesInput.disabled = true;
    timerObj.timerId = setInterval(function() {
        timerObj.seconds--;
        if (timerObj.seconds < 0) {
            if (timerObj.minutes == 0) {
                soundAlarm();
                return stopTimer();
            }
            timerObj.seconds = 59;
            timerObj.minutes--;
        }
        updateValue("minutes", timerObj.minutes);
        updateValue("seconds", timerObj.seconds);
    }, 1000);
}
function stopTimer() {
    let startButton = document.getElementById("start-button");
    let stopButton = document.getElementById("stop-button");
    let pauseButton = document.getElementById("pause-button");
    startButton.disabled = false;
    stopButton.disabled = true;
    pauseButton.disabled = true;
    let secondsInput = document.getElementById("seconds-input");
    let minutesInput = document.getElementById("minutes-input");
    secondsInput.disabled = false;
    minutesInput.disabled = false;
    clearInterval(timerObj.timerId);
    let seconds = secondsInput.value;
    if (seconds == 0) {
        seconds = "0" + seconds;
    }
    updateValue("minutes", minutesInput.value);
    updateValue("seconds", seconds);
}

function pauseTimer() {
    let startButton = document.getElementById("start-button");
    let stopButton = document.getElementById("stop-button");
    let pauseButton = document.getElementById("pause-button");
    startButton.disabled = false;
    stopButton.disabled = false;
    pauseButton.disabled = true;
    clearInterval(timerObj.timerId);
}
