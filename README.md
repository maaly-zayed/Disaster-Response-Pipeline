# Disaster-Response-Pipeline
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**
- [Project Descriptions](#project-descriptions)
- [Github account](#github-account)
- [Setting up the environment](#setting-up-the-environment)
- [Installation](#installation)
- [Folder Descriptions](#folder-descriptions)
- [Files Descriptions](#files-descriptions)
- [Instructions](#instructions)


<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Project Descriptions

In this project we will build a pipeline for ETL and Machine Learning to classify disasters messages. This project also has a web application where a message is entered and its classification is obtained.
The classification of disasters messages aims to send the message to the concerned relief agency in disaster situations.

## Github account
```bash
https://github.com/maaly-zayed/Disaster-Response-Pipeline.git
```
## Setting up the environment

It is very important to create separate environment to avoid dependecies conflict with other projects.
1. Have Anaconda installed [click here for Anaconda installation](https://www.anaconda.com)
2. Make sure you have [Anaconda path variable](https://www.geeksforgeeks.org/how-to-setup-anaconda-path-to-environment-variable/) set in windows environment variables. 
3. Open cmd and run this command to create environment (must be python 3.6 or later):
```bash
conda create --name Disaster-Response-Pipeline python==3.8 
```
4. Activate the environment:
```bash
conda activate Disaster-Response-Pipeline
```
Now, continue while the environemt is active.

## Installation

The required libraries are included in the file ```bash requirements.txt```

1. Install required libraries.
```bash
pip install -r requirements.txt
```

## Folder Descriptions
1. app folder:  containing a templates folder and flask app "run.py" 
2. data folder:  containing "DisasterResponse.db", "disaster_categories.csv", "disaster_messages.csv" and "process_data.py" which used for  cleaning and and transforming data.
3. models folder:  containing  "classifier.pkl" and "train_classifier.py" for bulding training and evaluation  machine learning model.
4. README file: a description file for the project and the instruction to run "process_data.py"  and "train_classifier.py" 
5. requirements file:  which containing the required libraries 
## Files Descriptions

        disaster_response_pipeline
          |-- app
                |-- templates
                        |-- go.html
                        |-- master.html
                |-- run.py
          |-- data
                |-- disaster_messages.csv
                |-- disaster_categories.csv
                |-- DisasterResponse.db
                |-- process_data.py
          |-- models
                |-- classifier.pkl
                |-- train_classifier.py
          |-- README
          |-- requirements.txt
## Instructions
1. To run ETL Pipeline that clean and store data in the sql database
```bash
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```
2. To run ML pipeline which train,  evaluate and save the classifier model
```bash
python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl
```
3. To run the web app. 
```bash
python run.py
```
4. To display the web page Go to
```bash
 http://127.0.0.1:3001/
```
