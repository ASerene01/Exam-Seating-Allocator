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

var fieldOfStudy = document.getElementById("fieldofstudy");
var year = document.getElementById("year");
var semester = document.getElementById("semester");
var currentSelection = {
  fieldOfStudy: fieldOfStudy.value,
  year: year.value,
  semester: semester.value,
};

// Add a common event listener to all three elements
fieldOfStudy.addEventListener("change", checkAndToggleSection);
year.addEventListener("change", checkAndToggleSection);
semester.addEventListener("change", checkAndToggleSection);

function checkAndToggleSection() {
  if (
    fieldOfStudy.value !== currentSelection.fieldOfStudy ||
    year.value !== currentSelection.year ||
    semester.value !== currentSelection.semester
  ) {
    var sectionOptions = document.querySelector(".section-options");
    if (sectionOptions) {
      sectionOptions.style.display = "none";
    }
  } else {
    // The values remain the same
    document.querySelector(".section-options").style.display = "block";
  }
}
