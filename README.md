# Football memories site
Football memories is a website that allows users to add/edit/delete/view football memories for given tournaments. 
It also allows users to rate and comment on football memories
- There are two types of users, and I have setup accounts for both
    - An admin user account has been setup with username/password of admin/Password123
    - A regular user account has been setup with username/password of
<br>

View the live site [here](https://ci-ms3-footballmemories.herokuapp.com/)
<br><br>
![Responsive site example](/football_memories/static/images/am_i_responsive/responsive_devices.png)

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
The primary goal of the website from the site 
owners perspective is as follows:
- To create/edit/delete tournaments so users can add a memory to a tournament(name and image)
- To allow users add/modify/delete their football memories(name, image, tournament, description, date, stadium)
- To allow users view their memories and other users memories
- To allow users comment on a memory
- To allow users rate a memory with a score from 1-5
- To delete a memory if required
- To view statistics on the usage of the site

The primary goal of the website from a site users perspective is as follows:
- To add/modify/delete their football memories(name, image, tournament, description, date, stadium)
- To view their memories and other users memories
- To comment on a memory
- To rate a memory with a score from 1-5

## Structure
### Database
- The website is a data-centric one with html, javscript, css used with the boostrap framework as a frontend
- The backend comprises of Python, flask and jinja templates with a database of a mongodb open-source document-oriented database


#### Conceptual database model
The first step in the database design was the create a conceptual data model. The helped me understand the design at a conceptual level while enabling me to understand the required collections in the database
![conceptual](/football_memories/static/images/database_design/conceptual_design_model.png)

#### Physical database model
From the conceptual database model I created the physical database model. This model contains all fields stored in the database collections with their data type and mimics the structure of what is actually stored in the mongo database(mongodb)
![conceptual](/football_memories/static/images/database_design/physical_design_model.png)

#### Mongo DB database information
- One production database(football_memories_prod) was created to store site information, it contains five collections described below
1. users - to store regusterd user information
2. tournaments - to store tournament information added by an admin user
3. memories - to store memory information added by an admin/regular user
4. comments - to store comment information for a memory added by an admin/regular user
5. ratings - to store rating information for a memory added by an admin/regular user

#### Users
- The users collection is used to store user information when they register.
- The fields stored in the collection are users username(String), password(String), first_name(String), last_name(String), favourite_team(String) and country(String) with a unique identifier(primary key) , "_id"(Object Id)
- The users password is encypted using a generate_password_hash from a werkzeug.security Python library.
![users](/football_memories/static/images/database_design/users.PNG)

#### Tournaments
- The tournaments that memories are added to are added by an admin user.
- The fields stored in the collection are the tournament name(String) and tournament image(String) with a unique identifier(primary key)  automatically assigned by the mongodb, "_id"(Object Id) primary key
![tournaments](/football_memories/static/images/database_design/tournaments.PNG)

#### Memories
- Memories are added by regular and admin users
- The fields stored in the collection are the memory_image(String), tournament name(String), memory name(String), memory_description(String), memory_date(String), memory_stadium(String), memory_view_count(Int32), memory_created_by(username) with a unique identifier(primary key) automatically assigned by the mongodb, "_id"(Object Id)
- When a user adds a memory, it stores the tournament name(from the tournaments added in the tournament table) and a memory_created_by(take from the User tables username field of the user who added the memory) to create a link between the two collections

![memories](/football_memories/static/images/database_design/memories.PNG)

#### Comments
- Comments are added to a memory by a regular or admin user
- The fields stored in the collection are the memory_id(String), comment_text(String), comment_date(String), comment_created_by(String) with a unique identifier(primary key) automatically assigned by the mongodb, "_id"(Object Id)
- When a user adds a comment, it stores the memory_id(from the memories table) in the collection and the comment_created_by field, storing the username(from the User table) who added the comment to create a link between the two collections

![comments](/football_memories/static/images/database_design/comments.PNG)

#### Ratings
- Ratings are added to a memory by a regular or admin user
- The fields stored in the collection are the ratibg value(Int32), the rating_created_by(String) with a unique identifier(primary key)  automatically assigned by the mongodb, "_id"(Object Id)
- When a user adds a rating, the rating_created_by field populated with the users username(from the User table) to create a link between the two collections

![memories](/football_memories/static/images/database_design/ratings.PNG)

### Website pages
I have structured the website into 19 pages, each with clear, concise structure, information and purpose. I use the Bootstrap grid system throughout, which gave a consistent structure and responsive design "out of the box"
1. Home/Landing Page: This is the landing page, and the first page the user encounters when they access the site, before they login/register
2. Register: This page allows the user to register an account to use the site
3. Login: This page allows the user to login to the site
4. Terms and Conditions: This page displays the sites terms and conditions
5. Privacy Policy: This page displays the sites privacy policy
6. Memories: This is the first page the user sees when the login/register, it displays all the football memories that have been added
7. Add Memory: This page allows the user to add a football memory
8. Edit Memory: This page allows a user to edit a memory they have created
9. Delete Memory: This button allows a user to delete a memory they have created
10. Profile: This page displays user information and allows the user to update their profile
11. Dashboard: This page displays statistics about the number of users, tournaments memories, comments
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
- User Story 1.1: As an regular user the navigation bar is displayed with a logo on all pages for easy navigation, with a burger menu on mobile devices
- User Story 1.2: As an regular user the navigation item selected is highlighted
User Story 1.3: As an regular user, when logged out, the home/landing page is the default page and there are three options with a logo, Home, Login, Register displayed
- User Story 1.4: As an regular user, when logged out, the memories page is the default page and there are six options with a logo: Memories, Add Memory, Tournaments, Profile, Dashboard, Logout
- User Story 1.5: As an regular user, when I am logged into the site, and I click Logout I am succesfully logged out of the site, and brought to the home/landing page, and the navigation bar is updated with three options with a logo, Home, Login, Register
- User Story 1.6: As an regular user, when I am logged into the site and I click the back button I am automatically redirected to the home/landing page, and the navigation bar is updated with three options with a logo, Home, Login, Register

### User Stories Website Owner
The user stories for the website owner(admin user) are described as follows: 
There is a lot of overlap between the two user types, the admin user however has more administrative rights throughout
- User Story 1.1: As an admin user the navigation bar is displayed with a logo on all pages for easy navigation, with a burger menu on mobile devices
- User Story 1.2: As an admin user the navigation item selected is highlighted
User Story 1.3: As an admin user, when logged out, the home/landing page is the default page and there are three options with a logo, Home, Login, Register displayed
- User Story 1.4: As an admin user, when logged out, the memories page is the default page and there are six options with a logo: Memories, Add Memory, Tournaments, Profile, Dashboard, Logout
- User Story 1.5: As an admin user, when I am logged into the site, and I click Logout I am succesfully logged out of the site, and brought to the home/landing page, and the navigation bar is updated with three options with a logo, Home, Login, Register
- User Story 1.6: As an admin user, when I am logged into the site and I click the back button I am automatically redirected to the home/landing page, and the navigation bar is updated with three options with a logo, Home, Login, Register

## Skeleton
### Wireframes

#### Desktop 


#### Tablet


#### Mobile


## Surface
### Color Palette
I have gone for a simple and minimal design for the website, with predominatly green font colours over a large hero image on all pages
There are five colours in the color palette
- #264653 - Dark green colour for some of the button and text colours
- #006400 - Light green colour for some of the button and text colours
- #000000 - Black color for some of the text
- #F8F9FA - Light grey colour for the header and footer and panel backgrounds
- #DC3545 - Red colour for some of the buttons, cancel and delete buttons

I feel the colours complement each other very well, and I choose those colours after testing a number of palettes while making sure the colour palette met accessibility standards.
![Palette](/football_memories/static/images/readme/color_palette.PNG)

### Typography
The Poppins font is the main font used throughout the whole website with Sans Serif as the fallback font in case for any reason the Poppins font cannot be imported into the website correctly. This font is from the Google fonts library.
![Font](/football_memories/static/images/readme/font.PNG)

# Features
The website has five webpages consisting of seven distinct features and they are described below
## Existing Features
### Feature 1 Navigation Bar/Logout
#### Description
This is the navigation bar of the website, and is displayed on all pages. The navigation bar is a bootstrap component, and is a responsive component. It becomes a burger menu on tablet and mobile devices.

When the user is not logged in, there are three options with a logo, Home, Login, Register
When the user is logged in, there are six options with a logo: Memories, Add Memory, Tournaments, Profile, Dashboard, Logout

Clicking on the Logout button logs the user out of the site, and their session is ended. If they click back they are automatically re-sent back to the home/landing page
The following code is a check on every route on the website

<code>
    if 'user' not in session:
        return redirect(url_for("administration.home"))
</code><br>

<br>

#### Nav Bar Logged Out
![Nav Bar 1](/football_memories/static/images/nav_bar/nav_bar_logged_out.PNG)
#### Nav Bar Logged Out Mobile
![Nav Bar 2](/football_memories/static/images/nav_bar/nav_bar_logged_out_mobile.PNG)
#### Navr Bar Logged In
![Nav Bar 3](/football_memories/static/images/nav_bar/nav_bar_logged_in.PNG)
#### Navr Bar Logged In Mobile
![Nav Bar 4](/football_memories/static/images/nav_bar/nav_bar_logged_in_mobile.PNG)



#### User Stories
- User Story 1.1: As an admin/regular user the navigation bar is displayed with a logo on all pages for easy navigation, with a burger menu on mobile devices
- User Story 1.2: As an admin/regular user the navigation item selected is highlighted
User Story 1.3: As an admin/regular user, when logged out, the home/landing page is the default page and there are three options with a logo, Home, Login, Register displayed
- User Story 1.4: As an admin/regular user, when logged out, the memories page is the default page and there are six options with a logo: Memories, Add Memory, Tournaments, Profile, Dashboard, Logout
- User Story 1.5: As an admin/regular user, when I am logged into the site, and I click Logout I am succesfully logged out of the site, and brought to the home/landing page, and the navigation bar is updated with three options with a logo, Home, Login, Register
- User Story 1.6: As an admin/regular user, when I am logged into the site and I click the back button I am automatically redirected to the home/landing page, and the navigation bar is updated with three options with a logo, Home, Login, Register

### Feature 2 Footer
#### Description
The footer of the website is displayed on all pages. It consists of three main sections

1. Logo with text and social media links
2. Terms and Conditions and Privacy Policy links
3. Newsletter signup

#### Footer desktop
![Footer desktop](/football_memories/static/images/footer/footer_desktop.PNG)

#### Footer Mobile
![Footer Mobile](/football_memories/static/images/footer/footer_mobile.PNG)

#### User Stories
- User Story 2.1: As an admin/regular user I can view the footers social icons(twitter, facebook, instagram, pinterest, snapchat) and the relevant website opens in a new tab when clicked
- User Story 2.2: As an admin/regular user I can view the websites terms and condition page by clicking on the link in the footer
- User Story 2.3: As an admin/regular user I can view the websites privacy policy page by clicking on the link in the footer
- User Story 2.4: As an admin/regular user I can signup to the football memories newsletter by entering my email and clicking SignUp. The email address entered will recieve an email


### Feature 3 Landing/Home page
#### Description
The landing/home page is displayed when the user first accessing the site, and when they logout. It displays a hero image with Login/Register buttons

##### Hero image
![Landing Page](/football_memories/static/images/landing_page/hero_image.PNG)

Below the hero image are the last three memories added by users. The following code is used to query the mongodb in the administation route python file
<code>
three_latest_memories = list(mongo.db.memories.find().
                                 sort("_id", -1).limit(3))
</code><br>

#### User Stories

### Feature 3 Login/Register/Logout administration
#### Description
The user can login into their account by clicking on the Login button on the landing page or clicking the Login link in the navigation bar. They must enter a valid username and password otherwise a relevant message will be displayed.
#### User Stories
2.1 As a regular user/admin user I can login to my account by providing my username and password. A username and password must be provided. If the username and/or password entered is incorrectly a relevant message will be displayed


### Feature 4 Memories, Memory, Add/Edit/Delete Memory
#### Description
#### User Stories



### Feature 5 Tournaments
#### Description
A regular user can view the tournaments they can add memories to. Three tournaments are displays per page(tournament name, tournament image), and pagination is displayed if there are more than three tournaments in the mongodb database
#### User Stories
2.1 As a regular user/admin user I can view a list of tournaments created with the tournament name and tournament image displayed
2.1 As a regular user/admin user the list of tournaments is displayed with three per page, and pagination if displayed if there are more than 3 tournaments
2.2 As an admin user I can add a new tournament with a tournament name and tournament image. Both fields are mandatory and a message is displayed accordingly. The tournament information is added in the mongo database and the tournament image is stored in an AWS S3 bucket 
2.2 As an admin user I can edit an existing tournament with a tournament name and tournament image. Both fields are mandatory and a message is displayed accordingly. The tournament information is updated in the mongo database and the tournament image is stored in an AWS S3 bucket
2.4 As an admin user I can delete an existing tournament, once I have confirmed that it is ok to delete the tournament. The tournament information is deleted from the mongo database
2.5 As an admin user if a tournament has memories associated with it, the tournament cannot be deleted and a message is displayed



### Feature 6 Dashboard
#### Description
The dashboard page displays the results of 5 queries against the mongo db for the number of users, number of tournaments, number of memories, number of ratings and number of comments added on the site
<code>
    number_of_users = mongo.db.users.count() <br>
    number_of_tournaments = mongo.db.tournaments.count() <br>
    number_of_memories = mongo.db.memories.count() <br>
    number_of_comments = mongo.db.comments.count() <br>
    number_of_ratings = mongo.db.ratings.count() <br>
</code>    

#### User Stories
- User Story 6.1: As a regular user/admin user I can view a dashboard to see the number of users, number of tournaments, number of memories, number of ratings and number of comments added on the site


### Feature 7 Profile
#### Description
A user can view or edit their profile details. Their username is displayed, but it is an un-editable field. When the user clicks save changes they are brougth back to the Profile page with the relevant updates made

#### Profile/Edit Profile
![Profile/Edit Profile](/football_memories/static/images/profile/profile.PNG)

#### User Stories
- User Story 7.1: As a regular user/admin user I can view my profile details: Username, First Name, Last Name, Favourite Team and Country. The country is selected from a dropdown of countries
- User Story 7.2: As a regular user/admin user I can update my profile password, but the confirm password entered must match with the password. The password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.
- User Story 7.3: As a regular user/admin user I can update my profile details: First Name, Last Name, Favourite Team and Country
- User Story 7.4: As a regular user/admin user the following fields are mandatory: Username, First Name, Last Name, Favourite Team and Country
- User Story 7.5: As a regular user I can delete my account. This will delete any memories I have added(including their associated comments and ratings) and will also delete any comments or ratings the regular user has added on others users memories. The user will be asked to confirm the delete account action, and will be brought to the homepage after their account is succesfully deleted.


##  Features Left to Implement
- I am content with what was implemented. The site is a feature rich site using a number of linked namespaces in a mongodb collection.
- However here are some additional "nice to have" features that could be added to the site

Number | Feature  
 ------------ | ------- |
1 | Social sharing of a memory on facebook, twitter  |
2 | The image type(jpg, png) is read and the memory displays a different image based on it
3 | Tags functionality and search by tags
4 | Enhance reporting/dashboard capabilities, and use a 3pp graph library
5 | User must verify their email address when registering, or 2 factor authentication is implemented
6 | Delete image from aws, when tournament, memory deleted

# Technologies Used
## Languages 
- HTML (https://en.wikipedia.org/wiki/HTML)
    - The project uses html to build the relevant pages
- CSS (https://en.wikipedia.org/wiki/CSS)
    - The project uses CSS to style the relevant pages
- Javascript (https://www.javascript.com/)
    - Javascript was used for all scripting on the site
- Python (https://www.python.org/)
    - Python was used for server side coding on the project, a number of libraries were also used: Boto3(AWS interface), Pytest(unit testing)
- Jinja (https://jinja.palletsprojects.com/en/3.0.x/)
    - Jinja is a templating engine for Python that is used throughout the project

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
- Lucidchat (http://lucidchart.com)    
    - Lucidchart was used to create the database design diagrams
- JQuery (https://jquery.com)
    - JQuery was used in some of the javascript files for DOM manipulation
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
    - The google maps geocode api is used to translate the event name returned from the memory stadium name value and translate to a google maps location on the memory page
- Gofullpage chrome plugin  (https://chrome.google.com/webstore/detail/gofullpage-full-page-scre)
    - This plugin was used to take full page screenshots for testing images
- Python online interpreter (https://www.programiz.com/python-programming/online-compiler/)
    - For testing python code snippets

# Testing
The testing information and results for this project are documented in [TESTING.md](TESTING.md)


# Deployment
The project uses a number of API's, below are the steps to configure the API in your environment

## Google Maps API
1. Create an account at https://console.developers.google.com
2. Create an API key and setup the account as requested by google, for example billing information
3. Configure 2 API's, Maps JavaScript API and Geocoding API
3. In the credentials screen, set the web restrictions url referrer to the urls of where the site will be hosted as well as your local development environment
4. In the API restrictions section in the credentials screen, limit to 2 API's: Maps JavaScript API and Geocoding API
5. In the memory.html file under the footer, update the google maps script src to include your API key

## Email JS
1. Create an account at emailjs.com 
2. In the integration screen in the emailjs dashboard, note your userid
3. Create an email service in the Email Services section and note the id
4. Create an email template in the Email templates section and note the id
5. Update the script sendEmail.js, method sendMail with your user id, email service id and email template id


# Credits
- For the memories page, I used some of the html code from https://bootstrapious.com/p/bootstrap-photo-gallery

- For the password validation, I built on examples code described here: 
    - https://www.w3schools.com/howto/howto_js_password_validation.asp
    - https://bootsnipp.com/snippets/67OaM
    - https://learncodeweb.com/bootstrap-framework/registration-form-with-validation-in-bootstrap-4/
    - https://getbootstrap.com/docs/5.0/forms/validation/

- For pagination on the memories, tournament I found the following links useful to implement pagination:  
    - https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
    - https://pythonhosted.org/Flask-paginate/

- For the footer to stick to the bottom of the I used code from the following pages:
    -https://stackoverflow.com/questions/4575826/how-to-push-a-footer-to-the-bottom-of-page-when-content-is-short-or-missing#:~:text=Just%20wrap%20your%20.,will%20move%20to%20the%20bottom.


- My project is built using a Blueprints structure, I found the following video and links invaluable to structure my project accordingly
    - https://www.youtube.com/watch?v=Wfx4YBzg16s&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=11 
    - https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog 

- For password validation I re-used some of the code here
https://stackoverflow.com/questions/9142527/can-you-require-two-form-fields-to-match-with-html5

- For storing images in an AWS S3 bucket, I found the following links very useful
    - https://www.youtube.com/watch?v=s1Tu0yKmDKU
    - https://stackoverflow.com/questions/44228422/s3-bucket-action-doesnt-apply-to-any-resources
    - https://www.youtube.com/watch?v=7gqvV4tUxmY 

- I found the following resource great for some jquery code used: https://api.jquery.com/replacewith/

- I used html/css code, then tweaked it accodingly for the site footer: https://jsfiddle.net/bootstrapious/c7ash30w/ */

# Content
- Country list (https://www.technicalkeeda.com/html-tutorials/all-countries-drop-down-list-in-html)
    - The country list on the registration page

- Font Awesome (http://fontawesome.com)    
    - The icons used on the site from font awesome

- Fonts (https://fonts.google.com/)    
    - The text font(Poppins) is from google fonts

- Google Maps (https://www.google.com/maps)
    - The google maps api is used to display maps in the memory page

<br>

# Media
- Pexels (https://www.pexels.com/)
    - The hero image used throughout the site is form Pexels, https://www.pexels.com/photo/aerial-view-of-soccer-field-1171084/ by user https://www.pexels.com/@mike-468229 

- The 42(www.the42.ie), Irish Independant(www.irishindependant.ie), Tokyvideo(www.tokyvideo.com)
    - The memory images added to the memories added to the website were taken from the above websites media galleries

 <br>

# Acknowledgements
- I would like to thank my fiancee Mary for her help, constant support and ideas for the website, my son Liam, and also to my dog Lily for her company during development of the website.
- I would like to thank my mentor Mo Shami for his input, help and feedback.