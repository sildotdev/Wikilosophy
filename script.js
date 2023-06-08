const searchInput = document.querySelector('#wiki-search');
const suggestionsList = document.querySelector('#suggestions');
const searchBtn = document.querySelector('#search-btn');
const resultsModal = document.querySelector('#results-modal');
const modalBodyThingy = document.querySelector('#modal-body-content-thing');

const loadingHTML = `
<div class="text-center">
<div class="spinner-border text-primary" role="status">
</div>
<p class="mt-3">Clicking a bunch of links...</p>
</div>
`

// show suggestions
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

var activeSearch = false;

// Do search
var search = function() {
    // Toggle modal
    // resultsModal.classList.toggle('show');

    if (searchInput.value.length == 0) {
        return;
    }    

    // const myModal = new bootstrap.Modal(document.getElementById('results-modal'));
    const myModalAlternative = new bootstrap.Modal('#results-modal');
    myModalAlternative.show();

    if (searchInput.value == 'Philosophy') {
        modalBodyThingy.innerHTML = `<p class="text-center">You think you're clever, don't you? Try something else.</p>`;
        return;
    }

    // clear previous results
    modalBodyThingy.innerHTML = loadingHTML;

    activeSearch = searchInput.value;
    var thisSearch = searchInput.value;

    fetch(`https://okqct25rme.execute-api.us-east-2.amazonaws.com/${searchInput.value}`)
    .then((response) => {
        if (thisSearch != activeSearch) {
            return;
        }

        modalBodyThingy.innerHTML = '';
        console.log("cool beans");
        console.log(response.body);
        // its a readable stream so we need to do this
        
        // catch errors
        if (!response.ok) {
          modalBodyThingy.innerHTML = 'Error: ' + response.status + ' ' + response.statusText;
          return;
        }

        response.body.getReader().read().then((result) => {
            // read as text
            const decoder = new TextDecoder('utf-8');
            const text = decoder.decode(result.value);
            // convert to list
            const output = JSON.parse(text);
            // console.log(text);

            // if output is text
            if (typeof output == 'string') {
                modalBodyThingy.innerHTML = output;
                return;
            }

            var ol = document.createElement('ul');
            ol.classList.add('list-group');

            for (var i = 0; i < output.length; i++) {
                var li = document.createElement('a');
                li.setAttribute('href', 'https://en.wikipedia.org/wiki/' + output[i]);
                li.setAttribute('target', '_blank');
                li.innerHTML = i + '. ' + output[i];
                li.classList.add('list-group-item');
                if (i == 0) {
                    li.classList.add('list-group-item-info');
                } else if (i == output.length - 1) {
                    li.classList.add('list-group-item-success');
                }
                ol.appendChild(li);
            }

            modalBodyThingy.appendChild(ol);

            modalBodyThingy.innerHTML += `<br>`
            modalBodyThingy.innerHTML += `<p class="text-center mt-3">See? All it took was ${output.length - 1} clicks!</p>`;

            // modalBodyThingy.innerHTML = text;
        });
    });
}

// search on enter
searchInput.onkeypress = function(event) {
    if (event.keyCode == 13) {
        console.log('enter');
        search(searchInput.value);
    }
};

// search on button click
searchBtn.addEventListener('click', function() {
    console.log('click');
    search(searchInput.value);
});