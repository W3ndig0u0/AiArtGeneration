const numInferenceStepsSlider = document.getElementById('num-inference-steps-slider');
numInferenceStepsSlider.addEventListener('input', updateSliderValue);

const etaSlider = document.getElementById('eta-slider');
etaSlider.addEventListener('input', updateSliderValue);

const guidanceScaleSlider = document.getElementById('guidance-scale-slider');
guidanceScaleSlider.addEventListener('input', updateSliderValue);

const batchSizeSlider = document.getElementById('batchsize-slider');
batchSizeSlider.addEventListener('input', updateSliderValue);

function updateSliderValue() {
  const numInferenceStepsValue = document.getElementById('num-inference-steps-slider').value;
  const etaValue = document.getElementById('eta-slider').value;
  const guidanceScaleValue = document.getElementById('guidance-scale-slider').value;

  document.getElementById('num-inference-steps-value').textContent = numInferenceStepsValue;
  document.getElementById('eta-value').textContent = etaValue;
  document.getElementById('guidance-scale-value').textContent = guidanceScaleValue;
  document.getElementById('batchsize-value').textContent = document.getElementById('batchsize-slider').value;
}

let currentWidthRatio = 16;
let currentHeightRatio = 9;

function setDimensions(widthRatio, heightRatio, clickedButton) {
  currentWidthRatio = widthRatio;
  currentHeightRatio = heightRatio;
  

  const dimensions = {
    small: `${widthRatio * 20}x${heightRatio * 20}`,
    medium: `${widthRatio * 40}x${heightRatio * 40}`,
    large: `${widthRatio * 56}x${heightRatio * 56}`,
  };

  const buttons = document.querySelectorAll("#format-buttons-show button span");
  if (buttons.length === 3) {
    buttons[0].textContent = dimensions.small;
    buttons[1].textContent = dimensions.medium;
    buttons[2].textContent = dimensions.large;
  }

  const allDimensionButtons = document.querySelectorAll("#format-buttons-set button");
  allDimensionButtons.forEach((btn) => btn.classList.remove("selected"));
  clickedButton.classList.add("selected");

  updateSize('medium', document.querySelector("#format-buttons-show button:nth-child(2)"));
}

function updateSize(size, clickedButton) {
  const sizeMap = {
    small: 20,
    medium: 40,
    large: 56,
  };

  const multiplier = sizeMap[size];
  const widthInput = document.getElementById("width-input");
  const heightInput = document.getElementById("height-input");

  widthInput.value = currentWidthRatio * multiplier;
  heightInput.value = currentHeightRatio * multiplier;

  const allSizeButtons = document.querySelectorAll("#format-buttons-show button");
  allSizeButtons.forEach((btn) => btn.classList.remove("selected"));
  clickedButton.classList.add("selected");
}

document.addEventListener("DOMContentLoaded", () => {
  const defaultRatioButton = document.querySelector("#format-buttons-set button:nth-child(1)");
  const defaultSizeButton = document.querySelector("#format-buttons-show button:nth-child(2)");
  setDimensions(16, 9, defaultRatioButton);
  updateSize('medium', defaultSizeButton);
});


function limitInputTo77Tokens() {
  var textarea = document.getElementById("prompt-input");
  var wordCountSpan = document.getElementById("word-count");
  var words = textarea.value.trim().split(/\s+/);
  var wordCount = words.length;
  var wordsLeft = 50 - wordCount;

  if (wordsLeft < 0) {
    // If the word count exceeds 77, truncate the input
    words = words.slice(0, 50);
    textarea.value = words.join(" ");
    wordsLeft = 0;
  }

  wordCountSpan.textContent = wordsLeft + " words left";
}
