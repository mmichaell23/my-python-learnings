from mysqlconnection import connectToMySQL

class Car:
    def __init__(self, data):
        self.id = data['id']
        self.make = data['make']
        self.model = data['model']
        self.year = data['year']
        self.description = data['description']

    @classmethod
    def create_car(cls, data):
        query = "INSERT INTO car_inventory (make, model, year, description) VALUES (%(make)s, %(model)s, %(year)s, %(description)s);"
        return connectToMySQL('car_inventory').query_db(query, data)

    @classmethod
    def get_all_cars(cls):
        query = "SELECT * FROM car_inventory;"
        results = connectToMySQL('car_inventory').query_db(query)
        cars = []
        for car in results:
            cars.append(cls(car))
        return cars

    @classmethod
    def update_car(cls, data):
        query = """
            UPDATE car_inventory 
            SET make = %(make)s, model = %(model)s, year = %(year)s, description = %(description)s 
            WHERE id = %(id)s;
        """
        return connectToMySQL('car_inventory').query_db(query, data)

    @classmethod
    def delete_car(cls, id):
        query = "DELETE FROM car_inventory WHERE id = %(id)s;"
        data = {"id": id}
        return connectToMySQL('car_inventory').query_db(query, data)
