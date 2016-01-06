# README #

Street Parking Notifier application for New York City.

### What is app for? ###

* When you park your car on the street of any borough of New York City, Street Parking Notifier saves your car location and later on would send notification over phone/email when you have to move your car in order to avoid parking ticket.

### How it works ###
* With a click of button app would define your current location on the street map.
* and let you select the parking signs from street block where you just parked your car 
* and hours within you would like be notified. 
* In a selected period of time you will receive notification when parking hours on the street expired
* Notification would be send as text message over your phone or email, depends on user preference
* If parking rules where suspended for this particular location, user will receive message from nyc 311 service    
* to view our app please follow the link http://parkingonstreet.heroku.com/

### What software were used ###

* For map we use open source OpenStreetMap API 
* to load map we use LeafLet java script library, that compatible with mobile devises as well as with wide screens.
* to define current user location on the map we use GPS navigator geolocation to find out latitude and longitude
* base on latitude and longitude we define address by calling Google reverse geocode API
* after that by using current address we define street block: from street and to street by calling NYC_Geoclient API
* as soon as from street and to street was obtained, we use SODA2 API to connect to NYC Open Data database and retrieve information about parking signs on the street block where the user parked her/his cur. 
* If car is parked on one way street - parking sign descriptions would be collected from both sides of street, limited by from street and to street intersections.
* If car is parked on two way street - parking signs descriptions only from the side where user parked her/his car would be collected 
* User would offer to select nearest parking sign from drop down list and time period in which she/he would like to be notified about parking rules on that particular side of street. In another words, when the car owner has to move her/his car.
* Information about current car location and selected parking sign and hours would be saved in Location table. And would be used to send notification to user later on.
* To send notification in scheduled time period we are planning to use Google Calendar API and NYC Open 311 API - has to be implemented.
