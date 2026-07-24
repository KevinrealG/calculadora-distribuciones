"""
===========================================================
Probability Calculator
Configuration File

Author : Kevin Sossa
===========================================================
"""

from dataclasses import dataclass


@dataclass
class Theme:

    PRIMARY = "#2563eb"
    SECONDARY = "#0ea5a5"

    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    DANGER = "#ef4444"

    LIGHT = "#ffffff"
    DARK = "#111827"

    TEXT = "#0f172a"
    TEXT_DARK = "#e5e7eb"

    BORDER = "#d1d5db"

    CARD_RADIUS = 18

    FONT = "Poppins"


@dataclass
class Plot:

    TEMPLATE = "plotly_white"

    WIDTH = None
    HEIGHT = 450

    RESPONSIVE = True

    SHOW_LOGO = False

    DISPLAY_MODE_BAR = True

    GRID_COLOR = "#e5e7eb"

    PAPER_COLOR = "white"

    PLOT_COLOR = "white"

    LINE_WIDTH = 3

    BAR_COLOR = "#2563eb"

    HIGHLIGHT = "#ef4444"

    FONT_SIZE = 14


@dataclass
class Table:

    DECIMALS = 6

    MAX_ROWS = 100

    STRIPED = True

    HOVER = True


@dataclass
class Calculator:

    DEFAULT_DISTRIBUTION = "binomial"

    MAX_POINTS = 300

    DEFAULT_BINOMIAL_N = 10

    DEFAULT_BINOMIAL_P = 0.50

    DEFAULT_POISSON = 4

    DEFAULT_SIGMA = 1

    DEFAULT_MU = 0

    DEFAULT_EXPONENTIAL = 0.5


@dataclass
class Messages:

    INVALID_PROBABILITY = "La probabilidad debe estar entre 0 y 1."

    INVALID_SIGMA = "σ debe ser mayor que cero."

    INVALID_LAMBDA = "λ debe ser mayor que cero."

    INVALID_K = "k debe ser un entero positivo."

    INVALID_N = "n debe ser mayor que cero."

    SUCCESS = "Cálculo realizado correctamente."


THEME = Theme()
PLOT = Plot()
TABLE = Table()
CALCULATOR = Calculator()
MESSAGES = Messages()