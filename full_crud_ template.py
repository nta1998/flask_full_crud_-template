from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
CORS(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/add', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created!'})

@app.route('/', methods=['GET'])
def read_user():
    user = User.query.all()
    return jsonify(user)

@app.route('/upd/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    user.name = data['name']
    user.email = data['email']
    db.session.commit()
    return jsonify({'message': 'user updated!'})

@app.route('/del/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'user deleted!'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
