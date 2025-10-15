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
