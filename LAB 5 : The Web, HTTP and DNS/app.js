
const images = ["image1.jpg", "image2.jpg", "image3.jpg","image4.jpg", "image5.jpg", "image6.jpg",  "image7.jpg"]; // Array of image URLs
const imageElement = document.getElementById("myImage"); // Get the image element
const buttonElement = document.getElementById("changeButton"); // Get the button element
let currentIndex = 0; // Current image index

buttonElement.addEventListener("click", function() {
  // Increment the index, or go back to 0 if we've reached the end of the array
  currentIndex = (currentIndex + 1) % images.length;
  
  // Set the image source to the new URL
  imageElement.src = images[currentIndex];
});
