let initialGeneration = true;

function generateArt() {
  const promptInput = document.getElementById('prompt-input').value;
  const negativePromptInput = document.getElementById('negative-prompt-input').value;

  console.log(negativePromptInput);

  const numInferenceStepsSlider = document.getElementById('num-inference-steps-slider');
  const etaSlider = document.getElementById('eta-slider');
  const guidanceScaleSlider = document.getElementById('guidance-scale-slider');
  const widthInput = document.getElementById('width-input');
  const heightInput = document.getElementById('height-input');
  const batchsizeSlider = document.getElementById('batchsize-slider');
  const seedInput = document.getElementById('seed-input');

  const requestData = {
    prompt: promptInput,
    negativePromt : negativePromptInput,
    num_inference_steps: numInferenceStepsSlider?.value,
    eta: etaSlider?.value,
    guidance_scale: guidanceScaleSlider?.value,
    width: widthInput?.value,
    height: heightInput?.value,
    batch_size: batchsizeSlider?.value,
    seed: seedInput.value,
    initial_generation: initialGeneration
  };
  console.log(requestData);

  fetch('/generate_art', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => {
      console.log(response);
      return response.json();
    })
    .then(data => {
      console.log(data.response);
      const imgElement = document.getElementById('generated-art');
      imgElement.src = data.generated_art_url;

      const progressBar = document.getElementById('progress-bar');
      const progressLabel = document.getElementById('progress-label');
      const estimatedTimeElement = document.getElementById('estimated-time');

      updateGeneratedArt(data, progressBar, progressLabel, estimatedTimeElement);
    })
    .catch(error => {
      console.log(error);
    });
}

// Update the generated art, progress bar, progress label, and estimated time
function updateGeneratedArt(data, progressBar, progressLabel, estimatedTimeElement) {
  const progress = data.progress;
  const totalSteps = data.total_steps;
  const progressPercent = (progress / totalSteps) * 100;
  progressBar.style.width = progressPercent + '%';
  progressLabel.innerText = `Progress: ${progress} / ${totalSteps}`;

  console.log(`Progress: ${progress} / ${totalSteps}`);
  console.log(`Generated Art URL: ${data.generated_art_url}`);

  if (!data.generation_complete) {
    setTimeout(() => {
      initialGeneration = false;
      generateArt();
    }, 1000);
  } else {
    const estimatedTime = data.estimated_time;
    estimatedTimeElement.innerText = `Estimated Time Left: ${estimatedTime}`;
    initialGeneration = true;  // Reset the flag for the next generation
  }
}

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