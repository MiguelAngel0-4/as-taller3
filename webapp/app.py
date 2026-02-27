from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
from datetime import datetime

# TODO: Configurar la aplicación Flask
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'clave-por-defecto-cambiar')

# TODO: Configurar la URL de la API
API_URL = os.getenv('API_URL', 'http://api:8000')

#Helpers
def api_request(endpoint, method="GET", data=None, headers=None):
    """Realizar una petición HTTP a la API y devolver la respuesta JSON."""
    url = f"{API_URL}{endpoint}"
    try:
        resp = requests.request(method, url, json=data, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        return {"error": str(e)}
    except requests.exceptions.RequestException:
        return {"error": "No se pudo conectar con la API"}


def is_logged_in():
    """Verificar si hay una sesión de usuario activa."""
    return "user_id" in session and "username" in session


@app.route('/')
def index():
    # TODO: Implementar página principal
    # Obtener productos destacados de la API
    resultado = api_request("/api/v1/products/")
    productos = resultado if isinstance(resultado, list) else []
    destacados = productos[:4]
    return render_template('index.html', productos=destacados, is_logged_in=is_logged_in())

@app.route("/products")
def products():
    """Catálogo completo de productos."""
    resultado = api_request("/api/v1/products/")
    productos = resultado if isinstance(resultado, list) else []
    return render_template("products.html", productos=productos, logged_in=is_logged_in())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Página e inicio de sesión."""
    if is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        datos = {"username": request.form["username"], "password": request.form["password"]}
        resultado = api_request("/api/v1/users/login", method="POST", data=datos)

        if "error" in resultado:
            flash("Credenciales incorrectas. Intenta de nuevo.", "danger")
        else:
            session["user_id"]  = resultado["id"]
            session["username"] = resultado["username"]
            flash(f"Bienvenido, {resultado['username']}!", "success")
            return redirect(url_for("index"))

    return render_template("login.html", logged_in=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Página y formulario de registro."""
    if is_logged_in():
        return redirect(url_for("index"))

    if request.method == "POST":
        datos = {
            "username": request.form["username"],
            "email":    request.form["email"],
            "password": request.form["password"],
        }
        resultado = api_request("/api/v1/users/register", method="POST", data=datos)

        if "error" in resultado:
            flash("Error al registrar. El usuario o correo ya existe.", "danger")
        else:
            flash("Cuenta creada correctamente. Inicia sesión.", "success")
            return redirect(url_for("login"))

    return render_template("register.html", logged_in=False)


@app.route("/cart")
def cart():
    """Página del carrito del usuario."""
    if not is_logged_in():
        flash("Debes iniciar sesión para ver tu carrito.", "warning")
        return redirect(url_for("login"))

    resultado = api_request(f"/api/v1/carts/{session['user_id']}")
    items = resultado.get("items", []) if "error" not in resultado else []
    total = sum(item.get("product_price", 0) * item.get("quantity", 0) for item in items)
    return render_template("cart.html", items=items, total=total, logged_in=True)


@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    """Agregar un producto al carrito del usuario autenticado."""
    if not is_logged_in():
        flash("Debes iniciar sesión para agregar productos al carrito.", "warning")
        return redirect(url_for("login"))

    datos = {
        "user_id":    session["user_id"],
        "product_id": product_id,
        "quantity":   int(request.form.get("quantity", 1)),
    }
    resultado = api_request("/api/v1/carts/items", method="POST", data=datos)

    if "error" in resultado:
        flash("No se pudo agregar el producto al carrito.", "danger")
    else:
        flash("Producto agregado al carrito.", "success")

    return redirect(url_for("products"))


@app.route("/remove-from-cart/<int:item_id>", methods=["POST"])
def remove_from_cart(item_id):
    """Eliminar un item del carrito."""
    if not is_logged_in():
        return redirect(url_for("login"))

    api_request(f"/api/v1/carts/items/{item_id}", method="DELETE")
    flash("Producto eliminado del carrito.", "info")
    return redirect(url_for("cart"))


@app.route("/logout")
def logout():
    """Cerrar la sesión del usuario."""
    session.clear()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)