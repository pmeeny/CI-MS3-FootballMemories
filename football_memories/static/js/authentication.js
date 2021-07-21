// Example starter JavaScript for disabling form submissions if there are invalid fields
// Credit: https://getbootstrap.com/docs/5.0/forms/validation/
  var forms = document.querySelectorAll('.needs-validation');
  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add('was-validated');
      }, false);
    });
/**
* [validateUserNameAndPassword() validates the 
  username and password against a regular expression]
*/
function validateUserNameAndPassword(){
  var username = document.getElementById("username");
  var password = document.getElementById("password");
  var confirm_password = document.getElementById("confirm-password");
  // Username must be a minimum of 6 characters and contain at least one lowercase letter, with no special characters
  var regExprUsername= /^(?=.*[a-z])\w{6,}$/;
  // Password must be a minimum of 6 characters and contain least one number, one lowercase and one uppercase letter, with no special characters
  var regExprPassword = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/;
  // Username validation
  if(!(regExprUsername.test(username.value))){
    username.setCustomValidity("Username doesnt match pattern");
  }else {
    username.setCustomValidity('');
  }
  // Password validation
  if(!(regExprPassword.test(password.value))){
    password.setCustomValidity("Password doesnt match pattern");
  }else {
    password.setCustomValidity('');
  }
  // Compare password fields and check do they match
  if(password.value != confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity('');
  }
}