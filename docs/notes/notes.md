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
tk                        8.6.14               h39e8969_0  
tzdata                    2025a                h04d1e81_0  
urllib3                   2.5.0                    pypi_0    pypi
wheel                     0.45.1          py312h06a4308_0  
xz                        5.4.6                h5eee18b_1  
zlib                      1.2.13               h5eee18b_1  

```
___

# Models

~~![ER Diagram](https://raw.githubusercontent.com/tairesu/Assignment_Project_Tyrese_tyresec2/refs/heads/main/docs/notes/erDiagram.png)~~

#### Relationships: 
- A User has 0 or many Cards
- A User has 0 or 1 Profile
- A Card must have 1 Design
- A Design is used in 0 or many Cards (1->M)
  
I chose my models to make the process of handling card-based redirects easier. There are 4 different ways of handling a card. 

1) A customer can activate the card (checks Card.user)
2) Redirect to the URL in the card model (Card.reroute_url)
3) Redirect to the card owners profile (checks Card.show_profile)
4) 404: Redirect to 404

This setup was decided to effortlessly handle this reroute logic, because the attributes that determine this handling logic are found in one Model (Card).



#### dev notes:

*[?]*

- profile_slug shouldnt have more than 25 characters. customers simply give their profile a way to be found with field (Ex "reese" => https://tcdigitalcards.com/profile/reese). These should be unique 
- Card model should certainly have a unique token. Im wondering if the combination of both fields user and alias should be unique as well. I can't name 2 cards the same thing...unless I was a church who ordered 50 cards. theoretically each church member would activate their own cards (including accounts)... so there shouldn't be a case where a user has the same alias. Each member may have the same card name of "X Church Card". I'll leave these rwo fields alone for now. 
- I do want to change the format for the card model to show unclaimed if user is not attached. Cards that are already on display or in my current inventory should be easily retrievable in the database. I'll add some conditions to the __Str__ method of Card
- Whoops. It looks like i shouldve made profile slug's blank = False
- I added a bio to the Profile. This decision was made to help fill the empty space in the profile.html template from the profile detail view.

*[Sun Oct 5 2025]*

- I've added the Design Model for more efficient stats gathering. I'm seeking to answer questions like which designs are the most/least popular. 
- I've added the design foreign key to the card model, since the Design model holds front/rear design attributes. 

- The Design model holds the images taht'll go on a card. Customers may opt to customize their own cards post payment. This will insert into design with a preset name. For this I'll add a status model to differ between requested/approved cards.
	- the goal is to distinguish b/w presets and user designs in Design model

	Trainway (approved)
	Mountain top (approved)
	Custom: [owner]'s Custom Design (pending)

	
___

# Views


## card_detail(request, card_token).
This retrieves a singlular `Card` model instance where Card.token = `card_token`. 

It also redirects the browser according. There are 4 possible redirects that may occur:
- Redirect the browser to this card's `reroute_url`
- Redirect the browser to the activate card url (`activate/<str:card_token>`)
- Redirect the browser to the profile url of the cards owner ('profile/<str:profile_slug')
- Redirect the browser to an error page

#### dev notes:

*[Sun Sep 21]*

- I will use `card_token` to find this Card's user, and the Profile slug of the user, then send that slug to the profile view url (/profile/<str:profile_slug>)
  
## profile_detail(request, profile_slug)
	
#### dev notes:

*[?]*

- I'm working on the profile_detail view and Im wondering how i should go about redirecting the browser to the profile_view alias in (urs.py). The general redirect may do the trick if i can access the name of my profile detail view from views.profile_details

*[Sun Sep 21]*

- I've rendered the matching Profile instance to the profile_html template. The attributes in this instance that have values in it's attributes, are visbile in the template .

- Now I need to configure static and media, so that I can display the images from the Profile model.  As of now, my media's root is the base directory [^1]. Let's get back to the `card_detail` view and see if we can properly redirect that specific case to the profile url of the car

*[Thurs Sep 30]*

- I'm going to turn the view function into a subclass of detail view. it's a requirement for this week's presentation, so I'll make it happen. My only problem is that this view is requested from a url string like so: `profile/<str:profile_slug>` 
	- By default DetailView relies on pk because I got an error when I first made a request to the class based version of this profile_detail function view. it turns out that the DetailView subclasses a mixin called `SingleObjectMixin` [^9]
	- This mixin has attributes called `slug_field` and `slug_url_kwarg`. They help tell Django the name of the field/attribute containing the slug, and the name of the slug placeholder going into the url. (For me it's also `profile_slug`). I'll set these and see what happens

## card_activate(request, card_token)

This is a view that is visible if any only if the card with card_token is not owned.
If a card is owned,  pass `card_token` to the card detail view (/card/<str:card_token>)

#### dev notes:

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


~~## CardUpdate(UpdateView)~~

Renders the CardForm to the card_update template. (It reroutes to the dashboard) 

~~## LoginView(auth_views.LoginView)~~

Renders login template

#### dev notes:

**[Thu Sep 25 2025]**

- I modified the django auth LoginView to use get_success_url() to make the success url dynamic. If `next` parameter gets passed into this view, set the `success url` to the value of `next`

**[Sun Sep 28 2025]**

- I added a "I'm new here" button to the  login.html template. I noticed the next parameter when the LoginRequiredMixin redirects to the login url. that next parameter is what tells django to go to a specific page post login

- If a user tries to sign in to claim a card (Goes to login), there'll be a next parameter.... but if they click "I'm new here" on that login page then the next parameter gets lost. I must fix that by holding the next parameter and handing it to the template. I'll use get_context_data in this view like so: 

- 	```
	class LoginView(auth_views.LoginView):
		template_name = 'cardManager/login.html'
		success_url = reverse_lazy('dashboard_view')

		def get_success_url(self):
			return self.request.GET.get('next') or self.success_url

		#Let's put the next param in the context 
		def get_context_data(self, **kwargs):
			context = super().get_context_data(**kwargs)
			context['nextUrlParam'] = self.request.GET.get('next')
			return context
	``` 
	- I'm going to try 2 solution to this problem .
		1. I see self.request.GET..... which is already accessible via template
			- So this works in the template: `{% url 'register_view' %}?next={{request.GET.next}}`
		2. ~~Just send it in context using get_context_data~~

- I chose option 1 since request is given in the template. Now option 1 may not be the most secure but I'll have to come back. Scratch that, option 2 better in the sense that I can validate the next parameter so people don't brute force their way accross the system. Any next parameter that isn't validated would get tossed (would be ideal in the future). For now we replicate this across the register page 

## UserRegistration(CreateView)

Renders UserForm to the `register.html` template.
(logs the user in within `form_valid` method)

#### dev notes:

**[?]**

- Like the `LoginView`, I will make the success url dynamic by defining the `get_success_url` method

## UserDashboard(LoginRequiredMixin, ListView)

A view that renders the cards, that belong to a user, into the `dashboard.html`template.

#### dev notes:

**[Sat Sep 27 2025]**

- I'm switching from a function view to a class view to have access to these [mixins](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/mixins.py#L46). I stumbled upon them last night and had a feeling that I'll use more than 1 of them for this application.

- Editing context is a bit different here. [^6]

- ```
   def get_context_data(self, **kwargs):
		user = self.object
		user_cards_list = user.cards
		# Let's get the context that exists already
		context = super().get_context_data(**kwargs)
		context['cards'] = user_cards_list
		return context
	```
	- My error says that theres no self.object. Well I wonder what self gives me when i print it. 

	- `<cardManager.views.UserDashboard object at 0x7fb0541abce0>` 

	- Hmmm, What does self.request say?

	- `<WSGIRequest: GET '/dashboard/'>`

	- :cool:. I know I can access `self.request.user` from this view safely. W/ this information this is what I've come up with

	- 	```
		def get_context_data(self, **kwargs):
			user_id = self.request.user.pk
			cards = Card.objects.filter(user=user_id)
			# Let's get the context that exists already
			context = super().get_context_data(**kwargs)
			context['cards'] = [card for card in cards]
			return context
		```
		- Works perfectly.  I expect their to be more info/metrics on the dashboard later, so I'll keep this code

~~## ProfileUpdate(UpdateView)~~

Renders ProfileForm to `profile_update.html` template. **Success url will dynamically route to the 'profile_view' URL with the proper profile_slug** 

#### dev notes:

**[Fri Sep 26 2025]**

- Adding LoginRequiredMixin class view because people shouldn't have access to editing that person profile. 

- Reroutes to profile_view wasn't working. So I opted to use get_success_url() to have access to self

- Adding get_success_url(self) to redirect to user profile. I opted to use reverse_lazy after trying to include some HttpResponseRedirect method because I knew the name of the URL view ('profile_view'), and what variable it needs in the URL parameter (<str:profile_slug). 

~~## ProfileCreate(CreateView, LoginRequiredMixin): ~~

Renders Profile form to `profile_create.html`

#### dev notes:

**[Fri Sep 26 2025]**

- Adding LoginRequiredMixin class view because people shouldn't have access to creating a profile if they aren't signed in . 


~~## LogoutView(auth_views.LogoutView)~~

Logs the user out. Requires post request

#### dev notes:

**[Fri Sep 26 2025]**

- This is beginning to be a pain :sweating:  . My issue is that LogoutView keeps defaulting to /accounts/login. The solution is to change `settings.LOGOUT_REDIRECT_URL`, but I did that. 
	- I tried:
		- setting it to '/login'
		- setting it to '/login/'
		- setting LogoutView.next_page to '/login/'
		- putting a redirect in LogoutView.get_success_url
			- nothing seemed to be printing from here
		- LoginView
			- Nothing seemed to be printing from here
	- It seems like LogoutView never gets called....Lets check the logs:
		- ```
	    	[26/Sep/2025 23:11:11] "GET /profile/1/update/ HTTP/1.1" 302 0
			Not Found: /accounts/login/
			[26/Sep/2025 23:11:11] "GET /accounts/login/?next=/profile/1/update/ HTTP/1.1" 404 5506```
	   		~~~
	- /logout isn't being called here. The system goes from `GET /profile/1/update` to `GET /accounts/login`. Let's check what the default is using `python manage.py shell`
		- ```
    		settings.LOGOUT_REDIRECT_URL
			>>> '/login'
			# Out of curiosity I checked to see what the logout url was
			settings.LOGOUT_URL
			>>> '/accounts/logout/'
		```
	- None of these show how accounts/login was requested. It seems like settings.LOGIN_URL could be responsible [^4]

	- **AHA! I needed to update settings.LOGIN_URL** 


## Stats(ListView)
Renders app-wide stats to statistics template

#### dev notes:

**[Wed Oct 8 2025]**

- There are questions I want to have answered about this application: 
	- Which owner has tapped the most cards? (Leaderboard)
	- Which design is least/most popular? 
	- How many cards are unclaimed/claimed ?
	- How many taps was my system responsible for? (N Total)

- `cleaned_user_taps` and `user_taps` answers how many taps each user is responsible for.  User_taps will use Count and annotate to count the number of unqiue card__owner_ids.
	- The format of this doesnt allow me to access the Owner models. So I created a list of dictionaries, where each obj is composed of two keys: `user` and `n_card_taps`. 
	- `user` will be the unique Owner instance 
	- `n_card_taps` the # of times a user tapped their cards

**[Sat Oct 11 2025]**

- I want to perform another aggregation of card taps grouped by unique  dates. I'd love to see how many people are using the cards.  I fear that the Model time stamps will get in the way of the process, unless I can format the dates before annotating them. 

- The dates are problematic as expected. I tried using Extract Year in the annotate method , but it annotated with a new attribute with just the year 2025.

- I snooped around and found a function that'll help me in `django.db.models.functions` called `TruncMonth`. 
	- I went into django's shell and ran `Usage.objects.exclude(card__owner=None).values('date_used').annotate(n_taps=Count('date_used'))`
	- This was the head of that result: <QuerySet [{'date_used': datetime.datetime(2025, 10, 5, 23, 38, 34, 680625, tzinfo=datetime.timezone.utc),  'n_taps': 1},{...}]

	- *Running annotate while selecting the date_used column gave me 38 items in the queryset*. The same number of usages that exist excluding the unclaimed cards. Essentially, `Usage.objects.exlude(card__owner=None) == Usage.objects.exclude(card__owner=None).values('date_used').annotate(n_taps=Count('date_used')).count()`, *and that is incorrect*

	- The latter portion of that should be smaller, so I tried TruncMonth like so: `Usage.objects.exclude(card__owner=None).values(n=TruncMonth('date_used')).annotate(n_taps=Count('n'))`

	- That returned a single queryset: `<QuerySet [{'n': datetime.datetime(2025, 10, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'n_taps': 38}]>` This set the hours and minutes of all my date_used fields to 0, and the day to be 1. All of my tests were conducted in the month of october, so annotate saw this as one unique datetime and counted every possible occurence. 
	- I took a guess and imported `TruncDay` and it worked. I substituted TruncMonth with TruncDay, and got this: `<QuerySet [{'n': datetime.datetime(2025, 10, 5, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'n_taps': 4}, {'n': datetime.datetime(2025, 10, 6, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'n_taps': 28}, {'n': datetime.datetime(2025, 10, 8, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'n_taps': 6}]>`. TruncDay formats the datetimes to set hour and minutes to 0. Since my tests were conducted on different days, there were more datetime objects instead of the one I got from TruncMonth. That explains why there were 3 unique objects. `TruncDay` is what I was looking for!!


## ~~design_usage~~ => config_plotly()

Function based view that **provides Plotly js with data** to plot multiple graphs. This returns a JsonResponse that follow this structure:

	[ 
		{ # Graph data object
			"target_elem": "",
			"type" : "",
			"x_series" : [],
			"y_series" : [], 
		}, 
		{...}, {...}
	]

#### how it works:

1) Request hits 'stats/fetch_plotly_data'
2) Config plotly gets instantiated
3) `graphs` is []
4) Define querysets : <Queryset [{},{}]>
5) Clean querysets: {x:[], y}
6) Append to graphs
7) return graphs json

#### dev notes:

**[Sun Oct 12 2025]**

- I should reconsider the Plotly structure 
___

# Forms

~~## ProfileForm~~

#### dev notes:

**[Fri Sep 26 2025]**

- I do not need the user_id and date_created to show up, so I'll exclude them from this ModelForm subclass


___

# Templates

## base.html 

#### dev notes:

**[Sat Sep 27 2025]**

- I like Tailwind [^7]. I'm using it w/ Django to dynamically render some good looking components. (Or should I say Jinja & Tailwind :inspect:)

- Not that Tailwind is installed, I'll be modifying this template to fit within my normal Tailwind flow. I'll keep my template's if blocks as thin as possible; Using them to generate dynamic elements /plain text only

- Tailwind <nav> is now ready
- Getting <body> ready for linear gradient [^8]

## activate.html 

#### dev notes:

- I'm adding the next parameter to the activate card button's url. It will normally point to the login/ view (unless a user is already signed in... Then it'd point to ). This lets me control the success url over at the login view. If the next parameter is found, the success url of the login form will be the url pathway 


~~## profile_update.html ~~

#### dev notes:

**[Fri Sep 26 2025]**

- Initialized template w/ form from `ProfileUpdate` view

~~## profile_create.html~~

The template for the ProfileCreate view. 

#### dev notes:

**[Sat Sep 27 2025]**

- I need to customize my form instead of using it like `form.as_p` because I'm going to add classes to them 

	- In inspect element, each input element has a corresponding id formatted like 'id_<fieldname>', and a name attr formatted like '<fieldname>'
	- Labels have a `for` attribute that's formatted like 'id_<fieldname>'

- Now I know I could replicate that, but what about form error messages? 
	- I triggered a form error to see the HTML handling of an error. 
	- 	```
		
		```

## login.html 

The template for the login view

#### dev notes:

**[Sun Sep 28 2025]**

- I added an if block that checks the context from LoginView:
- 	```
	# login.html
	{% if nextUrlParam %}
    <a href="{% url 'register_view' %}?next={{nextUrlParam}}" class="text-center text-md text-[var(--color-main)] mt-8">I'm new here</a>
    {% else %}
    <a href="{% url 'register_view' %}" class="text-center text-md text-[var(--color-main)] mt-8">I'm new here</a>
    {% endif %}
	```

	- the url route in nextUrlParam is set in LoginView.get_context_data() to be whatever next parameter value at the time of the LoginView's initiation 

___

## stats.html

A playground for displaying data aggregations and visualizations

#### dev notes:

**[Sat Oct 11 2025]**

- This was developed a couple of days ago
- Today I've decided to use plotly js to show a line graph of daily card usage. It seems simple and its all done in javascript [^14]. I'll create Json objects that my javascript will fetch from a url. 
# Static 

## /css
## /js/get_plotly_data.js

Retrieves JSON data from view and generates charts accordingly

#### dev_notes:

**[Sat Oct 11 2025]**

-This was fun. I've successfully managed to retrieve aggregated data from my database and graph it using JSONResponse and plotly. I created plot_design_usage to render the graph and define base variables (element id, data, layout, config)

- I need to expand this setup to enable the creation of model graphs. Lets start at the beginning: 
	1) JS Fetch Request comes to /stats/fetch_plotly_data
	2) Python view performs database aggregation, and returns json reponse 
		``` {x:[],y:[]}```
	3) When json response arrives, return the json version of the response
	4) With json data (`data`), call plot_design_usage function

- What if I added the leaderboard seed data into the json response data too? 
	- Well my plotly wouldn't look too different. I would have to define my trace obj,  layout obj, element id, and config obj differently. (Thats pretty different). If I executed the graphs via a class instance, i could loop through a json response  effortlessly. 
	- Imagine a response like this: 

	{
		graphs: [{},{},{}]
	}

	- Each {} containing keys:
		- `target_elem`
		- `traces` array 
		- `layout` obj
		- `config` obj
	- Well that would be annoying to config and send in python. Lets be lazy and have python have less to send.  I need x and y, and the target element
		- Each {} containing keys:
			- `target_elem`
			- `traces` array 
			- `layout` obj
			- `config` obj
	- I could loop through this response, and create a hypothetical Plot instance. That Plot instance would have the following methods: 
		- `plot(**kwargs)`: calls Plotly.newPlot and passes params
		- `__set_config(new_config={})`: set self.config to be new_config
		- `__set_traces([])`: loops through traces and append to self.traces
		- `__set_data()`: loops through traces and appends to self.data
		- `__set_layout({})`

	- Now that I created a class that will plot the graphs I've run into issues. In views.py config_plotly, I've developed a pipeline that pushes parsed aggregate querysets into a list called graphs. 
		-	In my parse qs function, I need to map the appropriate key value pair from the aggregate queryset into the x key.
		- When i formulate the queryset, I can rename a column (like annotate). To ensure that __parse_qs grab the right key value pair, I'll get my queryset to have an 'x' field. [^15]




# Helpful resources

[^1]: https://stackoverflow.com/questions/5517950/django-media-url-and-media-root
[^2]: Using Stripe with Django (https://testdriven.io/blog/django-stripe-tutorial/)
[^3]: Creating a checkout session in Stripe (https://docs.stripe.com/api/checkout/sessions/create)
[^4]: https://docs.djangoproject.com/en/5.2/ref/settings/#:~:text=LOGOUT_REDIRECT_URL
[^5]: All of Django's auth mixins (https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/mixins.py#L46)
[^6]: Using get_context_data() (https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-display/#adding-extra-context)
[^7]: Tailwind 'Play Cdn' (https://tailwindcss.com/docs/installation/play-cdn)
[^8]: Linear Gradient in Tailwind (https://tailwindcss.com/docs/background-image)
[^9]: CBVs subclass SingleObjectMixin! (https://docs.djangoproject.com/en/5.2/ref/class-based-views/mixins-single-object/)
[^10]: Aggregations? (https://docs.djangoproject.com/en/5.2/topics/db/aggregation/)
[^11]: Querying in Django (https://docs.djangoproject.com/en/5.2/topics/db/queries/)

[^12]: For-loop counter in template (https://stackoverflow.com/questions/11481499/django-iterate-number-in-for-loop-of-a-template)
[^13]: Annotating unique Datetime fields (https://forum.djangoproject.com/t/combining-count-and-queryset-datetimes/2799)
[^14]: Data Visualization using Plotly.js (https://plotly.com/javascript/line-charts/)
[^15]: renaming values in django (https://stackoverflow.com/questions/10598940/how-to-rename-items-in-values-in-django)