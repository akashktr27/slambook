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

//make the notification as marked
$(document).ready(function () {
    $("#markAllReadBtn").on("click", function () {
        $.ajax({
            type: "POST",
            url: "{% url 'your_mark_all_read_view' %}",
            success: function (data) {
                console.log("All notifications marked as read");
            },
            error: function (error) {
                console.error("Error marking all notifications as read", error);
            }
        });
    });
});

console.log('hi');
