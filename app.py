import os
from flask import Flask, session, render_template, redirect, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime
import random

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if session.get("usuario") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if request.method == 'POST':
            usuario = request.form.get('usuario')
            clave = request.form.get('clave')
           
            print(usuario)
            if usuario == None or clave == None:
                return render_template("login.html", error="Nombre de usuario o contraseña incorrectos, revise su información")
            
            #seleccionar usuario de la bd tabla usuarios
            seleccionar_usuario = text('''SELECT *, p."perfil" FROM public."usuarios" as u INNER JOIN public.perfiles as p ON 
                                       u."perfilid" = p."perfilid" WHERE "nombreusuario"=:usuario ''')
            usuario_seleccionado = db.execute(seleccionar_usuario,{'usuario': usuario}).fetchone()

            if(usuario_seleccionado):
                if (check_password_hash(usuario_seleccionado[2], clave) and usuario == usuario_seleccionado[1]):
                    session["usuario_id"] = usuario_seleccionado[0]
                    session["usuario"] = usuario_seleccionado[1]
                    session["perfil"] = usuario_seleccionado[5]
                    print(session["perfil"])
                    return render_template("inicio.html")
            else:
                error = "Nombre de usuario o contraseña incorrecta, favor verifique sus datos*" 
                return render_template("login.html", error=error) 
            
                
        return render_template("login.html")     


@app.route("/inicio", methods=["GET", "POST"])
@login_required
def inicio():
    return render_template("inicio.html")

@app.route("/gestionperfiles", methods=["GET", "POST"])
@login_required
def gestionarPerfiles():
    if request.method == "GET":
        #MOSTRAR PERFILES EN TABLA PERFILES
        perfilid = request.form.get("id_perfil")

        perfiles_query = text('''SELECT * FROM public.perfiles''')
        perfiles_info = db.execute(perfiles_query, {}).fetchall()
        return render_template("gestionPerfiles.html",perfiles=perfiles_info)
        
        
    else:
        if request.method == 'POST':
            #AGREGAR PERFILES
            nombre_perfil = request.form.get("nombre-perfil").upper()
            print(nombre_perfil)

            

            consulta_existenciaPerfiles = text('''SELECT COUNT(*) FROM public."perfiles" WHERE "perfil" = :nombre_perfil''')
            resultadoPerfiles = db.execute(consulta_existenciaPerfiles,{"nombre_perfil": nombre_perfil}).scalar()

            if resultadoPerfiles > 0:
                return render_template("error.html", error="El perfil ya existe")
            else:
                agregar_perfil = text('''INSERT INTO public.perfiles ("perfil") VALUES (:nombre_perfil)''')
                db.execute(agregar_perfil,{"nombre_perfil": nombre_perfil})
                db.commit()




    return redirect("/gestionperfiles")

# @app.route("/editarPerfil", methods=["GET","POST"])
# def editarperfil():
#     #EDITAR PERFILES
#     id_perfil = request.form.get("id_perfil")
#     nuevo_nombrePerfil = request.form.get("nuevo_nombrePerfil")

#     if request.method == "POST":
        
#         actualizarPerfil_Query = text('''UPDATE public."perfiles" SET "perfil" = :nuevoPerfil WHERE "perfilid" = :id_perfil''')
#         db.execute(actualizarPerfil_Query,{"nuevoPerfil": nuevo_nombrePerfil, "id_perfil":id_perfil})
#         db.commit()

#     return redirect("/gestionperfiles")

