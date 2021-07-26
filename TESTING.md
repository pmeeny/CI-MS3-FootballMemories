# Table of Contents

# Testing
The testing approach(described in detail in this testing readme) is as follows:
1. Manual testing using emulators and real devices
2. 
## Manual testing information
Testing was completed on the following browsers and device types

Device Number | Physical/Emulator | Device Name | Device Type | Browser | Version
------------ | ------------ | ------------- | ------------- | ------------- | -------------
1 | Physical | iPad | Tablet |  Safari | 14.4 |
2 | Physical | iPhone | Mobile |Safari | 14.4 |
3 | Physical | One Plus 5 | Mobile | Chrome | 88.0 |
4 | Physical | Windows Desktop| Desktop | IE Edge | 88.0 |
5 | Physical | Windows Desktop| Desktop | Mozilla Firefox | 85.0 |
6 | Physical | Windows Desktop| Desktop | Chrome | 86.0 |
7 | Emulator | Galaxy S5 | Mobile | Chrome Emulator | 86.0 |
8 | Emulator | iPad | Tablet | Chrome Emulator | 86.0 |
9 | Emulator | iPhone X | Mobile | Chrome Emulator | 86.0 |
10 | Emulator | iPhone 5/SE | Mobile | Chrome Emulator | 86.0 |

- Below are the test results for testing the website requirements against a range of browsers and devices
- For the purpose of the screenshots I used a Chrome emulator for desktop, tablet and mobile (Device numbers 6(Desktop), 8(Tablet), 9(Mobile))

## Feature 1 Navigation Bar
### User Story
User Story 1.1: 

### Test case steps
1. 

### Expected Result
1.
2.

## Feature 2 Footer
### User Story


# Bugs found during the testing phase

Bug no. | Bug description |  Bug fix |
------------ | ------------- | ------------- | 
1 | When adding a memory, the memory_name was being stored as null in the memory collection| The "name" field was missing from the form field for the input type memory_name
2 | Adding a comment was throwing a 404 error | The form in memory.html file updated to send in id only, and not memory, that was not required
3 | Deleting a tournament was deleting the wrong tournament| The tournament id needed to be correctly passed down into the modal
4 | Comments not ordered by date on memory page | The fix was to sort by date <code> mongo.db.comments.find({"memory_id":  id}).sort("_id", -1) </code>
5 | When an image was added to s3, it stores the file locally also | The fix was to use the put_object boto3 method 
6 | A memory on the index/landing page was clickable, only a logged in user should be able to see the memory information | The fix was to remove the a href link 
7 | An admin should not be able to edit a users memory. Only the memory creator should be allowed to edit a memory | The fix was to update the memory route and memories template
8 | After adding a comment, the user was not routed back to the memory | Fix in add_comment(id): in route.py (memories)
9 | The email js code was sending the email to the same user, a test user.|  The fix was to update the send_email.js to update a parameter, and then update the emailjs template accordingly with a link to that field<code>"to_email": contactForm.email_address.value</code>
10 | Editing an admin user incorrectly updates the users user_type to regular_user| The fix in route.py (administration) was to get the users type first and store that when updating the users profile


# Code Validators and Website Analysis
The website's pages was tested against the following validators:

## HTML Markup Validation Service
I used https://validator.w3.org/ to validate the html files

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
index.html | Passed, No errors found | [Results](assets/images/testing/html-validation/index_html_validation.jpg)
TBC
TBC

<br>

## CSS Validation Service
I used https://jigsaw.w3.org/css-validator/ to validate the css(style.css)
<p>
    <a href="https://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="https://jigsaw.w3.org/css-validator/images/vcss"
            alt="Valid CSS!" />
    </a>
</p>

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
style.css | Passed, No errors found | [Results](/football_memories/static/images/css_validation/css_validation.PNG)

<br>

## Chrome Dev tools Lighthouse 

