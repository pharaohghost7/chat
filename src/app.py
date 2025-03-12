from flask import Flask, render_template,request,redirect,url_for,flash,session
from config import config
from sqlalchemy import create_engine
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect

from sqlagent import human_query
import asyncio
from database import update_tokens

# Models
from models.ModelUser import ModelUser

# Entities
from models.entities.User import User


app = Flask(__name__)
csrf = CSRFProtect()

db = create_engine(config['development'].SQLALCHEMY_DATABASE_URI1)

login_manager = LoginManager(app=app)

@login_manager.user_loader
def load_user(user_id):
    return ModelUser.get_user_by_id(user_id, db)


@app.route('/')
def index():
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['email'])
        # print(request.form['password'])
        user = User(0, '', request.form['password'], request.form['email'], 0, 0,0)
        
        logged_user = ModelUser.login(user, db)
        if logged_user != None:
            if logged_user.password != None:
                
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash('Password incorrect')
                return render_template('auth/login.html')
        else:
            flash('User not found')
            return render_template('auth/login.html')

       
    else:
        return render_template('auth/login.html')
    
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.pop("conversation", None)
    return redirect(url_for('login'))

    
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if "conversation" not in session:
        session["conversation"] = ""
    if request.method == 'POST':
        user_input = request.form['user_input']

        if user_input:
            try:
                response, promt_tokens_sql, response_tokens_sql, promt_tokens_answer, response_tokens_answer = asyncio.run(human_query(user_input))
                total_tokens = promt_tokens_sql + response_tokens_sql + promt_tokens_answer + response_tokens_answer
                costo_tokens = ((promt_tokens_answer + promt_tokens_sql)*0.00005 + (response_tokens_answer + response_tokens_sql)*0.00015)*1.2
                tokens = current_user.tokens + total_tokens
                costtokens = current_user.costtokens + costo_tokens
                update_tokens(tokens,costtokens, current_user.id)

                if response:
                    session["conversation"] += f"User: {user_input}\nDisruptBot: {response}\n"
                else:
                    response = "No se encontró respuesta"
                    session["conversation"] += f"User: {user_input}\nDisruptBot: {response}\n"
            except Exception as e:
                response = "No se encontró respuesta" + str(e)
                session["conversation"] += f"User: {user_input}\nDisruptBot: {response}\n"
        return render_template('home.html', conversation=session["conversation"])
    else:
        response = f"Hola {current_user.username} , soy DisruptBot, en que puedo ayudarte?"
        session["conversation"] += f"DisruptBot: {response}\n"
        return render_template('home.html', conversation=session["conversation"])
                

    




def status_401(error):
    
    return render_template('auth/login.html')

def status_404(error):
   
    return render_template('auth/login.html')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(host='0.0.0.0', port=5000, debug=True)