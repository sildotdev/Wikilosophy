const searchInput = document.querySelector('#wiki-search');
const suggestionsList = document.querySelector('#suggestions');
const searchBtn = document.querySelector('#search-btn');
const resultsModal = document.querySelector('#results-modal');

searchInput.addEventListener('input', function() {
  if (this.value.length > 0) {
    fetch(`https://en.wikipedia.org/w/api.php?origin=*&action=opensearch&search=${this.value}&limit=5&format=json`)
    .then(response => response.json())
    .then(data => {
      suggestionsList.innerHTML = "";
      data[1].forEach(page => {
        const listItem = document.createElement('li');
        listItem.classList.add('list-group-item');
        listItem.innerText = page;
        listItem.addEventListener('click', function() {
          searchInput.value = this.innerText;
          suggestionsList.style.display = 'none';
        });
        suggestionsList.appendChild(listItem);
      });
      suggestionsList.style.display = 'block';
    });
  } else {
    suggestionsList.style.display = 'none';
  }
});

// hide suggestions when clicked outside
document.addEventListener('click', function(e) {
  if (!e.target.closest('#wiki-search')) {
    suggestionsList.style.display = 'none';
  }
});

// Do search
var search = function() {
    // Toggle modal
    // resultsModal.classList.toggle('show');

    // const myModal = new bootstrap.Modal(document.getElementById('results-modal'));
    const myModalAlternative = new bootstrap.Modal('#results-modal');
    myModalAlternative.show();
}

searchInput.onkeypress = function(event) {
    if (event.keyCode == 13) {
        console.log('enter');
        search(searchInput.value);
    }
};

searchBtn.addEventListener('click', function() {
    console.log('click');
    search(searchInput.value);
});