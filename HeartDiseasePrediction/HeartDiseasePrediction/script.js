
// Validate the 'Sex' input field
function validateSexInput(input) {
  const value = input.value;

  // Check if the value is not 0 or 1
  if (value !== "0" && value !== "1") {
      input.value = ""; // Clear the input if invalid
      document.getElementById("sexError").style.display = "block";
  } else {
      document.getElementById("sexError").style.display = "none";
  }
}

// Attach an event listener to the 'Sex' input field
document.getElementById("sex").addEventListener("input", function () {
  validateSexInput(this);
});

document.getElementById("prediction-form").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const formData = new FormData(e.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
  
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  
      const result = await response.json();
      const resultDiv = document.getElementById("result");
  
      if (result.prediction === 1) {
        resultDiv.innerHTML = "<p style='color: red;'>High Risk of Heart Disease</p>";
      } else {
        resultDiv.innerHTML = "<p style='color: green;'>Low Risk of Heart Disease</p>";
      }
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("result").innerText = "Error making prediction. Please try again.";
    }
  });
  