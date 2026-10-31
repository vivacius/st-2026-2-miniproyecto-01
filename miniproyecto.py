"""Miniproyecto 1: la serie del grupo, de las líneas base al mejor modelo clásico.

Se corre de principio a fin con

    python miniproyecto.py

y deja las figuras en figuras/ y la tabla en resultados/metricas.csv. Las
partes marcadas con TODO las completa el grupo; mientras falten, el guion las
reporta como pendientes y sigue. El informe, docs/informe.md, cita las cifras
y las figuras que produce este guion.
"""
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from comun import (RAIZ, backtest, cargar_serie, estacional_ingenuo,  # noqa: E402
                   fechas_siguientes, ingenuo)
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from itertools import product
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
REGISTRO_AJUSTES = []
FIGURAS = RAIZ / "figuras"
RESULTADOS = RAIZ / "resultados"
FIGURAS.mkdir(exist_ok=True)
RESULTADOS.mkdir(exist_ok=True)

# ============================================================
# 1. La serie
# ============================================================
# Cambie estos cuatro datos por los de la serie del grupo y documente la
# fuente en datos/README.md. La serie de ejemplo solo sirve para probar que
# el guion corre.
ARCHIVO = "datos/ventas_mensuales.csv"
FECHA = "observation_date"
VALOR = "MRTSSM452USN"
PERIODO = 12

DECISION = (
    "Sin faltantes ni fechas duplicadas; "
    "se conservan los valores extremos observados"
)
def preparar(serie):
    serie = serie.copy()

    if serie.isna().any():
        raise ValueError(
            "Se encontraron valores faltantes no previstos"
        )

    if not np.isfinite(serie.to_numpy()).all():
        raise ValueError("Existen valores no finitos")

    return serie

def graficar_serie(serie):
    figura, eje = plt.subplots(figsize=(9, 3.4))
    eje.plot(serie.index, serie.to_numpy())
    eje.set_title(f"{VALOR}: serie mensual")
    eje.set_ylabel(VALOR)
    figura.tight_layout()
    figura.savefig(FIGURAS / "serie.png", dpi=120)
    plt.close(figura)


# ============================================================
# 2. Descomposición
# ============================================================
def descomponer(serie):
    """Descomposición STL robusta con periodo estacional 12."""

    resultado = STL(
        serie,
        period=PERIODO,
        robust=True
    ).fit()

    figura = resultado.plot()
    figura.set_size_inches(11, 8)
    figura.suptitle(
        "Descomposición STL de ventas mensuales",
        fontsize=14
    )
    figura.tight_layout()
    figura.savefig(FIGURAS / "stl.png", dpi=150)
    plt.close(figura)

    estacional = resultado.seasonal
    tendencia = resultado.trend
    residuos = resultado.resid

    promedio_mensual = estacional.groupby(
        estacional.index.month
    ).mean()

    mes_alto = promedio_mensual.idxmax()
    mes_bajo = promedio_mensual.idxmin()

    fecha_residuo = residuos.abs().idxmax()

    print("\n--- DESCOMPOSICIÓN STL ---")
    print(f"Tendencia inicial: {tendencia.iloc[0]:.2f}")
    print(f"Tendencia final: {tendencia.iloc[-1]:.2f}")
    print(
        f"Mes estacional más alto: {mes_alto}, "
        f"efecto: {promedio_mensual.loc[mes_alto]:.2f}"
    )
    print(
        f"Mes estacional más bajo: {mes_bajo}, "
        f"efecto: {promedio_mensual.loc[mes_bajo]:.2f}"
    )
    print(
        f"Mayor residuo: {fecha_residuo:%Y-%m}, "
        f"valor: {residuos.loc[fecha_residuo]:.2f}"
    )

    return resultado
# ============================================================
# 3. Estacionariedad e identificación
# ============================================================

