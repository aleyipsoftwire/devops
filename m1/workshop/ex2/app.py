from flask import Flask,render_template,request, redirect
from cli_app import append_film

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/films/list')
def get_films_list():
    films = ["Flubber", "Jumanji", "Aladdin", "Patch Adams", "Mrs Doubtfire"]
    return render_template('films_list.html', films=films)
    
@app.route('/films/table')
def get_films_table(): 
    stars_filter = request.values.get("stars", None)

    with open("films.csv", "r") as file:
        lines = file.readlines()
        films = [line.strip().split(",") for line in lines]
        if stars_filter != None:
            films = filter(lambda x: x[1] == stars_filter, films)

        return render_template('films_table.html', films=films)

@app.route('/films/submit', methods=['GET'])
def get_form():
    return render_template('films_submit.html')

@app.route('/films/submit', methods=['POST'])
def handle_submission():
    data = request.form
    film = data['film']
    stars = data['stars']

    append_film(film, stars)

    return redirect('/films/table')
