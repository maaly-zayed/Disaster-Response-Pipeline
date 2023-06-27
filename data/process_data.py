# import necessary libraries
import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    The function to load data .
    Parameters:
        messages_path: the file path to the messages CSV dataset.
        categories_path: the file path to the categories CSV dataset.
    """
    # Load messages and categories csv files
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    # Merge the two datasets
    df = messages.merge(categories, on='id', how='inner')

    return df


def clean_data(df):
    """
    Function to clean data included in the DataFrame and transform categories part

    Parameters:
        model: trained model.
        df (DataFrame): merged DataFrame

    Output:
        df (DataFrame): cleaned DataFrame
    """

    # Create a datafrm of 36 columns by splitting the values
    #  in the categories column on the ";" character. 
    categories = df.categories.str.split(";", expand=True)
    # Get the first row from categories dataframe.
    first_row = categories.loc[0]

    # Extract a list of new column names for categories by getting
    #  the first (n-2) characters from a string
    category_col_names = first_row.apply(lambda i: i[:-2])
    # Rename the categories column name
    categories.columns = category_col_names

    # Loop over the category columns to keep only 
    # the last character of each string (the 1 or 0). 
    for category in categories:
        # Set each value to be the last character of the string
        categories[category] =  categories[category].str[-1]
        # Convert the data for each column  from string to numeric
        categories[category] = pd.to_numeric(categories[category])
    
    # Drop the categories column from the df
    df = df.drop(columns='categories') 
    # merge the new categories to the df dataframe
    df = df.join(categories)
    # Replace 2 values in related column to 1
    df['related']=df['related'].map(lambda x: 1 if x == 2 else x)
    # Drop the duplicates
    df = df.drop_duplicates()
    
    return df


def save_data(df, database_filename):
    """
    The function to save cleaned data into sql database.

    Parameters:
        df: cleaned datafram.
        database_filename: name of database

    Output: sql database
    """
    # Save a dataframe to sqlite database
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('DisasterResponse', engine,if_exists = 'replace', index=False)


def main():

    if len(sys.argv) == 4:
        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]
        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
                .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)
        print('Cleaning data...')
        df = clean_data(df)
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
                'datasets as the first and second argument respectively, as '\
                'well as the filepath of the database to save the cleaned data '\
                'to as the third argument. \n\nExample: python process_data.py '\
                'disaster_messages.csv disaster_categories.csv '\
                'DisasterResponse.db')


if __name__ == '__main__':
    main()
