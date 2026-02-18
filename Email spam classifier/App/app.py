import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def transform_text(Message):
    Message = Message.lower()
    Message = nltk.word_tokenize(Message)

    y = []
    for i in Message:
        if i.isalnum():
            y.append(i)

    Message = y[:]
    y.clear()

    for i in Message:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    Message = y[:]
    y.clear()

    for i in Message:
        y.append(ps.stem(i))
    return  " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title("Email Spam Classifier")

input_mail = st.text_area("Enter the message")

if st.button("Predict"):

    transform_message = transform_text(input_mail)

    vector_input = tfidf.transform([transform_message])

    result = model.predict(vector_input)[0]

    if result == 1:
        st.header('Spam')

    else:
        st.header("Not Spam")

