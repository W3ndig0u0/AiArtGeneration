function upscaleImage() {
  const chosenImageUrl = document.getElementById("chosen-image").getAttribute("src");

  document.getElementById("upscaled-image").src = "https://cdn.dribbble.com/users/2081/screenshots/4645074/loading.gif";

  fetch(`/upscale_image?image=${encodeURIComponent(chosenImageUrl)}`)
    .then(response => response.json())
    .then(data => {
      document.getElementById("upscaled-image").src = data.upscaled_image;
    })
    .catch(error => {
      console.log(error);
      alert("Error occurred while upscaling the image. Please try again.");
    });
}

document.getElementById("upscale-button").addEventListener("click", upscaleImage);
