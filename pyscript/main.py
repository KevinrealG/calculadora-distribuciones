"""
===========================================================

Probability Calculator

main.py

Punto de entrada de la aplicación.

Author : Kevin Sossa

===========================================================
"""
print("Main iniciado")
import json
import numpy as np
from scipy.stats import linregress
from pyscript import document, window
from router import Router
from calculator_factory import CalculatorFactory
from distributions.discrete.binomial import Binomial
from pyodide.ffi import create_proxy
from distributions.discrete.negative_binomial import NegativeBinomial
from distributions.discrete.poisson import Poisson
from distributions.discrete.hypergeometric import Hypergeometric
from distributions.continuous.normal import Normal
from distributions.discrete.uniforme_discreta import UniformDiscrete
from distributions.continuous.t_student import TStudent
from distributions.continuous.uniform import UniformContinuous
from distributions.continuous.chi_square import ChiSquare
from distributions.continuous.exponential import Exponential
from distributions.continuous.fisher import Fisher
#from distributions.continuous.uniform import Uniform
#from distributions.discrete.geometric import Geometric

# Importación de la lógica de estadística descriptiva
from estadistica.descriptive import procesar_estadistica_descriptiva

class Application:

    """
    Clase principal de la aplicación.

    Su única responsabilidad es inicializar
    la interfaz y delegar el trabajo al Router.
    """

    def __init__(self):

        self.router = Router()
        self.calculate_proxy = create_proxy(
            self.router.calculate
        )

        self.change_proxy = create_proxy(
            self.router.change_distribution
        )

        # Proxy para el botón de la nueva calculadora Descriptiva
        self.calculate_desc_proxy = create_proxy(
            self.calculate_descriptive
        )
        # 1. Creamos los proxies para cada pestaña descriptiva
        self.calc_uni_proxy = create_proxy(self.calcular_univariado)
        self.calc_agr_proxy = create_proxy(self.calcular_agrupados)
        self.calc_cual_proxy = create_proxy(self.calcular_cualitativas)
        self.calc_cualf_proxy = create_proxy(self.calcular_cualitativas_freq)
        self.calc_cont_proxy = create_proxy(self.calcular_contingencia)
        self.calc_biv_proxy = create_proxy(self.calcular_bivariado)

    # --------------------------------------------------
    # Inicio
    # --------------------------------------------------

    def start(self):

        self.load_catalog()
        self.register_events()
        self.router.load_default()

    # --------------------------------------------------
    # Cargar catálogo
    # --------------------------------------------------

    def load_catalog(self):

        select = document.getElementById(
            "distribution-select"
        )

        select.innerHTML = ""
        catalog = CalculatorFactory.catalog()

        for item in catalog:
            option = document.createElement("option")
            option.value = item["id"]
            option.textContent = item["name"]
            select.appendChild(option)

    # --------------------------------------------------
    # Eventos
    # --------------------------------------------------

    def register_events(self):

        # Eventos originales de distribuciones
        document.getElementById(
            "distribution-select"
        ).addEventListener(
            "change",
            self.change_proxy
        )

        document.getElementById(
            "calculate-btn"
        ).addEventListener(
            "click",
            self.calculate_proxy
        )

        # Registro del nuevo botón de Estadística Descriptiva
        btn_calc_desc = document.getElementById("calc-desc-btn")
        if btn_calc_desc:
            btn_calc_desc.addEventListener(
                "click", 
                self.calculate_desc_proxy
            )
        # 2. Conectamos cada botón HTML con su proxy en Python
        botones = {
            "calc-uni-btn": self.calc_uni_proxy,
            "calc-agr-btn": self.calc_agr_proxy,
            "calc-cual-btn": self.calc_cual_proxy,
            "calc-cualf-btn": self.calc_cualf_proxy,
            "calc-cont-btn": self.calc_cont_proxy,
            "calc-biv-btn": self.calc_biv_proxy
        }

        for btn_id, proxy in botones.items():
            btn = document.getElementById(btn_id)
            if btn:
                btn.addEventListener("click", proxy)

    # --------------------------------------------------
    # Lógica de Interfaz: Estadística Descriptiva
    # --------------------------------------------------
    
    def calculate_descriptive(self, event=None):
        """
        Captura los datos de la tabla dinámica HTML,
        los formatea y los envía a procesar a la lógica de Python.
        """
        try:
            # 1. Seleccionamos todas las entradas de valores y frecuencias de la tabla HTML
            inputs_valores = document.querySelectorAll(".fila-valor")
            inputs_frecuencias = document.querySelectorAll(".fila-frecuencia")
            
            valores_lista = []
            
            # Recorremos cada fila para extraer la información
            for val_input, freq_input in zip(inputs_valores, inputs_frecuencias):
                val = val_input.value.strip()
                freq = freq_input.value.strip()
                
                # Solo procesamos si ambos campos de la fila tienen datos
                if val != "" and freq != "":
                    try:
                        # Convertimos la frecuencia a entero para saber cuántas veces repetir el valor
                        f = int(freq)
                        # Agregamos el valor a la lista tantas veces como indique la frecuencia
                        valores_lista.extend([val] * f)
                    except ValueError:
                        pass # Ignoramos filas con errores tipográficos sutiles
                        
            # Unimos la lista final con espacios para que sea leída por nuestra función existente
            datos_texto = " ".join(valores_lista)
            
            # 2. Llamamos a nuestra función de cálculo en Python
            resultados = procesar_estadistica_descriptiva(datos_texto)
            
            # 3. Ubicamos el contenedor en el HTML y mostramos los resultados
            contenedor = document.getElementById("desc-stats-container")
            
            if "error" in resultados:
                contenedor.innerHTML = f"<div class='callout alert'>{resultados['error']}</div>"
            else:
                html_salida = f"""
                <table class="hover">
                    <thead>
                        <tr><th>Métrica</th><th>Valor</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Muestra Total (n)</td><td>{resultados.get('n', '-')}</td></tr>
                        <tr><td>Media</td><td>{resultados.get('media', '-')}</td></tr>
                        <tr><td>Mediana</td><td>{resultados.get('mediana', '-')}</td></tr>
                        <tr><td>Moda</td><td>{resultados.get('moda', '-')}</td></tr>
                        <tr><td>Varianza Muestral</td><td>{resultados.get('varianza', '-')}</td></tr>
                        <tr><td>Desviación Estándar</td><td>{resultados.get('desviacion', '-')}</td></tr>
                        <tr><td>Cuartil 1 (Q1)</td><td>{resultados.get('q1', '-')}</td></tr>
                        <tr><td>Cuartil 3 (Q3)</td><td>{resultados.get('q3', '-')}</td></tr>
                        <tr><td>Asimetría</td><td>{resultados.get('asimetria', '-')}</td></tr>
                        <tr><td>Curtosis</td><td>{resultados.get('curtosis', '-')}</td></tr>
                    </tbody>
                </table>
                """
                contenedor.innerHTML = html_salida

        except Exception as e:
            print(f"Error procesando descriptiva: {e}")


    def mostrar_error_desc(self, mensaje):
        """Función auxiliar para mostrar alertas en la interfaz."""
        contenedor = document.getElementById("desc-error-container")
        if contenedor:
            contenedor.innerHTML = f"<div class='callout alert' style='margin-bottom: 1rem;'>⚠️ {mensaje}</div>"

    def calcular_univariado(self, event=None):
        print("Calculando Numérico Univariado...")
        
        # Limpiamos errores previos
        document.getElementById("desc-error-container").innerHTML = ""
        
        try:
            # 1. RECOPILACIÓN DE DATOS
            texto = document.getElementById("uni-data-txt").value.strip()
            valores = []
            
            if texto:
                # Entrada por texto
                valores = [float(x) for x in texto.replace(',', ' ').split() if x.strip()]
            else:
                # Entrada por lista/filas dinámicas
                inputs_val = document.querySelectorAll(".val-uni")
                for inp in inputs_val:
                    v = inp.value.strip()
                    if v:
                        valores.append(float(v))

            if not valores:
                self.mostrar_error_desc("Por favor, ingresa datos válidos para calcular.")
                return

            data = np.array(valores)
            n_total = len(data)

            # 2. CÁLCULO DE ESTADÍSTICAS, IQR Y OUTLIERS
            from estadistica.descriptive import procesar_estadistica_descriptiva
            datos_texto = " ".join(map(str, valores))
            stats = procesar_estadistica_descriptiva(datos_texto)
            
            # Nuevos cálculos
            q1 = stats.get('q1', 0)
            q3 = stats.get('q3', 0)
            iqr = q3 - q1
            lim_inf = q1 - 1.5 * iqr
            lim_sup = q3 + 1.5 * iqr
            
            # Detección de outliers
            outliers = [v for v in valores if v < lim_inf or v > lim_sup]
            outliers_str = ", ".join(map(str, outliers)) if outliers else "Ninguno"

            html_stats = f"""
            <table class="hover">
                <thead><tr><th>Métrica</th><th>Valor</th></tr></thead>
                <tbody>
                    <tr><td>Media</td><td>{stats.get('media', '-')}</td></tr>
                    <tr><td>Mediana</td><td>{stats.get('mediana', '-')}</td></tr>
                    <tr><td>Moda</td><td>{stats.get('moda', '-')}</td></tr>
                    <tr><td>Desviación Estándar</td><td>{stats.get('desviacion', '-')}</td></tr>
                    <tr><td>IQR</td><td>{iqr:.4f}</td></tr>
                    <tr><td>Límite Inferior</td><td>{lim_inf:.4f}</td></tr>
                    <tr><td>Límite Superior</td><td>{lim_sup:.4f}</td></tr>
                    <tr><td>Outliers Detectados</td><td>{outliers_str}</td></tr>
                </tbody>
            </table>
            """
            document.getElementById("uni-stats").innerHTML = html_stats

            # 3. TABLA DE FRECUENCIAS
            k = int(1 + 3.322 * np.log10(n_total)) if n_total > 0 else 1
            frecuencias, limites = np.histogram(data, bins=k)
            
            # CONVERSIÓN para evitar el error JSON "int32 is not JSON serializable"
            frecuencias_list = frecuencias.tolist()
            limites_list = limites.tolist()
            
            html_frec = "<table class='hover'><thead><tr><th>Clase (Intervalo)</th><th>Frec. Absoluta</th><th>Frec. Acumulada</th></tr></thead><tbody>"
            acumulada = 0
            for i in range(len(frecuencias_list)):
                acumulada += int(frecuencias_list[i])
                intervalo = f"[{limites_list[i]:.2f} - {limites_list[i+1]:.2f})"
                html_frec += f"<tr><td>{intervalo}</td><td>{int(frecuencias_list[i])}</td><td>{acumulada}</td></tr>"
            html_frec += "</tbody></table>"
            
            document.getElementById("uni-frec").innerHTML = html_frec

            # 4. GRÁFICAS CON PLOTLY
            # 4. GRÁFICAS CON PLOTLY
            layout_base = {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "#666666"}, # Color visible para los textos
                "margin": {"t": 50, "b": 50, "l": 50, "r": 20},
                "autosize": True # Asegura que tome el tamaño del contenedor
            }
            
            # Configuración para hacer la gráfica responsive
            config_plotly = {"responsive": True}

            # Convertimos data a flotantes nativos para JSON
            data_py = [float(x) for x in data]

            document.getElementById("uni-graf").innerHTML = """
                <div id='uni-hist-container' style='width: 100%; margin-bottom: 20px;'></div>
                <div id='uni-box-container' style='width: 100%;'></div>
            """

            # A) Render Histograma
            hist_data = [{
                "x": data_py,
                "type": "histogram",
                "marker": {"color": "#e83e8c"},
                "xbins": {"size": float(limites_list[1] - limites_list[0])}
            }]
            hist_layout = {
                **layout_base, 
                "title": "Histograma de Frecuencias",
                "xaxis": {"title": "Valores (X)"},
                "yaxis": {"title": "Frecuencia Absoluta"}
            }
            
            # Enviamos data, layout y config
            window.Plotly.newPlot(
                "uni-hist-container", 
                window.JSON.parse(json.dumps(hist_data)), 
                window.JSON.parse(json.dumps(hist_layout)),
                window.JSON.parse(json.dumps(config_plotly))
            )

            # B) Render Boxplot
            box_data = [{
                "x": data_py,
                "type": "box",
                "name": "Muestra",
                "marker": {"color": "#4a54e1"}
            }]
            box_layout = {
                **layout_base, 
                "title": "Diagrama de Caja (Boxplot)",
                "xaxis": {"title": "Valores (X)"}
            }
            window.Plotly.newPlot(
                "uni-box-container", 
                window.JSON.parse(json.dumps(box_data)), 
                window.JSON.parse(json.dumps(box_layout)),
                window.JSON.parse(json.dumps(config_plotly))
            )

            # C) Polígono / Ojiva
            frec_acumulada_arr = np.cumsum(frecuencias_list).tolist()
            x_vals = [(limites_list[i] + limites_list[i+1])/2 for i in range(len(frecuencias_list))]
            
            ojiva_data = [{
                "x": [float(x) for x in x_vals],
                "y": [float(y) for y in frec_acumulada_arr],
                "mode": "lines+markers",
                "type": "scatter",
                "marker": {"color": "#4CAF50"},
                "line": {"shape": "spline"}
            }]
            ojiva_layout = {
                **layout_base, 
                "title": "Ojiva de Frecuencias Acumuladas",
                "xaxis": {"title": "Marcas de Clase"},
                "yaxis": {"title": "Frecuencia Acumulada"}
            }
            window.Plotly.newPlot(
                "uni-ojiva", 
                window.JSON.parse(json.dumps(ojiva_data)), 
                window.JSON.parse(json.dumps(ojiva_layout)),
                window.JSON.parse(json.dumps(config_plotly))
            )
        except Exception as e:
            self.mostrar_error_desc(f"Ocurrió un error al procesar los datos: {str(e)}")
    # --------------------------------------------------
    # Lógica de Interfaz: Numérico Agrupados
    # --------------------------------------------------

    def calcular_agrupados(self, event=None):
        print("Calculando Numérico Agrupados...")
        document.getElementById("desc-error-container").innerHTML = ""
        
        try:
            # 1. RECOPILACIÓN DE DATOS
            texto = document.getElementById("agr-data-txt").value.strip()
            clases = []
            frecuencias = []
            
            if texto:
                # Entrada por texto: "10-20, 5; 20-30, 8"
                pares = texto.split(';')
                for par in pares:
                    if ',' in par:
                        c, f = par.split(',')
                        clases.append(c.strip())
                        frecuencias.append(int(f.strip()))
            else:
                # Entrada por filas dinámicas
                filas = document.querySelectorAll("#tbody-agr tr")
                for fila in filas:
                    inputs = fila.querySelectorAll("input")
                    if len(inputs) >= 2:
                        c = inputs[0].value.strip()
                        f = inputs[1].value.strip()
                        if c and f:
                            clases.append(c)
                            frecuencias.append(int(f))

            if not clases or not frecuencias:
                self.mostrar_error_desc("Ingresa clases y frecuencias válidas.")
                return

            # 2. CÁLCULOS MATEMÁTICOS
            marcas_clase = []
            limites_sup = []
            
            # Extraer puntos medios y límites superiores para las gráficas
            for c in clases:
                partes = c.split('-')
                if len(partes) == 2:
                    inf, sup = float(partes[0]), float(partes[1])
                    marcas_clase.append((inf + sup) / 2)
                    limites_sup.append(sup)
                else:
                    # En caso de que se ingrese un solo número en lugar de rango
                    marcas_clase.append(float(c))
                    limites_sup.append(float(c))
                    
            n_total = sum(frecuencias)
            if n_total == 0:
                self.mostrar_error_desc("La suma de frecuencias debe ser mayor a 0.")
                return

            media = sum(m * f for m, f in zip(marcas_clase, frecuencias)) / n_total
            varianza = sum(f * (m - media)**2 for m, f in zip(marcas_clase, frecuencias)) / (n_total - 1 if n_total > 1 else 1)
            desviacion = np.sqrt(varianza)

            # 3. TABLA DE FRECUENCIAS Y ESTADÍSTICAS
            frec_acum = np.cumsum(frecuencias).tolist()
            
            html_frec = "<table class='hover'><thead><tr><th>Clase</th><th>Marca (X)</th><th>Frec. Absoluta</th><th>Frec. Acumulada</th></tr></thead><tbody>"
            for i in range(len(clases)):
                html_frec += f"<tr><td>{clases[i]}</td><td>{marcas_clase[i]:.2f}</td><td>{frecuencias[i]}</td><td>{frec_acum[i]}</td></tr>"
            html_frec += "</tbody></table>"
            document.getElementById("agr-frec").innerHTML = html_frec

            html_stats = f"""
            <table class="hover">
                <thead><tr><th>Métrica</th><th>Valor</th></tr></thead>
                <tbody>
                    <tr><td>Muestra Total (n)</td><td>{n_total}</td></tr>
                    <tr><td>Media Agrupada</td><td>{media:.4f}</td></tr>
                    <tr><td>Varianza Muestral</td><td>{varianza:.4f}</td></tr>
                    <tr><td>Desviación Estándar</td><td>{desviacion:.4f}</td></tr>
                </tbody>
            </table>
            """
            document.getElementById("agr-stats").innerHTML = html_stats

            # 4. GRÁFICAS CON PLOTLY
            layout_base = {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "#666666"},
                "margin": {"t": 50, "b": 50, "l": 50, "r": 20},
                "autosize": True
            }
            config_plotly = {"responsive": True}

            # Histograma (Gráfico de barras sin separación)
            hist_data = [{
                "x": clases,
                "y": frecuencias,
                "type": "bar",
                "marker": {"color": "#e83e8c"}
            }]
            hist_layout = {
                **layout_base, 
                "title": "Histograma de Frecuencias Agrupadas",
                "xaxis": {"title": "Intervalos de Clase"},
                "yaxis": {"title": "Frecuencia Absoluta"},
                "bargap": 0  # Esto une las barras como en un histograma real
            }
            window.Plotly.newPlot("agr-hist", window.JSON.parse(json.dumps(hist_data)), window.JSON.parse(json.dumps(hist_layout)), window.JSON.parse(json.dumps(config_plotly)))

            # Ojiva
            ojiva_data = [{
                "x": [float(x) for x in limites_sup],
                "y": [float(y) for y in frec_acum],
                "mode": "lines+markers",
                "type": "scatter",
                "marker": {"color": "#4CAF50"},
                "line": {"shape": "spline"}
            }]
            ojiva_layout = {
                **layout_base, 
                "title": "Ojiva (Frecuencias Acumuladas)",
                "xaxis": {"title": "Límite Superior de Clase"},
                "yaxis": {"title": "Frecuencia Acumulada"}
            }
            window.Plotly.newPlot("agr-ojiva", window.JSON.parse(json.dumps(ojiva_data)), window.JSON.parse(json.dumps(ojiva_layout)), window.JSON.parse(json.dumps(config_plotly)))

        except Exception as e:
            self.mostrar_error_desc(f"Error en datos agrupados: Verifica que el formato sea válido (Ej: 10-20, 5). Detalle técnico: {str(e)}")
        
    # --------------------------------------------------
    # Lógica de Interfaz: Datos Cualitativos
    # --------------------------------------------------

    def calcular_cualitativas(self, event=None):
        print("Calculando Cualitativo...")
        document.getElementById("desc-error-container").innerHTML = ""
        
        try:
            # 1. RECOPILACIÓN DE DATOS
            texto = document.getElementById("cual-data-txt").value.strip()
            
            if not texto:
                self.mostrar_error_desc("Ingresa datos cualitativos válidos (ej: Perro, Gato, Perro).")
                return
                
            # Separar por comas y limpiar espacios
            datos = [x.strip() for x in texto.split(',') if x.strip()]
            n_total = len(datos)
            
            # 2. CÁLCULO DE FRECUENCIAS
            frecuencias = {}
            for item in datos:
                frecuencias[item] = frecuencias.get(item, 0) + 1
                
            categorias = list(frecuencias.keys())
            conteos = list(frecuencias.values())
            
            # Calcular la moda (la categoría o categorías que más se repiten)
            max_frec = max(conteos)
            modas = [cat for cat, frec in frecuencias.items() if frec == max_frec]
            moda_str = ", ".join(modas)
            
            # 3. TABLAS HTML
            html_frec = "<table class='hover'><thead><tr><th>Categoría</th><th>Frecuencia Absoluta</th><th>Porcentaje</th></tr></thead><tbody>"
            for cat, count in frecuencias.items():
                porcentaje = (count / n_total) * 100
                html_frec += f"<tr><td>{cat}</td><td>{count}</td><td>{porcentaje:.2f}%</td></tr>"
            html_frec += "</tbody></table>"
            document.getElementById("cual-frec").innerHTML = html_frec
            
            html_stats = f"""
            <table class="hover">
                <thead><tr><th>Métrica</th><th>Valor</th></tr></thead>
                <tbody>
                    <tr><td>Muestra Total (n)</td><td>{n_total}</td></tr>
                    <tr><td>Moda(s)</td><td>{moda_str} ({max_frec} repeticiones)</td></tr>
                </tbody>
            </table>
            """
            document.getElementById("cual-stats").innerHTML = html_stats
            
            # 4. GRÁFICAS CON PLOTLY
            layout_base = {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "#666666"},
                "margin": {"t": 50, "b": 50, "l": 50, "r": 20},
                "autosize": True
            }
            config_plotly = {"responsive": True}
            
            # Gráfico de Barras
            bar_data = [{
                "x": categorias, 
                "y": conteos, 
                "type": "bar", 
                "marker": {"color": "#4a54e1"}
            }]
            bar_layout = {
                **layout_base, 
                "title": "Frecuencia por Categoría", 
                "xaxis": {"title": "Categorías"}, 
                "yaxis": {"title": "Frecuencia Absoluta"}
            }
            window.Plotly.newPlot("cual-bar", window.JSON.parse(json.dumps(bar_data)), window.JSON.parse(json.dumps(bar_layout)), window.JSON.parse(json.dumps(config_plotly)))
            
            # Gráfico Circular (Pie Chart)
            pie_data = [{
                "labels": categorias, 
                "values": conteos, 
                "type": "pie",
                "hole": 0.3, # Para que sea un gráfico de dona (opcional)
                "marker": {"colors": ["#e83e8c", "#4a54e1", "#4CAF50", "#FFC107", "#00BCD4"]}
            }]
            pie_layout = {
                **layout_base, 
                "title": "Distribución Porcentual"
            }
            window.Plotly.newPlot("cual-pie", window.JSON.parse(json.dumps(pie_data)), window.JSON.parse(json.dumps(pie_layout)), window.JSON.parse(json.dumps(config_plotly)))
            
        except Exception as e:
            self.mostrar_error_desc(f"Error procesando datos cualitativos: {str(e)}")
        
    def calcular_cualitativas_freq(self, event=None):
        error_box = document.getElementById("cualf-error-container")
        error_box.innerHTML = "" # Limpiar errores previos
        
        try:
            # 1. Recopilar datos de la tabla dinámica
            tbody = document.getElementById("tbody-cual-freq")
            filas = tbody.getElementsByTagName("tr")
            
            categorias = []
            frecuencias = []
            n_total = 0
            
            for i in range(filas.length):
                inputs = filas[i].getElementsByTagName("input")
                # Asegurarse de que la fila tenga los dos inputs
                if inputs.length >= 2: 
                    cat = inputs[0].value.strip()
                    frec_str = inputs[1].value.strip()
                    
                    if cat and frec_str:
                        frec = int(frec_str)
                        categorias.append(cat)
                        frecuencias.append(frec)
                        n_total += frec
            
            if not categorias or n_total == 0:
                error_box.innerHTML = "⚠️ Ingresa al menos una categoría con frecuencia válida."
                return
                
            # 2. Generar Tabla HTML
            html_frec = "<table class='hover'><thead><tr><th>Categoría</th><th>Frecuencia</th><th>Porcentaje</th></tr></thead><tbody>"
            for cat, frec in zip(categorias, frecuencias):
                porcentaje = (frec / n_total) * 100
                html_frec += f"<tr><td>{cat}</td><td>{frec}</td><td>{porcentaje:.2f}%</td></tr>"
            
            html_frec += f"<tr><td><strong>Total</strong></td><td><strong>{n_total}</strong></td><td><strong>100.00%</strong></td></tr>"
            html_frec += "</tbody></table>"
            
            document.getElementById("cualf-frec").innerHTML = html_frec
            
            # 3. Gráficos Plotly
            layout_base = {
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "margin": {"t": 50, "b": 50, "l": 50, "r": 20},
                "autosize": True
            }
            config_plotly = {"responsive": True}
            
            # Gráfico de Barras en 'cualf-bar'
            bar_data = [{"x": categorias, "y": frecuencias, "type": "bar", "marker": {"color": "#e83e8c"}}]
            bar_layout = {**layout_base, "title": "Frecuencias por Categoría"}
            window.Plotly.newPlot("cualf-bar", window.JSON.parse(json.dumps(bar_data)), window.JSON.parse(json.dumps(bar_layout)), window.JSON.parse(json.dumps(config_plotly)))
            
            # Gráfico Circular en 'cualf-circ'
            pie_data = [{"labels": categorias, "values": frecuencias, "type": "pie", "hole": 0.3}]
            pie_layout = {**layout_base, "title": "Distribución Porcentual"}
            window.Plotly.newPlot("cualf-circ", window.JSON.parse(json.dumps(pie_data)), window.JSON.parse(json.dumps(pie_layout)), window.JSON.parse(json.dumps(config_plotly)))

        except ValueError:
            error_box.innerHTML = "⚠️ Asegúrate de que las frecuencias sean números enteros."
        except Exception as e:
            error_box.innerHTML = f"⚠️ Error inesperado: {str(e)}"
        
    def calcular_contingencia(self, event=None):
        error_box = document.getElementById("cont-error")
        if error_box: error_box.innerHTML = ""
        
        try:
            # 1. Leer entradas
            rows_input = document.getElementById("cont-rows").value.strip()
            cols_input = document.getElementById("cont-cols").value.strip()
            data_input = document.getElementById("cont-data").value.strip()

            if not rows_input or not cols_input or not data_input:
                if error_box: error_box.innerHTML = "⚠️ Completa nombres de filas, columnas y datos."
                return

            row_names = [r.strip() for r in rows_input.split(',')]
            col_names = [c.strip() for c in cols_input.split(',')]
            
            # 2. Parsear matriz de datos
            data_matrix = []
            for line in data_input.split('\n'):
                if line.strip():
                    # Separar por comas o espacios
                    row_data = [int(x.strip()) for x in line.replace(',', ' ').split() if x.strip()]
                    data_matrix.append(row_data)

            # Validar dimensiones
            if len(data_matrix) != len(row_names):
                if error_box: error_box.innerHTML = f"⚠️ Esperadas {len(row_names)} filas de datos, ingresadas {len(data_matrix)}."
                return
            for i, row in enumerate(data_matrix):
                if len(row) != len(col_names):
                    if error_box: error_box.innerHTML = f"⚠️ Fila {i+1} necesita {len(col_names)} valores numéricos."
                    return

            # Calcular totales
            row_totals = [sum(r) for r in data_matrix]
            col_totals = [sum(data_matrix[i][j] for i in range(len(row_names))) for j in range(len(col_names))]
            grand_total = sum(row_totals)

            # 3. Generar Tabla HTML
            html = "<table class='hover'><thead><tr><th></th>"
            for c in col_names:
                html += f"<th>{c}</th>"
            html += "<th>Total</th></tr></thead><tbody>"
            
            for i, r_name in enumerate(row_names):
                html += f"<tr><td><strong>{r_name}</strong></td>"
                for val in data_matrix[i]:
                    html += f"<td>{val}</td>"
                html += f"<td><strong>{row_totals[i]}</strong></td></tr>"
            
            html += "<tr><td><strong>Total</strong></td>"
            for ct in col_totals:
                html += f"<td><strong>{ct}</strong></td>"
            html += f"<td><strong>{grand_total}</strong></td></tr></tbody></table>"
            
            document.getElementById("cont-tbl").innerHTML = html

            # 4. Gráficos con Plotly
            config = {"responsive": True}
            layout_base = {"margin": {"t": 40, "b": 40, "l": 50, "r": 20}, "autosize": True}
            
            traces_bar = []
            traces_bar_pct = []
            
            for j, c_name in enumerate(col_names):
                y_vals = [data_matrix[i][j] for i in range(len(row_names))]
                traces_bar.append({"x": row_names, "y": y_vals, "name": c_name, "type": "bar"})
                
                # Porcentajes por fila (para apiladas 100%)
                y_pct = [(data_matrix[i][j] / row_totals[i] * 100) if row_totals[i] > 0 else 0 for i in range(len(row_names))]
                traces_bar_pct.append({"x": row_names, "y": y_pct, "name": c_name, "type": "bar"})

            # Barras Agrupadas
            layout_b1 = {**layout_base, "barmode": "group", "title": "Frecuencias Agrupadas"}
            window.Plotly.newPlot("cont-bar1", window.JSON.parse(json.dumps(traces_bar)), window.JSON.parse(json.dumps(layout_b1)), window.JSON.parse(json.dumps(config)))

            # Barras Apiladas
            layout_b2 = {**layout_base, "barmode": "stack", "title": "Frecuencias Apiladas"}
            window.Plotly.newPlot("cont-bar2", window.JSON.parse(json.dumps(traces_bar)), window.JSON.parse(json.dumps(layout_b2)), window.JSON.parse(json.dumps(config)))

            # Barras Porcentual (100% Stacked)
            layout_b3 = {**layout_base, "barmode": "stack", "title": "Proporción por Fila (100%)"}
            window.Plotly.newPlot("cont-bar3", window.JSON.parse(json.dumps(traces_bar_pct)), window.JSON.parse(json.dumps(layout_b3)), window.JSON.parse(json.dumps(config)))

            # Mapa de Calor
            heat_data = [{"z": data_matrix, "x": col_names, "y": row_names, "type": "heatmap", "colorscale": "Viridis"}]
            layout_heat = {**layout_base, "title": "Mapa de Calor de Frecuencias"}
            window.Plotly.newPlot("cont-heat", window.JSON.parse(json.dumps(heat_data)), window.JSON.parse(json.dumps(layout_heat)), window.JSON.parse(json.dumps(config)))

        except ValueError:
            if error_box: error_box.innerHTML = "⚠️ Solo se permiten números enteros en los datos."
        except Exception as e:
            if error_box: error_box.innerHTML = f"⚠️ Error: {str(e)}"
        
    def calcular_bivariado(self, event=None):
        error_box = document.getElementById("biv-error")
        if error_box: error_box.innerHTML = ""
        
        x_data, y_data = [], []
        
        try:
            # 1. Identificar de qué pestaña leer los datos
            txt_panel = document.getElementById("biv-txt")
            is_txt_active = "is-active" in txt_panel.className
            
            if is_txt_active:
                x_str = document.getElementById("biv-x-txt").value
                y_str = document.getElementById("biv-y-txt").value
                
                if x_str and y_str:
                    x_data = [float(i.strip()) for i in x_str.split(",") if i.strip()]
                    y_data = [float(i.strip()) for i in y_str.split(",") if i.strip()]
            else:
                tbody = document.getElementById("tbody-biv")
                filas = tbody.getElementsByTagName("tr")
                for i in range(filas.length):
                    inputs = filas[i].getElementsByTagName("input")
                    if inputs.length >= 2:
                        vx = inputs[0].value.strip()
                        vy = inputs[1].value.strip()
                        if vx and vy:
                            x_data.append(float(vx))
                            y_data.append(float(vy))
                            
            # 2. Validaciones básicas
            if not x_data or not y_data:
                if error_box: error_box.innerHTML = "⚠️ Ingresa datos en ambas variables."
                return
                
            if len(x_data) != len(y_data):
                if error_box: error_box.innerHTML = "⚠️ X e Y deben tener la misma cantidad de observaciones."
                return
                
            n = len(x_data)
            x_arr = np.array(x_data)
            y_arr = np.array(y_data)
            
            # 3. Cálculos Estadísticos
            slope, intercept, r_value, p_value, std_err = linregress(x_arr, y_arr)
            r_squared = r_value ** 2
            
            # 4. Inyección en Tabla de Datos
            html_tbl = "<table class='hover'><thead><tr><th>N</th><th>X</th><th>Y</th></tr></thead><tbody>"
            for i in range(n):
                html_tbl += f"<tr><td>{i+1}</td><td>{x_data[i]}</td><td>{y_data[i]}</td></tr>"
            html_tbl += "</tbody></table>"
            document.getElementById("biv-tbl").innerHTML = html_tbl
            
            # 5. Inyección de Correlación
            document.getElementById("biv-corr").innerHTML = f"""
                <div style="padding: 20px; text-align: center;">
                    <h3>Coeficiente de Correlación (Pearson)</h3>
                    <h2 style="color: #e83e8c;">r = {r_value:.4f}</h2>
                    <p>Fuerza explicativa (R²): {r_squared*100:.2f}%</p>
                </div>
            """
            
            # 6. Inyección de Regresión Lineal (Textos + Contenedor para gráfica)
            reg_html = f"""
                <div class="grid-x grid-margin-x" style="padding: 10px;">
                    <div class="cell small-12">
                        <h4>Modelo: Y = {slope:.4f}X + {intercept:.4f}</h4>
                    </div>
                </div>
                <div id='biv-reg-plot' style='width:100%; height:400px;'></div>
            """
            document.getElementById("biv-reg").innerHTML = reg_html
            
            # 7. Gráficos con Plotly
            config = {"responsive": True}
            layout_base = {"margin": {"t": 40, "b": 40, "l": 50, "r": 20}, "autosize": True}
            
            trace_disp = {"x": x_data, "y": y_data, "mode": "markers", "type": "scatter", "name": "Datos Reales", "marker": {"color": "#e83e8c"}}
            
            # Dispersión simple (Pestaña Dispersión)
            layout_disp = {**layout_base, "title": "Diagrama de Dispersión", "xaxis": {"title": "X"}, "yaxis": {"title": "Y"}}
            window.Plotly.newPlot("biv-disp", window.JSON.parse(json.dumps([trace_disp])), window.JSON.parse(json.dumps(layout_disp)), window.JSON.parse(json.dumps(config)))
            
            # Dispersión + Línea de Regresión (Pestaña Regresión)
            y_pred = slope * x_arr + intercept
            trace_reg = {"x": x_data, "y": y_pred.tolist(), "mode": "lines", "type": "scatter", "name": "Ajuste Lineal", "line": {"color": "#17a2b8", "width": 2}}
            layout_reg = {**layout_base, "title": "Ajuste por Mínimos Cuadrados", "xaxis": {"title": "X"}, "yaxis": {"title": "Y"}}
            
            # Dibujamos en el div creado dinámicamente 'biv-reg-plot'
            window.Plotly.newPlot("biv-reg-plot", window.JSON.parse(json.dumps([trace_disp, trace_reg])), window.JSON.parse(json.dumps(layout_reg)), window.JSON.parse(json.dumps(config)))

        except ValueError:
            if error_box: error_box.innerHTML = "⚠️ Asegúrate de ingresar únicamente números válidos."
        except Exception as e:
            if error_box: error_box.innerHTML = f"⚠️ Error inesperado: {str(e)}"

# =========================================================

app = Application()

app.start()
# Ocultar el spinner de carga al terminar de cargar la app
loader = document.getElementById("loading-overlay")
if loader:
    loader.style.display = "none"