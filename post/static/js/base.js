// Accordion
function myFunction(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
    x.previousElementSibling.className += " w3-theme-d1";
  } else {
    x.className = x.className.replace("w3-show", "");
    x.previousElementSibling.className =
    x.previousElementSibling.className.replace(" w3-theme-d1", "");
  }
}

// Used to toggle the menu on smaller screens when clicking on the menu button
function openNav() {
  var x = document.getElementById("navDemo");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}

//var updateBtns = document.getElementsById('btn btn-primary')

//console.log('upd', updateBtns)

//function handleClick(button) {
//    // Change the label (text) of the button
//    button.innerHTML = "Request sent";
//
//    // Get the URL from the button's data attribute
//    var url = button.getAttribute("data-url");
//    console.log(url)
//    // Redirect to the specified URL
//}
