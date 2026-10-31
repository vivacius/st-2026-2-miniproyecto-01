"""Actualiza la instantánea de la presentación sin ajustar modelos.

Ejecutar desde cualquier carpeta: python presentacion/generar_datos.py
Solo lee el repositorio y escribe presentacion/datos.js.
"""
import ast
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent


def tabla(nombre):
    with (RAIZ / "resultados" / nombre).open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


fuentes = {}
for archivo in ("miniproyecto.py", "comun.py"):
    texto = (RAIZ / archivo).read_text(encoding="utf-8")
    for nodo in ast.parse(texto).body:
        if isinstance(nodo, ast.FunctionDef):
            fuentes[f"{archivo}:{nodo.name}"] = {
                "archivo": archivo, "funcion": nodo.name, "linea": nodo.lineno,
                "codigo": ast.get_source_segment(texto, nodo),
            }

archivos = ["miniproyecto.py", "comun.py", "docs/informe.md",
            "datos/ventas_mensuales.csv"]
archivos += [f"resultados/{n}.csv" for n in
             ("metricas", "adf", "aic_sarima", "ljung_box", "convergencia")]
archivos += [f"figuras/{n}.png" for n in ("serie", "stl", "acf_pacf", "residuos")]
datos = {"metricas": tabla("metricas.csv"), "adf": tabla("adf.csv"),
         "aic": tabla("aic_sarima.csv"), "ljung": tabla("ljung_box.csv"),
         "convergencia": tabla("convergencia.csv"), "fuentes": fuentes,
         "sha256": {n: hashlib.sha256((RAIZ / n).read_bytes()).hexdigest()
                    for n in archivos}}
(BASE / "datos.js").write_text(
    "// Instantánea de archivos reales; regenerar con generar_datos.py.\n"
    "window.DATOS = " + json.dumps(datos, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8")
print("Instantánea actualizada. No se ejecutaron modelos.")
