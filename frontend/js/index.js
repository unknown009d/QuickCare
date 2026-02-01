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
  resetImage = false,
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
/*
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


function dataRetrive(imageFile) {
  document.querySelectorAll(".list-items").forEach((d) => {
    d.classList.add("runni");
  });

  const userId = "user-001";

  return new Promise((resolve, reject) => {
    setTimeout(async () => {
      try {
        const data = await processImage(userId, imageFile);
        resolve(data);
      } catch (err) {
        reject(err);
      }
    }, 6000); // keep your fake delay
  });
}
  */

const steps = document.querySelectorAll(".list-items");

function addRunni(index) {
  steps[index]?.classList.add("runni");
}
function removeRunni(index) {
  steps.forEach((d) => {
    d.classList.remove("runni");
  });
}

async function dataRetrive(imageFile) {
  document
    .querySelectorAll(".list-items")
    .forEach((step) => step.classList.remove("runni"));

  const userId = "user-002";
  return await processImage(userId, imageFile);
}

async function processImage(userId, imageFile) {
  const url = "http://192.168.1.6:5000";

  // Step -1: Check if server is running
  try {
    const healthRes = await fetch(url + "/health", {
      method: "GET",
      cache: "no-store",
    });

    if (!healthRes.ok) {
      throw new Error("Server not healthy");
    }
  } catch (err) {
    if (err instanceof TypeError) {
      throw new Error("Server unreachable. Is the backend running?");
    }
    throw err;
  }

  // Step 0: Upload
  let formData = new FormData();
  formData.append("image", imageFile);
  formData.append("user-id", userId);

  addRunni(0);
  let res = await fetch(url + "/upload", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Upload failed");

  // Step 1: Detect
  addRunni(1);
  res = await fetch(url + "/detect", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ "user-id": userId }),
  });
  if (!res.ok) throw new Error("Detect failed");

  // Step 2: Crop
  addRunni(2);
  res = await fetch(url + "/crop", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ "user-id": userId }),
  });
  if (!res.ok) throw new Error("Crop failed");

  // Step 3: Calculate
  addRunni(3);
  res = await fetch(url + "/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ "user-id": userId }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error("Calculation failed: " + text);
  }

  let result;
  try {
    result = await res.json();
  } catch (e) {
    throw new Error("Invalid JSON from server");
  }

  // Step 4: Almost done
  addRunni(4);

  return result;
}

// Form submission handler
document
  .getElementById("frmUploadIMG")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const imageFile = document.getElementById("eyeimg").files[0];
    if (!imageFile) return;

    document.getElementById("sectionOne").style.display = "none";
    document.getElementById("pagination").children[1].classList.add("active");
    sectionTwo.style.display = "grid";

    try {
      const response = await dataRetrive(imageFile);
      document.getElementById("hLevel").innerText = response.hemo;
    } catch (error) {
      console.error(error);
      removeRunni();
      if (error instanceof TypeError && error.message === "Failed to fetch") {
        alert("Network error: " + error);
      } else {
        alert("Processing failed. " + error.message);
      }
      //location.reload();
      return;
    }

    sectionTwo.style.display = "none";
    document.getElementById("pagination").children[2].classList.add("active");
    document.getElementById("sectionThree").style.display = "grid";

    /*
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
    */
  });

/*
async function processImage() {
  const userId = "user-001";
  const imageInput = document.getElementById("eyeimg").files[0];
  const responseDiv = document.getElementById("response");
  const imagesDiv = document.getElementById("images");
  imagesDiv.innerHTML = "";

  if (!imageInput) {
    alert("Please select an image file.");
    return;
  }

  try {
    // Step 1: Upload
    const formData = new FormData();
    formData.append("image", imageInput);
    formData.append("user-id", userId);

    responseDiv.textContent = "📤 Uploading image...";
    let res = await fetch("/upload", { method: "POST", body: formData });
    let result = await res.json();
    if (!res.ok) throw new Error(result.error || "Upload failed");

    // Step 2: Detect
    responseDiv.textContent += "\n👁️ Detecting eye region...";
    res = await fetch("/detect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "user-id": userId }),
    });
    result = await res.json();
    if (!res.ok) throw new Error(result.error || "Eye detection failed");

    // Step 3: Crop
    responseDiv.textContent += "\n✂️ Cropping conjunctiva...";
    res = await fetch("/crop", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "user-id": userId }),
    });
    result = await res.json();
    if (!res.ok) throw new Error(result.error || "Cropping failed");

    // Step 4: Calculate
    responseDiv.textContent += "\n🧮 Almost done, please wait...";
    res = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "user-id": userId }),
    });
    result = await res.json();
    if (!res.ok) throw new Error(result.error || "Calculation failed");

    responseDiv.innerHTML = `✅ Detection complete!<br><h2><strong>Hemoglobin: ${result.hemo} g/dL</strong></h2>`;

    // Step 5: Fetch user images (NEW SECTION)
    const imgRes = await fetch("/get_images", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "user-id": userId }),
    });

    const imgData = await imgRes.json();
    if (!imgRes.ok) throw new Error(imgData.error || "Could not load images");

    // Display all images in the new section
    imagesDiv.innerHTML = "";
    imgData.images.forEach((url) => {
      const img = document.createElement("img");
      img.src = `${url}?t=${Date.now()}`;
      img.alt = "User processed image";
      imagesDiv.appendChild(img);
    });
  } catch (error) {
    console.error(error);
    responseDiv.textContent = `❌ Error: ${error.message}`;
  }
}
*/

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
