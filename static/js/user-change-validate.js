// Using this library https://bootstrap-validate.js.org/usage.html


// For catching the enter key https://stackoverflow.com/a/45650898/14000441
document.querySelector("input").addEventListener("keyup", event => {
    if(event.key !== "Enter") return; // Use `.key` instead.
    document.querySelector("#bv-submit").click(); // Things you want to do.
    event.preventDefault(); // No need to `return false;`.
});

function check_changes(isValid) {
    if (isValid) {
        if ($(".invalid-feedback").length == 0) {
            $("#bv-submit").prop("disabled", false);
        } else if ($(".invalid-feedback").length == $(".invalid-feedback:hidden").length) {
            $("#bv-submit").prop("disabled", false);
        }
    } else {
        $("#bv-submit").prop("disabled", true);
    }
}

bootstrapValidate(
    // The fields to be Validated
    '#f_user_first_name',
    // Rules to use, we hane Alpha + ' '
    'regex:^[a-zA-Z ]*$:Only Alpha (a-Z) and Space (\' \') characters are allowed.|max:50:Your name must not be longer than 50 characters|min:3:Your name must not be shorter than 3 characters|required:Please enter a first name.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_last_name',
    'regex:^[a-zA-Z ]*$:Only Alpha (a-Z) and Space (\' \') characters are allowed.|max:50:Your name must not be longer than 50 characters|min:3:Your name must not be shorter than 3 characters|required:Please enter a last name.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_user_name',
    'alphanum:Only Alphanumeric (a-Z, 0-9) characters are allowed.|max:30:Your name must not be longer than 30 characters|min:3:Your name must not be shorter than 3 characters|required:Please enter a user name.',
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
    '#f_user_role',
    'required:Please choose a role.|inArray:(Admin,Submitter,Developer,Project Manager):Your input must be from above',
    function (isValid) {
        check_changes(isValid);
});