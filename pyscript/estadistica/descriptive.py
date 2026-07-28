import numpy as np
from scipy import stats

def procesar_estadistica_descriptiva(datos_texto):
    """
    Toma una cadena de texto con números separados por comas o espacios,
    y devuelve un diccionario con la estadística descriptiva.
    """
    try:
        # 1. Limpiar y convertir los datos
        # Reemplazamos comas por espacios y separamos
        datos_limpios = datos_texto.replace(',', ' ').split()
        
        # Convertimos a arreglo numérico de numpy
        data = np.array([float(x) for x in datos_limpios])
        
        if len(data) == 0:
            return {"error": "Por favor, ingresa al menos un valor numérico."}
            
        n = len(data)
        
        # 2. Cálculos estadísticos
        media = np.mean(data)
        mediana = np.median(data)
        
        # Moda (scipy.stats.mode)
        moda_res = stats.mode(data, keepdims=True)
        moda = moda_res.mode[0]
        
        # Varianza y desviación estándar (muestral: ddof=1)
        varianza = np.var(data, ddof=1) if n > 1 else 0
        desviacion = np.std(data, ddof=1) if n > 1 else 0
        
        # Cuartiles
        q1, q2, q3 = np.percentile(data, [25, 50, 75])
        
        # Asimetría y Curtosis
        asimetria = stats.skew(data)
        curtosis = stats.kurtosis(data)
        
        # 3. Retornar resultados formateados
        return {
            "n": n,
            "media": round(media, 4),
            "mediana": round(mediana, 4),
            "moda": round(moda, 4),
            "varianza": round(varianza, 4),
            "desviacion": round(desviacion, 4),
            "q1": round(q1, 4),
            "q2": round(q2, 4), # Es igual a la mediana
            "q3": round(q3, 4),
            "asimetria": round(asimetria, 4),
            "curtosis": round(curtosis, 4)
        }
        
    except ValueError:
        return {"error": "Entrada inválida. Asegúrate de ingresar solo números."}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}