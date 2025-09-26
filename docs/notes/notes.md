# Ideas & Selection Rationale

Between the 3 projects, I've decided on the following 2: A client intake system (Final project), and the digital card management system (Assignment). 

I sell digital cards both in-person, and online. There have been numerous occasions where clients would call back asking if they could change certain details about their cards (how it looks, or the URL). I'd like for the customers to have a way of signing in and managing how their card behaves to reduce the amount of touchpoints in my onboarding process. So I chose to spend the semester doing just that with this project

___

# Wireframe Notes

___

# Branching Strategy

Branches: main, dev, hotfix, features

Before this class, I'd only use the main and dev branches in my code. For this project, I know that there will be features that I want to try independent of dev, so I'm using a feature branch to act as a playground. It'll mainly pull from dev. 

From experience, I know that I can forget to take care of smaller tasks. Those smaller changes often get lost inside of the mountain of staged code, so I'll try hotfix to track the smaller changes. 

### Branch usage reflection
My proposed setup is keeping the main branch, and my stash list clean. I've been able to move between branches without having to solve git errors/warnings. 

___

# Django setup

I chose the project name tcDigitalCards because I am planning to merge my web services and digital cards into a company called TC Digital. the camel case makes it easier to remember for when I need to reference the project name down the line. 

The name of this app was a little trickier. To make things simpler, I made my goal more clear: I'm building the application to manage digital cards. After that, i stumbled upon cardManager. 

___

# Virtual Environment Choices
I use `e4_trainor_django_course` from a previous class, for this project.

Typing `conda --version` into my terminal returns :

```conda 24.9.2```


Typing `conda list` into my terminal returns:
	
```
# packages in environment at /home/tyro/anaconda3/envs/e4_trainor_django_course:
#
# Name                    Version                   Build  Channel
_libgcc_mutex             0.1                        main  
_openmp_mutex             5.1                       1_gnu  
asgiref                   3.8.1           py312h06a4308_0  
bzip2                     1.0.8                h5eee18b_6  
ca-certificates           2024.12.31           h06a4308_0  
certifi                   2025.8.3                 pypi_0    pypi
charset-normalizer        3.4.3                    pypi_0    pypi
django                    5.1.3           py312h06a4308_0  
expat                     2.6.4                h6a678d5_0  
idna                      3.10                     pypi_0    pypi
iniconfig                 1.1.1              pyhd3eb1b0_0  
ld_impl_linux-64          2.40                 h12ee557_0  
libffi                    3.4.4                h6a678d5_1  
libgcc-ng                 11.2.0               h1234567_1  
libgomp                   11.2.0               h1234567_1  
libstdcxx-ng              11.2.0               h1234567_1  
libuuid                   1.41.5               h5eee18b_0  
ncurses                   6.4                  h6a678d5_0  
openssl                   3.0.15               h5eee18b_0  
packaging                 24.2            py312h06a4308_0  
pillow                    11.1.0                   pypi_0    pypi
pip                       25.0            py312h06a4308_0  
pluggy                    1.5.0           py312h06a4308_0  
pytest                    8.3.4           py312h06a4308_0  
python                    3.12.9               h5148396_0  
readline                  8.2                  h5eee18b_0  
requests                  2.32.5                   pypi_0    pypi
setuptools                75.8.0          py312h06a4308_0  
sqlite                    3.45.3               h5eee18b_0  
sqlparse                  0.5.2           py312h06a4308_0  
stripe                    5.5.0                    pypi_0    pypi
tk                        8.6.14               h39e8969_0  
tzdata                    2025a                h04d1e81_0  
urllib3                   2.5.0                    pypi_0    pypi
wheel                     0.45.1          py312h06a4308_0  
xz                        5.4.6                h5eee18b_1  
zlib                      1.2.13               h5eee18b_1  

```
___

# Models

![ER Diagram](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/notes/erDiagram.png)

#### Relationships: 
- A User has many Cards
- A User has 0 or 1 Profile
  
I chose my 3 models to make the process of scanning cards and handling Django reroutes easier. There are 4 different possible ways of handling a card. 

1) A browser is opened and it points to the URL in the card model
2) A customer can activate the card if there is no user attached to the card
3) A browser is opened and it points to the attached users profile
4) (Error Case: Opens a 404 not found )

