let initialGeneration = false;

const progressLabel = document.getElementById('progress-label');
const estimatedTimeElement = document.getElementById('estimated-time');
const progressBar = document.getElementById('progress-bar');

function changeImage(data) {
  const image = document.getElementById('generated-art');
  if (!image || !data.folder_url || !data.img_name) {
    console.error("Image element or data properties missing.");
    return;
  }

  const imagePath = data.folder_url + data.img_name;
  console.log("Image path:", imagePath);

  fetch(imagePath)
    .then(response => {
      if (!response.ok) throw new Error('Image request failed');
      return response.blob();
    })
    .then(blob => {
      const objectURL = URL.createObjectURL(blob);
      image.src = objectURL;
      image.setAttribute('draggable', 'false');
    })
    .catch(error => {
      console.error('Error loading image:', error);
    });

  const stepElement = document.getElementById('current-step');
  if (stepElement) {
    stepElement.textContent = `Step: ${data.progress ?? 0}`;
  }
}

function generateArt() {
  initialGeneration = false;
  const promptInput = document.getElementById('prompt-input').value;
  const negativePromptInput = document.getElementById('negative-prompt-input').value;
  const numInferenceStepsSlider = document.getElementById('num-inference-steps-slider');
  const etaSlider = document.getElementById('eta-slider');
  const guidanceScaleSlider = document.getElementById('guidance-scale-slider');
  const widthInput = document.getElementById('width-input');
  const heightInput = document.getElementById('height-input');
  const batchsizeSlider = document.getElementById('batchsize-slider');
  const seedInput = document.getElementById('seed-input').value;

  if (!promptInput || !seedInput) {
    alert("Please enter a prompt and seed value.");
    return;
  }

  fakeProgressBarAnimation();

  const requestData = {
    prompt: promptInput,
    negativePrompt: negativePromptInput,
    num_inference_steps: numInferenceStepsSlider?.value,
    eta: etaSlider?.value,
    guidance_scale: guidanceScaleSlider?.value,
    width: widthInput?.value,
    height: heightInput?.value,
    batch_size: batchsizeSlider?.value,
    seed: seedInput,
    initial_generation: initialGeneration
  };

  console.log("Request data:", requestData);

  fetch('/generate_art', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
  })
    .then(response => {
      if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
      return response.json();
    })
    .then(data => {
      changeImage(data);
      realProgressBarAnimation(data);
    })
    .catch(error => {
      alert(`An error occurred: ${error.message}`);
      console.error("Fetch error:", error);
    });
}

let progressAnimationId;

function fakeProgressBarAnimation() {
  const totalSteps = 90;
  let currentProgress = 0;
  const incrementInterval = 1000;
  let maxRandomIncrement = 3;

  const incrementProgress = () => {
    if (initialGeneration) return;

    if (currentProgress >= totalSteps - 10) return;

    if (currentProgress >= totalSteps - 50) {
      maxRandomIncrement = 2;
    } else if (currentProgress >= totalSteps - 30) {
      maxRandomIncrement = 0.5;
    } else if (currentProgress >= totalSteps - 15) {
      maxRandomIncrement = 0.1;
    } else if (currentProgress >= totalSteps - 5) {
      maxRandomIncrement = 0;
      return;
    }

    const randomIncrement = Math.random() * maxRandomIncrement;
    currentProgress += randomIncrement;
    const progressPercent = (currentProgress / totalSteps) * 100;

    if (progressBar && progressLabel) {
      progressBar.style.width = `${progressPercent}%`;
      progressLabel.innerText = `Progress: ${currentProgress.toFixed(1)} / ${totalSteps}`;
    }

    progressAnimationId = setTimeout(incrementProgress, incrementInterval);
  };

  clearTimeout(progressAnimationId);
  currentProgress = 0;
  if (progressBar) progressBar.style.width = '0%';

  incrementProgress();
}

function realProgressBarAnimation(data) {
  initialGeneration = true;
  const progress = data.progress ?? 0;
  const totalSteps = data.total_steps ?? 100;
  const progressPercent = (progress / totalSteps) * 100;

  if (progressBar && progressLabel) {
    progressBar.style.width = `${progressPercent}%`;
    progressLabel.textContent = `Progress: ${progress} / ${totalSteps}`;
  }
}
