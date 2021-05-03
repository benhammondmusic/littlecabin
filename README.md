# Little Cabin

> Securely share your family's get-away and memories.

Secure, family-only web application providing:

- shared group calendar with permissions-based week swapping and selling
- micro-social media network offering "postcards" which a short message with a personal photo or suggested image
- requests list collecting suggestions from members on maintenance items, purchase ideas, or other helpful suggestions. Other members can upvote the requests by giving an "agree"
- static pages with important information including legal trust information, weekly chores, dues schedule, contact info for local businesses and emergency situations

## Pages

> Home page (not logged in) will display info mainly about Little Cabin the app. All other pages are only available if logged in, and will display information about the actual family and property

### Account

- Home (open)
- Login (open)
- Signup (open)
- App Info (open)
  - Emergency Info
  - Weekly Chores
  - Local Business Recommendations
  - Property History
  - Family Tree
  - Legal Trust Info

### Options

- Calendar
- Postcards
- Requests
- Camp Info / Family History

### Report A Bug

- Email Admin

# Style Guide

### Colors

### Design

### Terminology

# Problems Solved

- integrating an existing design into an extensible Django base template
- fixing deployment issues with DEBUG config vars
- integrating css variables (custom properties) with existing design to make future changes as simple as possible
- extending Django's `UserCreationForm`; requiring `first_name`, `last_name`, and `email`, and removing the field for `username`; actually presented `username` as **Email** to user for all account related services (Register, Login, etc), since all the solutions recommended creating a custom user model _before starting the project_..... too late.
- custom pagination (view one year at a time). sending value out from form btn into the views. saving fetched data in big chunk into db, and reading from there unless data is stale then refetching
- [Extending UserCreationForm](https://dev.to/yahaya_hk/usercreation-form-with-multiple-fields-in-django-ek9)
  https://developers.google.com/calendar/quickstart/python
  https://github.com/googleworkspace/python-samples/issues/134
  https://stackoverflow.com/questions/63956706/google-drive-api-quickstart-py-error-400-redirect-uri-mismatch
  need to add credentials file, and need to gitignore it
  need to run Google's Python "quickstart" commands INSIDE the env
  - use template filters to calculate previous and subsequent years for buttons and post request values. conditionally rendering "previous year" button to deny viewing past years.
  - different colors of icon/favicon/logo
  - Manually pivoting a table lookup; each Postcard contained an owner username, but I needed to get `first_name` and `last_name`; in the `view` method I looped through the postcards, and then built a context dictionary which contained a list of Postcards bundled with their User authors. This was I was able to easily access the Postcard info in the template using `{{ card.author.first_name }}`
  - naming collisions: bug with view method named "postcards" and list of objects from the database "postcards". Also, named my to-do items "Request" objects, which is confusing with the built in request keyword from Django's HTTP request/response framework
  - adding checkbox _inside_ the to-do item; required using `<button>` instead of `<input />` to place the svg graphic inside each generated form.

## ERD (Entity Relationship Diagram)

![ERD of Project Models](erd.svg)

## Tech

Fullstack Python App with Django

## Resources

- [Koka](https://angrystudio.com/themes/koka-free-bootstrap-5-website-template/)
- [Font Awesome Icons](https://fontawesome.com/)
- [Route Back To Section IDs](https://engineertodeveloper.com/a-better-way-to-route-back-to-a-section-ids-in-django/)
- [Extending UserCreationForm](https://dev.to/yahaya_hk/usercreation-form-with-multiple-fields-in-django-ek9)
  https://developers.google.com/calendar/quickstart/python
  https://github.com/googleworkspace/python-samples/issues/134
  https://stackoverflow.com/questions/63956706/google-drive-api-quickstart-py-error-400-redirect-uri-mismatch
  need to add credentials file, and need to gitignore it
  need to run Google's Python "quickstart" commands INSIDE the env
