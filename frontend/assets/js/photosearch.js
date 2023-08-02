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
