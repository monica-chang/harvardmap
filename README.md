# Harvard Map Project


CS50 Project

Welcome to our project!

We created and hosted our project on the CS50 IDE. To compile, configure, and use our project, login to the CS50 IDE and download all of our files, open a terminal window to execute the following: 
- Execute “cd harvardmap” to change into that (i.e. open) that directory. 
- You should see a file called authentication.txt in the harvardmap folder. To set the environment variables necessary for running the CS50 ID (Harvard Key authentication) and the Google Maps API, copy/paste the export commands from authentication.txt and run them in the terminal. 
- Execute “flask run” to start the website and click the provided link, which should be http://f4ee8546-ac3d-440c-94c2-b449f32e03c6-ide.cs50.xyz/.

Upon launching the website, please click on the “I solemnly swear I’m up to no good” button that will redirect you to the Harvard Authentication login, where you should log in with your Harvard ID. You will then be redirected back to our home page. If at any time you would like to log out, you can click the log out button on the home page or from the navigation bar.

To find study locations on campus, please click on the “Map” button in the nav bar that will direct you to our customized Google Map page. The markers on the map depict 39 study locations including first-year dorms, upperclassmen houses, cafes, and libraries on campus. To learn more about each location, click on one of the markers. An info window will appear containing information about the name of the location, the number of total people currently checked into that location. You will also be able to see the people at that location who are your friends. However, this feature is currently hard-coded in because we couldn't figure out how to loop through that information in the SQL database.

To check in or check out of a location please click on the “Check In/Out” button in the nav bar. If at anytime you would like to leave this page, please click on “Marauder's Map @ Harvard” to take you back to the home page. Once on the "Check In/Out" page, you should first select if you would like to check in or check out of your stated location. Then, you can select from a list of general categories (first-year dorms, houses, libraries, or cafes). Your choice will prompt another dropdown to appear, asking you to choose your specific location. Once your location is selected, please click the submit button to update your location and you will be redirected to a confirmation page saying “Mischief Managed!”. If you try to check into a location twice, you will be prompted with the apology message “you have already checked in”. If you try to check out of a location that you have not yet checked into, you will be prompted with the apology message "you have not checked in yet." The map currently has a watermark that say “for development purposes only” because we have not attached a billing account to it so please ignore this. 

To see the current locations of your friends, please click on the “Find My Friends” button in the nav bar. You will be able to see the locations of up to ten of your friends by entering their email into the form and clicking the “Follow” button. If you enter an invalid email, you will be presented with the apology message “you have typed an invalid email.” We did not figure out how to display names/locations from our SQL database to the website, so we have currently hard-coded in ten friends and locations. At this time, you will not be able to unfollow your friends (so choose wisely haha).

Mischief Managed! - Priyanka and Monica





