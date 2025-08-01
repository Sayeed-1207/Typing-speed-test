const texts = {
  Easy: [
    "I love Python.",
    "Typing is fun.",
    "Speed is key.",
    "Practice every day.",
    "Code more, worry less.",
    "Fast fingers win races.",
    "Python makes things easy."
  ],
  Medium: [
    "Python is a versatile programming language used in many fields.",
    "Accuracy and speed both matter in typing tests.",
    "Always try to improve your typing skill consistently.",
    "Typing with accuracy builds long-term speed.",
    "Functions in Python can return multiple values.",
    "Writing clean code helps reduce bugs and errors."
  ],
  Hard: [
    "In computer science, performance and precision are equally critical metrics.",
    "Achieving mastery in typing requires effort, discipline, and regular training.",
    "Multithreading and multiprocessing are advanced Python topics for parallel execution.",
    "Memory management and garbage collection are crucial for scalable applications.",
    "Syntax errors are easier to fix than logical bugs in complex code.",
    "Efficient algorithms and data structures lead to faster software performance."
  ]
};

let timer;
let startTime;
let timeLimit = 30;
let errorCount = 0;
let targetText = "";

function startTest() {
  const name = document.getElementById("username").value.trim();
  const difficulty = document.getElementById("difficulty").value;
  const inputBox = document.getElementById("userInput");
  const resultBox = document.getElementById("results");

  targetText = texts[difficulty][Math.floor(Math.random() * texts[difficulty].length)];
  timeLimit = parseInt(document.getElementById("timeLimit").value) || 30;
  errorCount = 0;

  document.getElementById("targetText").textContent = targetText;
  inputBox.value = "";
  inputBox.disabled = false;
  inputBox.focus();
  document.getElementById("timer").textContent = `Time: ${timeLimit}`;
  document.getElementById("errors").textContent = "Errors: 0";
  document.getElementById("wpm").textContent = "WPM: 0";
  resultBox.innerHTML = "";

  startTime = new Date();
  clearInterval(timer);
  timer = setInterval(() => updateTest(name), 1000);
}

function updateTest(name) {
  const input = document.getElementById("userInput").value;
  const elapsed = (new Date() - startTime) / 1000;

  const remaining = Math.max(0, Math.ceil(timeLimit - elapsed));
  document.getElementById("timer").textContent = `Time: ${remaining}`;
  if (remaining <= 0) {
    endTest(name);
    return;
  }
  const words = input.length / 5;
  const wpm = Math.round(words / (elapsed / 60));
  document.getElementById("wpm").textContent = `WPM: ${wpm}`;
  errorCount = 0;
  for (let i = 0; i < input.length; i++) {
    if (input[i] !== targetText[i]) errorCount++;
  }
  document.getElementById("errors").textContent = `Errors: ${errorCount}`;
  if (input === targetText) {
    endTest(name);
  }
}

function endTest(name) {
  clearInterval(timer);
  document.getElementById("userInput").disabled = true;
  const finalWpm = document.getElementById("wpm").textContent;
  document.getElementById("results").textContent = `✅ Well done, ${name}! Your final ${finalWpm}`;
}
