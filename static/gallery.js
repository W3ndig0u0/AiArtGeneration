var imageFiles = [];
var imagesPerPage = 30;
var folderPath = "fullImg/";


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
        console.log(data.imageFiles);
          imageFiles = data.imageFiles.sort(numericalSort);
          displayImages(imageFiles);
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

function displayImages(data, currentPage = 1) {
  var totalPages = Math.ceil(data.length / imagesPerPage);
  var startIndex = (currentPage - 1) * imagesPerPage;
  var endIndex = startIndex + imagesPerPage;

  var imageContainer = document.getElementById('imageContainer');
  var tempContainer = document.createElement('div');

  var imageSlice = data.slice(startIndex, endIndex);

  imageSlice.forEach(function(imageFile) {
    var img = document.createElement('img');
    img.src = "GeneratedImg" + '/' + imageFile;
    img.alt = imageFile;
    img.draggable = false;
    img.classList.add('image');

    img.addEventListener('click', function() {
      openModal(this);
    });

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
  var isNewOrderA = /^\d{8}_\d{6}_\d+\.png$/.test(a);
  var isNewOrderB = /^\d{8}_\d{6}_\d+\.png$/.test(b);

  if (isNewOrderA && isNewOrderB) {
    var numA = parseInt(a.match(/\d+/)[0]);
    var numB = parseInt(b.match(/\d+/)[0]);

    return numB - numA;
  } else if (isNewOrderA) {
    return -1;
  } else if (isNewOrderB) {
    return 1; 
  } else {
    var isNormalOrderA = /^\d+\.png$/.test(a);
    var isNormalOrderB = /^\d+\.png$/.test(b);

    if (isNormalOrderA && isNormalOrderB) {
      var numA = parseInt(a.match(/\d+/)[0]);
      var numB = parseInt(b.match(/\d+/)[0]);

      return numB - numA;
    } else if (isNormalOrderA) {
      return -1;
    } else if (isNormalOrderB) {
      return 1; 
    } else {
      return 0;
    }
  }
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


fetchImages();
