// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import {
  getFirestore,
  doc,
  getDoc,
  deleteDoc,
} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAZUPjfQSO6UvNAOZ840K1ni4pD_iCzKII",
  authDomain: "blogging-website-27f1f.firebaseapp.com",
  projectId: "blogging-website-27f1f",
  storageBucket: "blogging-website-27f1f.appspot.com",
  messagingSenderId: "521028220081",
  appId: "1:521028220081:web:c81eba924423979d92de90",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(app);

// Export Firestore instance and functions
export { db, doc, getDoc, deleteDoc };


