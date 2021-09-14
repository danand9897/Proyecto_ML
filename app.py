from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
import pickle
import keras.backend.tensorflow_backend as tb



app = Flask(__name__)
tb._SYMBOLIC_SCOPE.value = True

#Cargar Modelo               
mymodel = load_model('modelo.h5',compile=False)
myvectorizer = pickle.load(open("vectorizer_cnn.pkl", "rb"))
@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':                             
                  
        username_input = request.form["username"]
        #password_input = request.form.get('password')
        
        input_val = clean_data(username_input)
        input_val = [input_val]
        input_val=myvectorizer.transform(input_val).toarray()

        print(input_val)        
        result = mymodel.predict(input_val)

        if result > 0.75:
            print("ALERT!!!! SQL injection Detected")
        elif result <= 0.75:
            print("It is normal")

            

    return render_template('index.html')

def clean_data(input_val):

    input_val=input_val.replace('\n', '')
    input_val=input_val.replace('%20', ' ')
    input_val=input_val.replace('=', ' = ')
    input_val=input_val.replace('((', ' (( ')
    input_val=input_val.replace('))', ' )) ')
    input_val=input_val.replace('(', ' ( ')
    input_val=input_val.replace(')', ' ) ')
    input_val=input_val.replace('1 ', 'numeric')
    input_val=input_val.replace(' 1', 'numeric')
    input_val=input_val.replace("'1 ", "'numeric ")
    input_val=input_val.replace(" 1'", " numeric'")
    input_val=input_val.replace('1,', 'numeric,')
    input_val=input_val.replace(" 2 ", " numeric ")
    input_val=input_val.replace(' 3 ', ' numeric ')
    input_val=input_val.replace(' 3--', ' numeric--')
    input_val=input_val.replace(" 4 ", ' numeric ')
    input_val=input_val.replace(" 5 ", ' numeric ')
    input_val=input_val.replace(' 6 ', ' numeric ')
    input_val=input_val.replace(" 7 ", ' numeric ')
    input_val=input_val.replace(" 8 ", ' numeric ')
    input_val=input_val.replace('1234', ' numeric ')
    input_val=input_val.replace("22", ' numeric ')
    input_val=input_val.replace(" 8 ", ' numeric ')
    input_val=input_val.replace(" 200 ", ' numeric ')
    input_val=input_val.replace("23 ", ' numeric ')
    input_val=input_val.replace('"1', '"numeric')
    input_val=input_val.replace('1"', '"numeric')
    input_val=input_val.replace("7659", 'numeric')
    input_val=input_val.replace(" 37 ", ' numeric ')
    input_val=input_val.replace(" 45 ", ' numeric ')

    return input_val




if __name__ == '__main__':
    app.run(debug=True)    