def estacionariedad(serie):
    """ADF de cuatro versiones y análisis ACF/PACF."""

    versiones = {
        "Original": serie,
        "Diferencia regular": serie.diff().dropna(),
        "Diferencia estacional": serie.diff(12).dropna(),
        "Ambas diferencias": (
            serie.diff(12).diff().dropna()
        )
    }

    print("\n--- PRUEBAS ADF ---")

    resultados = []

    for nombre, datos in versiones.items():

        # La serie original puede presentar tendencia.
        # En las diferencias usamos constante.
        regression = "ct" if nombre == "Original" else "c"

        prueba = adfuller(
            datos,
            regression=regression,
            autolag="AIC"
        )

        resultados.append({
            "version": nombre,
            "estadistico": prueba[0],
            "p_valor": prueba[1],
            "rezagos": prueba[2]
        })

        print(
            f"{nombre}: "
            f"ADF={prueba[0]:.4f}, "
            f"p={prueba[1]:.6f}, "
            f"rezagos={prueba[2]}"
        )

    tabla_adf = pd.DataFrame(resultados)
    tabla_adf.to_csv(
        RESULTADOS / "adf.csv",
        index=False
    )

    # Selección provisional que debe contrastarse
    # con ADF, ACF/PACF y la forma de la serie.
    d = 0
    D = 1

    transformada = serie.diff(12).dropna()

    figura, ejes = plt.subplots(
        2, 1, figsize=(11, 7)
    )

    plot_acf(
        transformada,
        lags=36,
        ax=ejes[0],
        alpha=0.05
    )

    plot_pacf(
        transformada,
        lags=36,
        ax=ejes[1],
        alpha=0.05,
        method="ywm"
    )

    ejes[0].set_title("ACF - Diferencia estacional (D=1)")
    ejes[1].set_title("PACF - Diferencia estacional (D=1)")

    figura.tight_layout()
    figura.savefig(
        FIGURAS / "acf_pacf.png",
        dpi=150
    )
    plt.close(figura)

    print(f"\nOrden provisional: d={d}, D={D}")
    print("Revisar ADF y ACF/PACF antes de confirmar.")

    return d, D
# ============================================================
# 4. Modelos clásicos
# ============================================================
# Cada modelo es una función modelo(entrenamiento, h) que devuelve h
# pronósticos y solo usa `entrenamiento`. Así entra al backtest común.
def ajustar(modelo, etapa, origen):
    """Comprueba convergencia sin ocultar advertencias ni omitir orígenes."""
    ajuste = modelo.fit(disp=False, maxiter=100)
    convergio = bool(ajuste.mle_retvals.get("converged", False))
    REGISTRO_AJUSTES.append({
        "etapa": etapa, "origen": f"{origen:%Y-%m}",
        "orden": modelo.order, "estacional": modelo.seasonal_order,
        "convergio": convergio,
        "iteraciones": ajuste.mle_retvals.get("iterations"),
        "AIC": ajuste.aic,
    })
    pd.DataFrame(REGISTRO_AJUSTES).to_csv(
        RESULTADOS / "convergencia.csv", index=False
    )
    if not convergio and etapa != "rejilla":
        raise RuntimeError(
            f"{etapa} no convergió en {origen:%Y-%m}; se detiene la ejecución "
            "sin descartar el origen ni sustituir el modelo."
        )
    return ajuste


