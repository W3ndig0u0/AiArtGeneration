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