# Football memories  site
Football memories is a website that allows users to add/edit/delete/view football memories for given tournaments. 
It also allows users to rate and comment on football memories

An admin user account has been setup with username/password of admin/Password123
A regular user account has been setup with username/password of
<br>
View the live site [here](https://ci-ms3-footballmemories.herokuapp.com/)
<br><br>

# Table of Contents

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Project Overview
- This project is a website that allows users to add/edit/delete football memories for given tournament for submission as milestone project 3 as part of the Code Institute - Diploma in Software Development (Full stack) course.
- The website is deployed using Heroku pages at the following url: [Football Memories]((https://ci-ms3-footballmemories.herokuapp.com/)
- The repository on Github that contains the website source code and assets is available at the following url: [Code Repository](https://github.com/pmeeny/CI-MS3-FootballMemories)
- The website was built with a responsive look and feel for desktop, tablet and mobile devices

# UX
## Strategy
### Primary Goal
- The primary goal of the website from the site owners perspective is to allow users view/add/modify/delete football memories, to create tournaments so users can add a memory to a tournament and to see statistics about the memories
- The primary goal of the website from a site users perspective is to add/edit/delete memories, view other users memories, rate a memory and comment on a memory

## Structure
I have structured the website into XXX pages, each with clear, concise structure, information and purpose. I use the Bootstrap grid system throughout, which gave a consistent structure and responsive design "out of the box"
1. Home: This is the landing page, and the first page the user encounters when they access the site, before they login/register
2. Register: This page allows the user to register an account to use the site
3. Login: This page allows the user to login to the site
4. Terms and Conditions: This page displays the sites terms and conditions
5. Privacy Policy: This page displays the sites privacy policy
6. Memories: This is the first page the user sees when the login/register, it displays all the football memories that have been added
7. Add Memory: This page allows the user to add a football memory
8. Edit Memory: This page allows a user to edit a memory they have created
9. Delete Memory: This button allows a user to delete a memory they have created
10. Profile: This page displays user information and allows the user to update their profile
11. Dashboard: This page displays statistics about the number of users, memories, comments
12. Tournaments: This page displays the tournaments that have been created by the admin user. An admin user can add/edit or delete a tournament
13. Add Tournament: This page allows an admin user to add a football tournament
14. Edit Tournament: This page allows an admin user to edit a football tournament
15. Delete Tournament: This button allows an admin user to edit a football tournament
16. Logout: This link allows the user to logout of the site
17. Newsletter: The user can enter their email address in the site footer and subscribe to a mailing list
18. 404: The 404 error page is displayed if the user enters in an incorrect url when accessing the site.
19. 500: The 500 error page is displayed if the user encounters an error on the site

## Scope
### User Stories Potential or Existing Customer
The user stories for the website user "regular user" (a potential or existing customer) are described as follows: 
- As a regular user

### User Stories Website Owner
The user stories for the website owner(admin user) are described as follows: 
- As an admin user

## Skeleton
### Wireframes

#### Desktop 


#### Tablet


#### Mobile


## Surface
### Color Palette
I have gone for a simple and minimal design for the website, with black and white font colours over a large hero image on all pages
There are four colours in the color palette with a 
- #FFFFFF - White colour for text on background images
- #000000 - Black colour for text on a white background
- #0062CC - Blue colour for buttons and links
- rgba(255,255,255,.5) - Grey colour for not selected navbar icons and text

### Typography

# Features
The website has five webpages consisting of seven distinct features and they are described below
## Existing Features
### Feature 1 Navigation Bar
#### Description


#### User Stories


### Feature 2 Footer
#### Description


#### User Stories



##  Features Left to Implement

# Technologies Used
## Languages 
- HTML (https://en.wikipedia.org/wiki/HTML)
    - The project uses html to build the relevant pages
- CSS (https://en.wikipedia.org/wiki/CSS)
    - The project uses CSS to style the relevant pages
- Javascript (https://www.javascript.com/)
    - Javascript was used for all scripting on the site

## Libraries and other resources
- Bootstrap 5.0 (https://getbootstrap.com/docs/5.0)
    - The project uses the bootstrap library for some of the UI components in the website
- Gitpod (https://gitpod.io/)
    - Gitpod was used as an IDE for the project
- Github (https://github.com/)
    - Github was used to store the project code in a repository
- Google Fonts (https://fonts.google.com/)
    - Google font Roboto was used as the website font
- Balsamiq (https://balsamiq.com/)
    - Balsamiq was used to create the website wireframes
- Font Awesome (https://fontawesome.com/)
    - Font awesome was used to provide the relevant fonts/icons for the website
- JQuery (https://jquery.com)
    - JQuery was used throughout in several of the javascript files fro DOM manipulation
- TinyPNG (https://tinypng.com/)
    - TinyPNG was used to compress images
 - CSS Validation Service (https://jigsaw.w3.org/css-validator/)
    - CSS validation service for validation the css in the project  
- HTML Markup Validation Service (https://validator.w3.org/)   
    - HTML validation service for validation the css in the project  
- Chrome dev tools (https://developers.google.com/web/tools/chrome-devtools)
    - For troubleshooting and debugging of the project code
- Chrome Lighthouse (https://developers.google.com/web/tools/lighthouse)
    - For performance, accessibility, progressive web apps, SEO analysis of the project code
- Responsive Design (http://ami.responsivedesign.is/)
    - Website for generating the responsive image in this README
- JS Fiddle (https://jsfiddle.net/)
    - Used for testing html and css concepts
- GitHub Wiki TOC generator (https://ecotrust-canada.github.io/markdown-toc/)
    - Used for generating a table of contents for this README
- Cypress (https://www.cypress.io)
    - Cypress was used for automated e2e testing of all pages 

- Google Maps api (https://developers.google.com/maps)
    - The google maps api is used to display the stadium information on the memory page
- Google maps geocode API (https://developers.google.com/maps/documentation/geocoding/start)
    - The google maps geocode api is used to translate the event name returned from the memory stadium name value and translate to a the google maps location on the memory page
- Gofullpage chrome plugin  (https://chrome.google.com/webstore/detail/gofullpage-full-page-scre)
    - This plugin was used to take full page screenshots for testing images
- Python online interpreter (https://www.programiz.com/python-programming/online-compiler/)
    - For testign python code snippets

# Testing
The testing information and results for this project are documented in [TESTING.md](TESTING.md)
Bug 1: add_memory , the memroy name was being stored as null in database
fix: the name field was missing from the form field

Bug2: Add comment was throwing a 404 error. 
Form in memory.html file updated to send in id only, and not memory, that was not required

# Deployment


The project uses a number of API's and the Cypress testing framework, below are the steps to configure the API in your environment




## Google Maps API


## Email JS

## Cypress Testing framework.


# Credits

# Content

Couintry list taken from https://www.technicalkeeda.com/html-tutorials/all-countries-drop-down-list-in-html

photo gallery   https://bootstrapious.com/p/bootstrap-photo-gallery

password validation: https://www.w3schools.com/howto/howto_js_password_validation.asp

Pagination: https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
https://pythonhosted.org/Flask-paginate/

Footer sticks to bottom of page:
https://stackoverflow.com/questions/4575826/how-to-push-a-footer-to-the-bottom-of-page-when-content-is-short-or-missing#:~:text=Just%20wrap%20your%20.,will%20move%20to%20the%20bottom.

Bluprints
schafers youtuibe and github

Password calidation
https://stackoverflow.com/questions/9142527/can-you-require-two-form-fields-to-match-with-html5

aws buckets, public facing and allowing public access to files in the bucket
https://www.youtube.com/watch?v=s1Tu0yKmDKU
https://stackoverflow.com/questions/44228422/s3-bucket-action-doesnt-apply-to-any-resources

jquery documentation:
https://api.jquery.com/replacewith/

<br>

# Media


 <br>

# Acknowledgements
