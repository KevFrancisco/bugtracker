// Using this library https://bootstrap-validate.js.org/usage.html

function check_changes(isValid) {
    if (isValid) {
        if ($(".invalid-feedback").length == 0) {
            $("#btn-register").prop("disabled", false);
        } else if ($(".invalid-feedback").length == $(".invalid-feedback:hidden").length) {
            $("#btn-register").prop("disabled", false);
        }
    } else {
        $("#btn-register").prop("disabled", true);
    }
}

(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();


bootstrapValidate(
    '#f_user_name',
    'alphanum:Only Alphanumeric (a-Z, 0-9) characters are allowed.|max:30:Your username must not be longer than 30 characters|min:3:Your username must not be shorter than 3 characters|required:Please enter a username.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_email',
    'required:Please enter an email.|email:Please enter a valid email.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_password',
    'alphanum:Only Alphanumeric (a-Z, 0-9) characters are allowed.|max:30:Your password must not be longer than 30 characters|min:3:Your password must not be shorter than 3 characters|required:Please enter a password.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_confirmation',
    'matches:#f_user_password:Passwords must match.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_first_name',
    'regex:^[a-zA-Z ]*$:Only Alpha (a-Z) and Space (\' \') characters are allowed.|max:50:Your name must not be longer than 50 characters|min:3:Your name must not be shorter than 3 characters|required:Please enter a first and last name.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    // The fields to be Validated
    '#f_user_last_name',
    // Rules to use, we hane Alpha + ' '
    'regex:^[a-zA-Z ]*$:Only Alpha (a-Z) and Space (\' \') characters are allowed.|max:50:Your name must not be longer than 50 characters|min:3:Your name must not be shorter than 3 characters|required:Please enter a first and last name.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_role',
    'required:Please choose a role.|inArray:(Admin,Submitter,Developer,Project Manager):Your input must be from above',
    function (isValid) {
        check_changes(isValid);
});



/*

const form = document.querySelector("#registerform")
const username = document.querySelector("#regusernameinput")
const usernamefeedback = document.querySelector("#usernamefeedback")
const password = document.querySelector("#regpasswordinput")
const passwordfeedback = document.querySelector("#passwordfeedback")
const confirmation = document.querySelector("#regconfirmationinput")
const confirmationfeedback = document.querySelector("#confirmationfeedback")
const register = document.querySelector("#registerbutton")

form.addEventListener('keyup', (e) => {
  
    if (confirmation.value != '' && 
        confirmation.value != null && 
        username.value != null && 
        username.value != '' && 
        password.value != null && 
        password.value != '') {
        register.disabled = false;
    }
    else {
        register.disabled = true;
    }

})

form.addEventListener('submit', (e) => {
    var nameRegex = /^[a-zA-Z0-9\-]+$/;
    var validusername = username.value.match(nameRegex);

    if(validusername == null){
        username.classList.add("is-invalid");
        usernamefeedback.innerHTML = "Username invalid. Only characters A-Z, a-z, 0-9 and '-' are  acceptable.";
        usernamefeedback.classList.add("invalid-feedback")
        usernamefeedback.classList.add("d-block")
        usernamefeedback.classList.add("mb-2")
        e.preventDefault()
    } else if (validusername != null){
        username.classList.remove("is-invalid");
        username.classList.add("is-valid");
        usernamefeedback.innerHTML = "";
        usernamefeedback.classList.remove("invalid-feedback")
        usernamefeedback.classList.remove("d-block")
        usernamefeedback.classList.remove("mb-2")
    }

    if (password.value != confirmation.value) {
        confirmation.classList.add("is-invalid");
        confirmationfeedback.innerHTML = "Passwords do not match."
        confirmationfeedback.classList.add("invalid-feedback")
        e.preventDefault()
    }

    var pwdRegex = /^[a-zA-Z0-9]+$/;
    var validpassword = password.value.match(pwdRegex);
    var validconfirmation = confirmation.value.match(pwdRegex)

    if (validpassword == null){
        password.classList.add("is-invalid");
        passwordfeedback.innerHTML = "Password invalid. Only characters A-Z, a-z and '-' are  acceptable.";
        passwordfeedback.classList.add("invalid-feedback");
        passwordfeedback.classList.add("d-block");
        passwordfeedback.classList.add("mb-2");
        e.preventDefault()
    } else if (validpassword != null && validconfirmation != null && validpassword == validconfirmation) {
        password.classList.add("is-valid");
        password.classList.remove("is-invalid");
        passwordfeedback.innerHTML = "";
        passwordfeedback.classList.remove("invalid-feedback");
        passwordfeedback.classList.remove("d-block");
        passwordfeedback.classList.remove("mb-2");
    }

    
})

*/