"""
===========================================================

Probability Calculator

validation.py

Motor de validación de parámetros.

Author : Kevin Sossa

===========================================================
"""


# ==========================================================
# Resultado
# ==========================================================

class ValidationResult:

    def __init__(self):

        self.valid = True
        self.message = ""

    def error(self, message):

        self.valid = False
        self.message = message

        return self


# ==========================================================
# Validador
# ==========================================================

class Validator:

    # ------------------------------------------------------

    @staticmethod
    def required(value, name):

        if value is None:

            return ValidationResult().error(

                f"{name} es obligatorio."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def integer(value, name):

        if not isinstance(value, int):

            return ValidationResult().error(

                f"{name} debe ser entero."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def numeric(value, name):

        if not isinstance(value, (int, float)):

            return ValidationResult().error(

                f"{name} debe ser numérico."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def minimum(value, minimum, name):

        if value < minimum:

            return ValidationResult().error(

                f"{name} debe ser ≥ {minimum}."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def maximum(value, maximum, name):

        if value > maximum:

            return ValidationResult().error(

                f"{name} debe ser ≤ {maximum}."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def between(value, minimum, maximum, name):

        if value < minimum or value > maximum:

            return ValidationResult().error(

                f"{name} debe estar entre {minimum} y {maximum}."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def positive(value, name):

        if value <= 0:

            return ValidationResult().error(

                f"{name} debe ser mayor que cero."

            )

        return ValidationResult()

    # ------------------------------------------------------

    @staticmethod
    def non_negative(value, name):

        if value < 0:

            return ValidationResult().error(

                f"{name} no puede ser negativo."

            )

        return ValidationResult()


# ==========================================================
# Funciones específicas
# ==========================================================

def binomial(n, p, k):

    validators = [

        Validator.integer(n, "n"),

        Validator.minimum(n, 1, "n"),

        Validator.between(p, 0, 1, "p"),

        Validator.integer(k, "k"),

        Validator.minimum(k, 0, "k")

    ]

    for result in validators:

        if not result.valid:

            return result

    if k > n:

        return ValidationResult().error(

            "k no puede ser mayor que n."

        )

    return ValidationResult()


# ==========================================================

def poisson(lmbda, k):

    validators = [

        Validator.positive(

            lmbda,

            "λ"

        ),

        Validator.integer(

            k,

            "k"

        ),

        Validator.minimum(

            k,

            0,

            "k"

        )

    ]

    for result in validators:

        if not result.valid:

            return result

    return ValidationResult()


# ==========================================================

def normal(mu, sigma):

    validators = [

        Validator.numeric(

            mu,

            "μ"

        ),

        Validator.positive(

            sigma,

            "σ"

        )

    ]

    for result in validators:

        if not result.valid:

            return result

    return ValidationResult()


# ==========================================================

def exponential(rate):

    validators = [

        Validator.positive(

            rate,

            "λ"

        )

    ]

    for result in validators:

        if not result.valid:

            return result

    return ValidationResult()


# ==========================================================

def gamma(alpha, beta):

    validators = [

        Validator.positive(

            alpha,

            "α"

        ),

        Validator.positive(

            beta,

            "β"

        )

    ]

    for result in validators:

        if not result.valid:

            return result

    return ValidationResult()