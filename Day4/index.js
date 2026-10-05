const randomNumber = Math.floor(Math.random() * 20);
const inputElement = document.getElementById("userinput");
const messageElement = document.getElementById("randomvalue");
const checkButton = document.getElementById("checkButton");

function checkGuess() {
    const guess = Number(inputElement.value);

    if (inputElement.value.trim() === "" || !Number.isInteger(guess) || guess < 0 || guess > 19) {
        messageElement.textContent = "Enter a whole number from 0 to 19.";
        return;
    }

    if (guess === randomNumber) {
        messageElement.textContent = "You won! That is the lucky number.";
    } else {
        messageElement.textContent = "You lost. " + guess + " is not the lucky number.";
    }
}

checkButton.addEventListener("click", checkGuess);
inputElement.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        checkGuess();
    }
});
