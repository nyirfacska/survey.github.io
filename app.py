from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired

import csv
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key'  # Titkos kulcs a Flask-WTF-hez

# CSV fájl neve
csv_filename = "survey_responses.csv"

# Biztosítja, hogy a CSV fájl létezik
if not os.path.exists(csv_filename):
    with open(csv_filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Question1", "Question2", "Question3", "TextAnswer"])

# Űrlap osztály definiálása a FlaskForm-ból származtatva
class SurveyForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    question1 = SelectMultipleField('Question 1: What is your favorite color?', choices=[('red', 'Red'), ('green', 'Green'), ('blue', 'Blue')], validators=[InputRequired()])
    question2 = SelectMultipleField('Question 2: What is your favorite animal?', choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird')], validators=[InputRequired()])
    question3 = SelectMultipleField('Question 3: What is your favorite season?', choices=[('spring', 'Spring'), ('summer', 'Summer'), ('fall', 'Fall'), ('winter', 'Winter')], validators=[InputRequired()])
    text_answer = StringField('Additional Comments:')
    submit = SubmitField('Submit')

# FlaskForm osztály használata az űrlap létrehozásához
@app.route("/", methods=["GET", "POST"])
def index():
    form = SurveyForm()

    if form.validate_on_submit():
        # A form adatainak elérése
        name = form.name.data
        question1 = ', '.join(form.question1.data)
        question2 = ', '.join(form.question2.data)
        question3 = ', '.join(form.question3.data)
        text_answer = form.text_answer.data

        # Adatok hozzáadása a CSV fájlhoz
        with open(csv_filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, question1, question2, question3, text_answer])

        return redirect(url_for("index"))

    return render_template("index.html", form=form)

# Az eredmények megjelenítése egy másik oldalon
@app.route("/results")
def results():
    with open(csv_filename, newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    return render_template("results.html", rows=rows[1:])

# Letöltési funkció
@app.route("/download")
def download():
    return send_from_directory(os.getcwd(), csv_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
