document
  .getElementById("selectedStudy")
  .addEventListener("change", function () {
    document.getElementById("FieldofStudy").submit();
  });
function validateForm() {
  var checkboxes = document.getElementsByName("selectedcourses");
  var atLeastOneChecked = false;

  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      atLeastOneChecked = true;
      break;
    }
  }

  if (!atLeastOneChecked) {
    alert("Please select at least one course.");
    return false;
  }

  return true;
}
function handleCheckboxClick(checkbox) {
  var courseId = checkbox.value;
  var selectedYear = document.getElementById(courseId + "_year").value;
  var selectedSemester = document.getElementById(courseId + "_semester").value;

  var checkboxes = document.getElementsByName("selectedcourses");
  var selectedCount = 0;
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      selectedCount++;
    }
    if (selectedCount > 3) {
      alert("You cannot select more than three courses.");
      checkbox.checked = false;
      return;
    }
    if (checkboxes[i] !== checkbox && checkboxes[i].checked) {
      var otherCourseId = checkboxes[i].value;
      var otherYear = document.getElementById(otherCourseId + "_year").value;
      var otherSemester = document.getElementById(
        otherCourseId + "_semester"
      ).value;

      if (selectedYear === otherYear && selectedSemester === otherSemester) {
        alert("You cannot select two courses from the same year and semester.");
        checkbox.checked = false;
        return;
      }
    }
  }
}
