# Harvard Map Project


CS50 Project

Welcome to our project!

We created and hosted our project on the CS50 IDE. To compile, configure, and use our project, login to the CS50 IDE and download all of our files, open a terminal window to execute the following: Execute “cd harvardmap” to change into that (i.e. open) that directory. You should see a file called authentication.txt in the harvardmap folder. To set the environment variables necessary for running the CS50 ID (Harvard Key authentication) and the Google Maps API, copy/paste the export commands from authentication.txt and run them in the terminal. Execute “flask run” to start the website and click the provided link, which should be http://f4ee8546-ac3d-440c-94c2-b449f32e03c6-ide.cs50.xyz/.

Upon launching the website, please click on the “I solemnly swear I’m up to no good” button that will redirect you to the Harvard Authentication login, where you should log in with your Harvard ID. You will then be redirected back to our home page. If at any time you would like to log out, you can click the log out button on the home page or from the navigation bar.

To find study locations on campus, please click on the “Map” button in the navigation bar that will direct you to our customized Google Map page. The markers on the map depict 39 study locations such as first-year dorms, upperclassmen houses, cafes, and libraries on campus. To learn more about each location, click on one of the markers for an info window to appear which will contain information about the name of the location, the number of people currently checked into that location. You will also be able to see the people at that location who are your friends in the info window but this feature is currently hardcoded in because we were stuck on finding a way to loop through that information in the SQL database.

To check in or check out of a location please click on the “Check In/Out” button. If at anytime you would like to leave this page, please click on “Marauder's Map @ Harvard” to take you back to the home page. Once on the check in or check out page, you should first selected if you would like to check in or check out of your stated location. Then, you can select a location from a list of overarching categories (freshman dorms, houses, libraries, or cafes) which will prompt a second drop down box to appear that will ask you to elaborate on your specific location. Once you location is selected please click the submit button to update your location and you will be redirected to a confirmation page that says “Mischief Managed!”. If you try to check into a location twice, you will be prompted with the apology message “you have already checked in”. If you try to check out of a location that you have not checked in to, you will be prompted with the apology message "you have not checked in yet." The map currently has a watermark that say “for development purposes only” because we have not attached a billing account to it so please ignore this. 

To see the current locations of your friends, please click on the “Find My Friends” button in the navigation bar. You will be able to see the locations of up to ten of your friends by entering their email into the text box and clicking the “Follow” button. If you enter an invalid email, you will be presented with the apology message “you have typed an invalid email.” We did not figure out how to display from the SQL database to the website so we have currently hardcoded in ten friends to display their location. At this time, you will not be able to unfollow your friends (so choose wisely haha).

Mischief Managed! - Priyanka and Monica





