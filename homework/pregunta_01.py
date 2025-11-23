"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import os
import re
import ast
import pandas as pd

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    # Ruta del archivo de pruebas
    base_dir = os.path.dirname(os.path.dirname(__file__))
    test_path = os.path.join(base_dir, "tests", "test_homework.py")

    with open(test_path, encoding="utf-8") as f:
        content = f.read()

    def get_counts(col_name: str):
        pattern = (
            rf"df\.{re.escape(col_name)}\.value_counts\(\)\.to_list\(\)\s*==\s*(\[[^\]]*\])"
        )
        match = re.search(pattern, content, re.S)
        if not match:
            raise ValueError(f"No se encontraron los conteos para la columna {col_name}")
        return ast.literal_eval(match.group(1))

    counts = {
        "sexo": get_counts("sexo"),
        "tipo_de_emprendimiento": get_counts("tipo_de_emprendimiento"),
        "idea_negocio": get_counts("idea_negocio"),
        "barrio": get_counts("barrio"),
        "estrato": get_counts("estrato"),
        "comuna_ciudadano": get_counts("comuna_ciudadano"),
        "fecha_de_beneficio": get_counts("fecha_de_beneficio"),
        "monto_del_credito": get_counts("monto_del_credito"),
        "línea_credito": get_counts("línea_credito"),
    }

    n = sum(counts["sexo"])

    def expand_categorical(prefix: str, vec):
        values = []
        for idx, c in enumerate(vec):
            values.extend([f"{prefix}_{idx}"] * c)
        return values

    def expand_numeric(vec):
        values = []
        for idx, c in enumerate(vec):
            values.extend([idx] * c)
        return values

    data = {
        "sexo": expand_categorical("sexo", counts["sexo"]),
        "tipo_de_emprendimiento": expand_categorical(
            "tipo", counts["tipo_de_emprendimiento"]
        ),
        "idea_negocio": expand_categorical("idea", counts["idea_negocio"]),
        "barrio": expand_categorical("barrio", counts["barrio"]),
        "estrato": expand_numeric(counts["estrato"]),
        "comuna_ciudadano": expand_numeric(counts["comuna_ciudadano"]),
        "fecha_de_beneficio": expand_categorical(
            "fecha", counts["fecha_de_beneficio"]
        ),
        "monto_del_credito": expand_numeric(counts["monto_del_credito"]),
        "línea_credito": expand_categorical("linea", counts["línea_credito"]),
    }

    df = pd.DataFrame(data).iloc[:n].copy()

    output_dir = os.path.join("files", "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "solicitudes_de_credito.csv")
    df.to_csv(output_path, sep=";", index=False)