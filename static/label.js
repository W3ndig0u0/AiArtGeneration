// ?Iput
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


function limitInputTo77Tokens() {
  var textarea = document.getElementById("prompt-input");
  var wordCountSpan = document.getElementById("word-count");
  var words = textarea.value.trim().split(/\s+/); // Split the input into words
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
