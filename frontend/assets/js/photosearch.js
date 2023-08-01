// GET keyword

document.getElementById("getKeywordForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting via HTTP

  // Get form value
  var keyword = document.getElementById("keyword").value;

  // Do something with the form data
  console.log(keyword);
  return sdk.searchGet({q: keyword}, {}, {});
});


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

document.getElementById("getKeywordForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting via HTTP

  // Get form value
  var keyword = document.getElementById("keyword").value;

  // Do something with the form data
  console.log(keyword);
  return sdk.searchGet({q: keyword}, {}, {});
});
