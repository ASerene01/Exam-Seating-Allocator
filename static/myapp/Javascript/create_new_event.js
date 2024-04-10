// Get today's date
const today = new Date();
const year = today.getFullYear();
const startTimeInput = document.getElementById("startTime");
const endTimeInput = document.getElementById("endTime");
let month = today.getMonth() + 1;
let day = today.getDate();

// Pad month and day with leading zeros if necessary
month = month < 10 ? "0" + month : month;
day = day < 10 ? "0" + day : day;

// Format date as yyyy-mm-dd (required by input type="date")
const formattedDate = `${year}-${month}-${day}`;

// Set the minimum date for the input element to today's date
document.getElementById("inputDate").min = formattedDate;

// When the Start Time changes, update the minimum value of End Time
startTimeInput.addEventListener("input", function () {
  endTimeInput.value = startTimeInput.value;
  validateEndTime(); // Validate immediately when Start Time changes
});

// Validate End Time on input (as the user types)
endTimeInput.addEventListener("input", validateEndTime);

function validateEndTime() {
  const startTime = startTimeInput.value;
  const endTime = endTimeInput.value;
  console.log(startTime);
  console.log(endTime);
  if (endTime < startTime) {
    // Invalid End Time, show error message or take appropriate action
    window.alert("End Time must be later than Start Time");
    // Reset End Time value to prevent invalid selection
    endTimeInput.value = startTime;
  } else {
  }
}
