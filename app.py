from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)
model = joblib.load(open('model\\Student_mark_predictor_model.pkl','rb'))

def run_model(marks):
    global df
    input = [marks]
    feature_input = np.array(input)
    ans = -1.00
    
    if(input[0] >=0 and input[0]<=24):
        ans = model.predict([feature_input])[0][0].round(2)
    if(ans>100):
        ans = 100
    
    print("Model prediction is : ",ans)
    return ans

@app.route('/access_model/<int:marks>', methods = ['GET', 'POST'])
def access_model(marks):
    dir = {"predicted_marks":-1}
    
    if request.method == "GET":
        if(marks>=0 and marks<=24):
            dir = {"predicted_marks":run_model(marks)}
    return jsonify(dir)


@app.route('/predict', methods = ['POST'])
def predict():
    dir = {"predicted_marks":str(-1)}
    try:
        hrs = request.form.get('hours')
        hrs = float(hrs)
        if(hrs>=0 and hrs<=24):
            dir = {"predicted_marks":str(run_model(hrs))}
    except:
        pass
    return jsonify(dir)

@app.route('/', methods = ['GET', 'POST'])
def main_page():
    percentage_marks = "Null"
    if request.method == 'POST':
        try:
            input = request.form['marks']
            input = float(input)
            if(input >=0 and input<=24):
                percentage_marks = "Percentage Marks : "+str(run_model(input))+"%"
            else:
                percentage_marks = "Enter hour between 0 to 24"
        except :
            percentage_marks = "Please Fill all values Properly"
    return render_template('index.html', percentage_marks = percentage_marks)



if __name__ == "__main__":
    app.run(debug=True)