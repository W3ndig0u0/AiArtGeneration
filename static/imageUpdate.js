document.addEventListener('DOMContentLoaded', function() {
  updateGeneratedArt();
});

function updateGeneratedArt() {
  fetch('/generate_art')
    .then(response => response.json())
    .then(data => {
      const imgElement = document.getElementById('generated-art');
      imgElement.src = data.generated_art_url;

      const progressBar = document.getElementById('progress-bar');
      const progressLabel = document.getElementById('progress-label');
      const progress = data.progress;
      const totalSteps = data.total_steps;
      const progressPercent = (progress / totalSteps) * 100;
      progressBar.style.width = progressPercent + '%';
      progressLabel.innerText = `Progress: ${progress} / ${totalSteps}`;

      if (!data.generation_complete) {
        setTimeout(updateGeneratedArt, 1000);
      } else {
        const estimatedTime = data.estimated_time;
        const estimatedTimeElement = document.getElementById('estimated-time');
        estimatedTimeElement.innerText = `Estimated Time Left: ${estimatedTime}`;
      }
    })
    .catch(error => console.log(error));
}
