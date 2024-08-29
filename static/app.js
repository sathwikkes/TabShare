function uploadReceipt() {
    const fileInput = document.getElementById('receipt-upload');
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);  // Debugging line to check server response
        if (data.items && Array.isArray(data.items)) {
            items = data.items;
            displayItems();  // Call displayItems to show items on the screen
        } else {
            console.error("Data format error:", data);
        }
    })
    .catch(error => {
        console.error("Error uploading file:", error);
    });
}

function displayItems() {
    const itemList = document.getElementById('item-list');
    itemList.innerHTML = '';  // Clear previous items

    items.forEach((item) => {
        const listItem = document.createElement('li');
        listItem.classList.add('item');

        // Display either the raw line or the item with price if available
        if (item.item && item.price) {
            listItem.textContent = `${item.item}: $${item.price.toFixed(2)}`;
        } else if (item.line) {
            listItem.textContent = item.line;  // Display the raw line if item/price isn't available
        }
        
        itemList.appendChild(listItem);
    });

    setupDragAndDrop();  // If you have drag-and-drop functionality
}

function updateTabName() {
    const tabNameInput = document.getElementById('tabshare-name').value;
    const tabNameTitle = document.getElementById('tabshare-title');
    if (tabNameInput.trim() !== "") {
        tabNameTitle.textContent = tabNameInput;
    } else {
        alert("Please enter a valid tab name.");
    }
}

function promptForFriends() {
    const numFriends = prompt("How many friends do you want to split this bill with?");
    if (numFriends && !isNaN(numFriends)) {
        createPersonElements(parseInt(numFriends));
    } else {
        alert("Please enter a valid number.");
    }
}

function createPersonElements(numFriends) {
    const peopleList = document.getElementById('people-list');
    peopleList.innerHTML = '';

    for (let i = 1; i <= numFriends; i++) {
        const personDiv = document.createElement('div');
        personDiv.classList.add('person');
        personDiv.textContent = `Person ${i}`;
        personDiv.contentEditable = true;
        personDiv.dataset.name = `Person ${i}`;
        peopleList.appendChild(personDiv);
    }

    setupDragAndDrop();
}

function setupDragAndDrop() {
    const itemElements = document.querySelectorAll('.item');
    const peopleElements = document.querySelectorAll('.person');

    itemElements.forEach(item => {
        item.addEventListener('dragstart', function (e) {
            e.dataTransfer.setData('text', e.target.dataset.index);
        });
    });

    peopleElements.forEach(person => {
        person.addEventListener('dragover', function (e) {
            e.preventDefault();
        });

        person.addEventListener('drop', function (e) {
            e.preventDefault();
            const index = e.dataTransfer.getData('text');
            const item = document.querySelector(`[data-index='${index}']`);
            if (item) {
                e.target.appendChild(item);
            }
        });

        person.addEventListener('blur', function() {
            // Update dataset name when user changes the text
            person.dataset.name = person.textContent.trim();
        });
    });
}

function calculateTotals() {
    // Implement the logic to calculate totals for each person
    console.log("Calculating totals...");
}