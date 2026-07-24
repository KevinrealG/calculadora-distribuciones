"""
===========================================================

Probability Calculator

Distribution Factory

Registro y creación de distribuciones.

Author : Kevin Sossa

===========================================================
"""

from typing import Dict, Type


class CalculatorFactory:
    """
    Factory para crear distribuciones de probabilidad.

    Cada distribución se registra automáticamente mediante
    el decorador @DistributionFactory.register().
    """

    _registry: Dict[str, Type] = {}

    # =====================================================
    # Registrar distribución
    # =====================================================

    @classmethod
    def register(
        cls,
        name: str,
        category: str = "Discrete"
    ):
        """
        Decorador para registrar una distribución.

        Ejemplo:

        @DistributionFactory.register(
            "binomial",
            category="Discrete"
        )

        class Binomial(...):

            ...
        """

        def decorator(distribution_class):

            key = name.lower().strip()

            cls._registry[key] = {

                "class": distribution_class,

                "category": category,

                "name": name

            }

            return distribution_class

        return decorator

    # =====================================================
    # Crear distribución
    # =====================================================

    @classmethod
    def create(cls, name: str):

        key = name.lower().strip()

        if key not in cls._registry:

            raise ValueError(

                f"La distribución '{name}' no existe."

            )

        return cls._registry[key]["class"]()

    # =====================================================
    # Obtener información
    # =====================================================

    @classmethod
    def info(cls, name: str):

        key = name.lower().strip()

        return cls._registry.get(key)

    # =====================================================
    # Existe
    # =====================================================

    @classmethod
    def exists(cls, name: str):

        return name.lower().strip() in cls._registry

    # =====================================================
    # Todas las distribuciones
    # =====================================================

    @classmethod
    def all(cls):

        return sorted(

            cls._registry.keys()

        )

    # =====================================================
    # Distribuciones discretas
    # =====================================================

    @classmethod
    def discrete(cls):

        return [

            item["name"]

            for item in cls._registry.values()

            if item["category"] == "Discrete"

        ]

    # =====================================================
    # Distribuciones continuas
    # =====================================================

    @classmethod
    def continuous(cls):

        return [

            item["name"]

            for item in cls._registry.values()

            if item["category"] == "Continuous"

        ]

    # =====================================================
    # Agrupadas
    # =====================================================

    @classmethod
    def grouped(cls):

        groups = {}

        for item in cls._registry.values():

            category = item["category"]

            if category not in groups:

                groups[category] = []

            groups[category].append(

                item["name"]

            )

        for category in groups:

            groups[category].sort()

        return groups

    # =====================================================
    # Total
    # =====================================================

    @classmethod
    def count(cls):

        return len(

            cls._registry

        )

    # =====================================================
    # Reiniciar registro
    # =====================================================

    @classmethod
    def clear(cls):

        cls._registry.clear()

    # =====================================================
    # Mostrar catálogo
    # =====================================================

    @classmethod
    def catalog(cls):

        catalog = []

        for key in sorted(cls._registry):

            item = cls._registry[key]

            catalog.append({

                "id": key,

                "name": item["name"],

                "category": item["category"]

            })

        return catalog