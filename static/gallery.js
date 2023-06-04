var imageFiles = [];
var imagesPerPage = 20;

fetchImages();

function fetchImages() {
  fetch('/getImages')
      .then(response => {
          if (!response.ok) {
              alert("Oops, please try again.");
              throw new Error('Error retrieving image files.');
          }
          return response.json();
      })
      .then(data => {
          imageFiles = data.imageFiles.sort(numericalSort);
          displayImages(imageFiles);
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

function displayImages(data, currentPage = 1) {
  var totalPages = Math.ceil(data.length / imagesPerPage); // Total number of pages
  var startIndex = (currentPage - 1) * imagesPerPage; // Start index of the images to display
  var endIndex = startIndex + imagesPerPage; // End index of the images to display

  var imageContainer = document.getElementById('imageContainer');
  var tempContainer = document.createElement('div'); // Create a temporary container for shuffling

  // Slice the image array based on the current page and images per page
  var imageSlice = data.slice(startIndex, endIndex);

  imageSlice.forEach(function(imageFile) {
    var img = document.createElement('img');
    img.src = "GeneratedImg" + '/' + imageFile;
    img.alt = imageFile;
    img.draggable = false;
    img.classList.add('image');
    tempContainer.appendChild(img);
  });

  imageContainer.innerHTML = '';
  shuffleImages(tempContainer.children, imageContainer);

  // Add pagination controls
  addPagination(currentPage, totalPages);
}

function shuffleImages(images, container) {
  var imageArray = Array.from(images);
  var currentIndex = imageArray.length;
  var temporaryValue, randomIndex;

  // while (currentIndex > 0) {
    while (false) {
      randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    temporaryValue = imageArray[currentIndex];
    imageArray[currentIndex] = imageArray[randomIndex];
    imageArray[randomIndex] = temporaryValue;
  }

  var fragment = document.createDocumentFragment();
  imageArray.forEach(function(image) {
    image.classList.add('shuffle-animation');
    fragment.appendChild(image);
  });

  container.appendChild(fragment);
}

function numericalSort(a, b) {
  var numA = parseInt(a.match(/\d+/)[0]);
  var numB = parseInt(b.match(/\d+/)[0]);

  return numB - numA;
}

function addPagination(currentPage, totalPages) {
  var paginationContainer = document.getElementById('paginationContainer');
  paginationContainer.innerHTML = '';

  if (totalPages > 1) {
    var previousButton = createPaginationButton('Previous', currentPage - 1);
    previousButton.classList.add('pagination-button', 'previous-button');
    if (currentPage === 1) {
      previousButton.disabled = true;
    }
    paginationContainer.appendChild(previousButton);

    for (var i = 1; i <= totalPages; i++) {
      var pageButton = createPaginationButton(i, i);
      if (i === 1) {
        pageButton.classList.add('active');
      }
      paginationContainer.appendChild(pageButton);
    }

    var nextButton = createPaginationButton('Next', currentPage + 1);
    nextButton.classList.add('pagination-button', 'next-button');
    if (currentPage === totalPages) {
      nextButton.disabled = true;
    }
    paginationContainer.appendChild(nextButton);
  }
}



function createPaginationButton(text, page) {
  var button = document.createElement('button');
  button.classList.add('pagination-button');
  button.textContent = text;
  button.dataset.page = page;

  button.addEventListener('click', function() {
    var currentPage = parseInt(this.dataset.page);
    displayImages(imageFiles, currentPage);
    setActiveButton(this);
  });

  return button;
}

var changeOrderButton = document.getElementById('changeOrderButton');
changeOrderButton.addEventListener('click', function() {
  imageFiles.reverse();
  displayImages(imageFiles);
});

function setActiveButton(button) {
  var buttons = document.querySelectorAll('.pagination-button');
  var activePage = parseInt(button?.getAttribute('data-page'));

  if (activePage === undefined) {
    activePage = 1
  }

  buttons.forEach(function(btn) {
    var page = parseInt(btn.getAttribute('data-page') ?? '');
    if (page === activePage) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
}