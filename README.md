# [Toronto Network Map] [docs]
Toronto network map is a portal for [M-LAB](http://www.measurementlab.net/) NDT test which focuses on
mapping speed and quality of the Internet in Toronto.

## Technologies
### Backend
The backend is written in Python and we use [Django](https://www.djangoproject.com/) as the web framework. The whole
projects is broken down into different django apps. NDT is responsible for saving/listing NDT tests, accounts takes care
of user registration/login, isp handles internet service providers profiles and stats.

#### Setup
We tested the environment under Apache mod_wsgi and NGINX/gunicorn. However, other web servers should be able to serve
the application as well. In order to setup the project dependencies, we suggest that you set up a virtual environment and simply run:
```
pip install -r requirements.txt
```
### Frontend
Frontend section of the application is located under <code>assets</code> folder and it is written on top of 
[AngularJS](https://angularjs.org/) Framework. Each module is separated intro different folders which include
corresponding controllers and services. 

#### Setup
We use bower as package management which takes care of installing the dependencies. Simply go to assets folder
and run:

```
bower install
```

Documentation on how to install bower and other requirements can be found on the Internet.


## Contribution and Issues
This is our team's side project and we believe we are going to publicly launch the beta version by the End of 2015. If you
want to contribute to this project please get in touch with us or open a pull request so we can review your code before
putting it into our development branches. 


## Install GEOIP globally with the following command
brew install geoip