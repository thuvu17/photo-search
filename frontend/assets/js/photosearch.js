// GET keyword

document.getElementById("getKeywordForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting via HTTP

  // Get form value
  var keyword = document.getElementById("keyword").value;

  // Do something with the form data
  console.log(keyword);
  return sdk.searchGet({q: keyword}, {}, {});
});


// PUT photo

document.getElementById('uploadImageForm').addEventListener('submit', function (event) {
  event.preventDefault();
  // Get image input
  var imageFile = document.getElementById('imageInput').files[0];

  // Get the custom labels 
  var customLabels = document.getElementById('customLabels').value.split(',');

  // Create a FormData object to send the file and custom labels
  var formData = new FormData();
  formData.append('image', imageFile);
  formData.append('customLabels', JSON.stringify(customLabels));

  uploadImage(formData);
});

function uploadImage(file) {
  return sdk.uploadPut();
}
