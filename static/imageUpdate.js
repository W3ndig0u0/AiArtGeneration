let initialGeneration = false;


const progressLabel = document.getElementById('progress-label');
const estimatedTimeElement = document.getElementById('estimated-time');
const progressBar = document.getElementById('progress-bar');

function changeImage(data) {
  var image = document.getElementById('generated-art');
  var folder_path = data.folder_url;
  var img_name = data.img_name;

  var imagePath = folder_path + img_name;

  console.log(imagePath);

  fetch(imagePath)
    .then(function(response) {
      if (!response.ok) {
        throw new Error('Image request failed');
      }
      return response.blob();
    })
    .then(function(blob) {
      var objectURL = URL.createObjectURL(blob);
      image.src = objectURL;
      image.setAttribute('draggable', 'false');
    })
    .catch(function(error) {
      console.error('Error:', error);
    });
}


function generateArt() {
  initialGeneration = false
  const promptInput = document.getElementById('prompt-input').value;
  const negativePromptInput = document.getElementById('negative-prompt-input').value;
  const numInferenceStepsSlider = document.getElementById('num-inference-steps-slider');
  const etaSlider = document.getElementById('eta-slider');
  const guidanceScaleSlider = document.getElementById('guidance-scale-slider');
  const widthInput = document.getElementById('width-input');
  const heightInput = document.getElementById('height-input');
  const batchsizeSlider = document.getElementById('batchsize-slider');
  const seedInput = document.getElementById('seed-input').value;

  if (promptInput === undefined || promptInput === "" || seedInput === undefined || seedInput === "") {
    alert("Please enter a prompt");
    return;
  }

  fakeProgressBarAnimation();

  const requestData = {
    prompt: promptInput,
    negativePromt: negativePromptInput,
    num_inference_steps: numInferenceStepsSlider?.value,
    eta: etaSlider?.value,
    guidance_scale: guidanceScaleSlider?.value,
    width: widthInput?.value,
    height: heightInput?.value,
    batch_size: batchsizeSlider?.value,
    seed: seedInput,
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
      return response.json();
    })
    .then(data => {
      changeImage(data);
      console.log(data);

      realProgressBarAnimation(data);
    })
    .catch(error => {
      alert(error);
    });
}


function fakeProgressBarAnimation() {
  const totalSteps = 90; // Set the total number of steps
  let currentProgress = 0; // Start with 0 progress
  const incrementInterval = 700; // Interval in milliseconds between each increment
  let maxRandomIncrement = 5;

  const incrementProgress = () => {
    if (initialGeneration) {
      return;
    }

    if (currentProgress >= totalSteps) {
      // Reached the end, stop incrementing
      return;
    }

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
    
    // Increment progress randomly
    const randomIncrement = Math.random() * maxRandomIncrement;
    currentProgress += randomIncrement;

    // Update progress bar and label
    const progressPercent = (currentProgress / totalSteps) * 100;
    progressBar.style.width = progressPercent + '%';
    progressLabel.innerText = `Progress: ${currentProgress.toFixed(1)} / ${totalSteps}`;

    setTimeout(incrementProgress, incrementInterval);
  };

  incrementProgress();
}

function realProgressBarAnimation(data) {
  initialGeneration = true;
  const progress = data.progress;      
  const totalSteps = data.total_steps;
  const progressPercent = (progress / totalSteps) * 100;

  progressBar.style.width = 110 + '%';
  progressLabel.innerText = `Progress: ${progress} / ${totalSteps}`;
}