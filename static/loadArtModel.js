document.addEventListener('DOMContentLoaded', function () {
  loadSelectedModel();

  document.getElementById('openModelSelector').addEventListener('click', function() {
    document.getElementById('modelModal').style.display = 'block';
    loadModels();
  });

  window.addEventListener('click', function(event) {
    const modal = document.getElementById('modelModal');
    const modalContent = document.querySelector('.model-modal-content');

    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });

  function loadModels() {
    fetch('/available_models')
      .then(response => response.json())
      .then(data => {
        const modelSelectContainer = document.getElementById('modelSelectContainer');
        modelSelectContainer.innerHTML = '';

        data.all_models.forEach(model => {

            const modelCard = document.createElement('div');
            modelCard.classList.add('model-card');
            modelCard.setAttribute('data-model', model.name);

            const img = document.createElement('img');
            img.src = model.image;
            img.alt = model.name;
            img.classList.add('model-image');
            modelCard.appendChild(img);

            const modelName = document.createElement('h4');
            modelName.textContent = model.name;
            modelCard.appendChild(modelName);

            const modelSize = document.createElement('p');
            modelSize.textContent = `Size: ${model.size}`;
            modelCard.appendChild(modelSize);

            modelCard.addEventListener('click', function() {
              selectModel(model.name, model.image);
              document.getElementById('modelModal').style.display = 'none';
            });

            modelSelectContainer.appendChild(modelCard); 
        });
      });
  }

  function selectModel(modelName, modelImage) {
    document.getElementById('selectedModelName').textContent = modelName;
    document.getElementById('selectedModelImage').src = modelImage;

    fetch('/selected_model', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ selected_model: modelName }),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Model selected:', data);
    });
  }

  function loadSelectedModel() {
    fetch('/available_models')
      .then(response => response.json())
      .then(data => {
  
        if (data.active_models) {
          const activeModelName = data.active_models.split('/').pop();
          console.log('Active model name:', activeModelName);
  
          const activeModel = data.all_models.find(model => model.name.includes(activeModelName));
  
          if (activeModel) {
            document.getElementById('selectedModelName').textContent = activeModel.name;
            document.getElementById('selectedModelImage').src = activeModel.image;
          }
        }
      });
  }
  
  
});
