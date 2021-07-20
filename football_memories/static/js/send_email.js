/**
 * [sendEmail to send email using EmailJS
 * Credit: Code Institute material "Sending Emails Using EmailJS"]
 * The API that is used is described here: https://www.emailjs.com/
 * @param contactForm [The contact form object]
 */
 function sendMail(contactForm) {
    emailjs.init("user_wxBAvg07l9uKgfV3nW0x3");
    emailjs.send("gmail", "football_memories", {
        "to_email": contactForm.email_address.value
    }).then(
        function (response) {
            console.log("SUCCESS")
            $("#mailing-list").replaceWith( "Thanks for subscribing to our mailing list" );
        },
        function (error) {
            console.log("FAILED", error);
        }
    );
    return false;  // To block from loading a new page
}