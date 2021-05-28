# Student Enquiry Assistant(SEAN)

SEAN is an AI chatbot designed and built by a team of 5 University of Glasgow students.<br>
It was designed in order to assist Social and Public Policies students and take some strain off staff members by dealing with commonly asked questions<br>
This document contains installation requirements, motivations, features, limitations, and licensing<br>
If you have any questions or queries about our product please contact us using our emails below

# Introduction


## The Team

* **Fahad Hafiz(Product Owner) 2314120h@student.gla.ac.uk**
* **Veronika Andrea Polakova(Presenter) 2327846p@student.gla.ac.uk**
* **Ming Ho Wu(Checker) 2133861w@student.gla.ac.uk** 
* **Alan McNamee(Chair) 2324958m@student.gla.ac.uk**
* **Charles Varley(Note Taker) 2391564v@student.gla.ac.uk**

## Motivation

We created this product in colaboration with the University of Glasgow Social and Public Policies department as part of our 3rd year Computing science product.
We spoke to Mark Wong who was looking for us to create a functional chatbot that would hopefully be implemented to assist students with any questions or queries
they had about the course. If successful the product would hopefully deployed elsewhere on other courses within the university and perhaps wider. Because of this
the chatbot has been designed in such a way that it is easily adaptable. Any number of files can be uploaded for the chatbot to use to pull information from, rather
than being hard-coded to only work with very specific questions.

## Requirements

The core requirements of the chatbot were that it must be able to respond to user inputs with hopefully intelligent and meaningful responses. This meant creating
a user interface that was intuitive and familiar. In order to have this be useful to students we decided that it would be best to either create an mobile or web application.
We created a web app as we all had experience with making such as part of our 2nd year Web App development course. It was also required, as established with our client in our
first meeting that our app can gather data from any resources provided i.e. to future proof the chatbot by allowing it to deal with new files as the course has content added/changed.
It was also established that our client would like users responses to be stored and viewed by admins with the appropriate permissions.<br><br>
As none of the group had previously worked with AI before we did not set our requirement list too high. Due to our lack of experience we
were unsure how difficult the task would be. This led to requirements not being set in stone or too strict


## Features

### Web Application
* Intuitive and familiar user interface
* admin abilities to view user logs and add/delete chatbot resources
* cross browser and OS support
* users are able to view and download the resources that the chatbot uses

### Rasa chatbot API
* Intuitive and easily extendable
* wide documentation and active community
* learns interactively from real conversations
* Will improve with frequent use

# Installation

## 1. Basic Setup

