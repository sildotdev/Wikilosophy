const searchInput = document.querySelector('#wiki-search');
const suggestionsList = document.querySelector('#suggestions');
const searchBtn = document.querySelector('#search-btn');
const resultsModal = document.querySelector('#results-modal');
const modalBodyThingy = document.querySelector('#modal-body-content-thing');

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

    fetch(`https://okqct25rme.execute-api.us-east-2.amazonaws.com/${searchInput.value}`)
    .then((response) => {
        console.log("cool beans");
        console.log(response.body);
        // its a readable stream so we need to do this
        response.body.getReader().read().then((result) => {
            // read as text
            const decoder = new TextDecoder('utf-8');
            const text = decoder.decode(result.value);
            console.log(text);

            modalBodyThingy.innerHTML = text;
        });
    });
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