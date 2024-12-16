var imageFiles = [];
var imagesPerPage = 30;
var folderPath = "fullImg/";

var imageFiles = [];
var imagesPerPage2 = 4;

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
          displayImagesSmall(imageFiles);
          displayImages(imageFiles);
      })
      .catch(error => {
          console.log('Error:', error);
      });
}

function displayImagesSmall(data) {
  var imageContainer = document.getElementById('imageContainer2');
  var tempContainer = document.createElement('div');
  tempContainer.className = 'imageContainer2'

  if (imageContainer != null) {
    imageContainer.innerHTML = '';

    for (let i = 0; i < Math.min(4, data.length); i++) {
      var imageFile = data[i];
      var img = document.createElement('img');
      img.src = "GeneratedImg/" + imageFile;
      img.alt = imageFile;
      img.draggable = false;
      img.classList.add('image');

      img.addEventListener('click', function() {
        openModal(this);
      });

      tempContainer.appendChild(img);
    }

    imageContainer.appendChild(tempContainer);
  }
}

function displayImages(data, currentPage = 1) {
  var totalPages = Math.ceil(data.length / imagesPerPage);
  var startIndex = (currentPage - 1) * imagesPerPage;
  var endIndex = startIndex + imagesPerPage;

  var imageContainer = document.getElementById('imageContainer');
  var tempContainer = document.createElement('div');

  var imageSlice = data.slice(startIndex, endIndex);

  if(imageContainer != null){
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

    addPagination(currentPage, totalPages);
  }

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
  var pattern = /^(\d{8}_\d{6})|(\d{8}_\d{6}_\d+)|(\d+)$/;
  
  var matchA = a.match(pattern);
  var matchB = b.match(pattern);

  if (matchA && matchB) {
    if (matchA[1] && matchB[1]) {
      return b.localeCompare(a);
    } else if (matchA[2] && matchB[2]) {
      var partsA = matchA[2].split("_");
      var partsB = matchB[2].split("_");
      if (partsA[0] === partsB[0]) {
        if (partsA[1] === partsB[1]) {
          var numberA = parseInt(partsA[2]);
          var numberB = parseInt(partsB[2]);
          if (numberA !== numberB) {
            return numberB - numberA;
          }
        } else {
          return parseInt(partsB[1]) - parseInt(partsA[1]);
        }
      } else {
        return parseInt(partsB[0]) - parseInt(partsA[0]);
      }
    } else if (matchA[3] && matchB[3]) {
      return parseInt(b) - parseInt(a);
    }
  } else if (matchA && matchA[1]) {
    return -1;
  } else if (matchB && matchB[1]) {
    return 1;
  } else {
    var numberA = parseInt(a);
    var numberB = parseInt(b);
    if (!isNaN(numberA) && !isNaN(numberB)) {
      return numberB - numberA;
    }
  }

  return a.localeCompare(b);
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
changeOrderButton?.addEventListener('click', function() {
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
