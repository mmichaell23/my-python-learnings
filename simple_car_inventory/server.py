from flask import Flask, render_template, request, redirect
from car_inventory import Car

app = Flask(__name__)

@app.route('/index')
def home():
    # Retrieve all cars from the database
    all_cars = Car.get_all_cars()
    return render_template('index.html', cars=all_cars)


@app.route('/car', methods=['GET', 'POST'])
def car():
    if request.method == 'POST':
        data = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": int(request.form['year']),
            "description": request.form['description']
        }
        Car.create_car(data)
        return render_template('car.html', 
                               car_make=data['make'], 
                               car_model=data['model'],
                               car_year=data['year'],
                               car_description=data['description'])
    else:
        return redirect('/index')
    

@app.route('/cars')
def list_cars():
    all_cars = Car.get_all_cars()
    return render_template('list_cars.html', cars=all_cars)

@app.route('/edit/<int:id>', methods=['GET'])
def edit_car(id):
    all_cars = Car.get_all_cars()
    car = next((c for c in all_cars if c.id == id), None)
    return render_template('edit_car.html', car=car)

@app.route('/update_car/<int:id>', methods=['POST'])
def update_car(id):
    data = {
        "id": id,
        "make": request.form['make'],
        "model": request.form['model'],
        "year": int(request.form['year']),
        "description": request.form['description']
    }
    Car.update_car(data)
    return redirect('/cars')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_car(id):
    Car.delete_car(id)
    return redirect('/cars')


if __name__ == '__main__':
    app.run(debug=True)
