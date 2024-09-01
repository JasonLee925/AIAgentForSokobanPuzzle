import { db } from "./firebase.js";
import {
  collection,
  doc,
  setDoc,
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-firestore.js";

document.addEventListener("DOMContentLoaded", () => {
  const blogTitleField = document.querySelector(".title");
  const articleField = document.querySelector(".article");
  const bannerImage = document.querySelector("#banner-upload");
  const banner = document.querySelector(".banner");
  const publishBtn = document.querySelector(".publish-btn");
  const uploadInput = document.querySelector("#image-upload");

  let bannerPath = "";
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];

  // Event listeners for image uploads
  if (bannerImage) {
    bannerImage.addEventListener("change", () =>
      handleImageUpload(bannerImage, "banner")
    );
  } else {
    console.error("Element with ID 'banner-upload' not found.");
  }

  //if (uploadInput) {
  //  uploadInput.addEventListener("change", () =>
  //    handleImageUpload(uploadInput, "image")
  // );
  //} else {
  //  console.error("Element with ID 'image-upload' not found.");
  //}

  async function handleImageUpload(inputElement, type) {
    const [file] = inputElement.files;
    if (!file || !file.type.includes("image")) {
      alert("Please upload a valid image file.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      if (data.imageUrl) {
        const imagePath = data.imageUrl;

        if (type === "image") {
          insertImageMarkdown(imagePath, file.name);
        } else {
          bannerPath = `${location.origin}/${imagePath}`;
          banner.style.backgroundImage = `url("${bannerPath}")`;
        }
      } else {
        throw new Error("Unexpected response format");
      }
    } catch (error) {
      console.error("There was a problem with the upload:", error);
      alert("Image upload failed. Please try again.");
    }
  }

  function insertImageMarkdown(imagePath, altText) {
    const curPos = articleField.selectionStart;
    const markdown = `![${altText}](${imagePath})`;
    articleField.value = `${articleField.value.slice(
      0,
      curPos
    )}${markdown}${articleField.value.slice(curPos)}`;
    articleField.selectionStart = articleField.selectionEnd =
      curPos + markdown.length;
  }

  if (publishBtn) {
    publishBtn.addEventListener("click", publishBlog);
  } else {
    console.error("Element with class 'publish-btn' not found.");
  }

  function countWords(text) {
    return text.trim().split(/\s+/).length;
  }

  async function publishBlog() {
    const title = blogTitleField.value.trim();
    const article = articleField.value.trim();

    if (countWords(title) > 15) {
      alert("Title cannot exceed 15 words.");
      return;
    }

    if (countWords(article) > 20) {
      alert("Article cannot exceed 20 words.");
      return;
    }

    if (!title || !article || !bannerPath) {
      alert("Title, article content, and banner image cannot be empty.");
      return;
    }

    const id = generateRandomId();
    const docName = `${title.split(" ").join("-")}-${id}`;
    const date = new Date();
    const publishedAt = `${date.getDate()} ${
      months[date.getMonth()]
    } ${date.getFullYear()}`;

    try {
      await setDoc(doc(collection(db, "blogs"), docName), {
        title,
        article,
        bannerImage: bannerPath,
        publishedAt,
        userType: "standard", // Adjust this based on user type or other criteria
      });
      console.log("Document written successfully");
      location.href = "home.html"; // Redirect to home.html
    } catch (error) {
      console.error("Error adding document:", error);
      alert("Failed to publish the blog. Please try again.");
    }
  }

  function generateRandomId() {
    const letters = "abcdefghijklmnopqrstuvwxyz";
    return Array.from(
      { length: 4 },
      () => letters[Math.floor(Math.random() * letters.length)]
    ).join("");
  }

  console.log("Editor initialized");
});
