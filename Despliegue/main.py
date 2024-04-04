from flask import Flask, render_template, request, redirect, url_for
import pickle  # Módulo para serializar/deserializar objetos
from  model.Producto import Producto 
from model.Carrito import Carrito
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    usuario = "Juan"
    carrito = Carrito()

    # Lista de productos disponibles
    productos_disponibles = [
        Producto("Smartphone", 500),
        Producto("Auriculares", 50),
        Producto("Teclado", 30)
    ]

    if request.method == 'POST':
        # Obtener los productos seleccionados por el usuario
        productos_seleccionados = request.form.getlist('producto')

        # Agregar los productos seleccionados al carrito
        for nombre_producto in productos_seleccionados:
            producto = next((p for p in productos_disponibles if p.nombre == nombre_producto), None)
            if producto:
                carrito.agregar_producto(producto)

        # Serializar el carrito y pasar como un argumento de la URL
        carrito_serializado = pickle.dumps(carrito)
        return redirect(url_for('confirmacion_compra', carrito=carrito_serializado.decode('latin1')))

    return render_template('index.html', usuario=usuario, productos=productos_disponibles)

@app.route('/confirmacion')
def confirmacion_compra():
    # Obtener el carrito serializado de la URL y deserializarlo
    carrito_serializado = request.args.get('carrito', None)
    carrito = None
    if carrito_serializado:
        try:
            carrito = pickle.loads(carrito_serializado.encode('latin1'))
        except pickle.UnpicklingError as e:
            print(f"Error al deserializar el carrito: {e}")

    # Si no se puede cargar el carrito, crea uno nuevo
    if not carrito:
        carrito = Carrito()

    # Calcular el total
    total = carrito.calcular_total()

    return render_template('confirmacion.html', carrito=carrito.items, total=total)

if __name__ == '__main__':
    app.run(debug=True)
