var clickCount = 0; // Variable to keep track of button clicks

function dbQuery() {
  var userInput1 = document.getElementById("userInput1").value;
  var userInput2 = document.getElementById("userInput2").value;
  var output = document.getElementById("output");

  var concatenatedString = 'you are a bot that will be given a persona and a question answer the question based on the persona, persona: ' + userInput1 + '. question: ' + userInput2; // Concatenate the two strings

  fetch('/dbQuery', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 'input_string': concatenatedString })
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('fileoutput').innerHTML = data.full_sentence.replace(/\n/g, "<br>");
    })
    .catch(error => {
      console.error('Error:', error);
    });
}


function countButtonClick() {
  clickCount++;
  document.getElementById("clickCount").textContent = "Button clicked " + clickCount + " times.";
}

function displayFileName() {
  const fileInput = document.getElementById("fileUpload");
  const selectedFileName = document.getElementById("selectedFileName");

  if (fileInput.files.length > 0) {
    selectedFileName.textContent = "Selected file: " + fileInput.files[0].name;
  } else {
    selectedFileName.textContent = "";
  }
}

function fetchFileList() {
  fetch('/fileList')
    .then(response => response.json())
    .then(data => {
      const fileList = document.getElementById("fileList");
      fileList.innerHTML = ""; // Clear the existing file list

      for (let i = 1; i < data.uploaded_files.length; i++) {
        const listItem = document.createElement("li");
        listItem.textContent = data.uploaded_files[i]; // Display the filename
        fileList.appendChild(listItem);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

const form = document.getElementById("uploadForm");
const outputDiv = document.getElementById("fileoutput");

form.addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the default form submission

  const fileInput = document.getElementById("fileUpload");
  const file = fileInput.files[0]; // Get the selected file

  if (file) {
    const reader = new FileReader();

    reader.onload = function(e) {

      fetch('/upload', {
        method: 'POST',
        body: new FormData(form) // Send the form data
      })
        .then(response => response.json())
        .then(data => {
          console.log(data); // Optional: Display or handle the response from the backend

          const fileList = document.getElementById("fileList");
          fileList.innerHTML = ""; // Clear the existing file list

          for (let i = 0; i < data.uploaded_files.length; i++) {
            const listItem = document.createElement("li");
            listItem.textContent = data.uploaded_files[i]; // Display the filename
            fileList.appendChild(listItem);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    };

    reader.readAsText(file); // Read the file as text
  } else {
    // No file selected
    console.log("No file selected.");
  }
});

window.addEventListener('DOMContentLoaded', (event) => {
  fetchFileList();
});
