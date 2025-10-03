# Assignment_Project_Tyrese_tyresec2

Django application for my digital card management system. It enables customers to alter how their digital cards work from the comfort of their home. 

##ER Diagram:
![ER Diagram](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/notes/erDiagram.png)

## Testing:

To test this application, you'll need to install stripe

`(env)$ pip install stripe==5.5.0`

It enables this application to verify if payment is confirmed, and it relies on Stripe webhook to do so. Stripe listens for `checkout.session.completed` event type. When it is found, it'll update the card model by setting the `card.user` to the user id that was placed in checkout session's metadata. 


(I will create a test that bypasses this action)

## A5 Updates

- Added tailwind to Base template
- Began customizing forms
- Used get_context data in LoginView
- Switched from dashboard fbv to cbv 
- Add conditional block to display anchor tag (w/ proper next paremeters) in login.html

