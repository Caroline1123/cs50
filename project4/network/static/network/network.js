document.addEventListener('DOMContentLoaded', function() {

  document.querySelector("#create-post").onsubmit = create_post;
  
  // By default, load the posts
  load_posts();
  console.log("after load posts");
  });

function create_post() {
  // Store text of the post
  let text = document.querySelector('#text').value;
  // Create JSON object and post it
  fetch('/posts', {
    method: 'POST',
    body: JSON.stringify({
        text:text,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Reset text field and reload the page
      document.querySelector('#text').value = "";
      location.reload();
      console.log(result);
  });
  return false;
}

function load_posts() {
  // Retrieve existing posts
  fetch("/posts")
  .then(response => response.json())
  .then(posts => {
      // Print posts
      console.log(posts);
      posts.forEach(post => {
        const ViewPost = document.createElement('div');
        ViewPost.setAttribute("id", "view-post");
        // Inject display fields of the post to page
        ViewPost.innerHTML = `
        <div class="user"><a href="#" onclick="show_profile('${post.user}')"> ${post.user}</a></div>
        <div class="edit">Edit</div>
        <div class="text">${post.text}</div>
        <div class="timestamp">${post.timestamp}</div>
        <div class="likes">\u2764${post.likes}</div>
        <div class="comment">Comment</div>
        `;
        document.querySelector('#post-view').append(ViewPost);
        //document.querySelector('.user').addEventListener('click', () => show_profile(post.user));
      })
    });
}

function show_profile(username) {
  
  fetch(`users/${username}`)
  .then (response => response.json())
  .then (user => 
    {console.log(user);
  
  });
}