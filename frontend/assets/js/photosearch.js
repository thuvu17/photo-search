// GET keyword
document.getElementById("getKeywordForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting via HTTP

  // Get form value
  var keyword = document.getElementById("keyword").value;

  // Do something with the form data
  const searchQuery = keyword;
  const apiUrl = `https://24x5cq0m0i.execute-api.us-east-1.amazonaws.com/dev/search?q=${encodeURIComponent(searchQuery)}`;
  fetch(apiUrl)
  .then(response => {
    // Check if the response status is OK (200) before proceeding
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Assuming the response is in JSON format
  })
  .then(data => {
    // Handle the response data here
    console.log('API Response:', data['results'][0]['url']);
    returnUrl = data['results'][0]['url'];
  })
  .catch(error => {
    // Handle any errors here
    console.error('API Error:', error);
  });
});

// Add an event listener to the "Search" button for voice-to-text
document.getElementById("searchVoiceForm").addEventListener("click", function() {
  const searchText = document.getElementById("search_query").value;

  if (searchText.trim() !== "") {
      const apiUrl = `https://24x5cq0m0i.execute-api.us-east-1.amazonaws.com/dev/search?q=${encodeURIComponent(searchText)}`;
      fetch(apiUrl)
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              if (data['results'].length === 0) {
                  document.getElementById('no-result-message').innerHTML = "No results found";
              } else {
                  // Update the imageList with the search results
                  var imageList = document.getElementById("imageList");
                  imageList.innerHTML = '';
                  for (let i = 0; i < data['results'].length; i++) {
                      const listItem = document.createElement("li");
                      const imageElement = document.createElement("img");
                      imageElement.src = data['results'][i]['url'];
                      imageElement.alt = "Image";
                      listItem.appendChild(imageElement);
                      imageList.appendChild(listItem);
                  }
              }
          })
          .catch(error => {
              console.error('API Error:', error);
          });
  } else {
      alert("Please provide a search query.");
  }
});


// Construct the API URL with the search query as a parameter

// Make the GET request using Fetch API


  // Add an event listener to the submit button
  document.getElementById('uploadImageForm').addEventListener('submit', function (event) {
    event.preventDefault();
    var file = document.getElementById('imageInput').files[0];
      var customLabels = document.getElementById("customLabels");
      console.log(customLabels.value);
      var reader = new FileReader();

      reader.onload = function (event) {//
          // var body = btoa(event.target.result.replace(/^data:(.*;base64,)?/, ''));
          var body = event.target.result;
          // console.log(body);
          // console.log(file.type);
          var filename = Date.now() + file.name
          // console.log(filename)
          var params = {
              'bucket': 'new-b2-bucket',
              'filename': filename,
              'Content-Type': file.type,
              'x-amz-meta-customLabels': customLabels.value,
          };
          sdk.uploadPut(params, body, {})
              .then(function (res) {
                  if (res.status == 200) {
                      alert(filename, "IMAGE UPLOADED!!")
                  }
              });
      }
      reader.readAsDataURL(file);
  }, false);

// PUT photo

// document.getElementById('uploadImageForm').addEventListener('submit', function (event) {
//   event.preventDefault();
//   // Get image input
//   var imageFile = document.getElementById('imageInput').files[0];

//   // Get the custom labels 
//   var customLabels = document.getElementById('customLabels').value.split(',');
//   console.log(customLabels);
//   // Create a FormData object to send the file and custom labels
//   var formData = new FormData();
//   formData.append('image', imageFile);
//   formData.append('customLabels', JSON.stringify(customLabels));

//   return sdk.uploadPut(formData)
// });