This setup was decided to effortlessly handle this reroute logic, because the attributes that determine this handling logic are found in one Model (Card).



#### Developer updates

*[?]*

- profile_slug shouldnt have more than 25 characters. customers simply give their profile a way to be found with field (Ex "reese" => https://tcdigitalcards.com/profile/reese). These should be unique 
- Card model should certainly have a unique token. Im wondering if the combination of both fields user and alias should be unique as well. I can't name 2 cards the same thing...unless I was a church who ordered 50 cards. theoretically each church member would activate their own cards (including accounts)... so there shouldn't be a case where a user has the same alias. Each member may have the same card name of "X Church Card". I'll leave these rwo fields alone for now. 
- I do want to change the format for the card model to show unclaimed if user is not attached. Cards that are already on display or in my current inventory should be easily retrievable in the database. I'll add some conditions to the __Str__ method of Card
- Whoops. It looks like i shouldve made profile slug's blank = False
- I added a bio to the Profile. This decision was made to help fill the empty space in the profile.html template from the profile detail view.

___

# Views


## card_detail(request, card_token).
This retrieves a singlular `Card` model instance where Card.token = `card_token`. 

It also redirects the browser according. There are 4 possible redirects that may occur:
- Redirect the browser to this card's `reroute_url`
- Redirect the browser to the activate card url (`activate/<str:card_token>`)
- Redirect the browser to the profile url of the cards owner ('profile/<str:profile_slug')
- Redirect the browser to an error page

#### Developer Updates

*[Sun Sep 21]*

- I will use `card_token` to find this Card's user, and the Profile slug of the user, then send that slug to the profile view url (/profile/<str:profile_slug>)
  
## profile_detail(request, profile_slug)
	

#### Developer Updates

*[?]*

- I'm working on the profile_detail view and Im wondering how i should go about redirecting the browser to the profile_view alias in (urs.py). The general redirect may do the trick if i can access the name of my profile detail view from views.profile_details

*[Sun Sep 21]*

- I've rendered the matching Profile instance to the profile_html template. The attributes in this instance that have values in it's attributes, are visbile in the template .

- Now I need to configure static and media, so that I can display the images from the Profile model.  As of now, my media's root is the base directory [^1]. Let's get back to the `card_detail` view and see if we can properly redirect that specific case to the profile url of the car
	

## card_activate(request, card_token)

This is a view that is visible if any only if the card with card_token is not owned.
If a card is owned,  pass `card_token` to the card detail view (/card/<str:card_token>)


#### Developer Updates

*[?]* 

- The activation template will show the design of the card, the token, and a button asking to claim this card.
- When that button is clicked, the browser is taken to stripe for purchasing. Once a payment intent is received at some url/view combo, update card by setting card.user. 
- I just realized that cards are one of two type cards are one of 2 types: a preset, or a custom design (There are several types of presets) :thinking:. I'm wondering if I should alter my Card model and add a card_type foreign key becuase I'll be able to link the following attribute(s): stripe payment link, default designs, etc. I mean it would it would be cool to show the customers the preset design they chose (in the beginning of the activation process) in the Stripe checkout session

	-		# I propose a new Model called `CardType`
 			CardType:
			pk type_id
			char name
			url stripe_payment 
			
			# Update the existing Card model
 			Card:
			fk type

			# Example Data this would offer 
				=> 1,"Colorful Chicago", "https://strip.com/paymentLink",
				=> 2,"Basic White", "https://strip.com/paymentLinkforwhitecard",
				=> 2,"Custom", "https://strip.com/paymentLinkforwhitecard",

	- Hmmm, I would be able to access the correct payment link from a Card model... but what if this is overkill? To determine that, I'd have to experiment with stripe's post checkout ui. I know that I can send metadata like a card_token... enough talk. To the feature_stripe branch we go (right after this git stash)

- Alright,  embedding Stripe into Django requires 4 steps [^2].
	1. Get Publishable Key
		- bye bye settings.py 
	2. Create a checkout session 
		- Checkout session was a bit messy until I switched to test account (keys) and test price from the custom card product. 
	3. Redirect user to success/cancelled
		- Post checkout redirect goes back to success/ or cancelled. I will be  
	4. Check webhook for checkout.session.completed		

- While this all works, **I need to have access to the card_token and user_id variables at the /webhook/ view to let the system know a card is being activated**.

- Stripe can hold these two![^3]  Which means I'll need to have the two ready before creating a stripe checkout session. I'll use request session to hold the info, but **the question is when**. 

	- Lets visualize the customer flow:
		1. Tap unclaimed card
		2. Sign in / Create Account (if not signed in)
		3. Pay for that card
		4. Update Card details
		6. To dashboard with success message

	- Choices on when to set session data:
		- ~~At Card detail view~~
			-  ~~Can set request card_token~~
		- At card_activate view
			- Can set request  card_token
			-  Will go to checkout_session 		view
		- ~~At checkout session view~~
			- ~~Need to get user_id~~
		- ~~At success view~~
			-~~Needs to get card_token user_id~~
		- ~~At webhook view~~
			- ~~Needs to get card_token~~
			- ~~Needs to get user_id~~
			- ~~Will go to payment_confirmed~~

	- Based on these options I'm going set card_token in card_activate. The button will do one of the two:
		- Go to checkout (if signed in)
		- Go to signin (if signed out)

	- Now the request session data sticks after a stripe checkout. My webhook now updates the card model on payment confirmation.

- To handle Stripe, I've implemented 3 new csrf_exempt function views: **stripe_config**, **create-checkout-session**, **stripe_webhook**. And 2 new function views: **success**, **cancelled**

## stripe_config(request)
Returns Stripe Publishable Key (for test environment) as JSON 

## create_checkout_session(request)
Returns a unique Stripe checkout session id with customized parameters in JSON. The checkout session's UI will be determined by these parameters [^2] 

**Relies on request.session**

## stripe_webhook(request)

Listens for payment confimation @ webhook/

## success(request))
 
Renders success template

**!!Stripe routes to success even when payment isn't confirmed!!**

## cancelled(request))

Renders cancelled template

## CardUpdate(UpdateView)

Renders the CardForm to the card_update template. (It reroutes to the dashboard) 

## LoginView(auth_views.LoginView)

Renders login template

#### Developer Updates

**[Thu Sep 25 2025]**

- I modified the django auth LoginView to use get_success_url() to make the success url dynamic. If `next` parameter gets passed into this view, set the `success url` to the value of `next`

## UserRegistration(CreateView)

Renders UserForm to the `register.html` template.
(logs the user in within `form_valid` method)

#### Developer Updates

**[?]**

- Like the `LoginView`, I will make the success url dynamic by defining the `get_success_url` method

## ProfileUpdate(UpdateView)

Renders ProfileForm to `profile_update.html` template. Success url will dynamical route to the 'profile_view' URL with the proper profile_slug 

#### Developer Updates

**[Fri Sep 26 2025]**

- Adding LoginRequiredMixin class view because people shouldn't have access to editing that person profile. 

- Reroutes to profile_view wasn't working. So I opted to use get_success_url() to have access to self

- Adding get_success_url(self) to redirect to user profile. I opted to use reverse_lazy after trying to include some HttpResponseRedirect method because I knew the name of the URL view ('profile_view'), and what variable it needs in the URL parameter (<str:profile_slug). 

## ProfileCreate(CreateView, LoginRequiredMixin): 

Renders Profile form to `profile_create.html`

#### Developer Updates

**[Fri Sep 26 2025]**

- Adding LoginRequiredMixin class view because people shouldn't have access to creating a profile if they aren't signed in . 



___

# Forms

## ProfileForm

#### Developer Updates

**[Fri Sep 26 2025]**

- I do not need the user_id and date_created to show up, so I'll exclude them from this ModelForm subclass


___

# Templates

## activate.html 

#### Developer Updates

- I'm adding the next parameter to the activate card button's url. It will normally point to the login/ view (unless a user is already signed in... Then it'd point to ). This lets me control the success url over at the login view. If the next parameter is found, the success url of the login form will be the url pathway 

## profile_update.html 

#### Developer Updates

**[Fri Sep 26 2025]**

- Initialized template w/ form from `ProfileUpdate` view

## profile_create.html

The template for the ProfileCreate view. 
___

# Helpful resources

[^1]: https://stackoverflow.com/questions/5517950/django-media-url-and-media-root
[^2]: Using Stripe with Django (https://testdriven.io/blog/django-stripe-tutorial/)
[^3]: Creating a checkout session in Stripe (https://docs.stripe.com/api/checkout/sessions/create)



