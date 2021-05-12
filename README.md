# [Little Cabin App](https://littlecabin.herokuapp.com)

![Securely share your family's get-away and memories](little-cabin-meta.png)

Secure, family-only web application providing:

- **shared group calendar** with permissions-based week swapping and selling
- **social network** offering "postcards" (short note with a photo)
- **collaborative todo list** collecting requests from members on maintenance items, purchase ideas, or other helpful suggestions. Members can "agree" and upvote requests
- **knowledge center** with important information including legal trust information, weekly chores, dues schedule, contact info for local businesses and emergency protocols

## Project Planning

My initial planning started by writing out my user stories, and conceptually working through all of the actions I personally had wished I could do in an app to help manage our family's camp.

_As A User (Not Logged In) I Want To:_

- View information about the app itself, and understand why I would want to make an account for an existing managed property, or use the app for my own property

_As An Authorized User I Want To:_

**Account**

- Register a new account, and be automatically pre-approved based on an admin "whitelist"
- Log in to my existing account, using the email address I registered with
- Log out of an account

**Postcards**

- View existing postcards, with the most recent at the top
- Create a new postcard (greeting and message)
- Upload a photo to my postcard
- Delete one of my existing postcards
- Edit one of my existing postcards

**Calendar**

- See existing property schedule

**Requests**

- Add a request
- Mark a request as completed
- Hide completed tasks

**Info**

- View emergency, legal, and other information about the property
- View nearby business info

**UI/UX**

- Report a bug to the property admin
- View app on a variety of devices responsively

**Stretch Goals**

- Log in using Facebook, Google, etc

- View app in a variety of themes (dark, light, forest, beach, mountain, etc)
- Signup for notifications (text, email) when actions occur such as a request for one of my weeks is made, or a family member reacts to one of my postcards

- Sort the businesses by family recommendations, dynamically load via API
- Recommend a business on the list
- View my family tree
- Upload a photo for my leave of the tree

- "Agree" with an existing request to prioritize it

- Offer one of my weeks up for sale
- Offer to swap one of my weeks for another family's week
- Request to purchase another family's week

- Add an emoji reaction to someone's post

### Structure

After the stories were in place, I categorized those stories, leaving me with the general navigation structure of the entire site and its pages. The Home page (not logged in) would display info mainly about Little Cabin, the app. All other pages would be private and only available if logged in; those would display and manipulate information about the property itself.

### Open Access Pages (Not Logged In / Unauthorized Users)

- Home
  - About (Public info about Little Cabin App)
- Login
- Register

### Authorized Access Pages

- Postcards
- Calendar
- Requests
- App Info
  - Emergency Info
  - Weekly Chores
  - Local Business Recommendations
  - Property History
  - Family Tree
  - Legal Trust Info

### Wireframes

On [Chuck](https://github.com/chuckchoiboi)'s recommendation, I used [Mockflow](https://mockflow.com/) to quickly and easily sketch some initial wireframes for these main page views.

![Wireframe Mockup Images](wireframes.png)

### Pitch Deck

I then used Google Slides to create a [pitch deck](https://docs.google.com/presentation/d/1wABAwaZubhI4hExwqxWG6zBW7y5OyL_w92NW8NEWQnM/edit#slide=id.gd480e80180_0_52) to present to my stakeholders, and receive their feedback on project scope, tech and design pattern suggestions, and field initial questions and concerns.

## Building

I intentionally started this project from the _user_ perspective; getting an attractive frontend built as quickly as possible (using Bootstrap) to help make the project "real" and inspire ideas for features at an early stage. In previous large projects I had started by building backend instead (API, and databases models), however using a new framework (Django) and new database (PostgreSQL) for this project meant it would be easiest to have the schema conceptually as complete as possible before starting to actually write to the database.

### ERD

To assist in developing the data models, I sketched an ERD (entity relationship diagram) to help visualize the way the various objects would interact. This working sketch also made it simple to conceptualize new features, and adapt the models' properties before committing them to database tables.

![Entity Relationship Diagram ERD](erd.svg)

### Style Guide

Since I was creating this project on my own, the function of my style guide was more to help me keep track of design and copy ideas that I liked, rather than to strictly guide team members on a unified style. The choices certainly evolved and shifted as the app expanded, but updating the guide as the "source of truth" was essential to the workflow, even when working alone. It saves time to be able to copy/paste HEX color codes, font styles, terminology and slogans, etc, and reduces executive function required to make all of those tiny decisions over and over.

### Colors:

![Screenshot of HEX codes from color scheme](little-cabin-colors.png)

### Terminology

- **Property**: the family location and structure being managed. Might refer to a "camp", "cabin", "lake house", "vacation home", "cottage", or other regional terms
- **Request**: a ToDo-style item including maintenance requests, etc
- **Week**: the unit of time a particular user or users has exclusive access to the property
- **Postcard**: a social media post including a written note and an optional photograph

### Copy

- **Title**: Little Cabin App
- **Subtitle**: Securely share your family get-away
- **Tagline**: Make Memories, Not Spreadsheets
- **Summary**: Little Cabin is a...
  - shared group calendar with permissions-based week swapping and selling
  - micro social media network offering "postcards" (short note with a photo)
  - collaborative "to-do" style list collecting requests from members on maintenance items, purchase ideas, or other helpful suggestions. Members can "agree" and upvote requests
  - knowledge center with important information including legal trust information, weekly chores, dues schedule, contact info for local businesses and emergency protocols

## Tech Used

- Python
- Django
- HTML / CSS / Bootstrap
- PostgreSQL
- Amazon AWS
- Google Calendar API
- Heroku

### Django

I followed [my own blog post](https://blog.benhammond.tech/django-getting-started) to get a "Hello World" Django application running locally, and then again followed my post [part 2 to deploy to Heroku](https://blog.benhammond.tech/deploying-django-to-heroku). I wanted the simplest possible app deployed early, so that eventual troubleshooting would be easier to pinpoint.

## Accessibility

Following the ethos of "accessibility is not a feature", I am making an effort to improve my projects by making and keeping them accessible from the very start. I have _much_ to learn in this space, but to start I frequently run the Lighthouse report tool in Chrome Dev Tools. This is not a complete testing, but it helps with the lowest hanging fruit:

- including a brief, descriptive `alt` attribute to add alternate text to your `<img>` tags. For _decorative_ images (those which are simply aesthetic or redundant based on adjacent text) it is recommended to set `alt=""` so that screen readers will know to skip it
- setting an `aria-label` attribute on any links or buttons that don't include descriptive text. In my case, the template's hamburger menu was an svg file, so it made sense to also label that image as `aria-hidden="true"` to let the screen reader know it didn't need to interpret that graphic
- organizing your headings hierarchy (`<h1>`-`<h6>`); in general there should only by one `<h1>`, and all subheadings should be in order (e.g. don't skip `<h3>` by going directly from an `<h2>` to an `<h4>`)
- ensuring the color contrast every bit of text and its background is high enough to be read

## Problems Solved (work in progress)

- Building the project from the user's perspective, i.e. getting a working frontend displayed as quickly as possible. integrating an existing design into an extensible Django base template
- fixing deployment issues with DEBUG config vars
- integrating css variables (custom properties) with existing design to make future changes as simple as possible
- extending Django's `UserCreationForm`; requiring `first_name`, `last_name`, and `email`, and removing the field for `username`; actually presented `username` as **Email** to user for all account related services (Register, Login, etc), since all the solutions recommended creating a custom user model _before starting the project_..... too late.
- custom pagination (view one year at a time). sending value out from form btn into the views. saving fetched data in big chunk into db, and reading from there unless data is stale then refetching
- [Extending UserCreationForm](https://dev.to/yahaya_hk/usercreation-form-with-multiple-fields-in-django-ek9)
- https://developers.google.com/calendar/quickstart/python
- https://github.com/googleworkspace/python-samples/issues/134
- https://stackoverflow.com/questions/63956706/google-drive-api-quickstart-py-error-400-redirect-uri-mismatch
- need to add credentials file, and need to gitignore it
- need to run Google's Python "quickstart" commands INSIDE the env
- https://github.com/googleworkspace/python-samples/issues/134
- https://stackoverflow.com/questions/63956706/google-drive-api-quickstart-py-error-400-redirect-uri-mismatch
- use template filters to calculate previous and subsequent years for buttons and post request values. conditionally rendering "previous year" button to deny viewing past years.
- different colors of icon/favicon/logo
- Manually pivoting a table lookup; each Postcard contained an owner username, but I needed to get `first_name` and `last_name`; in the `view` method I looped through the postcards, and then built a context dictionary which contained a list of Postcards bundled with their User authors. This was I was able to easily access the Postcard info in the template using `{{ card.author.first_name }}`
- naming collisions: bug with view method named "postcards" and list of objects from the database "postcards". Also, named my to-do items "Request" objects, which is confusing with the built in request keyword from Django's HTTP request/response framework
- adding checkbox _inside_ the to-do item; required using `<button>` instead of `<input />` to place the svg graphic inside each generated form.
- todo list: conditional rendering of "hide completed" button; calculating completion rates in the view method and then sending through to display as progress bars.
- deploying to Heroku with Google Cloud Platform which requires a `credentials.json`, had to move the json file to the floor, change the name, install a special buildpack, and add two new config vars. still wasn't able to get the credentialing screen to display to the user (instead it was logging the link in the Heroku logs).
- learned that Heroku config vars are ALWAYS strings, meaning when I had set `DEBUG` to `False` for production, it was actually reading the string `"False"` which it was evaluating as `True`. I was able to fix this by simply setting a different config var for development and production and then assign `DEBUG` as needed. This was resulting in a 500 Error; which took significant debugging to fix. First, followed [this stack overflow](https://stackoverflow.com/questions/52311724/500-error-when-debug-false-with-heroku-and-django) and set up detailed logging to discover the real issue that was causing the 500 error. It turns out it was a `ValueError: Missing staticfiles manifest entry for` one of my images. To remedy this error, I went into my terminal with the virtual environment activated, and ran `python3 manage.py collectstatic`. Still not entirely sure what this did, other than make copies of almost all of the images I had used in the project which increased my deploy and push times. But it basically hooked everything up image-wise for Django, and fixed the 500 error.
- Conditionally render the "edit" and "delete" buttons as accessible icons; even though the two variables were displaying the same, the current username was returning `False` when compared against the postcard owner. I was able to fix this by using a Django template tag to convert them to the same type of string `{% if card.postcard.owner|stringformat:"s" == user.username|stringformat:"s" %}`
- Needed to extend the builtin DeleteView class, and also to my detail function (for create and update) to lookup the Photo(s) that contained the currently detailed Postcard. This allowed all of these views to display the postcard along with its photos, even though the relationship is 1 POSTCARD->MANY PHOTOS, and therefor it's the Photo class that contains a Postcard foreign key. Had to overwrite the `get_context_data()` method to do the lookup, and then bundle those Photos into the returned `context`.
- Decided not to limit CRUD on the shared to do requests; this way anyone is able to edit an existing request (and fix a spelling error, or add details), complete a request, and then hide all complete requests. This only works since the view is for screened, authorized users. I decided to skip the pencil icon and instead make clicking the text of the request item the "edit" function, and then the complete/incomplete would be handled by the checkbox. I have some concerns that the way I've designed it might be less accessible than if I had relied on the browsers built-in check box.
- Make the postcards feel more "real world" by adding a tiny bit of random tilt to their display, and having them straighten and expand when hovering with mouse.
- Limit access to the app to users who have been approved; to do this I used the Group property of Django's built in User model. This creates a many-to-many relationship, and allows filter() and get() requests to the database to delegate functionality based on the group. I created a "member" group who's users have full create/read/update/destroy (CRUD) access to postcards, requests and weeks, and an "admin" group who's users will see and approve new member requests. Specifically, the admin `home` view queries the database for all users expect those who are already in the "member" group: `User.objects.all().exclude(groups__name='member')`, and then displays that list with associated "approve" buttons:
  ```django
  {% for pending_user in pending_users %}
    <li>
      <span>{{pending_user.first_name|title}} {{pending_user.last_name|title}} ({{pending_user.username}})</span>
      <a href="{% url 'approve_user' pending_user.id %}">Approve</a>
    </li>
  {% endfor %}
  ```
- implementing Swap objects (pending offers to swap Week objects between Groups, initiated and approved by Users). LOTS OF STUFF. this was hard
- error after adding "created"; used default value of `1` which didn't make sense, and wasn't able to run `migrate` even after dropping and recreating the db. Had to manually go into the migrations folder and alter the value of `default=1` to `default=django.utils.timezone.now`.
- setting up automatic population of db
- ordering my groups, decided to append a number so they were sortable
- avoiding name collisions; used `import calendar as calendar_lib` since I was already using `calendar` as a view method
- displaying a dropdown `<select>` with every pending user displayed to an admin; admin can then choose the correct owner_group and approve, or deny the user and delete the uncredentialed user. This was also complex; mainly in deciding between using Django's built-in form handling, and digging through obscure and tangential examples. I decided to implement it myself, changing my approve button from being an `<a>` to being a `<button>` inside of a `<form`>, and then adding a hidden `<input>` to contain the `user.id` . I also placed the `<select>` inside the same form, and then made `home/` intercept post requests and process the incoming data by finding the User, finding the Group, then adding the user to that group.
- I would love to have the "Approve" buttons stay disabled until the admin selects a Group; I tried using `required` in the `<select>` but that didn't work; I also researched using Javascript inside the view but it got complex due to the possibility of multiple, programmatically generated dropdowns and associated approve buttons.
- calculating an end date required adding a dateTime delta of 7 days, and then rendering that dateTime as a string to be sent to Google API
- Syncing will be possible, since we can know that every actual week will have a maximum of 1 Week object in our database, and also a maximum of 1 google calendar event. So rather than simply wiping gcal and pushing every week from the db when there is a change, it's possible to do incremental synchronization

? https://stackoverflow.com/questions/37754999/google-calendar-integration-with-django

## Tools and Libraries

- [Font Awesome](https://fontawesome.com/) - Icons
- [Metatags.io](https://metatags.io/) - Meta Tags
- [Mockflow](https://mockflow.com/) - Wireframes
- [Figma](https://www.figma.com/) - Graphics
- [Favicon.io](https://favicon.io/) - Favicon

## Resources

- [PngItem](https://www.pngitem.com/) - Icon
- Unsplash: [Cabin Photo](https://unsplash.com/@olivier_twwli?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText), [Firewood Photo](https://unsplash.com/@markuswinkler?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText), [Watering Can Photo](https://unsplash.com/photos/uWfYjWM8oGM?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink)
- [Koka](https://angrystudio.com/themes/koka-free-bootstrap-5-website-template/) - Bootstrap Template
- [Route Back To Section IDs](https://engineertodeveloper.com/a-better-way-to-route-back-to-a-section-ids-in-django/) - Blog Post
- [Extending UserCreationForm](https://dev.to/yahaya_hk/usercreation-form-with-multiple-fields-in-django-ek9) - Blog Post
- [Quickstart Google Calendar API - Python](https://developers.google.com/calendar/quickstart/python) - Guide
- [Accessibility for Hamburger Menu](https://medium.com/@linlinghao/accessibility-for-hamburger-menu-a37fa9617a89) - Blog Post
- [Adding Google Cloud Credentials To Heroku](https://devdojo.com/bryanborge/adding-google-cloud-credentials-to-heroku) - Blog Post
- Stack Overflow: [500 Error When Debug False With Heroku And Django](https://stackoverflow.com/questions/52311724/500-error-when-debug-false-with-heroku-and-django), [Getting last Monday of a month](https://stackoverflow.com/questions/12796389/python-get-last-monday-of-july-2010/12796542), [Using Service Account with Google API](https://stackoverflow.com/questions/49480930/django-server-rw-access-to-self-owned-google-calendar)
- [Intro to Google Developer Service Account](https://www.daimto.com/google-developer-console-service-account/) - Blog Post