**Step 1.1**
A full in-depth installation guide as well as testing, contributing and known bugs can be found [here](https://stgit.dcs.gla.ac.uk/tp3-2019-cs15/cs15-main/-/wikis/SEAN-Tech-Manual)<br>
before going any further ensure you have python installed<br><br>
Python version 3.6.8 was used for this project.
Windows link:
 * https://www.python.org/downloads/release/python-368/

Linux (Ubuntu) in terminal:
 * get https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
 * apt--get install python--dev libxml2--dev libxslt1--dev antiword unrtf poppler--utils pstotext tesseract--ocr flac ffmpeg lame libmad0 libsox--fmt--mp3 sox libjpeg--dev swig<br><br>
 

**Step 1.2** In the main project folder you will find requirements.txt. This contains the requirements necessary to set up
the chatbot. Open a terminal and navigate to the cs15-main directory. Enter the following<br>
**pip install -r requirements.txt**<br><br>

**Step 1.3** Once that is done open a command prompt and enter the following<br>
* **python import nltk**
* **nltk.download(’stopwords’)**
* **nltk.download(’punkt’)**

## 2. Rasa Setup

**Step 2.1** A folder called ‘Rasa’ should be visible in the root directory of the repository.
Navigate into the aforementioned folder. Now, in a terminal or command prompt run the command<br>

**rasa train**

**Step 2.2** To test if all the functions are working, and the program is working as intended.
Open a terminal in the root directory, and enter the following command:<br>

**python3 -m unittest discover scripts.tests**<br><br>

You should see a few things displayed to you, wait for it to all finish, and you should get a 'Job succeeded' at the end.

## 3. Django Setup

**Step 3.1** Our website makes use of a database, before we can use them, we must run the following command on the terminal:
**python manage.py makemigrations seanWebapp**
**python manage.py migrate**
This needs to be run only once.

**Step 3.2** It is highly recommended that you create an admin account to oversee the website.This should be done on the first initialisation.
To create a user who can login to the admin site, run the following command on the terminal:<br>
**python manage.py createsuperuser**<br>
It will prompt you for a desired username, write one, and press [ENTER].
You will then be prompted for your desired email address, write one, and press [ENTER].
The final step is password.
This will happen twice, the second time as a confirmation of the first.
A 'Superuser created successfully' should be displayed on the terminal.<br><br>

## 4. Running the Project

**Step 4.1** There are two parts that must be run for SEAN to perform at its full capabilities: Rasa API and Django
To start Rasa we must first open a terminal within the rasa folder found within cs-15 main and type<br>
**rasa run actions**

**Step 4.2** Open a second terminal in the same folder and enter<br>
**rasa run --m models ----enable-api ----log-file out.log**

**Step 4.3** Now navigate back to cs15-main and in to "sean". Open a terminal and run<br>
**python manage.py runserver**

**Step 4.4** This should provide a url that you can navigate to to begin using the chatbot

## 5. Testing

To test if all the functions are working, and the program is working as intended.
Open a terminal in the root directory, and enter the following command:
**python3 -m unittest discover scripts.tests**
You should see a few things displayed to you, wait for it to all finish, and you should get a 'Job succeeded' at the end.
There are a few tests missing.
In the scripts folder, there should be a folder called: needsNLTK_installed/, take the files inside, and place them with the rest of the tests.
It was not placed in there originally because we were unable to access to lab machine, and install nltk.

In order to test the Django webapp, traverse to the sean directory, and run the following command:
**coverage run --source='.' manage.py test seanWebapp**.
In order to view the test coverage produced by these tests, run:
**coverage report -m**.

## 6. Potential of improvement

There are a few key functions you can modify, and further improve upon: relevanceRatio, and searchfile.
These functions can be found in the refactoredSearch.py, and comments are included to help guide your understanding of the code.
Other than functions, we also have the RasaAPI, its understanding and language comprehension is wholly based on the stories.md, and nlu.md.
These files can be found from the root directory of the repository, then 'rasa/data/'.
The nlu.md is a collection of phrases, and possible replies from the user(s) grouped, and given a name called intent.
This is then used in stories.md to act out scenarios in which these intents might be used, and how to best respond to them.
In addition, testing can also be further expanded upon. You can access the test files from the root directory of the repository, then 'scripts/tests/'.
Every file to test by convention begins with the characters: 'test', and then the python module you would like to test appended to it.

## 7. Known bugs and missing features

Currently, there are a few known bugs.
The searchfile function belonging to refactoredSearch.py does not seem to give a satisfactory answer every time.
SEAN is also missing the following features:
handle how students fill out forms - good cause, extension, absence report. Give the option to have SEAN fill it out, or send inform a member of staff, and give the the details of the enquiry;
a quirky, and comedic SEAN, to be able to reply in jest, but give enough information that it also informs.


# How to Use
a full user guide for the Student Enquiry Assistant Chatbot, including admin use, can be found [here](https://stgit.dcs.gla.ac.uk/tp3-2019-cs15/cs15-main/-/wikis/SEAN-User-Manual)

## Standard user

### General Features
On each page, the left panel contains both the description of the page and instructions on how to best utilize it. Below, the main menu is located. The lower right side includes the buttons to the settings and help pages respectively.

### Chatbot
On the 'Home' page, the main chatbot feature of the application is located. Similarly to any other messaging application, the user simply types the text into the input box and sends it to the chatbot. Subsequently an automatic reply will be received.

### Resources
This page includes all the resources that contain information about the university and courses. In order to open a file, simply click on its name and it will be downloaded as is standard on other web applications.

