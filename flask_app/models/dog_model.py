# this is the page where we create our instance of a dog and all the class methods.

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import award_model
from flask import flash
import re

ALPHANUMERIC = re.compile(r"^[a-zA-Z0-9]+$")

# creates the class of dog

class Dog:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.breed = data['breed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# this is a class method which populates all instances of the dog class via SQL

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dogs;"
        results = connectToMySQL(DATABASE).query_db(query)
        all_dogs = []
        for one_row in results:
            this_dog_instance = cls(one_row)
            all_dogs.append(this_dog_instance)
        return all_dogs

# this is a classmethod which searches based upon id, pulls [0] which is the first and only result, 
# and returns the results.

    @classmethod
    def get_one(cls,data):
        query = """
            SELECT * FROM dogs LEFT JOIN awards ON dogs.id = awards.dog_id 
            WHERE dogs.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            dog_instance = cls(results[0])
            awards_list = []
            for row_in_db in results:
                if row_in_db['awards.id'] == None:
                    return dog_instance
                award_data = {
                    'id' : row_in_db['awards.id'],
                    'title' : row_in_db['title'],
                    'dog_id' : row_in_db['dog_id'],
                    'created_at' : row_in_db['awards.created_at'],
                    'updated_at' : row_in_db['awards.updated_at']
                }
                award_instance = award_model.Award(award_data)
                awards_list.append(award_instance)
            dog_instance.awards = awards_list
            return dog_instance

        return False

# This method creates a new dog by inserting the info into the database. 
# This function is called in the server.

    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO dogs (name,age,breed)
            VALUES (%(name)s,%(age)s,%(breed)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# This is a function which updates thedogs name, age, and breed in the SQL database when suppied with an ID.

    @classmethod
    def update(cls,data):
        query = """
            UPDATE dogs SET name = %(name)s, age = %(age)s, breed = %(breed)s
            WHERE dogs.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

# This method deletes the dog from SQL database.


    @classmethod
    def delete(cls,data):
        query = """
            DELETE FROM dogs where dogs.id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    
    @staticmethod
    def validator(potential_dog):
        is_valid = True
        if len(potential_dog['name']) < 1:
            is_valid = False
            flash("Name required")
        elif not ALPHANUMERIC.match(potential_dog['name']):
            is_valid = False
            flash("Name cannot contain special characters")
        if len(potential_dog['breed']) < 1:
            is_valid = False
            flash("Breed required")
        if len(potential_dog['age']) < 1:
            is_valid = False
            flash("Age required")
        elif int(potential_dog['age']) < 0:
            is_valid = False      
            flash("Age should be positive")      
        if "cool" not in potential_dog:
            is_valid = False
            flash("I think you meant to say that dog is cool")    
        return is_valid