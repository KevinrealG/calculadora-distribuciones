"""
===========================================================

Probability Calculator

panels.py

Construcción dinámica del panel de parámetros.

Author : Kevin Sossa

===========================================================
"""

from pyscript import document


# ==========================================================
# Componentes
# ==========================================================

class NumberField:

    def __init__(
        self,
        id,
        label,
        value=0,
        minimum=None,
        maximum=None,
        step=1
    ):

        self.id = id
        self.label = label
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.step = step


class SliderField:

    def __init__(
        self,
        id,
        label,
        value=0,
        minimum=0,
        maximum=1,
        step=0.01
    ):

        self.id = id
        self.label = label
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.step = step


class SelectField:

    def __init__(
        self,
        id,
        label,
        options, # options should be a dict like {"value": "label"} or a list of values
        value=None
    ):

        self.id = id
        self.label = label
        self.options = options
        self.value = value


class CheckField:

    def __init__(
        self,
        id,
        label,
        checked=False
    ):

        self.id = id
        self.label = label
        self.checked = checked


# ==========================================================
# Renderizador
# ==========================================================

class PanelRenderer:

    def __init__(self):

        self.container = document.getElementById(
            "parameter-panel"
        )

    # ------------------------------------------------------

    def clear(self):

        self.container.innerHTML = ""

    # ------------------------------------------------------

    def render(self, fields):

        self.clear()

        html = ""

        html += """

<div class="parameter-section">

<h3 class="parameter-title">📊 Parámetros</h3>

"""

        for field in fields:

            html += self.render_field(field)

        html += "</div>"

        self.container.innerHTML = html

    # ------------------------------------------------------

    def render_field(self, field):

        if isinstance(field, NumberField):

            return self.number(field)

        if isinstance(field, SliderField):

            return self.slider(field)

        if isinstance(field, SelectField):

            return self.select(field)

        if isinstance(field, CheckField):

            return self.checkbox(field)

        return ""

    # ------------------------------------------------------

    def number(self, field):

        minimum = "" if field.minimum is None else f'min="{field.minimum}"'
        maximum = "" if field.maximum is None else f'max="{field.maximum}"'

        return f"""

<div class="grid-x grid-margin-x">

<div class="cell">

<label>

{field.label}

<input
type="number"
id="{field.id}"
value="{field.value}"
{minimum}
{maximum}
step="{field.step}"
>

</label>

</div>

</div>

"""

    # ------------------------------------------------------

    def slider(self, field):

        return f"""

<div class="grid-x grid-margin-x">

<div class="cell">

<label>

{field.label}

<span id="{field.id}_value">

{field.value}

</span>

<input
type="range"
id="{field.id}"
min="{field.minimum}"
max="{field.maximum}"
step="{field.step}"
value="{field.value}"

oninput="document.getElementById('{field.id}_value').innerHTML=this.value"

>

</label>

</div>

</div>

"""

    # ------------------------------------------------------

    def select(self, field):

        options_html = ""

        if isinstance(field.options, dict):
            for val, label in field.options.items():
                selected = "selected" if val == field.value else ""
                options_html += f'<option value="{val}" {selected}>{label}</option>\n'
        else:
            for item in field.options:
                selected = "selected" if item == field.value else ""
                options_html += f'<option value="{item}" {selected}>{item}</option>\n'

        return f"""

<div class="grid-x grid-margin-x">

<div class="cell">

<label>

{field.label}

<select id="{field.id}">

{options_html}

</select>

</label>

</div>

</div>

"""

    # ------------------------------------------------------

    def checkbox(self, field):

        checked = ""

        if field.checked:

            checked = "checked"

        return f"""

<div class="grid-x">

<div class="cell">

<label>

<input
type="checkbox"
id="{field.id}"
{checked}
>

{field.label}

</label>

</div>

</div>

"""


# ==========================================================
# Instancia global
# ==========================================================

_renderer = PanelRenderer()


# ==========================================================
# API pública
# ==========================================================

def render(fields):

    _renderer.render(fields)


def clear():

    _renderer.clear()
