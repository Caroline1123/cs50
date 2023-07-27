document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // Add send function to compose form's submit button
  document.querySelector('#compose-form').onsubmit = send_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      emails.forEach(email => {
        const ViewEmail = document.createElement('div');
        ViewEmail.setAttribute("class", "view-email");
        ViewEmail.innerHTML = `
        <div class="sender">${email.sender}</div>
        <div class="subject">${email.subject}</div>
        <div class="timestamp">${email.timestamp}</div>
        `;
        if (email.read === true) {
          ViewEmail.style.backgroundColor = "rgb(240, 240, 240)";
        }
        ViewEmail.addEventListener('click', () => view_email(email.id, mailbox));
        document.querySelector('#emails-view').append(ViewEmail);
      })
    });

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

// Send email
function send_email() {
  // Store all submitted form values
  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;
  // Create JSON object and post it
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
      // Redirect to sent mailbox
      console.log(result);
      load_mailbox('sent');
  });
  // Return false to prevent default submissions of form
  return false;
}

// Displays details of the selected email and sets read status
function view_email(id, mailbox) {
  // Set email status to "read"
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  // Pass on all info about the mails to the page
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#email-details').innerHTML = `
        <b>From:</b> ${email.sender}<br>
        <b>To:</b> ${email.recipients}<br>
        <b>Subject:</b> ${email.subject}<br>
        <b>Timestamp:</b> ${email.timestamp}<br>
        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
        <button class="btn btn-sm btn-outline-primary" id="un-archive" hidden>Archive</button>
        <hr>
        ${email.body}
      `;
      // Add event listener to reply button
      document.querySelector("#reply").addEventListener('click', () => reply(id));
      // Add event listener to un-archive button
      let archiveButton = document.querySelector("#un-archive");
      archiveButton.addEventListener('click', () => archive(id));
      // Check if the selected email is in the inbox
      if (mailbox === 'inbox') {
        // Make Archive button visible
        archiveButton.removeAttribute("hidden");
        // Add event listener on archive button to place mail to archived box
        }
      else if (mailbox === 'archive') {
        // Change text on archive button to Unarchive
        archiveButton.innerHTML = "Unarchive";
        archiveButton.removeAttribute("hidden");
      }
    });
  // Hide unwanted divs and show details div
  document.querySelector('#email-details').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
}
  
function archive(id) {
  // Check if email is currently archived or unarchived
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          // set archive status to opposite of current status
          archived: !email.archived
      })
    })
    // Load inbox
    .then(() => {
    load_mailbox('inbox');
    })
  });
}

function reply(id) {
  compose_email()
  fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      if (email.subject.startsWith('Re:') ) {
        document.querySelector('#compose-subject').value = `${email.subject}`;
      }
      else {
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      }
      document.querySelector('#compose-body').value = `\n---------------\nOn ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
    })
}