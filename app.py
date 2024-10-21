from flask import Flask, session, request,render_template, url_for, redirect

app = Flask(__name__)
app.secret_key='nelro_123'

@app.route('/')
def index():
   return render_template('index.html')


def generar_id():
    if 'datos_reg_seminario' in session and len(session['datos_reg_seminario']) > 0:
        return max(item['id'] for item in session['datos_reg_seminario']) + 1
    else:
        return 1


@app.route('/registro_sem', methods=['GET', 'POST'])
def registro_sem():
    if request.method == 'POST':
        # Recibir datos del formulario
        fecha = request.form.get('fecha')  # Usa get para evitar KeyError
        nombre = request.form.get('nombre')
        apellidos = request.form.get('apellidos')
        turno = request.form.get('turno')
        seminario = request.form.getlist('seminario')

        # Asegurarse de que la lista de datos_reg_seminario exista en la sesión
        if 'datos_reg_seminario' not in session:
            session['datos_reg_seminario'] = []  # Inicializa la lista si no existe
        
        # Crear el nuevo registro
        nuevos_ins = {
            'id': generar_id(),
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'seminario': seminario
        }

        # Agregar el nuevo registro a la sesión
        session['datos_reg_seminario'].append(nuevos_ins)
        
        # Flask podría no detectar que la sesión ha sido modificada.
        # Entonces, manualmente indicamos que la sesión ha cambiado
        session.modified = True
        # Redirigir a la misma página para mostrar los datos
        return redirect(url_for('registro_sem'))

    # Aquí podrías obtener los registros almacenados para mostrar en el HTML
    mostrar_registros = session.get('datos_reg_seminario', [])

    return render_template('registro_sem.html', mostrar_registros=mostrar_registros)

    
#creando la funcin para poder editar
@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    #capturo los datos de la lista
    datos_editar= session.get('datos_reg_seminario')
    #busco el id que quiero editar es decir capturo el id
    captura_id = next((item for item in datos_editar if item['id'] == id),None)
    #comprueba si encontro el id y si no vulve a la  pagina de registro
    if not captura_id:
        return redirect(url_for('registro_sem'))
    else:
        #si encontro el id
        if request.method == 'POST':
            # Recibir datos del formulario para modificarlo
            captura_id['fecha']= request.form['fecha']
            captura_id['nombre']= request.form['nombre']
            captura_id['apellidos']= request.form['apellidos']
            captura_id['turno']= request.form['turno']
            captura_id['seminario']=  request.form.getlist('seminario')
         
            #indicamos a session que se realizo una modificacion
            session.modified = True
            #retornamos a la pagina registro_sem
            return redirect(url_for('registro_sem'))

    return render_template('editar.html',captura_id=captura_id)        



#la opcion de poder eliminar un regiustro de sesssion
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    # Capturamos los datos de la lista
    datos_reg_seminario = session.get('datos_reg_seminario', [])
    
    # Filtramos los registros para eliminar el que coincide con el ID
    # session['datos_reg_seminario'] = [item for item in datos_reg_seminario if item['id'] != id]
    dato_eliminar=next((item for item in datos_reg_seminario if item['id']== id),None)
    #preguntando si capturo  el id
    if dato_eliminar:
        session['datos_reg_seminario'].remove(dato_eliminar)

    # Indicar que la sesión ha sido modificada
    session.modified = True
    
    # Redirigir a la página de registro
    return redirect(url_for('registro_sem'))


if __name__ == '__main__':
   app.run(debug=True)