@app.route("/registrarviatico", methods=["GET", "POST"])
@login_required
def registrarViatico():
     
    fecha_actual = datetime.now().strftime("%d-%m-%y")
    if request.method == "GET":
        cuentas_query = text('''SELECT * FROM public.tipos_viaticos''')
        cuentas_info = db.execute(cuentas_query, {}).fetchall()
        
        #Nombres en el select de busqueda
        nombres = text('SELECT * FROM public.datos_trabajadores')
        nombres_result = db.execute(nombres).fetchall()

        return render_template("registrarViatico.html", fechaActual = fecha_actual, tiposviaticos = cuentas_info , nombreTrabajador = nombres_result )
    else:
        monto_desayuno=float(request.form.get('montoDesayuno', 0.00)),
        monto_almuerzo=float(request.form.get('montoAlmuerzo', 0.00)),
        monto_cena=float(request.form.get('montoCena', 0.00)),
        monto_hospedaje=float(request.form.get('montoHospedaje', 0.00)),
        monto_leon=float(request.form.get('montoLeon', 0.00)),
        monto_managua=float(request.form.get('montoTransporteManagua', 0.00)),
        monto_otros=float(request.form.get('montoOtros', 0.00)),
        observaciones=request.form.get('Observaciones'),
        total_cordobas=float(request.form.get('montoCordobas', 0.00)),
        total_dolares=float(request.form.get('montoDolares', 0.00)),
        tipo_viatico_id=request.form.get('tipoViaticoid'),
        empleado_user_id=request.form.get('empleadoid'),
        numero_empleado=request.form.get('numeroEmpleado'),
        nombre_completo=request.form.get('nombreCompleto'),
        departamento=request.form.get('departamento'),
        area=request.form.get('area'),
        cecco=request.form.get('cecco'),
        numero_cedula=request.form.get('numeroCedula')

         # Verifica si la combinación ya existe en la base de datos
        # check_query = text('''SELECT COUNT(*) FROM public."registro_viaticos" as r INNER JOIN public."datos_trabajadores" as p
        #                    ON r."usuarioID" = p."usuarioID"
        #             WHERE "tipo_viatico_id" = :tipo_viatico_id ''')
        # result = db.execute(check_query, {"tipo_viatico_id": tipo_viatico_id})
        # count = result.scalar()
        #Insert
        insertar_viatico_query = text('''INSERT INTO public."registro_viaticos" ("fechadelviatico", "fechadeelaboracion","entregaencaja","tipoviaticoid"
                                      , "desayuno", "almuerzo", "cena", "transporteleon", "transportemanagua", hospedaje, "otros","observaciones","totalcordobas","numeroempleado" )
                                      VALUES ( :fechadelviatico,:fechadeelaboracion, :entregaencaja, :tipoviaticoid, :desayuno, :almuerzo, :cena, :trasnporteleon, :transportemanagua,
                                      :hospedaje, :otros, :observaciones, :totalcordobas, :numeroempleado) ''')
        
        db.execute(insertar_viatico_query,{"fechadelviatico": fecha_actual, "fechadeelaboracion": fecha_actual, "entregaencaja": fecha_actual, "tipoviaticoid":tipo_viatico_id, "desayuno":monto_desayuno,"almuerzo":monto_almuerzo,"cena":monto_cena,"trasnporteleon":monto_leon, "transportemanagua":monto_managua,"hospedaje":monto_hospedaje,"otros":monto_otros,"observaciones":observaciones,"totalcordobas":total_cordobas,"numeroempleado":empleado_user_id})
        db.commit()
        return redirect("/registrarviatico")
    return render_template("registrarViatico.html")

@app.route("/listadoviatico")
@login_required
def listadoviatico():
    if request.method == "GET":
        select_viaticoInfoQuery = text(''' SELECT r.* , v."tipoviatico", u."nombresapellidos" FROM public."registro_viaticos" as r
                                       INNER JOIN public."tipos_viaticos" as v ON r."tipoviaticoid" = v."tipoviaticoid" 
                                       INNER JOIN public."datos_trabajadores" as u ON r."numeroempleado" = u."usuarioid" ''')
        viatico_info = db.execute(select_viaticoInfoQuery).fetchall()
    return render_template("listadoViaticos.html", viaticoInfo = viatico_info)


@app.route("/gestioncuentas", methods = ["GET", "POST"])
@login_required
def gestionCuentas():
    if request.method == "GET":
        #MOSTRAR PERFILES EN TABLA PERFILES
        cuentaid = request.form.get("id_cuenta")

        cuentas_query = text('''SELECT * FROM public.tipos_viaticos''')
        cuentas_info = db.execute(cuentas_query, {}).fetchall()

       
        return render_template("gestionCuentas.html",cuentas=cuentas_info)
    if request.method == 'POST':
            #AGREGAR cunetas
            tipo_cuenta = request.form.get("tipo-cuenta").upper()
            numero_cuenta = request.form.get("cuenta")
            print(tipo_cuenta)

            consulta_existenciaCuentas = text('''SELECT COUNT(*) FROM public."tipos_viaticos" WHERE "tipoviatico" = :tipoviatico''')
            resultadoCuentas = db.execute(consulta_existenciaCuentas,{"tipoviatico": tipo_cuenta}).scalar()

            if resultadoCuentas > 0:
                return render_template("gestionCuentas.html", error="tipo de cuenta ya existe")
            else:
                agregar_cuenta = text('''INSERT INTO public.tipos_viaticos ("tipoviatico", "cuenta") VALUES (:tipoviatico, :cuenta)''')
                db.execute(agregar_cuenta,{"tipoviatico": tipo_cuenta, "cuenta":numero_cuenta})
                db.commit()
            return redirect("/gestioncuentas")
    
    return render_template("gestionCuentas.html")


