Our web application is hosted on the CS50 IDE. The back-end consists of a Python-based web application (Flask) and a SQL database (MySQL). The front-end was written in HTML/CSS and Javascript (Jinja). 
	
We created a SQL database that stores two tables - one that holds information about our users and one that holds information about campus locations. The users table contains information for each user’s unique ID, name, Harvard email, current location, and followed friends. The location table contains information for each location name and the corresponding number of people at the location.

Application.py contains all of the Python code that sets up our web app. It contains the information that allows for Harvard Key authentication, keeps track of which user is logged in, and controls all of the different routes in our web app. Each route accounts for whether a user is submitting information through a form or simply viewing the page, and renders or redirects to the correct HTML file. It references our SQL database using sqlite3 and runs relevant queries.

Index.html is our homepage. 

Layout.html includes code that was common among all of our HTML files (e.g. Bootstrap navbar, linking to CSS stylesheet/jQuery/Bootstrap, etc.)

For our “Map” page, map.html displays the front-end and /map is the corresponding route in application.py. This page displays an interactive Google Maps representation of locations on campus, the number of people at each location, and the names of people at each location. An error kept occurring when we linked map.html to styles.css so that’s why we coded the navbar/other common elements separately. 
We used the Maps Javascript API to create our Google Maps functionality and get an API key. The code for setmarkers() and initialize() came from the Google Maps API, allowing us to create markers and display information in pop-up windows for each location. 
To create labels for each marker, we used a string variable of the entire alphabet and for loop to assign a letter to each marker. 
To identify the location of each place on campus, we stored the name, latitude, and longitude of each place in an array of arrays called markers. 
To identify the number of people at each place on campus, we ran SQL queries in the front-end for each location.
We were unable to figure out how to have the map dynamically display the names of people at any given location, so we ended up hard-coding the names of individuals to show what we would ideally want it to look like.



For our “Check In/Out” page, check.html displays the front-end and /check is the corresponding route in application.py. 
On the front end, check.html displays a form with two dropdown menus.
The first dropdown allows users to check in or out. 
The second dropdown allows users to choose from a list of general categories (First-Year Dorms, Upperclassmen Houses, Libraries, or Cafes). 
Then, based on the user’s choice from the second dropdown, the Javascript in check.html uses addEventListener to make the corresponding third dropdown appear. The third dropdown allows users to choose their specific location without needing to sort through a huge list of dropdown options. 
On the back end, the /check route gets the values submitted from the form. To check the user in, the user’s location is also updated in the SQL database and the number of people at that location is incremented in the SQL database. To check out, the opposite occurs. If statements are used to carry out the correct operations.

For our “Find my Friends” page, friends.html displays the front-end and /friends is the corresponding route in application.py. 
On the front end, friends.html allows users to follow up to 10 friends by entering their email. After submitting an email, the user sees a confirmation page if the email is a valid Harvard email. We couldn’t figure out how to display the names of each user’s friends and locations from our SQL database, so we ended up hard-coding ten names and locations to show what we wish it would look like.
On the back end, the /friends route searches for the entered email, ensures the email is a valid Harvard email, and queries for the corresponding name. Then, a SQL database query adds that friend’s name to the current user’s row in the users table.

