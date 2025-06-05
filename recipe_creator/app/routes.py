from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from app.models import Users, Recipe
from app import app

bcrypt = Bcrypt(app)

@app.route('/', defaults={'path': '/login'})
@app.route('/<path:path>')
def login(path):
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/insert_user', methods=['POST'])
def insert_user():
    if not Users.validate_user(request.form):
        return redirect('/register')

    pw_hash = bcrypt.generate_password_hash(request.form['pword'])

    data = {
        "last_name": request.form['lname'],
        "first_name": request.form['fname'],
        "email": request.form['email'],
        "username": request.form['usr'],
        "password": pw_hash
    }

    Users.add_user(data)
    flash("Successfully registered!")
    return redirect('/login')


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    if 'usr' not in session:
        return redirect('/login')

    current_user = Users.get_by_username(session['usr'])
    if not current_user:
        flash("User not found.")
        return redirect('/login')

    data = {
        "name": request.form['recipe_name'],
        "ingredient": request.form['ingredient'],
        "cooking_tools": request.form['cooking_tools_needed'],
        "procedure": request.form['procedure'],
        "user_id": current_user.id
    }

    Recipe.add_recipe(data)
    flash("Successfully added recipe!")
    return redirect('/dashboard')

@app.route('/login_user', methods=['POST'])
def login_user():
    data = {
        "username": request.form['usr'],
        "password": request.form['pword']
    }

    user = Users.retrieve_user(data)
    if not user or not bcrypt.check_password_hash(user.password, request.form['pword']):
        flash("Invalid Username/Password")
        return redirect('/login')

    session['usr'] = user.username
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect('/login')


@app.route('/dashboard')
def dashboard():
    if 'usr' not in session:
        return redirect('/login')

    current_user = Users.get_by_username(session['usr'])
    if not current_user:
        flash("User not found.")
        return redirect('/login') 

    recipe_list = Recipe.recipe_records(current_user.id)

    return render_template('dashboard.html', recipe_records=recipe_list, current_user_id=current_user.id)

@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html')


@app.route('/view_recipe/<id>')
def view_recipe(id):
    if 'usr' not in session:
        return redirect('/login')
    data = {
        "id": id,
    }
    recipe = Recipe.get_by_id(data)
    return render_template('view_recipe.html', recipe=recipe)

@app.route('/delete_recipe/<id>')
def delete_recipe(id):
    data = {
        "id":id
    }
    Recipe.recipe_delete(data)
    flash("Successfully deleted recipe!")
    return redirect('/dashboard')

@app.route('/update_recipe/<id>')
def update_recipe(id):
    if 'usr' not in session:
        return redirect('/login')
    data = {
        "id": id,
    }
    recipe = Recipe.get_by_id(data)
    return render_template('update_recipe.html', recipe=recipe)

@app.route('/update_recipe_post/<id>', methods=['POST'])
def update_recipe_post(id):
    data = {
        "id": id,
        "name": request.form['recipe_name_update'],
        "ingredient": request.form['ingredient_update'],
        "cooking_tools": request.form['cooking_tools_needed_update'],
        "procedure": request.form['procedure_update']
    }
    Recipe.recipe_update(data)
    flash("Successfully updated recipe!")
    return redirect('/dashboard')


@app.route('/user_profile/<id>')
def user_profile(id):
    if 'usr' not in session:
        return redirect('/login')
    data = {
        "id": id,
    }
    current_user = Users.get_by_username(session['usr'])
    if not current_user:
        flash("User not found.")
        return redirect('/login')
    
    return render_template('user_profile.html', user=current_user)


@app.route('/user_profile_update/<id>', methods=['POST'])
def user_profile_update(id):
    if 'usr' not in session:
        return redirect('/login')

    current_user = Users.get_by_username(session['usr'])
    if not current_user:
        flash("User not found.")
        return redirect('/login')

    data = {
        "id": id,
        "last_name": request.form['lname_update'],
        "first_name": request.form['fname_update'],
        "email": request.form['email_update'],
        "username": request.form['usr_update'],        
    }

    Users.user_profile_update(data)
    flash("Successfully updated profile!")
    return redirect('/dashboard')