// TODO: Agregar funcionalidad JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // TODO: Inicializar componentes cuando cargue la página
    initSearch();
    initAlertAutoClose();
});

/**
 * Filtro de búsqueda en tiempo real sobre el catálogo de productos.
 */
function initSearch() {
    const input = document.getElementById('searchInput');
    if (!input) return;

    input.addEventListener('input', function () {
        const termino = this.value.toLowerCase().trim();
        const items = document.querySelectorAll('.product-item');

        items.forEach(function (item) {
            const nombre = item.dataset.name || '';
            item.style.display = nombre.includes(termino) ? '' : 'none';
        });
    });
}

/**
 * Cerrar alertas de Bootstrap automáticamente después de 4 segundos.
 */
function initAlertAutoClose() {
    const alertas = document.querySelectorAll('.alert');
    alertas.forEach(function (alerta) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alerta);
            bsAlert.close();
        }, 4000);
    });
}

// TODO: Función para agregar productos al carrito con AJAX
function addToCart(productId) {
    // TODO: Implementar agregado al carrito
    fetch('/add-to-cart/' + productId, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: 'quantity=1',
})
        .then(function (response) {
            if (response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(function (err) {
            console.error('Error al agregar al carrito:', err);
        });
}

// TODO: Función para actualizar cantidad en el carrito
function updateCartQuantity(itemId, quantity) {
    // TODO: Implementar actualización de cantidad
    fetch('/api/v1/carts/items/' + itemId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: quantity }),
    }).then(function () {
        window.location.reload();
    });
}

// TODO: Función para remover items del carrito
function removeFromCart(itemId) {
    // TODO: Implementar remoción de items
    if (!confirm('¿Deseas eliminar este producto del carrito?')) return;
    fetch('/remove-from-cart/' + itemId, { method: 'POST' }).then(function () {
        window.location.reload();
    });
}