#Gestion de usuarios
@app.route("/gestionusuarios", methods=["GET", "POST"])
@login_required
def gestionUsuarios():
    if request.method == "GET":
        #MOSTRAR PERFILES EN EL SELECT PERFILES
        perfilesParaSelect_query = text('''SELECT * FROM public.perfiles ''')
        perfiles_select = db.execute(perfilesParaSelect_query,{}).fetchall()

        #Mostrar usuario en la tabla 
        usuarios_query = text('''SELECT * FROM public.usuarios INNER JOIN public.perfiles ON public.usuarios."perfilid" = public.perfiles."perfilid"  ''')
        usuarios_table = db.execute(usuarios_query, {}).fetchall()
        return render_template("gestionUsuario.html",Perfiles = perfiles_select, usuarios = usuarios_table )
    
    if request.method == "POST":
        #AGREGAR USUARIO
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")
        hash_clave = generate_password_hash(clave)
        perfil_seleccionado = request.form.get("idperfilselect")

        print("ESTE ES EL USUARIO INGRESADO:", usuario, "y tambien su perfilid", perfil_seleccionado)
        #validar si ya existe el usuario
        validar_usuario = text('SELECT * FROM public."usuarios" WHERE "nombreusuario"=:usuario')

        if db.execute(validar_usuario, {'usuario': usuario}).rowcount > 0:
            duplicado = "Usuario ya existe"
            return render_template('gestionUsuario', duplicado)
        else:
            agregar_usuario = text('''INSERT INTO public.usuarios ("nombreusuario", "clave", "perfilid") VALUES (:nombreusuario, :clave, :perfilid) ''')
            db.execute(agregar_usuario,{"nombreusuario": usuario, "clave": hash_clave, "perfilid": perfil_seleccionado})
            db.commit()
        print("este es el id del perfil", perfil_seleccionado)
        return redirect("/gestionusuarios")
    
    return render_template("gestionUsuario.html")

@app.route('/obtener_info/<int:id>', methods=['GET'])
def obtener_info(id):
    #obtener el perfil del usuario
    obtener_perfil = text("SELECT * FROM public.perfiles WHERE perfilid = :id")
    result = db.execute(obtener_perfil, {"id": id})
    info = result.fetchone()

    if info:
        # Obtener los nombres de las columnas
        columns = result.keys()
        # Construir el diccionario manualmente
        info_dict = dict(zip(columns, info))
        return jsonify(info_dict)
    else:
        return jsonify({'error': 'Item not found'}), 404
    
@app.route('/editar_perfil', methods=['POST'])
def editar_perfil():

    id_perfil = request.form.get('id_perfil')
    nuevo_perfil = request.form.get('nuevo_nombrePerfil')

    actualizarPerfil_Query = text('''UPDATE public."perfiles" SET "perfil" = :nuevoPerfil WHERE "perfilid" = :id_perfil''')
    db.execute(actualizarPerfil_Query,{"nuevoPerfil": nuevo_perfil, "id_perfil":id_perfil})
    db.commit()

    return redirect("/gestionperfiles")

@app.route('/eliminar_perfil', methods=['POST'])
def eliminar_perfil():

    id_perfil = request.form.get('id_perfil')
    eliminarPerfil_Query = text('''DELETE FROM public.perfiles WHERE "perfilid" = :id_perfil''')
    db.execute(eliminarPerfil_Query,{"id_perfil":id_perfil})
    db.commit()

    return redirect("/gestionperfiles")

#Gestion Personal
@app.route('/gestionpersonal', methods=['GET','POST'])
@login_required
def gestion_personal():
    if request.method == "GET":
        #Nombres en el select de busqueda
        nombres = text('SELECT * FROM public.datos_trabajadores')
        nombres_result = db.execute(nombres).fetchall()

        #Obtener los id del usuario
        id_trabajador = request.form.get('empleadoUserid')
        print("idEmploy",id_trabajador)
        #Obtener lo datos del usuario
        obtener_trabajador = text('''SELECT * FROM public.datos_trabajadores WHERE "usuarioid" = :usuarioid''')
        resultado=db.execute(obtener_trabajador,{"usuarioid": id_trabajador}).fetchall()
        
        return render_template("gestionPersonal.html", nombresynumero = nombres_result, dataEmpleado = resultado)

#obtener data de los empleados
@app.route('/get_numero_empleado/<int:empleado_id>', methods=['GET'])
def get_numero_empleado(empleado_id):
    obtener_trabajador = text('''SELECT * FROM public.datos_trabajadores WHERE "usuarioid" = :usuarioid''')
    resultado = db.execute(obtener_trabajador, {"usuarioid": empleado_id}).fetchone()

    if resultado:
        numero_empleado = resultado[0]  # Ajusta esto según la posición de 'numero_empleado' en tu resultado
        nombres_empleado = resultado[2]
        departamento = resultado[3]
        area = resultado[4]
        cecc = resultado[5]
        cedula = resultado[6]
        return jsonify({"numeroEmpleado": numero_empleado, "nombresEmpleado":nombres_empleado,"departamento": departamento,"area":area,"cecc":cecc,"cedula":cedula})
    else:
        return jsonify({"numeroEmpleado": ""}), 404


@app.route("/cerrarsesion")
def cerrarsesion():
     session.clear()
     return render_template("login.html")