document.addEventListener('DOMContentLoaded', function() {
  let initialGeneration = false;

  const progressLabel = document.getElementById('progress-label');
  const estimatedTimeElement = document.getElementById('estimated-time');
  const progressBar = document.getElementById('progress-bar');

  function changeImage(data) {
      // Ensure data is valid and contains necessary properties
      if (!data || !data.folder_url || !data.img_name) {
          console.error('Invalid data:', data);
          return;
      }

      var image = document.getElementById('generated-art');
      var folder_path = data.folder_url;
      var imagePath = folder_path + data.img_name;

      console.log('Image path:', imagePath); // Log the image path

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
              console.error('Error fetching image:', error);
          });

      var stepElement = document.getElementById('current-step');
      if (stepElement) {
          stepElement.textContent = 'Step: ' + data.progress;
      } else {
          console.error('current-step element not found');
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
          alert("Please enter a prompt and a seed");
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

      console.log('Request Data:', requestData); // Log request data

      fetch('/generate_art', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
      })
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              console.log('Response Data:', data); // Log response data
              changeImage(data);
              realProgressBarAnimation(data);
          })
          .catch(error => {
              alert('Error: ' + error.message);
          });
  }

  let progressAnimationId;

  function fakeProgressBarAnimation() {
      const totalSteps = 90;
      let currentProgress = 0;
      const incrementInterval = 1000;
      let maxRandomIncrement = 3;

      const incrementProgress = () => {
          if (initialGeneration) {
              return;
          }

          if (currentProgress >= totalSteps - 10) {
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

          progressAnimationId = setTimeout(incrementProgress, incrementInterval);
      };

      clearTimeout(progressAnimationId);
      currentProgress = 0;
      progressBar.style.width = '0%';

      incrementProgress();
  }

  function realProgressBarAnimation(data) {
      initialGeneration = true;
      const progress = data.progress;
      const totalSteps = data.total_steps;

      if (progress !== undefined && totalSteps !== undefined) {
          const progressPercent = (progress / totalSteps) * 100;

          progressBar.style.width = progressPercent + '%'; // Updated to reflect actual progress
          progressLabel.innerText = `Progress: ${progress} / ${totalSteps}`;
      } else {
          console.error('Invalid progress data:', data);
      }
  }

  // Expose the generateArt function to the global scope
  window.generateArt = generateArt;
});
