function sendModelDownloadText() {
  var labelText = document.getElementById("modelDownload").value.trim();
  alert('Model is starting to download, wait a few minutes');

  fetch('/downloadModel', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ labelText: labelText }),
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error sending label text to backend');
      }
    })
    .then(data => {
      alert('Model downloaded successfully');
      console.log('Response from backend:', data);
    })

    .catch(error => {
      alert('Could not download the model:' + error);
    });
}

document.getElementById("modelDownload").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendModelDownloadText();
  }
});
