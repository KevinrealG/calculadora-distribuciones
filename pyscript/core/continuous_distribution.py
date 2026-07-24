"""
===========================================================
Probability Calculator

ContinuousDistribution

Clase base para todas las distribuciones continuas.

Author : Kevin Sossa
===========================================================
"""

import numpy as np

from core.base_distribution import BaseDistribution


class ContinuousDistribution(BaseDistribution):

    """
    Clase base para distribuciones continuas.

    Las clases hijas únicamente implementan:

        pdf(x)

        cdf(x)

        mean()

        variance()

        read_parameters()

        validate()

        domain()

    """

    # ------------------------------------------------------

    def __init__(self):

        super().__init__()

        self.x = None

        self.y = None

        self.cdf_values = None

        self.value = None

        self.points = 400

        self.minimum = None

        self.maximum = None

    # ------------------------------------------------------
    # Métodos abstractos
    # ------------------------------------------------------

    def pdf(self, x):

        raise NotImplementedError()

    def cdf(self, x):

        raise NotImplementedError()

    def mean(self):

        raise NotImplementedError()

    def variance(self):

        raise NotImplementedError()

    def domain(self):

        """
        Debe devolver:

            (xmin,xmax)

        """

        raise NotImplementedError()

    # ------------------------------------------------------
    # Cálculo
    # ------------------------------------------------------

    def compute(self):

        self.minimum, self.maximum = self.domain()

        self.x = np.linspace(

            self.minimum,

            self.maximum,

            self.points

        )

        self.y = self.pdf(

            self.x

        )

        self.cdf_values = self.cdf(

            self.x

        )

        self.result = self.pdf(

            self.value

        )

    # ------------------------------------------------------
    # Resumen
    # ------------------------------------------------------

    def create_summary(self):

        self.summary_data = {

            "Media":

                self.mean(),

            "Varianza":

                self.variance(),

            "Desviación":

                np.sqrt(

                    self.variance()

                ),

            "f(x)": self.result,

            "F(x)": self.cdf(

                self.value

            )

        }

    # ------------------------------------------------------
    # Tabla
    # ------------------------------------------------------

    def create_table(self):

        rows = []

        for i in range(

            len(self.x)

        ):

            rows.append([

                self.x[i],

                self.y[i],

                self.cdf_values[i]

            ])

        self.table_data = (

            [

                "x",

                "f(x)",

                "F(x)"

            ],

            rows

        )

    # ------------------------------------------------------
    # Gráfico
    # ------------------------------------------------------

    def create_chart(self):

        punto = self.pdf(

            self.value

        )

        self.chart_data = {

            "type": "line_point",

            "args": {

                "x": self.x,

                "y": self.y,

                "px": self.value,

                "py": punto,

                "title": self.title,

                "x_title": "x",

                "y_title": "f(x)"

            }

        }

    # ------------------------------------------------------
    # Fórmula
    # ------------------------------------------------------

    def create_formula(self):

        pass

    # ------------------------------------------------------
    # Descripción
    # ------------------------------------------------------

    def create_description(self):

        pass

    # ------------------------------------------------------
    # Interpretación
    # ------------------------------------------------------

    def create_interpretation(self):

        self.interpretation_text = f"""

        Para

        <b>x = {self.value:.4f}</b>

        la densidad es

        <b>{self.result:.6f}</b>

        y la probabilidad acumulada es

        <b>{self.cdf(self.value):.6f}</b>.

        """

    # ------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------

    def probability_between(

        self,

        a,

        b

    ):

        return self.cdf(

            b

        ) - self.cdf(

            a

        )

    # ------------------------------------------------------

    def probability_less(

        self,

        x

    ):

        return self.cdf(

            x

        )

    # ------------------------------------------------------

    def probability_greater(

        self,

        x

    ):

        return 1 - self.cdf(

            x

        )

    # ------------------------------------------------------

    def quantile(

        self,

        p

    ):

        """
        Las clases hijas pueden sobrescribir este método
        usando scipy.stats.ppf().
        """

        raise NotImplementedError()