(I used Lighthouse https://developers.google.com/web/tools/lighthouse) to test the performance, seo, best practices and accessability of the site

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
index.html (Desktop) | Performance: 98, Accessibility: 100, Best practices: 100, SEO: 100 | [Results](/football_memories/static/images/wave_validation/wave_landing.PNG)
football_memories/templates/base.html | 0 errors and 0 contrast errors| [Results](assets/images/testing/wave-validation/index_wave_validation.PNG)
football_memories/templates/administration/dashboard.html | 0 errors and 0 contrast errors|
football_memories/templates/administration/index.html  | 0 errors and 0 contrast errors|
football_memories/templates/administration/privacy_policy.html  | 0 errors and 0 contrast errors|
football_memories/templates/administration/terms_and_conditions.html  | 0 errors and 0 contrast errors|
football_memories/templates/authentication/login.html | 0 errors and 0 contrast errors|
football_memories/templates/authentication/profile.html | 0 errors and 0 contrast errors|
football_memories/templates/authentication/register.html | 0 errors and 0 contrast errors|
football_memories/templates/errors/404.html | 0 errors and 0 contrast errors|
football_memories/templates/errors/500.html | 0 errors and 0 contrast errors|
football_memories/templates/memories/add_memory.html | 0 errors and 0 contrast errors|
football_memories/templates/memories/edit_memory.html | 0 errors and 0 contrast errors|
football_memories/templates/memories/memories.html | 0 errors and 0 contrast errors|
football_memories/templates/memories/memory.html | 0 errors and 0 contrast errors|
football_memories/templates/tournaments/add_tournament.html | 0 errors and 0 contrast errors|
football_memories/templates/tournaments/edit_tournament.html | 0 errors and 0 contrast errors|
football_memories/templates/tournaments/tournament.html | 0 errors and 0 contrast errors|

<br>

## Wave Accessibility
- Wave accessibility(https://wave.webaim.org/) was used to test the websites accessibility

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
football_memories/templates/administration/dashboard.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_dashboard.PNG)
football_memories/templates/administration/index.html  | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_landing.PNG)
football_memories/templates/administration/privacy_policy.html  | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_dashboard.PNG)
football_memories/templates/administration/terms_and_conditions.html  | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_terms_and_conditions.PNG)
football_memories/templates/authentication/login.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_login.PNG)
football_memories/templates/authentication/profile.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_profile.PNG)
football_memories/templates/authentication/register.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_register.PNG)
football_memories/templates/errors/404.html | 0 errors and 0 contrast errors|
football_memories/templates/errors/500.html | 0 errors and 0 contrast errors|
football_memories/templates/memories/add_memory.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_add_memory.PNG)
football_memories/templates/memories/edit_memory.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_edit_memory.PNG)
football_memories/templates/memories/memories.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_memories.PNG)
football_memories/templates/memories/memory.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_memory.PNG)
football_memories/templates/tournaments/add_tournament.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_add_tournament.PNG)
football_memories/templates/tournaments/edit_tournament.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_edit_tournament.PNG)
football_memories/templates/tournaments/tournament.html | 0 errors and 0 contrast errors| [Results](/football_memories/static/images/wave_validation/wave_tournaments.PNG)

## JSHint
- JSHint was used to analyse the Javascript files

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
authentication.js | 0 errors and 0 warnings | [Results](football_memories/static/images/jshint/authentication.PNG)
memory.js | 0 errors and 0 warnings | [Results](football_memories/static/images/jshint/memory.PNG)
send_email.js | 0 errors and 0 warnings | [Results](football_memories/static/images/jshint/send_email.PNG)

<br>

## PEP8Online
- PEP8online was used to analyse the Javascript files

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
app.py | | [Results](assets/images/testing/jshint/about_jshint.PNG)
football_memories/__init__.py |  | [Results](assets/images/testing/jshint/about_jshint.PNG)
football_memories/administration/routes.py |  | [Results](assets/images/testing/jshint/about_jshint.PNG)
football_memories/authentication/routes.py |  | [Results](assets/images/testing/jshint/about_jshint.PNG)
football_memories/errors/routes.py |  | [Results](assets/images/testing/jshint/about_jshint.PNG)
football_memories/memories/routes.py |  | [Results](assets/images/testing/jshint/about_jshint.PNG)
football_memories/tournaments/routes.py |  | [Results](assets/images/testing/jshint/about_jshint.PNG)