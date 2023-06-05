fetch('/available_models')
  .then(response => response.json())
  .then(data => {
    console.log(data);

    const parentElement = document.getElementById('menu');

    const selectElement = document.createElement('select');
    selectElement.id = 'modelSelect';

    const defaultOption = document.createElement('option');
    defaultOption.text = data.active_models;
    defaultOption.disabled = true;  // Make the default option read-only
    defaultOption.selected = true;  // Make the default option selected
    selectElement.appendChild(defaultOption);

    data.all_models.forEach(model => {
      const option = document.createElement('option');
      option.value = model.name;
      option.text = `${model.name} (${model.size})`;
      selectElement.appendChild(option);
    });

    parentElement.appendChild(selectElement);

    selectElement.addEventListener('change', (event) => {
      const selectedModel = event.target.value;

      fetch('/selected_model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ selected_model: selectedModel }),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Response from backend:', data);
        })
      });
    })