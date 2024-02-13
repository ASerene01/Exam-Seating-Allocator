document.getElementById("userType").addEventListener("change", function () {
  if (this.value === "Student" || this.value === "student") {
    document.querySelector(".student-options").style.display = "block";
  } else {
    document.querySelector(".student-options").style.display = "none";
  }
});
