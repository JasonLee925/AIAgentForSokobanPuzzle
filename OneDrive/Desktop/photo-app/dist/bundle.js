/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => {
  // webpackBootstrap
  /******/ var __webpack_modules__ = {
    /***/ "./public/js/editor.js":
      /*!*****************************!*\
  !*** ./public/js/editor.js ***!
  \*****************************/
      /***/ () => {
        eval(
          'const blogTitleField = document.querySelector(".title");\nconst articleField = document.querySelector(".article");\n\n// Banner\nconst bannerImage = document.querySelector("#banner-upload");\nconst banner = document.querySelector(".banner");\nlet bannerPath;\nconst publishBtn = document.querySelector(".publish-btn");\nconst uploadInput = document.querySelector("#image-upload");\n\n// Ensure correct event listener attachment\nbannerImage.addEventListener("change", () => {\n  uploadImage(bannerImage, "banner");\n});\nuploadInput.addEventListener("change", () => {\n  uploadImage(uploadInput, "image");\n});\nconst uploadImage = (uploadFile, uploadType) => {\n  const [file] = uploadFile.files;\n  if (file && file.type.includes("image")) {\n    const formdata = new FormData();\n    formdata.append("image", file);\n    fetch("/upload", {\n      method: "POST",\n      body: formdata\n    }).then(res => {\n      if (!res.ok) {\n        throw new Error("Network response was not ok");\n      }\n      return res.json();\n    }).then(data => {\n      if (uploadType === "image") {\n        addImage(data, file.name);\n      } else {\n        bannerPath = `${location.origin}/${data}`;\n        banner.style.backgroundImage = `url("${bannerPath}")`;\n      }\n    }).catch(error => {\n      console.error("There was a problem with the upload:", error);\n      alert("Image upload failed. Please try again.");\n    });\n  } else {\n    alert("Please upload a valid image file.");\n  }\n};\nconst addImage = (imagepath, alt) => {\n  let curPos = articleField.selectionStart;\n  let textToInsert = `![${alt}](${imagepath})`; // Markdown image syntax\n\n  // Insert text at cursor position\n  articleField.value = articleField.value.slice(0, curPos) + textToInsert + articleField.value.slice(curPos);\n  let months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Jun", "Aug", "Sep", "Oct", "Nov", "Dec"];\n\n  // Reset cursor position after insertion\n  articleField.selectionStart = articleField.selectionEnd = curPos + textToInsert.length;\n};\n\n// Debugging: log current state\nconsole.log("Editor initialized");\npublishBtn.addEventListener("click", () => {\n  if (articleField.value.length && blogTitleField.value.length) {\n    //generating id\n    let letters = "abcdefghijklmnopqrstuvwvyz";\n    let blogTitle = blogTitleField.value.split(" ").join("-");\n    let id = "";\n    for (let i = 0; i < 4; i++) {\n      id += letters[Math.floor(Math.random() * letters.length)];\n    }\n\n    // setting up docName\n    let docName = `${blogTitle}-${id}`;\n    let date = new Date(); //for published at info\n\n    //access firestore with db variable;\n    db.collection("blogs").doc(docName).set({\n      title: blogTitleField.value,\n      article: articleField.value,\n      bannerImage: bannerPath,\n      publishedAt: `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`\n    }).then(() => {\n      console.log("date entered");\n    }).catch(err => {\n      console.error(err);\n    });\n  }\n});\n\n//# sourceURL=webpack://bloggin-site/./public/js/editor.js?'
        );

        /***/
      },

    /******/
  };
  /************************************************************************/
  /******/
  /******/ // startup
  /******/ // Load entry module and return exports
  /******/ // This entry module can't be inlined because the eval devtool is used.
  /******/ var __webpack_exports__ = {};
  /******/ __webpack_modules__["./public/js/editor.js"]();
  /******/
  /******/
})();
