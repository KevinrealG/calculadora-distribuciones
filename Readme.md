calculadora-distribuciones/
│
├── index.html                     # Página principal
├── README.md
│
├── assets/
│   ├── favicon.ico
│   ├── logo.png
│   └── icons/
│
├── css/
│   ├── styles.css
│   ├── darkmode.css
│   ├── cards.css
│   ├── sidebar.css
│   ├── tabs.css
│   ├── tables.css
│   ├── forms.css
│   └── responsive.css
│
├── js/
│   ├── ui.js
│   ├── tabs.js
│   └── theme.js
│
└── pyscript/
    │
    ├── main.py                     # Punto de entrada
    ├── config.py
    ├── router.py                   # Navegación
    ├── distribution_factory.py     # Registro y creación
    │
    ├── core/
    │   ├── base_distribution.py
    │   ├── discrete_distribution.py
    │   ├── continuous_distribution.py
    │   ├── registry.py             # (Opcional)
    │   └── exceptions.py
    │
    ├── ui/
    │   ├── panels.py
    │   ├── tables.py
    │   ├── charts.py
    │   ├── validation.py
    │   └── helpers.py
    │
    ├── distributions/
    │   │
    │   ├── discrete/
    │   │   ├── binomial.py
    │   │   ├── poisson.py
    │   │   ├── negative_binomial.py
    │   │   └── hypergeometric.py
    │   │
    │   └── continuous/
    │       ├── normal.py
    │       ├── exponential.py
    │       ├── gamma.py
    │       ├── beta.py
    │       ├── weibull.py
    │       ├── uniform.py
    │       ├── lognormal.py
    │       ├── chi_square.py
    │       ├── t_student.py
    │       └── fisher.py
    │
    ├── statistics/
    │   ├── probability.py
    │   ├── cumulative.py
    │   ├── intervals.py
    │   ├── descriptive.py
    │   ├── moments.py
    │   └── validators.py
    │
    ├── graphs/
    │   ├── common.py
    │   ├── bar.py
    │   ├── line.py
    │   ├── continuous.py
    │   └── histogram.py
    │
    └── utils/
        ├── constants.py
        ├── formatters.py
        ├── mathml.py
        └── latex.py