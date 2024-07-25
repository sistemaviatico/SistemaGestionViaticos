import os
from flask import Flask, session, render_template, redirect, render_template, request
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.method == 'POST':
            usuario = request.form.get('usuario')
            clave = request.form.get('clave')

            print(usuario)
            print(clave)
            if usuario == None or clave == None:
                return render_template("error.html", error="Nombre de usuario o contraseña incorrectos, revise su información")
            
            #seleccionar usuario de la bd tabla usuarios
            seleccionar_usuario = text('''SELECT *, p."perfil" FROM public."usuarios" as u INNER JOIN public.perfiles as p ON 
                                       u."perfilid" = p."perfilid" WHERE "nombreusuario"=:usuario AND "clave"=:clave''')
            usuario_seleccionado = db.execute(seleccionar_usuario,{'usuario': usuario,'clave':clave}).fetchone()

            if(usuario_seleccionado):
                if (clave == usuario_seleccionado[2] and usuario == usuario_seleccionado[1]):
                    session["usuario_id"] = usuario_seleccionado[0]
                    session["usuario"] = usuario_seleccionado[1]
                    session["perfil"] = usuario_seleccionado[5]
                    print(session["perfil"])
                    return render_template("layout.html")
            else:
                error = "Nombre de usuario o contraseña incorrecta, favor verifique sus datos" 
                return render_template("error.html", error=error) 
            
                
        return render_template("login.html")     
            
@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    return render_template("inicio.html")

@app.route("/gestionperfiles", methods=["GET", "POST"])
def gestionarPerfiles():
    if request.method == "GET":
        #MOSTRAR PERFILES EN SELECT DEL FORM
        perfiles_query = text('''SELECT * FROM public.perfiles''')
        perfiles_info = db.execute(perfiles_query).fetchall()
        
        return render_template("gestionPerfiles.html", perfiles=perfiles_info)
    

        

@app.route("/registrarviatico", methods=["GET", "POST"])
def registrarViatico():
    return render_template("registrarViatico.html")