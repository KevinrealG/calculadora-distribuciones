"""
===========================================================
Probability Calculator

BaseDistribution

Clase base para todas las distribuciones.

Author : Kevin Sossa
===========================================================
"""

from abc import ABC
from abc import abstractmethod

from ui import tables
from ui import charts


class BaseDistribution(ABC):

    """
    Clase base para todas las distribuciones.
    """

    # ------------------------------------------------------
    # Constructor
    # ------------------------------------------------------

    def __init__(self):

        self.name = ""

        self.parameter_values = {}

        self.result = None

        self.summary_data = {}

        self.table_data = None

        self.chart_data = None

        self.description_text = ""

        self.formula_html = ""

        self.interpretation_text = ""

    # ------------------------------------------------------
    # Información general
    # ------------------------------------------------------

    @property
    def title(self):

        return self.name

    # ------------------------------------------------------
    # Flujo principal
    # ------------------------------------------------------

    def run(self):
        """
        Ejecuta toda la distribución.
        """

        self.read_parameters()

        self.validate()

        self.compute()

        self.create_summary()

        self.create_table()

        self.create_chart()

        self.create_formula()

        self.create_description()

        self.create_interpretation()

        self.render()

    # ------------------------------------------------------
    # Render
    # ------------------------------------------------------

    def render(self):

        self.render_result()

        self.render_summary()

        self.render_table()

        self.render_chart()

        self.render_formula()

        self.render_description()

        self.render_interpretation()

    # ------------------------------------------------------
    # Render resultado
    # ------------------------------------------------------

    def render_result(self):

        tables.result(

            "Resultado",

            self.result

        )

    # ------------------------------------------------------

    def render_summary(self):

        tables.summary(

            self.summary_data

        )

    # ------------------------------------------------------

    def render_table(self):

        if self.table_data is not None:

            headers, rows = self.table_data

            tables.dataframe(

                headers,

                rows

            )

    # ------------------------------------------------------

    def render_chart(self):

        if self.chart_data is None:

            return

        tipo = self.chart_data["type"]

        if tipo == "bar":

            charts.bar(

                **self.chart_data["args"]

            )

        elif tipo == "line":

            charts.line(

                **self.chart_data["args"]

            )

        elif tipo == "area":

            charts.area(

                **self.chart_data["args"]

            )

        elif tipo == "line_point":

            charts.line_with_point(

                **self.chart_data["args"]

            )

    # ------------------------------------------------------

    def render_formula(self):

        tables.formula(

            self.formula_html

        )

    # ------------------------------------------------------

    def render_description(self):

        tables.description(

            self.description_text

        )

    # ------------------------------------------------------

    def render_interpretation(self):

        tables.interpretation(

            self.interpretation_text

        )

    # ======================================================
    # Métodos que implementará cada distribución
    # ======================================================

    @abstractmethod
    def read_parameters(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def compute(self):
        pass

    @abstractmethod
    def create_summary(self):
        pass

    @abstractmethod
    def create_table(self):
        pass

    @abstractmethod
    def create_chart(self):
        pass

    @abstractmethod
    def create_formula(self):
        pass

    @abstractmethod
    def create_description(self):
        pass

    @abstractmethod
    def create_interpretation(self):
        pass