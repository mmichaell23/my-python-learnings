from app.mysqlconnection import MySQLConnection
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Users:
    def __init__(self, data):
        self.id = data['id']
        self.lastname = data['last_name']
        self.firstname = data['first_name']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']

    @classmethod
    def add_user(cls, data):
        query = """
            INSERT INTO user_auth (last_name, first_name, email, username, password)
            VALUES (%(last_name)s, %(first_name)s, %(email)s, %(username)s, %(password)s);
        """
        return MySQLConnection('recipe_creator').query_db(query, data)

    @classmethod
    def retrieve_user(cls, data):
        query = "SELECT * FROM user_auth WHERE username = %(username)s;"
        results = MySQLConnection('recipe_creator').query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def get_by_username(cls, username):
        query = "SELECT * FROM user_auth WHERE username = %(username)s;"
        results = MySQLConnection('recipe_creator').query_db(query, {"username": username})
        return cls(results[0]) if results else None

    @classmethod
    def user_profile_update(cls, data):
        query = """
            UPDATE user_auth
            SET last_name = %(last_name)s, first_name = %(first_name)s, email = %(email)s, username = %(username)s
            WHERE id = %(id)s;
        """
        return MySQLConnection('recipe_creator').query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['usr']) <= 7:
            flash("Username must be at least 8 characters long!")
            is_valid = False
        if len(user['pword']) <= 7:
            flash("Password must be at least 8 characters long!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if user['pword'] != user['cpword']:
            flash("Passwords do not match!")
            is_valid = False
        return is_valid

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.ingredient = data['ingredient']
        self.cooking_tools = data['cooking_tools']
        self.procedure = data['procedure']

    @classmethod
    def add_recipe(cls, data):
        query = """
            INSERT INTO recipe (name, ingredient, cooking_tools, `procedure`, user_id)
            VALUES (%(name)s, %(ingredient)s, %(cooking_tools)s, %(procedure)s, %(user_id)s);
        """
        return MySQLConnection('recipe_creator').query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipe WHERE id = %(id)s;"
        results = MySQLConnection('recipe_creator').query_db(query, data)
        return cls(results[0]) if results else None

    @classmethod
    def recipe_records(cls, user_id):
        query = "SELECT * FROM recipe WHERE user_id = %(user_id)s;"
        results = MySQLConnection('recipe_creator').query_db(query, {"user_id": user_id})
        return [cls(recipe) for recipe in results] if results else []

    @classmethod
    def recipe_delete(cls, data):
           query = "DELETE FROM recipe WHERE id = %(id)s;"
           return MySQLConnection('recipe_creator').query_db(query, data)

    @classmethod
    def recipe_update(cls, data):
         query = "UPDATE recipe SET name = %(name)s, ingredient = %(ingredient)s, cooking_tools = %(cooking_tools)s, `procedure` = %(procedure)s  WHERE id = %(id)s;"
         return MySQLConnection('recipe_creator').query_db(query, data)