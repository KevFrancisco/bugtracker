// Using this library https://bootstrap-validate.js.org/usage.html


// Submit form when the user presses the enter key https://stackoverflow.com/a/45650898/14000441
// Listen to key up on input
document.querySelectorAll("input").forEach(inp => 
    addEventListener("keypress", event => {
    if(event.key !== "Enter") return; // Use `.key` instead.
    document.querySelector("#bv-submit").click(); // Things you want to do.
    event.preventDefault(); // No need to `return false;`.
    }
));

// Enable the submit button if all fields are valid
function check_changes(isValid) {
if (isValid) {
    // If there are no invalid indicators
    if ($(".invalid-feedback").length == 0) {
        $("#bv-submit").prop("disabled", false);
    // Or if the invalid indicators are all hidden
    } else if ($(".invalid-feedback").length == $(".invalid-feedback:hidden").length) {
        $("#bv-submit").prop("disabled", false);
    }
} else {
    $("#bv-submit").prop("disabled", true);
}
}

bootstrapValidate(
'.bv-req',
'required:Required.',
function (isValid) {
    check_changes(isValid);
});

bootstrapValidate(
'.bv-alphaspacenum',
'regex:^[a-zA-Z0-9\ \?\']*$:Invalid characters.',
function (isValid) {
    check_changes(isValid);
});

bootstrapValidate(
'.bv-alphaspacenumarea',
'regex:^[a-zA-Z0-9.,\-\:\?\(\)\' ]*$:Invalid characters.',
function (isValid) {
    check_changes(isValid);
});

bootstrapValidate(
'.bv-max50',
'max:50:May not be longer than 50 characters',
function (isValid) {
    check_changes(isValid);
});

bootstrapValidate(
'.bv-max555',
'max:555:May not be longer than 555 characters',
function (isValid) {
    check_changes(isValid);
});

bootstrapValidate(
'.bv-min5',
'min:5:May not be shorter than 5 characters',
function (isValid) {
    check_changes(isValid);
});