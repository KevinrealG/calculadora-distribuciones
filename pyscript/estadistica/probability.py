"""
===========================================================
Probability Calculator

probability.py

Motor de probabilidades reutilizable.

Author : Kevin Sossa
===========================================================
"""

import numpy as np


class ProbabilityEngine:

    """
    Motor general para trabajar con cualquier distribución
    de scipy.stats.

    La distribución debe implementar:

        pmf()
        pdf()
        cdf()
        sf()
        ppf()

    """

    # ------------------------------------------------------

    def __init__(self, distribution):

        self.dist = distribution

    # ======================================================
    # DISCRETAS
    # ======================================================

    def pmf(self, x):

        return self.dist.pmf(x)

    # ======================================================
    # CONTINUAS
    # ======================================================

    def pdf(self, x):

        return self.dist.pdf(x)

    # ======================================================
    # ACUMULADA
    # ======================================================

    def cdf(self, x):

        return self.dist.cdf(x)

    # ======================================================
    # COMPLEMENTO
    # ======================================================

    def sf(self, x):

        """
        Survival Function

        P(X>x)

        """

        return self.dist.sf(x)

    # ======================================================
    # INTERVALO
    # ======================================================

    def between(self, a, b):

        return self.cdf(b) - self.cdf(a)

    # ======================================================
    # MENOR
    # ======================================================

    def less(self, x):

        return self.cdf(x)

    # ======================================================
    # MENOR O IGUAL
    # ======================================================

    def less_equal(self, x):

        return self.cdf(x)

    # ======================================================
    # MAYOR
    # ======================================================

    def greater(self, x):

        return self.sf(x)

    # ======================================================
    # MAYOR O IGUAL
    # ======================================================

    def greater_equal(self, x):

        return self.sf(x)

    # ======================================================
    # CUANTIL
    # ======================================================

    def quantile(self, p):

        return self.dist.ppf(p)

    # ======================================================
    # MEDIANA
    # ======================================================

    def median(self):

        return self.quantile(0.5)

    # ======================================================
    # PERCENTILES
    # ======================================================

    def percentiles(self):

        p = {}

        for i in range(5,100,5):

            p[i] = self.quantile(

                i/100

            )

        return p

    # ======================================================
    # RANGO INTERCUARTÍLICO
    # ======================================================

    def iqr(self):

        return (

            self.quantile(0.75)

            -

            self.quantile(0.25)

        )

    # ======================================================
    # MEDIA
    # ======================================================

    def mean(self):

        return self.dist.mean()

    # ======================================================
    # VARIANZA
    # ======================================================

    def variance(self):

        return self.dist.var()

    # ======================================================
    # DESVIACIÓN
    # ======================================================

    def std(self):

        return self.dist.std()

    # ======================================================
    # ASIMETRÍA
    # ======================================================

    def skewness(self):

        return self.dist.stats(

            moments="s"

        )

    # ======================================================
    # CURTOSIS
    # ======================================================

    def kurtosis(self):

        return self.dist.stats(

            moments="k"

        )

    # ======================================================
    # RESUMEN
    # ======================================================

    def summary(self):

        return {

            "Media":

                self.mean(),

            "Mediana":

                self.median(),

            "Varianza":

                self.variance(),

            "Desviación":

                self.std(),

            "Asimetría":

                self.skewness(),

            "Curtosis":

                self.kurtosis(),

            "IQR":

                self.iqr()

        }

    # ======================================================
    # TABLA
    # ======================================================

    def probability_table(

            self,

            values

    ):

        rows = []

        for x in values:

            rows.append({

                "x": x,

                "pdf": self.pdf(x)

                if hasattr(

                    self.dist,

                    "pdf"

                )

                else None,

                "pmf": self.pmf(x)

                if hasattr(

                    self.dist,

                    "pmf"

                )

                else None,

                "cdf": self.cdf(x),

                "sf": self.sf(x)

            })

        return rows

    # ======================================================
    # VECTOR PDF
    # ======================================================

    def pdf_vector(self, x):

        return self.dist.pdf(x)

    # ======================================================
    # VECTOR PMF
    # ======================================================

    def pmf_vector(self, x):

        return self.dist.pmf(x)

    # ======================================================
    # VECTOR CDF
    # ======================================================

    def cdf_vector(self, x):

        return self.dist.cdf(x)

    # ======================================================
    # VECTOR SF
    # ======================================================

    def sf_vector(self, x):

        return self.dist.sf(x)

    # ======================================================
    # Dominio automático
    # ======================================================

    def automatic_domain(self):

        a = self.quantile(0.001)

        b = self.quantile(0.999)

        return np.linspace(

            a,

            b,

            400

        )