"""
===========================================================

Probability Calculator

charts.py

Generador de gráficos con Plotly.

Author : Kevin Sossa

===========================================================
"""

from inspect import trace

from pyscript import window, document
from pyodide.ffi import to_js

# ==========================================================
# Clase principal
# ==========================================================

class ChartRenderer:

    def __init__(self):


        self.container = document.getElementById("chart-container")

    # ------------------------------------------------------

    def clear(self):

        try:

            window.Plotly.purge(self.container)

        except:

            pass

    # ------------------------------------------------------
    def continuous(self, data):
        # Trazo de la curva principal
        curve_trace = {
            "type": "scatter",
            "mode": "lines",
            "x": data["x"],
            "y": data["y"],
            "name": "Normal",
            "line": {"color": "#3498db", "width": 2}
        }
        
        # Trazo del área sombreada
        fill_trace = {
            "type": "scatter",
            "mode": "lines",
            "x": data["fill_x"],
            "y": data["fill_y"],
            "name": data.get("prob_label", "Probabilidad"),
            "fill": "tozeroy",
            "line": {"color": "transparent"},
            "fillcolor": "rgba(231, 76, 60, 0.4)" # Rojo semitransparente como en la imagen
        }

        layout = self.layout(data)
        layout["showlegend"] = True

        
        window.Plotly.newPlot(
            self.container,
            to_js([curve_trace, fill_trace]),
            to_js(layout),
            to_js({"responsive": True})
        )
    def render(self, chart_data):

        """
        chart_data debe tener el formato:

        {
            "type":"bar",
            "x":[...],
            "y":[...],
            "title":"Distribución Binomial",
            "x_label":"k",
            "y_label":"P(X=k)"
        }
        """

        if chart_data is None:

            self.clear()

            return

        chart_type = chart_data.get("type", "bar")

        if chart_type == "bar":

            self.bar(chart_data)

        elif chart_type == "line":

            self.line(chart_data)

        elif chart_type == "scatter":

            self.scatter(chart_data)
        elif chart_type == "continuous":
            self.continuous(chart_data)

    # ------------------------------------------------------

    def layout(self, data):

        return {

            "title": data.get("title", ""),

            "paper_bgcolor": "rgba(0,0,0,0)",

            "plot_bgcolor": "rgba(0,0,0,0)",

            "hovermode": "closest",

            "margin": {

                "l": 50,

                "r": 20,

                "t": 50,

                "b": 50

            },

            "xaxis": {

                "title": data.get(

                    "x_label",

                    ""

                )

            },

            "yaxis": {

                "title": data.get(

                    "y_label",

                    ""

                )

            }

        }

    # ------------------------------------------------------
   

    def bar(self, data):

        x_values = data["x"]

        y_values = data["y"]

        highlight_k = data.get("highlight_k")

        prob_type = data.get("prob_type", "equal")

        colors = []

        for x_value in x_values:

            if highlight_k is None:

                colors.append("#4f46e5")

                continue

            if prob_type == "equal":

                selected = x_value == highlight_k

            elif prob_type == "less":

                selected = x_value <= highlight_k

            elif prob_type == "less_strict":

                selected = x_value < highlight_k

            elif prob_type == "greater":

                selected = x_value >= highlight_k

            elif prob_type == "greater_strict":

                selected = x_value > highlight_k

            else:

                selected = x_value == highlight_k

            if selected:

                colors.append("#dc2626")

            else:

                colors.append("#4f46e5")

        trace = {
            "type": "bar",
            "x": x_values,
            "y": y_values,
            "marker": {
                "color": colors,
                "line": {
                    "color": "#111827",
                    "width": 1
                }
            }
        }

        layout = self.layout(data)

        window.Plotly.newPlot(
            self.container,
            to_js([trace]),
            to_js(layout)
        )

       # ------------------------------------------------------

    def line(self, data):

        trace = {

            "type": "scatter",

            "mode": "lines",

            "x": data["x"],

            "y": data["y"]

        }
       

        window.Plotly.newPlot(

            self.container,

            [trace],

            self.layout(data),

            {

                "responsive": True

            }

        )

    # ------------------------------------------------------

    def scatter(self, data):

        trace = {

            "type": "scatter",

            "mode": "markers",

            "x": data["x"],

            "y": data["y"]

        }
        print(self.container)
        print(data)
        print(trace)
        print(self.layout(data))

        window.Plotly.newPlot(

            self.container,

            [trace],

            self.layout(data),

            {

                "responsive": True

            }

        )


# ==========================================================
# Instancia global
# ==========================================================

_renderer = ChartRenderer()


# ==========================================================
# API pública
# ==========================================================

def render(chart_data):

    _renderer.render(chart_data)


def clear():

    _renderer.clear()