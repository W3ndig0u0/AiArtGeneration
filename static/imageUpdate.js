document.addEventListener('DOMContentLoaded', function() {
  updateGeneratedArt();
});

function updateGeneratedArt() {
  fetch('/get_generated_art')  // Modify the route according to your Flask app's configuration
    .then(response => response.json())
    .then(data => {
      const imgElement = document.getElementById('generated-art');
      imgElement.src = data.generated_art_url;

      if (!data.generation_complete) {
        setTimeout(updateGeneratedArt, 1000);
      }
    })
    .catch(error => console.log(error));
}
