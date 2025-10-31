# Assignment_Project_Tyrese_tyresec2

Django application for my digital card management system. It enables **customers** to alter how their digital cards work from the comfort of their home. 

##ER Diagram:

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