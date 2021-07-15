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

Bug Number | Comment |  Solution/Design decision |
------------ | ------------- | ------------- | 
1 |  |
Bug 1: add_memory , the memroy name was being stored as null in database
fix: the name field was missing from the form field

Bug2: Add comment was throwing a 404 error. 
Form in memory.html file updated to send in id only, and not memory, that was not required

Bug 3: Delete ytournament was deleting the wrong tournament
Need to pass down the tournament id into the modal

Bug 4: comments not ordered by date on memory page

bug 5: Whe add image to s3, it also stores the file locally
Fix was to use a different method 

Bug 6: A memory on the landing page is a clicable link into the memory
A user should only be able to see this infroamtion if they are logged in
Fix: Update index.html to remove ahref link

Bug 7, an admin can edit a memory, if an admin edits a memory, it then becomes the uploaded by of the memory
This is a bug, an admin should be allowed delete a memeory, but not edit.
Only the memory creator should be allowed to edit a memory
The code was updated to fix this

Bug8, routing not working after adding a comment
Fix in add_comment(id): in toute.py

# Code Validators and Website Analysis
The website's pages were run against the following validators:

## HTML Markup Validation Service
I used https://validator.w3.org/ to validate the html files

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
index.html | Passed, No errors found | [Results](assets/images/testing/html-validation/index_html_validation.jpg)

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
style.css | Passed, No errors found | [Results](assets/images/testing/css-validation/css_validation.JPG)

<br>

## Chrome Dev tools Lighthouse 

(I used Lighthouse https://developers.google.com/web/tools/lighthouse) to test the performance, seo, best practices and accessability of the site

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
index.html (Desktop) | Performance: 98, Accessibility: 100, Best practices: 100, SEO: 100 | [Results](assets/images/testing/lighthouse-testing/index_desktop.JPG)
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

## JSHint
- JSHint was used to analyse the Javascript files

Page | Result | Test Detail/Screenshot
------------ | ------------- | -------------
authentication.js | 0 errors and 0 warnings | [Results](assets/images/testing/jshint/about_jshint.PNG)
memory.js | 0 errors and 0 warnings | [Results](assets/images/testing/jshint/about_jshint.PNG)
send_email.js | 0 errors and 0 warnings | [Results](assets/images/testing/jshint/about_jshint.PNG)

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