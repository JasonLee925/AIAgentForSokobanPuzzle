import {
  getDocs,
  collection,
  deleteDoc,
  doc
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-firestore.js";
import { db } from "./firebase.js";

const blogSection = document.querySelector(".blogs-section");

// Reference to the "blogs" collection
const blogsCollectionRef = collection(db, "blogs");

// Function to fetch and display blog posts
const fetchBlogs = async () => {
  try {
    const querySnapshot = await getDocs(blogsCollectionRef);

    if (querySnapshot.empty) {
      blogSection.innerHTML = "<p>No photo posts available.</p>";
      return;
    }

    const fragment = document.createDocumentFragment();
    querySnapshot.forEach((docSnapshot) => {
      const data = docSnapshot.data();
      const bannerImage = data.bannerImage || "default-image.jpg";
      const title = data.title
        ? data.title.substring(0, 100) + "..."
        : "No Title";
      const article = data.article
        ? data.article.substring(0, 200) + "..."
        : "No Overview";

      const blogCard = document.createElement("div");
      blogCard.classList.add("blog-card");
      blogCard.innerHTML = `
        <img src="${bannerImage}" class="blog-image" alt="" />
        <h1 class="blog-title">${title}</h1>
        <p class="blog-overview">${article}</p>
        <button class="btn save-btn" data-url="${bannerImage}" download>Save Image</button>
        <button class="btn delete-btn" data-id="${docSnapshot.id}">Delete</button>
      `;
      fragment.appendChild(blogCard);
    });
    blogSection.appendChild(fragment);

    // Add event listener for all buttons
    document.querySelectorAll('.btn').forEach(button => {
      button.addEventListener('click', async (event) => {
        const id = event.target.getAttribute('data-id');
        const url = event.target.getAttribute('data-url');
        if (event.target.classList.contains('delete-btn')) {
          // Handle delete button click
          if (id && confirm('Are you sure you want to delete this blog post?')) {
            try {
              await deleteDoc(doc(db, "blogs", id));
              alert('Blog post deleted successfully.');
              // Refresh the blog section
              blogSection.innerHTML = '';
              fetchBlogs();
            } catch (error) {
              console.error("Error deleting document: ", error);
              alert('Error deleting blog post.');
            }
          }
        } else if (event.target.classList.contains('save-btn')) {
          // Handle save image button click
          if (url) {
            const link = document.createElement('a');
            link.href = url;
            link.download = url.split('/').pop();
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }
        }
      });
    });

  } catch (error) {
    console.error("Error getting documents: ", error);
  }
};

// Fetch and display blogs on page load
fetchBlogs();
