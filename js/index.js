// Fucntion for previewing images
const setupImagePreview = (fileInput, input, restore = false) => {
  const file = fileInput.files[0];
  const fileinp = document.getElementById(input);
  const imagePreview = fileinp.nextElementSibling;
  if (restore) imagePreview.setAttribute("data-restore", imagePreview.src);

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imagePreview.style.display = "block";

      document.getElementById("resEye").src = e.target.result;
    };

    reader.readAsDataURL(file);
  }
};

const checkImage = (
  file,
  bfu = false,
  placeholder = false,
  resetImage = false
) => {
  // BFU = Button for uploading
  const imagePreview = file.nextElementSibling;
  const imagePreviousImage = imagePreview.getAttribute("data-restore");
  const fileParent = file.parentElement;
  const buttonForUploading = bfu ? file.parentElement.nextElementSibling : "";
  const placeholderElement = file.previousElementSibling;

  if (file.files.length >= 1) {
    if (placeholder) placeholderElement.style.display = "none";
    fileParent.classList.add("checkboard");
    fileParent.classList.remove("fileupload");
    if (bfu) buttonForUploading.style.display = "block";
  } else {
    if (placeholder) placeholderElement.style.display = "grid";
    fileParent.classList.remove("checkboard");
    fileParent.classList.add("fileupload");
    if (bfu) buttonForUploading.style.display = "none";
    if (resetImage) imagePreview.src = imagePreviousImage;
    else imagePreview.style.display = "none";
  }
};

function dataRetrive(url, options) {
  // Add class to elements
  document.querySelectorAll(".list-items").forEach((d) => {
    d.classList.add("runni");
  });

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (url === "/error") {
        reject(new Error("Fetch request failed!"));
      } else {
        // Perform the real fetch
        fetch(url, options) // have to change the options to send image
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => resolve(data))
          .catch((error) => reject(error));
      }
    }, 6000); // Keeps the delay
  });
}

// Form submission handler
document
  .getElementById("frmUploadIMG")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // Hide sectionOne, show sectionTwo
    document.getElementById("sectionOne").style.display = "none";
    document.getElementById("pagination").children[1].classList.add("active");
    sectionTwo.style.display = "grid";

    await dataRetrive("data/eye.json", { method: "GET" })
      .then((response) => {
        const hemoLevel = response.hemo;
        document.getElementById("hLevel").innerText = hemoLevel;
      })
      .catch((error) => {
        console.error("Error:", error.message);
      });

    // After processing, hide sectionTwo and show sectionThree
    sectionTwo.style.display = "none";
    document.getElementById("pagination").children[2].classList.add("active");
    document.getElementById("sectionThree").style.display = "grid";
  });

const inpage = document.getElementById("instructions");

document.body.onload = () => {
  document.querySelector("body").style.opacity = 1;
  if (localStorage.getItem("instruction"))
    inpage.parentElement.removeChild(inpage);
};

const neverShowAgain = () => {
  inpage.parentElement.removeChild(inpage);
  localStorage.setItem("instruction", false);
};
