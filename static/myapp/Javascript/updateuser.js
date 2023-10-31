document.addEventListener("DOMContentLoaded", function () {
  // This code will execute when the page is fully loaded.
  var userType = document.getElementById("userType");

  if (userType.value.toLowerCase() === "student") {
    document.querySelector(".student-options").style.display = "block";
  } else {
    document.querySelector(".student-options").style.display = "none";
  }
});

document.getElementById("userType").addEventListener("change", function () {
  if (this.value === "Student" || this.value === "student") {
    document.querySelector(".student-options").style.display = "block";
  } else {
    document.querySelector(".student-options").style.display = "none";
  }
});
