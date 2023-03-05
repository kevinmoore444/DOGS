from flask import Flask, render_template, request, redirect
from flask_app.models.dog_model import Dog
from flask_app.models.award_model import Award
from flask_app import app

@app.route('/awards/new')
def new_award_form():
    all_dogs = Dog.get_all()
    return render_template("awards_new.html", all_dogs=all_dogs)

@app.route('/awards/create', methods=['POST'])
def create_award():
    Award.create(request.form)
    return redirect(f'/dogs/{request.form["dog_id"]}/view')

@app.route('/awards')
def all_awards():
    all_awards = Award.get_all()
    return render_template("awards_all.html", all_awards=all_awards)


@app.route('/awards/<int:id>/view')
def one_award(id):
    data = {
        'id':id
    }
    one_award = Award.get_one(data)
    return render_template("awards_one.html", one_award=one_award)