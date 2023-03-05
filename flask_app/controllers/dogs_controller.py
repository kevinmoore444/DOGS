from flask import Flask, render_template, request, redirect
from flask_app.models.dog_model import Dog
from flask_app import app


# Dog.get_all is invoking the function which pulls all dog info from SQL.We're pulling the info from SQL 
# and setting it equal to a variable called "all_dogs". Then we're rendering the index.html template
# and passing in the alldogs variable.

@app.route('/')
def index():
    all_dogs = Dog.get_all()
    return render_template("index.html", all_dogs=all_dogs)
            
# This route is for viewing one dog. The function plugs an id into the get_one class method,
#  stores that data in the one_dog variable, and passes that into the dogs_one.html page which requires that variable

@app.route('/dogs/<int:id>/view')
def get_one(id):
    data = {
        'id':id
    }
    one_dog = Dog.get_one(data)
    return render_template("dogs_one.html", one_dog = one_dog)

# This route sends the user to the new dog html page.

@app.route('/dogs/new')
def new_dog_form():
    return render_template("dogs_new.html")

# This is a post method which calls upon the create function defined in the dog_model, creates a new instance of 
# Dog via request.form and finally, redirects the user to the home page.

@app.route('/dogs/create', methods=['POST'])
def create_dog():
    if not Dog.validator(request.form):
        return redirect('/dogs/new')
    Dog.create(request.form)
    return redirect('/')

# clicking on the edit button sends the user to this route. The id is supplied. 
# The info for the dog which was clicked upon is obtained via the get_one function, then stored in the 
# this_dog variable. Then the user is redirected to the edit html page along with "thisdog", the data for the 
# dog being edited

@app.route("/dogs/<int:id>/edit")
def edit_dog(id):
    this_dog = Dog.get_one({'id':id}) 
    return render_template("dogs_edit.html", this_dog=this_dog)
    # Alternate method for passing in dictionary to the get_one route

# User directed here after submitting the dogs_edit form. This is a post method. Data stored in dictionary 
# based upon request form from the dogs_edit html. Invokes the update function listed in the dog_model and 
# passes along the data dictionary which we defined. Finally send the user back to home page.

@app.route('/dogs/<int:id>/update', methods=['POST'])
def update_dog(id):
    if not Dog.validator(request.form):
        return redirect(f"/dogs/{id}/edit")
    data = {
        'id': id,
        'name': request.form['name'],
        'age': request.form['age'],
        'breed': request.form['breed']
    }
    Dog.update(data)
    return redirect("/")

# User is directed here after clicking on it in the index.html. it invokes the delete dog function 
# which is definted in the dog model. 

@app.route('/dogs/<int:id>/delete')
def delete_dog(id):
    Dog.delete({'id':id})
    return redirect('/')