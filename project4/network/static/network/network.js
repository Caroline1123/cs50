function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

function editPost(postId) {
    const NewText = document.getElementById(`modal-post${postId}`).value;
    const modal = document.getElementById(`EditModal${postId}`);
    console.log(NewText);
    console.log(postId);
    console.log(modal);
    fetch(`/edit/${postId}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            post_text : NewText
        })
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById(`text${postId}`).innerHTML = result.text;
        
        // on every modal change state like in hidden modal
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');
    
        // get modal backdrops
        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');
    
        // remove every modal backdrop
        for(let i=0; i < modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);
        }
    })
}