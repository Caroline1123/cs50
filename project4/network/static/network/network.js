document.addEventListener('DOMContentLoaded', function () {
  const editButton = document.querySelector('[data-bs-target="#EditModal"]');
  const saveButton = document.querySelector('#saveChanges');
  const modalPostTextarea = document.getElementById('modal-post');

  

  editButton.addEventListener('click', function () {
    getPostText(editButton, modalPostTextarea);
  });

  // saveButton.addEventListener('click', function () {
  //   getPostText(editButton, modalPostTextarea);
  // });

});


function getPostText(editButton, modalPostTextarea) {
  var postText = editButton.getAttribute('data-post-content');
  modalPostTextarea.value = postText;
}
