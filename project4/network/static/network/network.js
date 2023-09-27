function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

function editPost(postId) {
    const NewText = document.getElementById(`modal-post${postId}`).value;
    const modal = document.getElementById(`EditModal${postId}`);
    fetch(`/edit/${postId}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            post_text : NewText
        })
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById(`text${postId}`).innerText = result.text;
    })
}

function updateLikes(postId, likesList) {
    const likeLink = document.getElementById(`like${postId}`);
    const likeCount = document.getElementById(`like_count${postId}`);
    fetch(`/like/${postId}`)
    .then(response => response.json())
    .then(result => {
        likeCount.innerText = result['likes_count'];
        if (result["newText"] == "Unlike") {
            likeLink.innerHTML = `<img src="static/images/thumbs-down.png" class="thumbs">`
        }
        else {
            likeLink.innerHTML = `<img src="static/images/thumbs-up.png" class="thumbs">`
        }
    })
    }
