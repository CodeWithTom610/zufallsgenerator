from flask import Blueprint, render_template, url_for, request, redirect, jsonify
from .models import db, User
import random

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def zufallsgenerator():
    return render_template("index.html")

@main.route('/result')
def result():
    # Nur User ohne Berufsschule berücksichtigen
    users = User.query.filter_by(nicht_da=False).all()
    names = [u.name for u in users if not u.nicht_da]
    exclnames = []  # Optional: ExcludedNames-Logik, falls benötigt

    chosen_names = []
    def chooseName():
        if len(chosen_names) + len(exclnames) >= len(names):
            return
        choise = random.choice(names)
        if (choise not in chosen_names) and (choise not in exclnames):  
            chosen_names.append(choise)
        else:
            chooseName()

    for i in range(0, 6):
        chooseName()
    return render_template('result.html', names=chosen_names)

@main.route('/create_user', methods=['POST'])
def create_user():
    name = request.form.get('name')
    beruf = request.form.get('beruf')
    lehrjahr = request.form.get('lehrjahr')
    if name and beruf and lehrjahr:
        new_user = User(name=name, Beruf=beruf, lehrjahr=int(lehrjahr), nicht_da=False)
        db.session.add(new_user)
        db.session.commit()
    return redirect(url_for('main.admin'))

@main.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("main.admin"))

@main.route('/admin')
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)

@main.route('/toggle_berufsschule/<int:id>', methods=['POST'])
def toggle_berufsschule(id):
    user = User.query.get_or_404(id)
    user.berufsschule = not user.berufsschule
    db.session.commit()
    return redirect(url_for('main.admin'))

@main.route('/toggle_berufsschule_ajax', methods=['POST'])
def toggle_berufsschule_ajax():
    lehrjahr = request.json.get('lehrjahr')
    users = User.query.filter_by(lehrjahr=lehrjahr).all()
    if users:
        # Toggle: Wenn mindestens einer auf True steht, alles auf False, sonst alles auf True
        new_status = not any(u.berufsschule for u in users)
        for user in users:
            user.berufsschule = new_status
        db.session.commit()
        return jsonify({'success': True, 'berufsschule': new_status})
    return jsonify({'success': False}), 400

@main.route('/get_names_by_beruf')
def get_names_by_beruf():
    beruf = request.args.get('beruf')
    users = User.query.filter_by(Beruf=beruf).all()
    return jsonify({'namen': [
        {'id': u.id, 'name': u.name, 'nicht_da': u.nicht_da} for u in users
    ]})

@main.route('/get_names_by_lehrjahr')
def get_names_by_lehrjahr():
    lehrjahr = request.args.get('lehrjahr', type=int)
    users = User.query.filter_by(lehrjahr=lehrjahr).all()
    return jsonify({'namen': [
        {'id': u.id, 'name': u.name, 'nicht_da': u.nicht_da} for u in users
    ]})

@main.route('/heraufstufen', methods=['POST'])
def heraufstufen():
    user_id = request.json.get('id')
    user = User.query.get(user_id)
    if user and user.lehrjahr < 4:
        user.lehrjahr += 1
        db.session.commit()
        return jsonify({'success': True})
    elif user and user.lehrjahr == 4:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False}), 400

@main.route('/nicht_da', methods=['POST'])
def nicht_da():
    user_id = request.json.get('id')
    checked = request.json.get('checked')
    user = User.query.get(user_id)
    if user:
        user.nicht_da = checked
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@main.route('/entfernen', methods=['POST'])
def entfernen():
    user_id = request.json.get('id')
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@main.route('/set_lehrjahr_nicht_da', methods=['POST'])
def set_lehrjahr_nicht_da():
    lehrjahr = request.json.get('lehrjahr')
    checked = request.json.get('checked')
    users = User.query.filter_by(lehrjahr=lehrjahr).all()
    if users:
        for user in users:
            user.nicht_da = checked
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@main.route('/get_names_by_beruf_lehrjahr')
def get_names_by_beruf_lehrjahr():
    beruf = request.args.get('beruf')
    lehrjahr = request.args.get('lehrjahr', type=int)
    users = User.query.filter_by(Beruf=beruf, lehrjahr=lehrjahr).all()
    return jsonify({'namen': [
        {'id': u.id, 'name': u.name, 'nicht_da': u.nicht_da} for u in users
    ]})

