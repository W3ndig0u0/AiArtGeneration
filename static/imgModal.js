let currentImageFileName = '';
let selectedModalImage = null;

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
        <button class="download-button">Download Image</button>
        <button class="upscaling-button">Upscale Image</button>
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
  const downloadButton = modal.querySelector('.download-button');
  const upscalingButton = modal.querySelector('.upscaling-button');

  const fetchJsonData = () => {
    return fetch('./static/imageJson.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        return data;
      })
      .catch(error => {
        console.error('An error occurred:', error);
      });
  };
  

  const openModal = (image) => {
    const modalImage = modal.querySelector('.modal-image');
    const modalPrompt = modal.querySelector('.modal-prompt');
    const modalNegativePrompt = modal.querySelector('.modal-negative-prompt');
    const modalInfo = modal.querySelector('.modal-info');
  
    modalImage.src = image.src;
    currentImageFileName = image.src.split('/').pop();
    console.log(currentImageFileName)
    selectedModalImage = image;
    
    
    fetchJsonData().then(data => {
      const imageName = image.src.split('/').pop();
      const imageData = getImageData(imageName, data);
  
      console.log(imageData)
      if (imageData !== undefined) {
        const { prompt, negativePrompt, width, height, num_inference_steps, eta, guidance_scale, seed,  get_active_model, vae } =  imageData.settings;
        const { img_name, folder_url } = imageData;
        modalPrompt.textContent = `Prompt: ${prompt}`;
        modalNegativePrompt.textContent = `Negative Prompt: ${negativePrompt}`;
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
  
      modal.style.display = 'block';

    });
  };
  
  function getImageData(imageName, data) {
    if (data && data.hasOwnProperty(imageName)) {
      return data[imageName];
    }
    return undefined;
  }
  
  closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
  });
  
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
  
  window.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      modal.style.display = 'none';
    }
  });
  

  removeButton.addEventListener('click', () => {
    if (currentImageFileName) {
      deleteImage(currentImageFileName);
    } else {
      alert('No image selected');
    }
  });
  
    const deleteImage = (imageFileName) => {
      fetch('/delete_image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ fileName: imageFileName })
      })
      .then(response => {
        if (response.ok) {
          alert('Image deleted successfully');
          fetchImages();
        } 
      })
      .catch(error => {
        alert('Error occurred while deleting image:'+ error);
      });
    };
    
    openFolderButton.addEventListener('click', async () => {
      try {
        const data = await fetchJsonData();
        const folderUrl = data[currentImageFileName].folder_url;
        console.log(folderUrl + data[currentImageFileName].img_name);
        window.open(folderUrl + data[currentImageFileName].img_name);
      } catch (error) {
        console.error('An error occurred:', error);
      }
    });

    function downloadImage(imageUrl) {
      if (selectedModalImage) {
        const link = document.createElement('a');
        link.href = imageUrl;
        link.download = currentImageFileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        alert('No image selected');
      }
    }

    downloadButton.addEventListener('click', () => {
      if (selectedModalImage) {
        downloadImage(selectedModalImage.src);
      }
    });


    upscalingButton.addEventListener('click', () => {
      if (selectedModalImage) {
        const imageUrl = selectedModalImage.src;
        const upscalingSiteUrl = `/upscale?image=${encodeURIComponent(imageUrl)}`;
        window.location.href = upscalingSiteUrl;
      } else {
        alert('No image selected');
      }
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