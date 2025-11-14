# Assignment_Project_Tyrese_tyresec2

Django application for my digital card management system. It enables **customers** to alter how their digital cards work from the comfort of their home. 

## ER Diagram:

![ER Diagram](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/notes/erDiagram.png)

# Weekly Updates

## A5 Updates

- Added tailwind to Base template
- Began customizing forms
- Used get_context data in LoginView
- Switched from dashboard fbv to cbv 
- Add conditional block to display anchor tag (w/ proper next paremeters) in login.html

## A6 Updates 

- I purged everything that we haven't covered in class: Forms, Login/Logout Views, Stripe, etc
- I created two aggregations (leaderboard, and design usage) and one filtering functionality (for searching cards)

## A7 Updates 

I used Plotly JS to visualize two of my aggregations from A6. JS fetches the JSON data powering PlotlyJS from the `config_plotly` function-based view's JsonResponse . (See `config_plotly` JsonResponse below)

I originally thought I'd visualize more than two aggregations, so I created a JS class called `Plot` that wraps around Plotly's `newPlot()` method and its 4 major parameters: target_elem (str), data (array), layout (obj), config (obj). It enables my application to go from this: 

![Plotly JSON seed data](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/assignment_screenshots/config_plotly_json_data.png)

to this:

![Plotly Visuals](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/assignment_screenshots/plotly_visuals.png)

Graph 1 represents daily usage. It's aggregration counts the number of uses (in Usage model) grouped by unique day.
Graph 2 represents a leaderboard which tells which owners used their cards the most. It's aggregation counts the number of uses in (Usage model) grouped by a card's owner (Relation Traversal: card__owner_id)

## A8 Updates 

- I created the `card_update()` fbv, and the `CardUpdate()` cbv.
- They both use the CardForm form class that I created, but the cbv uses less code. The fbv gave me more control over my application since I handle the request from start to finish. The cbv has alot going on underneath that makes it so that i can use less code, but that's not my code per se (and that comes with disadvantages). 
- CardForm works with POST requests and the csrf token to prevent cross site requests. I didn't care in my GET function, but this form is used to update data in my database (DANGER!)
- Set `CardForm` exlude to prevent updating non-permitted fields. 
- Used `CardForm.clean()` method to validate Card fields that depend on each other (e.g, "reroute_url", "show_profile")

## A9 Updates

- I created the `daily_usage` fbv, and  `daily_usage_png` fbv to return the JSON data of card usages grouped by date,  and generate a matplotlib based chart (from the data) respectively. For ease of use, I built `daily_usage` to contain labels (the x values) and value (the y values). 

## A10 External APis

- I used this [QR Code API](https://goqr.me/api/) to create the QR codes that will be adhered to the back of my digital cards. Sending a GET request with the `format` parameter `=svg`, and the `data` parameter to a generated URL (the same as the `card_detail_view` urlpattern) returns the raw svg code for a unique qr code. I made Javascript responsible for handling this raw svg code by building a blob object, a temporary URL for that blob object, and an anchor tag with download capabilities. 

- In the event that the Api response's status code is not 200, my application hides the anchor tag and it's JS dependencies 

## A11 CSV/JSON Exports (Part 1)

I wanted to track the number of cards that are tapped within my application. To do so, I've created a CSV & JSON export view to summarize data selected from **Usage**. 

### New URLS

- **/reports/**: Page with charts and tables 
- **/export/usage.csv**: Downloads a csv file of total card taps by day
- **/export/usage.json**: Downloads a JSON file of total card taps by day


## A11 Authentication & Access Control (Part 2)

My signup process consists of a function based view (`cardManager.views.signup_view`) that renders the `cardManager.forms.OwnerSignUpForm` form to my registration template. If the request method is POST, I save a new non-staff user (by ignoring the `is__x` fields), log the user in, and redirect the browser to the dashboard. If the request method is GET, I send a blank form. The `cardManager.forms.OwnerSignUpForm` includes 6 fields: First & Last names, email, username, password & confirm password. 

### Protected Routes 

- Dashboard: this view requires specific user data so protecting this ensures that the user data is provided.
- Profile Create: Only users should be able to do this
- Card Update: Only a user can update a card. 
- Reports: Protected to hide important summaries/aggregrations 
- Order Detail: Everyone shouldn't know the details of a report. Certain privileges were needed 
- Exports(CSV & JSON): Protected to hide important summaries/aggregrations 

### Public Routes 

- Card Activate: This is where customers claim their cards. I'm required a login right after they 
- Signup
- Card Scan: I didn't want the people tapping the cards to have to sign in if they aren't users
- Profile Detail: profiles are visible to the public 
- daily_usage: I got a JSON Decode error because of how the `daily_usage_png` fbv relies on it. Protecting this view hands an HTTPResponse carrying the login page's HTML,instead of the expected JSONResponse, when an unauthorized user visits.


### Credentials for grading

username: **mohitg2** 
password: **graingerlibrary** 


