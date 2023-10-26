document.getElementById("userType").addEventListener("change", function () {
  if (this.value === "Student") {
    document.querySelector(".student-options").style.display = "block";
  } else {
    document.querySelector(".student-options").style.display = "none";
  }
});
