from flask import Blueprint, render_template, url_for, request, redirect
from .models import *
import random


main = Blueprint("main", __name__)

names = []
chosen_names = []
exclnames = []


@main.route("/", methods=["GET", "POST"])
def zufallsgenerator():

    return render_template("index.html")

@main.route('/result')
def result():
    names = []
    chosen_names = []

    # Nur Lehrjahre ohne Berufsschule berücksichtigen
    x = Lehrjahr1.query.filter_by(berufsschule=False).all()
    y = Lehrjahr2.query.filter_by(berufsschule=False).all()
    z = Lehrjahr3.query.filter_by(berufsschule=False).all()
    a = Lehrjahr4.query.filter_by(berufsschule=False).all()

    # Alle Namen sammeln
    for i in x:
        names.append(i.name)
    for i in y:
        names.append(i.name)
    for i in z:
        names.append(i.name)
    for i in a:
        names.append(i.name)

    # Excludierte Namen als Liste von Strings
    exclnames = [i.name for i in ExcludedNames.query.all()]

    def chooseName():
        choise = random.choice(names)
        if (choise not in chosen_names) and (choise not in exclnames):  
            chosen_names.append(choise)
            return
        else:
            # Rekursion nur, wenn noch Auswahl möglich ist
            if len(chosen_names) + len(exclnames) < len(names):
                chooseName()

    for i in range(0, 6):
        chooseName()
    print(chosen_names)
    return render_template('result.html', names=chosen_names)

@main.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        lehrjahr = request.form.get('lehrjahr')
        print(name, lehrjahr)
        beruf = request.form.get('Beruf')

        if name and lehrjahr:
            if lehrjahr == '1':
                new_user = Lehrjahr1(name=name, beruf=beruf)
            elif lehrjahr ==  '2':
                new_user = Lehrjahr2(name=name, beruf=beruf)
            elif lehrjahr == '3':
                new_user = Lehrjahr3(name=name, beruf=beruf)
            elif lehrjahr == '4':
                new_user = Lehrjahr4(name=name, beruf=beruf)
            else:
                return redirect(url_for('main.admin'))

            db.session.add(new_user)
            db.session.commit()
        else:
            return redirect(url_for('main.admin'))
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

@main.route('/excluded_names', methods=['GET', 'POST'])
def excluded_names():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            new_excluded = ExcludedNames(name=name)
            db.session.add(new_excluded)
            db.session.commit()
        return redirect(url_for('main.excluded_names'))

    excluded = ExcludedNames.query.all()
    return render_template('excluded_names.html', excluded=excluded)

@main.route('/delete_excluded/<int:id>', methods=['POST'])
def delete_excluded(id):
    ex = ExcludedNames.query.get_or_404(id)
    db.session.delete(ex)
    db.session.commit()
    return redirect(url_for('main.excluded_names'))

@main.route('/toggle_berufsschule/<int:lehrjahr>', methods=['POST'])
def toggle_berufsschule(lehrjahr):
    model_map = {1: Lehrjahr1, 2: Lehrjahr2, 3: Lehrjahr3, 4: Lehrjahr4}
    model = model_map.get(lehrjahr)
    if model:
        # Toggle für alle Einträge des Lehrjahrs
        current = model.query.first()
        if current:
            new_state = not current.berufsschule
            for user in model.query.all():
                user.berufsschule = new_state
            db.session.commit()
    return redirect(url_for('main.admin'))

