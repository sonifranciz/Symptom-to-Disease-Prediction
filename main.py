# from flask import Flask, render_template, request
# import json
# import pickle
# app = Flask(__name__)
# #app = Flask(__name__, template_folder=r'C:\Users\sonia\PycharmProjects\Symptoms\html')
#
# """with open('model.pckl', 'rb') as file:
#     clf = model.load(file)
# """
#
# @app.route('/')
# def index():
#     return render_template('chat1.html')
# @app.route('/diagnosis', methods=['GET', 'POST'])
# def diagnosis():
#     if request.method == 'POST':
#     # Get the input data from the form submission
#     # Assuming you have form fields 'feature1', 'feature2', etc.
#         symptoms = request.form.get('symptoms')
#     # Replace 'text_data' with the name of the input field for text data
#     #image = request.files['image']
#         prediction = clf.predict([symptoms])
#     return render_template('chat3.html', prediction=prediction)
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.corpus import stopwords
import re
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         print(email,password)
#
#         # Connect to your MySQL database
#         mydb = mysql.connector.connect(
#           host="localhost",
#           user="root",
#           password="12345@Soni",
#           database="symptoms"
#         )
#
#         mycursor = mydb.cursor()
#
#         # Make sure to avoid SQL injection
#         query = "SELECT * FROM users WHERE email = %s AND password = %s"
#         mycursor.execute(query, (email, password))
#
#         user = mycursor.fetchone()
#         print(user)
#
#         # Close the connection
#         mycursor.close()
#         mydb.close()
#         print("Checking done")
#
#         if user:
#             print("Success")
#             # User login successful
#             # Here you could set the user session and then redirect to the predict page
#             return redirect(url_for('predict'))
#         else:
#             # User login failed
#             # Here you could return an error message to be displayed on the login page
#             return render_template('chat1.html', error="Invalid email or password.")
#
#     return render_template('chat1.html')

email_const=0
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to your MySQL database
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="12345@Soni",
          database="symptoms"
        )

        mycursor = mydb.cursor()

        # Fetch the user by email
        query = "SELECT * FROM users WHERE email = %s"
        mycursor.execute(query, (email,))

        user = mycursor.fetchone()

        # Close the connection
        mycursor.close()
        mydb.close()
        print(user)

        # Check the password against the hash
        if user and check_password_hash(user[5], password):
            # User login successful
            email_const = email
            return redirect(url_for('predict'))

        else:
            # User login failed
            return render_template('chat1.html', error="Invalid email or password.")

    return render_template('chat1.html')


# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         print(email,password)
#
#         mydb = mysql.connector.connect(
#           host="localhost",
#           user="root",
#           password="12345@Soni",
#           database="symptoms"
#         )
#
#         mycursor = mydb.cursor()
#
#         query = "SELECT * FROM users WHERE email = %s"
#         mycursor.execute(query, (email,))
#
#         user = mycursor.fetchone()
#         mycursor.close()
#         mydb.close()
#
#         if user and check_password_hash(user[2], password):
#             # User login successful
#             return redirect(url_for('predict'))
#         else:
#             # User login failed
#             pass
#
#     return render_template('chat1.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('dob')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password == confirm_password:
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              password="12345@Soni",
              database="symptoms"
            )

            mycursor = mydb.cursor()

            # hash and salt the password
            hashed_password = generate_password_hash(password)

            query = "INSERT INTO users (first_name, last_name, dob, email, password) VALUES (%s, %s, %s, %s, %s)"
            mycursor.execute(query, (first_name, last_name, dob, email, hashed_password))

            mydb.commit()

            mycursor.close()
            mydb.close()

            # Redirect to the login page
            return redirect(url_for('login'))
        else:
            # Password and confirm password do not match
            pass

    return render_template('chat2.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    predicted = None  # Initialize 'predicted' with a default value
    symptoms = None  # Initialize 'symptoms' with a default value
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')

        print(symptoms)

        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password="12345@Soni",
          database="symptoms"
        )

        # The rest of your code here...

        ocr_text = pd.DataFrame([textconvert(symptoms)], columns=['Combined Data'])
        print(ocr_text)
        ocr_text['cleanText'] = preprocess(symptoms)
        print(ocr_text)
        predicted = predictfunc(ocr_text)

        print(predicted)

    return render_template('chat3.html', prediction=predicted[0] if predicted else "No prediction", symptoms=symptoms)




def textconvert(user):
    STRING = user

    # Split the string into rows using commas as delimiters
    rows = STRING.split(',')

    # Create a list to store the data for each row
    data = []

    # Loop through each row and clean the data
    for row in rows:
        data.append(row.strip())

    # Concatenate all the rows into a single string
    combined_data = ', '.join(data)

    # Create a DataFrame with a single row containing the combined data

    # Display the DataFrame
    print(combined_data)
    return combined_data
def preprocess(sentence):
  sentence=str(sentence)
  sentence = sentence.lower()
  sentence=sentence.replace('{html}',"")
  cleanr = re.compile('<.*?>:')
  cleantext = re.sub(cleanr, '', sentence)
  rem_url=re.sub(r'http\S+', '',cleantext)
  rem_num = re.sub('[0-9]+', '', rem_url)
  tokenizer = RegexpTokenizer(r'\w+')
  tokens = tokenizer.tokenize(rem_num)
  filtered_words = [w for w in tokens if len(w) > 2 if not w in stopwords.words('english') and "amp"]
  stem_words=[stemmer.stem(w) for w in filtered_words]
  lemma_words=[lemmatizer.lemmatize(w) for w in stem_words]
  return " ".join(lemma_words)
def predictfunc(txt):
    print(txt)
    #newfeatures = vectorizer.transform(txt['cleanText'])
    pipeline = joblib.load('model_pipeline.pkl')
    predictions = pipeline.predict(txt['cleanText'])
    return predictions

if __name__ == '__main__':
    app.run(debug=True)

