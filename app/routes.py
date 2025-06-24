from flask import Blueprint, render_template, url_for, request, redirect
from flask_bcrypt import bcrypt
from bcrypt import hashpw, checkpw
from .models import *



main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def zufallsgenerator():

    return render_template("index.html")

@main.route('/result')
def result():
    return render_template('result.html')

@main.route('/create_user', methods=['POST'])
def create_user():
    # Add user creation logic here
    # name = request.form['name']
    # lehrjahr = int(request.form['lehrjahr'])
    # Save to DB or data structure
    return redirect(url_for('main.admin'))

@main.route('/delete_user/<int:id>/<int:lehrjahr>', methods=['POST'])
def delete_user(id, lehrjahr):
    if lehrjahr == 1:
        user = Lehrjahr1.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("main.admin"))
    elif lehrjahr == 2:
        user = Lehrjahr2.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("main.admin"))
    elif lehrjahr == 3:
        user = Lehrjahr3.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("main.admin"))
    elif lehrjahr == 4:
        user = Lehrjahr4.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("main.admin"))
    else:
        pass
    return redirect(url_for('main.admin'))

@main.route('/admin')
def admin():
    users_lj_1 = Lehrjahr1.query.all()
    users_lj_2 = Lehrjahr2.query.all()
    users_lj_3 = Lehrjahr3.query.all()
    users_lj_4 = Lehrjahr4.query.all()
    return render_template('admin.html', lj1 = users_lj_1, lj2=users_lj_2, lj3=users_lj_3, lj4=users_lj_4)
