import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import re
from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
# from sklearn.externals import joblib
import joblib
from sqlalchemy import create_engine

app = Flask(__name__)

def tokenize(text):
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    # Replace all url with "url"
    for url in detected_urls:
        text = text.replace(url, "url")
    # remove special characters from the text and and convert char to lowercase char
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse', con=engine)
# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    security_counts = df.groupby('security').count()['message']
    security_names = list(security_counts.index)
    # Count number of Categories
    category_count = df.iloc[:,4:].sum().sort_values(ascending=False)
    category_names = list(category_count.index)
    
    category = df.iloc[:,4:]
    # Finding the mean of top 5 categories
    top_category_mean = category.mean().sort_values(ascending=False)[1:6]
    top_category_name = list(top_category_mean.index)

    # Finding the least 5 categories
    least_category_mean = category.mean().sort_values(ascending=True)[1:6]
    least_category_name = list(least_category_mean.index)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
         # Fig1 Distribution of Message genre
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message genre',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "genre"
                },
                'width': 1000,
                'height': 700,
                'margin': dict(
                    pad=10,
                    b=150,
                )
            }
        },

         # Fig2 Distribution of Message security
        {
            'data': [
                Bar(
                    x=security_names,
                    y=security_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message security',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "security"
                },
                'width': 1000,
                'height': 700,
                'margin': dict(
                    pad=10,
                    b=150,
                )
            }
        },
        # Fig3 Distribution of categories
                {
            'data': [
                Bar(
                    x=category_names,
                    y=category_count
                )
            ],

            'layout': {
                'title': 'Distribution of Message Categories',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category"
                },
                'width': 1000,
                'height': 700,
                'margin': dict(
                    pad=10,
                    b=150,
                )
            }
        },
                # Fig4 Distribution of Top 5 Message Categories
               {
            'data': [
                Bar(
                     x=top_category_name,
                     y=top_category_mean

                )

            ],

            'layout': {

                'title': 'Distribution of Top 5 Message Categories',
                 'yaxis': {
                'title': "Average count"
                },
                 'xaxis': {
                'title': "Categories"
                },
                'width': 1000,
                'height': 700,
                'margin': dict(
                    pad=10,
                    b=150,
                    )
                }
            }, 
            # Fig5 Distribution of least 5 Message Categories
               {
            'data': [
                Bar(
                     x=least_category_name,
                     y=least_category_mean

                )

            ],

            'layout': {

                'title': 'Distribution of least 5 Message Categories',
                 'yaxis': {
                'title': "Average count"
                },
                 'xaxis': {
                'title': "Categories"
                },
                'width': 1000,
                'height': 700,
                'margin': dict(
                    pad=10,
                    b=150,
                    )
                }
            }
        ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()