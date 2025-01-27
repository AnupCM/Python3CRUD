# Python3
 Python Assessment
 # Python sample application

## Setup

The first thing to do is to clone the repository

```sh
$ git clone https://github.com/AnupCM/PythonInterviewTest.git
$ cd anup
```

Create a virtual environment to install dependencies in and activate it

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies

```sh
(env)$ pip3 install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies
```sh
(env)$ cd mysite
(env)$ python manage.py runserver
```
And navigate to `http://ec2-18-221-36-217.us-east-2.compute.amazonaws.com/account/activities`.

You will get all the data present in the databse
And navigate to `http://ec2-18-221-36-217.us-east-2.compute.amazonaws.com/admin`
you can create new superuser or you can use login credentials(username=anupcm, password=Password@123)
 
For custom management commands use
```
python manage.py seed 10 #to create users
python manage.py actvity #to create random working times

