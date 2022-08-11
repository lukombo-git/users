from flask import Blueprint, jsonify, request
from flask.helpers import make_response
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_login import login_user,current_user,logout_user

user_blueprint=Blueprint('user_api_routes',__name__,url_prefix='/api/user')

#creating an user
@user_blueprint.route('/create', methods=['POST'])
def create_user():
    try:
        user = User()
        user.username = request.form["username"]
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.address = request.form["address"]
        user.city = request.form["city"]
        user.country = request.form["country"]
        user.post_code = request.form["post_code"]
        #user.password = generate_password_hash(request.form["password"],method=['sha256'])
        user.password = generate_password_hash(request.form["password"])
        db.session.commit()
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        response ={'mensagem':'Usuário criado com sucesso!','result':user.serialize()}
    except Exception as e:
        print(str(e))
        response = {'mensagem':'Erro ao criar o usuário'}
    return jsonify(response)

#updating user
@user_blueprint.route('/update/<id_user>', methods=['PUT'])
def update_user(id_user):
    try:
        user = User.query.get(id_user)
        user.username = request.form["username"]
        user.first_name = request.form["first_name"]
        user.last_name = request.form["last_name"]
        user.address = request.form["address"]
        user.city = request.form["city"]
        user.country = request.form["country"]
        user.post_code = request.form["post_code"]
        user.password = generate_password_hash(request.form["password"])

        db.session.commit()
        db.session.add(user)
        db.session.commit()

        response ={'message':'Usuario atualizado com sucesso!','result':user.serialize()}
    except Exception as e:
        print(str(e))
        response = {'mensagem':'Erro ao enviar a resposta.'}
    return jsonify(response)


#deleting user
@user_blueprint.route('/delete/<id_user>', methods=['DELETE'])
def user_delete(id_user):
    try:
        user = User.query.get(id_user)
        db.session.delete(user)
        db.session.commit()
        response ={'mensagem':'Usuario eliminado com sucesso!','result':user.serialize()}
    except Exception as e:
        print(str(e))
        response = {'mensagem':'Usuario não existe.'}
    return jsonify(response)



@user_blueprint.route('/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        response = {'message':'Usuário não existe.'}
        return make_response(jsonify(response), 401)
    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        login_user(user)
        response = {'mensagem':' Usuário Logado ','api_key':user.api_key}
        return make_response(jsonify(response), 200)
    response = {'message': 'Access denied'}
    return make_response(jsonify(response), 401)

#logging out
@user_blueprint.route('/logout',methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message':'Usuário Deslogado'})
    return jsonify({'mensagem':'Nenhum usuário logado'}), 401

#checking if user exists
@user_blueprint.route('/<username>/exists', methods=['GET'])
def user_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"result":True}), 200
    return jsonify({"result":False}), 404


#getting all users
@user_blueprint.route('/all', methods=['GET'])
def get_all_users():
    all_user = User.query.all()
    result = [user.serialize() for user in all_user]
    response = {'message':'Retornando todos os usuários','result': result}
    return jsonify(response)

#getting current user
@user_blueprint.route('/', methods=['GET'])
def get_current_user():
    #if current_user.is_authicated:
    if current_user:
        return jsonify({'result':current_user.serialize()}),200
    else:
        return jsonify({'mensagem':'Usário não logado'}), 200

#counting all users
@user_blueprint.route('/count_users', methods=['GET'])
def count_users():
    total_users = User.query.count()
    response = {'mensagem':'Retornando todos Usuários','result': total_users}
    return jsonify(response)

#get an user by id
@user_blueprint.route('/<int:id>', methods=['GET'])
def users_id(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({"result":user.serialize()}), 200
    return jsonify({"result":"Usuário não existe."}), 404