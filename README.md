# Ontario Parks Reservation Scraper
Get notifications when sites become available at the Park and campground of your choice

## How to use
### Requirements
* Python3
  - smtplib
  - selenium
  - pync (on Mac)
  - urllib
* MAC OS for desktop notification (email works on all operating systems)

### Config.py
* Fill in the variables in the config.py to match your case
* The Location and Campground must be spelled the way it appears on the reservations.ontarioparks.com website
* Start Date and End Date shold be in yyyy-MM-dd format
* *TIME\_TO\_RETRY *, in the case that no available campsites are found, is the amount of time in seconds before trying to find available sites again
* For the email address password, use an app password

### Output
If no available campsites are found matching the criteria in config.py, the script will run again after *\<TIME\_TO\_RETRY\>* seconds.
If one or more campsites are available, the configured email address will receive an email with the link to reserve the site.