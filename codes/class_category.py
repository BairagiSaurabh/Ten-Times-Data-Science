"""

This script takes in data as input and further combines the title and description, cleans the textual data
and uses transformer to label the article based on the given categories

"""

from transformers import pipeline
import concurrent.futures
from tqdm import tqdm
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import logging

class NewsProcessor:
    def __init__(self, dataframe):
        self.df = dataframe
        self.df1 = self.df.copy()
        self.df1['text'] = self.df1['Title'] + ' ' + self.df1['Description']

        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Download NLTK resources
        if not nltk.download('stopwords', quiet=True):
            nltk.download('stopwords')
        if not nltk.download('punkt', quiet=True):
            nltk.download('punkt')
        if not nltk.download('averaged_perceptron_tagger', quiet=True):
            nltk.download('averaged_perceptron_tagger')

        # Lemmatizer and stopwords
        self.lemma = WordNetLemmatizer()
        self.all_stopwords = stopwords.words('english')

        # Remove specific words from the list of stopwords
        for word in ['not', 'against', 'up', 'down']:
            self.all_stopwords.remove(word)

    def clean_text(self, reviews):
        """
        This method removes punctuations, stopwords, and other non-alphanumeric characters.
        It expands the contractions and replaces some words with an empty string.
        """
        try:
            statement = reviews.lower().strip()
            statement = statement.replace("won't", "will not").replace("cannot", "can not").replace("can't", "can not") \
                .replace("n't", " not").replace("what's", "what is").replace("it's", "it is") \
                .replace("'ve", " have").replace("i'm", "i am").replace("'re", " are") \
                .replace("he's", "he is").replace("she's", "she is").replace("*****", " ") \
                .replace("%", " percent ").replace("₹", " rupee ").replace("$", " dollar ") \
                .replace("€", " euro ").replace("'ll", " will").replace("doesn't", "does not")

            statement = re.sub('[^a-zA-Z]', ' ', statement)
            statement = statement.split()
            final_statement = [self.lemma.lemmatize(word) for word in statement if word not in set(self.all_stopwords)]
            final_statement_ = ' '.join(final_statement)
            return final_statement_
        except Exception as e:
            logging.error(f"Error in data cleaning: {e}")
            return ""

    def data_cleaning(self):
        self.df1['clean'] = [self.clean_text(i) for i in self.df1.text.values]
        logging.info("Data cleaning done.")

    def category_classification(self):
        pipe = pipeline(model="facebook/bart-large-mnli")

        def category(sentence, labels):
            try:
                result = pipe(sentence, candidate_labels=labels)
                return result['labels'][0]
            except Exception as e:
                logging.error(f"Error in category classification: {e}")
                return ""

        def allot_category(data, feature):
            labels = ['Terrorism', 'protest', 'political unrest', 'riot', 'Positive', 'Uplifting', 'Natural Disasters',
                      'Others']

            inputs = [(x, labels) for x in data[feature].values]

            # Using ThreadPoolExecutor for multithreading
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Create a list to store futures
                futures = [executor.submit(lambda args: category(*args), input_tuple) for input_tuple in inputs]
                # Use tqdm to track progress
                results_multithreading = []
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Multithreading"):
                    result = future.result()
                    results_multithreading.append(result)

            try:
                data['Category'] = results_multithreading
                replace = {'riot': 'Terrorism / protest / political unrest / riot',
                           'protest': 'Terrorism / protest / political unrest / riot',
                           'political unrest': 'Terrorism / protest / political unrest / riot',
                           'Terrorism': 'Terrorism / protest / political unrest / riot',
                           'Positive': 'Positive/Uplifting',
                           'Uplifting': 'Positive/Uplifting'}
                data.replace({'Category': replace}, inplace=True)
                data.drop(['text', 'clean'], axis=1, inplace=True)
                logging.info("Category allotment done.")
                return data
            except Exception as e:
                logging.error(f"Error in multithreading: {e}")
                return pd.DataFrame()

        try:
            d1 = allot_category(self.df1, 'clean')
            #print(d1)
            logging.info("Category classification and data processing completed successfully.")
            return d1
        except Exception as e:
            logging.error(f"Error: {e}")

