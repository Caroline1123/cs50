document.addEventListener("DOMContentLoaded", function() {

    const saveButton = document.getElementById("saveButton");
    saveButton.addEventListener('click', checkMail);
})

function fadeOut(element) {
    setTimeout(function() {
        element.classList.add("fade-out");
        setTimeout(function() {
            element.style.display= 'none';
            element.classList.remove('fade-out');
        }, 700);
    }, 2000);
}

function checkMail() {
    const mail = document.getElementById("newsLetterMail").value;
    let re = /^\S+@\S+\.\S+$/;
    const is_valid = re.test(mail);
    console.log(is_valid);

    if (is_valid == true) {
        const successBox = document.getElementById("successAlert");
        successBox.innerText = "Successfully registered to the newsletter";
        successBox.style.display = "block";
        $("#NewsletterModal").modal("hide");
        fadeOut(successBox);
    }
    else {
        const ErrorBox = document.getElementById("alertBox");
        ErrorBox.innerText = "Invalid email address";
        ErrorBox.style.display = "block";
        fadeOut(ErrorBox);
    }
}
