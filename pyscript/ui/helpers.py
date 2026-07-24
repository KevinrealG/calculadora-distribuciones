"""
===========================================================

Probability Calculator

helpers.py

Funciones auxiliares para acceder a los componentes HTML.

Author : Kevin Sossa

===========================================================
"""

from pyscript import document


# ==========================================================
# Obtener elemento
# ==========================================================

def element(id):
    """
    Retorna el elemento HTML.

    Parameters
    ----------
    id : str

    Returns
    -------
    HTMLElement
    """

    return document.getElementById(id)


# ==========================================================
# Texto
# ==========================================================

def text_value(id):

    return element(id).value.strip()


# ==========================================================
# Entero
# ==========================================================

def int_value(id):

    value = text_value(id)

    if value == "":
        return 0

    return int(value)


# ==========================================================
# Decimal
# ==========================================================

def float_value(id):

    value = text_value(id)

    if value == "":
        return 0.0

    return float(value)


# ==========================================================
# Booleano
# ==========================================================

def bool_value(id):

    return element(id).checked


# ==========================================================
# Valor seleccionado
# ==========================================================

def selected_value(id):

    return element(id).value


# ==========================================================
# Cambiar valor
# ==========================================================

def set_value(id, value):

    element(id).value = str(value)


# ==========================================================
# Cambiar texto
# ==========================================================

def set_text(id, text):

    element(id).innerHTML = str(text)


# ==========================================================
# Obtener HTML
# ==========================================================

def html(id):

    return element(id).innerHTML


# ==========================================================
# Cambiar HTML
# ==========================================================

def set_html(id, value):

    element(id).innerHTML = value


# ==========================================================
# Limpiar HTML
# ==========================================================

def clear(id):

    element(id).innerHTML = ""


# ==========================================================
# Mostrar
# ==========================================================

def show(id):

    element(id).style.display = "block"


# ==========================================================
# Ocultar
# ==========================================================

def hide(id):

    element(id).style.display = "none"


# ==========================================================
# Deshabilitar
# ==========================================================

def disable(id):

    element(id).disabled = True


# ==========================================================
# Habilitar
# ==========================================================

def enable(id):

    element(id).disabled = False


# ==========================================================
# Agregar clase CSS
# ==========================================================

def add_class(id, css_class):

    element(id).classList.add(css_class)


# ==========================================================
# Eliminar clase CSS
# ==========================================================

def remove_class(id, css_class):

    element(id).classList.remove(css_class)


# ==========================================================
# Alternar clase CSS
# ==========================================================

def toggle_class(id, css_class):

    element(id).classList.toggle(css_class)


# ==========================================================
# Enfocar componente
# ==========================================================

def focus(id):

    element(id).focus()