document.getElementById("getKeywordForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent the form from submitting the traditional way

  // Get the search keyword from the input field
  var keyword = document.getElementById("keyword").value;

  // Make the API request using the SDK's method (assuming the SDK has a `searchPhotoAlbums` method)
  sdk.searchPhotoAlbums({ keyword: keyword })
    .then(function(response) {
      // Request succeeded, handle the response data here
      console.log(response.data); // Process the response data as needed
    })
    .catch(function(error) {
      // Request failed, handle the error here
      console.error("Error:", error);
    });
});