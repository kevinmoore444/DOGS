from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import dog_model

class Award:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dog_id = data['dog_id']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO awards (title, dog_id)
            VALUES (%(title)s,%(dog_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM awards JOIN dogs
            ON dogs.id = awards.dog_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_awards = []
        if results:
            for row in results:
                award_instance = cls(row)
                dog_data = {
                    **row,
                    "id" : row['dogs.id'],
                    "created_at" : row['dogs.created_at'],
                    "updated_at" : row['dogs.updated_at'],

                }
                dog_instance = dog_model.Dog(dog_data)
                award_instance.recipient = dog_instance
                all_awards.append(award_instance)
        return all_awards

    @classmethod
    def get_one(cls,data):
        query = """
            SELECT * FROM awards JOIN dogs
            ON dogs.id = awards.dog_id
            WHERE awards.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            award_instance = cls(results[0])
            row = results[0]
            dog_data = {
                    **row,
                    "id" : row['dogs.id'],
                    "created_at" : row['dogs.created_at'],
                    "updated_at" : row['dogs.updated_at'],

            }
            dog_instance = dog_model.Dog(dog_data)
            award_instance.recipient = dog_instance
            return award_instance
        return False