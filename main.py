from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    items = {
        'name': random_cafe.name,
        'map_url': random_cafe.map_url,
        'img_url': random_cafe.img_url,
        'location': random_cafe.location,
        'seats': random_cafe.seats,
        'coffee_price': random_cafe.coffee_price,
        'amenities':{
            'has_sockets': random_cafe.has_sockets,
            'has_toilet': random_cafe.has_toilet,
            'has_wifi': random_cafe.has_wifi,
            'can_take_calls': random_cafe.can_take_calls,
        }
    }
    return jsonify(cafe=items)


@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    cafe_info_list = []
    for cafe in all_cafes:
        item = {
            'name': cafe.name,
            'map_url': cafe.map_url,
            'img_url': cafe.img_url,
            'location': cafe.location,
            'seats': cafe.seats,
            'coffee_price': cafe.coffee_price,
            'amenities': {
                'has_sockets': cafe.has_sockets,
                'has_toilet': cafe.has_toilet,
                'has_wifi': cafe.has_wifi,
                'can_take_calls': cafe.can_take_calls,
            }
        }
        cafe_info_list.append(item)
    return jsonify(cafes=cafe_info_list)


@app.route("/search")
def search():
    location = request.args.get('loc').capitalize()
    all_cafes = list(Cafe.query.filter_by(location=location))
    if len(all_cafes) > 0:
        cafe_info_list = []
        for cafe in all_cafes:
            item = {
                'name': cafe.name,
                'map_url': cafe.map_url,
                'img_url': cafe.img_url,
                'location': cafe.location,
                'seats': cafe.seats,
                'coffee_price': cafe.coffee_price,
                'amenities': {
                    'has_sockets': cafe.has_sockets,
                    'has_toilet': cafe.has_toilet,
                    'has_wifi': cafe.has_wifi,
                    'can_take_calls': cafe.can_take_calls,
                }
            }
            cafe_info_list.append(item)
        return jsonify(cafes=cafe_info_list)
    else:
        item = {
            "Not Found": "Sorry, we do not have a cafe at that location."
        }
        return jsonify(error=item)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        cafe_to_add = Cafe(
            name=request.form['name'],
            map_url=request.form['map_url'],
            img_url=request.form['img_url'],
            location=request.form['location'],
            seats=request.form['seats'],
            has_toilet=bool(request.form['has_toilet']),
            has_wifi=bool(request.form['has_wifi']),
            has_sockets=bool(request.form['has_sockets']),
            can_take_calls=bool(request.form['can_take_calls']),
            coffee_price=request.form['coffee_price']
        )
        db.session.add(cafe_to_add)
        db.session.commit()
        return jsonify(response={
            "success": "Successfully added the new cafe"
        })
    return jsonify(response={
        "error": "Request was not completed"
    })


@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = request.args.get('new_price')
        db.session.commit()
        return jsonify(response={
            "success": "Successfully updated the price"
        }), 200
    else:
        return jsonify(response={
            "Not found": "Sorry a cafe with the id you inputed was not found in the database"
        }), 404


@app.route('/delete/<int:cafe_id>', methods=['DELETE'])
def delete(cafe_id):
    if request.args.get('api_key') == 'AndrewsKey':
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={
                "success": "Cafe successfully deleted"
            }), 200
        else:
            return jsonify(response={
                "error": "The cafe you were looking for was not found"
            }), 404

    else:
        return jsonify(response={
            "error": "Sorry that is not allowed make sure you have a valid api key."
        }), 403


if __name__ == '__main__':
    app.run(debug=True)
