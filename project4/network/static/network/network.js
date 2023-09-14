document.addEventListener("DOMContentLoaded", (event) => {

    document.querySelector("#saveChanges").addEventListener("click", editPost);

});

function editPost() {
    NewText = document.querySelector("#modal-post").value
    console.log(NewText)
    fetch(`edit/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            post_text : NewText
        }),
        }
    )};