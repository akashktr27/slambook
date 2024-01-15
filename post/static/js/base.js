//// Accordion
//function myFunction(id) {
//  var x = document.getElementById(id);
//  if (x.className.indexOf("w3-show") == -1) {
//    x.className += " w3-show";
//    x.previousElementSibling.className += " w3-theme-d1";
//  } else {
//    x.className = x.className.replace("w3-show", "");
//    x.previousElementSibling.className =
//    x.previousElementSibling.className.replace(" w3-theme-d1", "");
//  }
//}
//
//// Used to toggle the menu on smaller screens when clicking on the menu button
//function openNav() {
//  var x = document.getElementById("navDemo");
//  if (x.className.indexOf("w3-show") == -1) {
//    x.className += " w3-show";
//  } else {
//    x.className = x.className.replace(" w3-show", "");
//  }
//}

console.log("nase.js")

function searchFriends() {
    var mysearch = $('#mysearch').val();
    var spinner = $('.spinner');
    spinner.show();

    $.ajax({
        url: `/account/search/?q=${mysearch}`,
        method: 'GET',
        dataType: 'json'
    })
    .done(function(data) {
        updateTable(data);
    })
    .fail(function(error) {
        console.error('Error:', error);
    })
    .always(function() {
        // Hide spinner regardless of success or failure
        spinner.hide();
    });
}

function updateTable(data) {
    var tableBody = document.querySelector('#friendsTable tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    if (data.length > 0) {
        data.forEach(friend => {
            var row = document.createElement('tr');
            var cell = document.createElement('td');
            cell.style.border = '1px solid #343a40';
            var link = document.createElement('a');
            link.style.textDecoration = 'none';
            link.style.color = '#007bff';
            link.href = friend.url; // Make sure to provide the correct URL property in your data
            link.textContent = friend.full_name; // Adjust this based on your data structure
            cell.appendChild(link);
            row.appendChild(cell);
            tableBody.appendChild(row);
        });
    } else {
        // Display a message when there are no results
        var row = document.createElement('tr');
        var cell = document.createElement('td');
        cell.style.border = '1px solid #343a40';
        var text = document.createTextNode('No results found.');
        cell.appendChild(text);
        row.appendChild(cell);
        tableBody.appendChild(row);
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent form submission
        searchFriends();
    }
}