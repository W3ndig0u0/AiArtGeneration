  const modal = document.createElement('div');
  modal.classList.add('modal');
  modal.id = 'image-modal';
  modal.innerHTML = `
    <div class="modal-content">
      <span class="close">&times;</span>
      <img class="modal-image" alt="Generated Art">
      <div class="modal-text">
        <p class="modal-prompt"></p>
        <p class="modal-negative-prompt"></p>
        <p class="modal-info"></p>
      <div class="button-container">
        <button class="remove-button">Remove Image</button>
        <button class="open-folder-button">Open Folder</button>
      </div>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  const modalImage = modal.querySelector('.modal-image');
  const modalPrompt = modal.querySelector('.modal-prompt');
  const modalNegativePrompt = modal.querySelector('.modal-negative-prompt');
  const modalInfo = modal.querySelector('.modal-info');
  const closeButton = modal.querySelector('.close');
  const removeButton = modal.querySelector('.remove-button');
  const openFolderButton = modal.querySelector('.open-folder-button');

  const fetchJsonData = () => {
    return fetch('./static/imageJson.json')
    .then(response => response.json())
      .then(data => {
      return data;
      });
  };

  const openModal = (image) => {
    const modalImage = modal.querySelector('.modal-image');
    const modalPrompt = modal.querySelector('.modal-prompt');
    const modalNegativePrompt = modal.querySelector('.modal-negative-prompt');
    const modalInfo = modal.querySelector('.modal-info');
  
    modalImage.src = image.src;
  
    fetchJsonData().then(data => {
      const imageName = image.src.split('/').pop();
      const imageData = getImageData(imageName, data);
  
      if (imageData !== undefined) {
        const { prompt, negativePromt, width, height, num_inference_steps, eta, guidance_scale, seed,  get_active_model, vae } =  imageData.settings;
        const { img_name, folder_url } = imageData;
        modalPrompt.textContent = `Prompt: ${prompt}`;
        modalNegativePrompt.textContent = `Negative Prompt: ${negativePromt}`;
        modalInfo.innerHTML = `
          <p>Image Name: ${img_name}</p>
          <p>Size: ${width} x ${height}</p>
          <p>Number of Inference Steps: ${num_inference_steps}</p>
          <p>Eta: ${eta}</p>
          <p>Guidance Scale: ${guidance_scale}</p>
          <p>Seed: ${seed}</p>
          <p>Ai Model: ${get_active_model}</p>
          <p>VAE: ${vae}</p>
          <p>Folder URL: ${folder_url}</p>
        `;
      } else {
        modalPrompt.innerHTML = "";
        modalInfo.innerHTML = "<p>Image generated in an older version. No settings found.</p>";
        modalNegativePrompt.innerHTML = "";
      }
  
      // Show the modal
      modal.style.display = 'block';
    });
  };
  
  function getImageData(imageName, data) {
    if (data && data.hasOwnProperty(imageName)) {
      return data[imageName];
    }
    return undefined;
  }
  
  // Close the modal when the close button is clicked
  closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  removeButton.addEventListener('click', () => {
    //image.remove();
    alert("Function not added");
  });

  openFolderButton.addEventListener('click', () => {
    fetchJsonData().then(data => {
      const folderUrl = data.folder_url;
      alert("Function not added: folder at : " + folderUrl)
    });
  });

  function getActiveImgs() {
    const imageElements = document.getElementsByClassName('image');

    Array.from(imageElements).forEach(function(imageElement) {
      const imageUrl = imageElement.src;

      imageElement.addEventListener('click', function() {
        openModal(this);
      });

    });
  }