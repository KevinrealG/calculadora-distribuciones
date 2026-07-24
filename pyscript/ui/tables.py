"""
===========================================================

Probability Calculator

tables.py

Renderizador de tablas HTML.

Author : Kevin Sossa

===========================================================
"""

from pyscript import document


# ==========================================================
# Clase principal
# ==========================================================

class TableRenderer:

    def __init__(self):

        self.container = document.getElementById(
            "table-container"
        )

    # ------------------------------------------------------

    def clear(self):

        self.container.innerHTML = ""

    # ------------------------------------------------------

    def render(self, table_data):

        """
        Espera un diccionario con la estructura:

        {
            "title":"Distribución Binomial",
            "headers":["k","P(X=k)"],
            "rows":[
                [0,0.002],
                [1,0.021],
                ...
            ]
        }
        """

        if table_data is None:

            self.clear()

            return

        html = self.build(table_data)

        self.container.innerHTML = html

    # ------------------------------------------------------

    def build(self, table):

        title = table.get("title", "")

        headers = table.get("headers", [])

        rows = table.get("rows", [])

        highlight_k = table.get("highlight_k")

        prob_type = table.get("prob_type", "equal")

        html = f"""

<div class="card">

<div class="card-divider">

<h5>{title}</h5>

</div>

<div class="card-section">

<div class="table-scroll">

<table class="table-results hover unstriped">

<thead>

<tr>

"""

        # -----------------------------
        # Encabezados
        # -----------------------------

        for index, header in enumerate(headers):

            th_class = "k-header" if index == 0 and highlight_k is not None else ""

            html += f"<th scope=\"col\" class=\"{th_class}\">{header}</th>"

        html += """

</tr>

</thead>

<tbody>

"""

        # -----------------------------
        # Filas
        # -----------------------------

        for row in rows:

            is_selected = False

            row_value = row[0]

            if highlight_k is None:

                is_selected = False

            elif prob_type == "equal":

                is_selected = str(row_value) == str(highlight_k)

            elif prob_type == "less":

                is_selected = row_value <= highlight_k

            elif prob_type == "less_strict":

                is_selected = row_value < highlight_k

            elif prob_type == "greater":

                is_selected = row_value >= highlight_k

            elif prob_type == "greater_strict":

                is_selected = row_value > highlight_k

            row_class = "k-row" if is_selected else ""

            html += f"<tr class=\"{row_class}\">"

            for index, value in enumerate(row):

                cell_class = "k-cell" if index == 0 and is_selected else ""

                html += f"<td class=\"{cell_class}\">{self.format(value)}</td>"

            html += "</tr>"

        html += """

</tbody>

</table>

</div>

</div>

</div>

"""

        return html

    # ------------------------------------------------------

    def format(self, value):

        if isinstance(value, float):

            return f"{value:.6f}"

        return str(value)


# ==========================================================
# Instancia global
# ==========================================================

_renderer = TableRenderer()


# ==========================================================
# API pública
# ==========================================================

def render(table_data):

    _renderer.render(table_data)


def clear():

    _renderer.clear()