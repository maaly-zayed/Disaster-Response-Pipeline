# import important libraries
import sys
from sqlalchemy import create_engine
import nltk
nltk.download(['punkt', 'wordnet'])
import re
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.multioutput import MultiOutputClassifier
import pickle
from sklearn.metrics import precision_score


def load_data(database_filepath):
    """
    The function to load the created database.

    Parameters:
        database_filepath: the file path to the database_filepath.
    """
    # Create a connection to the sql database
    engine = create_engine('sqlite:///'+database_filepath)
    # Read sql tables into datafram
    df = pd.read_sql_table('DisasterResponse', engine)
    # Get the message data
    message = df['message']
    # Get the categories name
    categories = df.iloc[:,4:]
    category_names = categories.columns 

    return message, categories, category_names


def tokenize(text):
    """
    The function to tokenize the text messages.

    Parameters:
        text: text messages.
    Output:
        lemm_lower_tokens: a list of the root for each word
    """
    # Preprocessing using regex to detect url in the message
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Find all url in the message text
    detected_urls = re.findall(url_regex, text)
    # Replace all url with "url"
    for url in detected_urls:
        text = text.replace(url, "url")
    # remove special characters from the text and and convert char to lowercase char
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    # Convert text messages into tokens
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    # Preprocessing
    lemm_lower_tokens = []
    for token in tokens:
        # Lemmatize each token 
        process_token = lemmatizer.lemmatize(token).strip()
        lemm_lower_tokens.append(process_token)

    return lemm_lower_tokens    


def build_model():
    """
    The function to create a pipeline for model to classify a disaster messages.
    """
    # Create a pipline of CountVectorizer, TfidfTransformer and MultiOutputClassifier
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))
        ])
    # Set the parameters 
    # parameters = {
    #     'clf__estimator__n_estimators': [10,20],
    #     'clf__estimator__min_samples_split': [2,4],
    # }
    # Note i change the parameters because I couldn't push the model to github
    parameters = {
        'clf__estimator__n_estimators': [10],
        'clf__estimator__min_samples_split': [2,4],
        }
    model = GridSearchCV(pipeline, param_grid=parameters, n_jobs=4, verbose=2, cv=3)

    return model


def evaluate_model(model, X_test, Y_test, category_names):
    """
    The function to evaluate the model performance.

    Parameters:
        model: trained model.
        X_test: test text message
        y_test: the correct target
        category_names: the target names

    Output: priniting the classification report
    """
    # Get the prediction of test data
    y_pred = model.predict(X_test)
    for indx, category in enumerate(category_names):
        print('The classification_report for: {}'.format(category))
        print(classification_report(list(Y_test.values[:, indx]), list(y_pred[:, indx])))


def save_model(model, model_filepath):
    """
    The function to save model.

    Parameters:
        model: trained model.
        model_filepath: the model path

    Output: pikle version of the model
    """
    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()