def elegir_sarima(serie, d, D):
    """Selecciona SARIMA por AIC y diagnostica residuos."""

    resultados = []

    for p, q, P, Q in product(
        [0, 1, 2], [0, 1, 2], [0, 1], [0, 1]
    ):
        orden = (p, d, q)
        estacional = (P, D, Q, PERIODO)

        try:
            modelo = SARIMAX(
                serie,
                order=orden,
                seasonal_order=estacional,
                trend="n",
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            ajuste = ajustar(modelo, "rejilla", serie.index[-1])

            if not ajuste.mle_retvals.get("converged", False):
                continue

            if not np.isfinite(ajuste.aic):
                continue

            resultados.append({
                "orden": orden,
                "estacional": estacional,
                "AIC": ajuste.aic
            })

        except (ValueError, np.linalg.LinAlgError) as error:
            warnings.warn(f"Rejilla {orden}{estacional}: {error}", RuntimeWarning)
            continue

    if not resultados:
        raise RuntimeError("Ningún SARIMA convergió.")

    tabla = pd.DataFrame(resultados).sort_values("AIC")
    tabla.to_csv(RESULTADOS / "aic_sarima.csv", index=False)

    print("\n--- MEJORES SARIMA POR AIC ---")
    print(tabla.head(10).to_string(index=False))

    mejor = tabla.iloc[0]
    orden = mejor["orden"]
    estacional = mejor["estacional"]

    modelo = SARIMAX(
        serie,
        order=orden,
        seasonal_order=estacional,
        trend="n",
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    ajuste = ajustar(modelo, "diagnostico", serie.index[-1])

    # Se excluyen residuos de inicialización para
    # no confundirlos con errores de pronóstico.
    inicio = max(
        int(ajuste.filter_results.nobs_diffuse),
        int(ajuste.loglikelihood_burn)
    )
    residuos = ajuste.resid.iloc[inicio:].dropna()

    model_df = orden[0] + orden[2] + estacional[0] + estacional[2]
    print(f"Residuos iniciales excluidos: {inicio}; model_df={model_df}")
    prueba = acorr_ljungbox(
        residuos,
        lags=[12, 24],
        model_df=model_df,
        return_df=True
    )
    prueba.index.name = "rezago"
    prueba.assign(model_df=model_df, residuos_excluidos=inicio).to_csv(
        RESULTADOS / "ljung_box.csv"
    )

    print("\n--- LJUNG-BOX ---")
    print(prueba.to_string())

    figura, ejes = plt.subplots(2, 1, figsize=(10, 7))

    ejes[0].plot(residuos.index, residuos)
    ejes[0].axhline(0, color="black", linestyle="--")
    ejes[0].set_title("Residuos SARIMA")

    plot_acf(residuos, lags=36, ax=ejes[1])

    figura.tight_layout()
    figura.savefig(FIGURAS / "residuos.png", dpi=150)
    plt.close(figura)

    return orden, estacional

def modelo_sarima(orden, orden_estacional):
    """SARIMA ajustado exclusivamente con el entrenamiento."""

    def pronosticar(entrenamiento, h):
        modelo = SARIMAX(
            entrenamiento,
            order=orden,
            seasonal_order=orden_estacional,
            trend="n",
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        ajuste = ajustar(modelo, "backtest SARIMA", entrenamiento.index[-1])

        return ajuste.forecast(steps=h).to_numpy()

    return pronosticar

def exogenas(serie):
    """Variable de calendario conocida anticipadamente."""

    fechas = pd.date_range(
        start=serie.index.min(),
        end=serie.index.max() + pd.DateOffset(months=12),
        freq="MS"
    )

    dias = []

    for fecha in fechas:
        inicio = fecha.date()
        fin = (fecha + pd.offsets.MonthBegin(1)).date()

        cantidad = np.busday_count(inicio, fin)
        dias.append(cantidad)

    x = pd.DataFrame(
        {"dias_lunes_viernes": dias},
        index=fechas
    )

    x.index.name = "fecha"

    return x
def modelo_sarimax(orden, orden_estacional, x):
    """SARIMAX con exógena de calendario, sin fuga."""

    def pronosticar(entrenamiento, h):

        x_entrenamiento = x.loc[
            entrenamiento.index
        ]

        fechas_futuras = fechas_siguientes(
            entrenamiento, h
        )

        x_futuro = x.loc[fechas_futuras]

        modelo = SARIMAX(
            entrenamiento,
            exog=x_entrenamiento,
            order=orden,
            seasonal_order=orden_estacional,
            trend="n",
            enforce_stationarity=False,
            enforce_invertibility=False
        )

        ajuste = ajustar(modelo, "backtest SARIMAX", entrenamiento.index[-1])

        pronostico = ajuste.forecast(
            steps=h,
            exog=x_futuro
        )

        return pronostico.to_numpy()

    return pronosticar

# ============================================================
# 5. La tabla de métricas
# ============================================================

def fila(nombre, serie, modelo):
    _, promedio = backtest(serie, modelo)
    return {"modelo": nombre, "decision": DECISION,
            "RMSE": round(promedio["RMSE"], 2), "MAE": round(promedio["MAE"], 2),
            "MAPE": round(promedio["MAPE"], 2)}


def pendiente(parte, error):
    print(f"  pendiente: {parte} ({error})")


def main():
    REGISTRO_AJUSTES.clear()
    cruda = cargar_serie(ARCHIVO, FECHA, VALOR)
    print(f"Serie: {len(cruda)} meses, de {cruda.index[0]:%Y-%m} a "
          f"{cruda.index[-1]:%Y-%m}, {cruda.isna().sum()} vacíos")
    serie = preparar(cruda)
    serie_seleccion = serie.iloc[:-24]
    print(f"Selección: {len(serie_seleccion)} meses hasta {serie_seleccion.index[-1]:%Y-%m}")
    graficar_serie(serie)

    filas = [fila("ingenuo", serie, ingenuo),
             fila("estacional ingenuo", serie,
                  lambda t, h: estacional_ingenuo(t, h, PERIODO))]

    try:
        descomponer(serie)
    except NotImplementedError as error:
        pendiente("parte 2", error)

    try:
        d, D = estacionariedad(serie_seleccion)
    except NotImplementedError as error:
        pendiente("parte 3", error)
        d = D = None

    if d is not None:
        try:
            orden, estacional = elegir_sarima(
                serie_seleccion, d, D
            )
            filas.append(fila(f"SARIMA{orden}{estacional}", serie,
                              modelo_sarima(orden, estacional)))
            x = exogenas(serie)
            filas.append(fila(f"SARIMAX{orden}{estacional} + exógenas", serie,
                              modelo_sarimax(orden, estacional, x)))
        except NotImplementedError as error:
            pendiente("parte 4", error)

    tabla = pd.DataFrame(filas).sort_values("RMSE")
    tabla.to_csv(RESULTADOS / "metricas.csv", index=False)
    print(tabla.drop(columns="decision").to_string(index=False))
    print("Mejor modelo por RMSE:", tabla.iloc[0]["modelo"])


if __name__ == "__main__":
    main()
