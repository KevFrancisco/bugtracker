// Using this library https://bootstrap-validate.js.org/usage.html


// For catching the enter key https://stackoverflow.com/a/45650898/14000441
document.querySelector("input").addEventListener("keyup", event => {
    if(event.key !== "Enter") return; // Use `.key` instead.
    document.querySelector("#btn-save").click(); // Things you want to do.
    event.preventDefault(); // No need to `return false;`.
});

function check_changes(isValid) {
    if (isValid) {
        if ($(".invalid-feedback").length == 0) {
            $("#btn-save").prop("disabled", false);
        } else if ($(".invalid-feedback").length == $(".invalid-feedback:hidden").length) {
            $("#btn-save").prop("disabled", false);
        }
    } else {
        $("#btn-save").prop("disabled", true);
    }
}
/* Short Sheet
name - 100
desc - 555
datetime
*/

bootstrapValidate(
    // The fields to be Validated
    '#f_proj_name',
    // Rules to use, we hane Alpha + ' '
    'regex:^[a-zA-Z0-9 ]*$:Invalid character.|max:100:Your Project Name must not be longer than 100 characters|min:5:Your Project Name must not be shorter than 5 characters|required:Please enter a Project Name.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_proj_user_id',
    'required:Please choose a Project Manager.',
    function (isValid) {
        check_changes(isValid);
});

bootstrapValidate(
    '#f_proj_desc',
    'regex:^[a-zA-Z0-9, \n\r.]*$:Contains invalid characters.|max:555:Your Project Description must not be longer than 555 characters|min:5:Your Project Description must not be shorter than 5 characters|required:Please enter a project description.',
    function (isValid) {
        check_changes(isValid);
});