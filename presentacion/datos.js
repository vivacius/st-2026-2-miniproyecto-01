// Instantánea de archivos reales; regenerar con generar_datos.py.
window.DATOS = {
  "metricas": [
    {
      "modelo": "SARIMAX(1, 0, 2)(1, 1, 1, 12) + exógenas",
      "decision": "Sin faltantes ni fechas duplicadas; se conservan los valores extremos observados",
      "RMSE": "1082.02",
      "MAE": "890.76",
      "MAPE": "1.16"
    },
    {
      "modelo": "SARIMA(1, 0, 2)(1, 1, 1, 12)",
      "decision": "Sin faltantes ni fechas duplicadas; se conservan los valores extremos observados",
      "RMSE": "1102.38",
      "MAE": "907.45",
      "MAPE": "1.17"
    },
    {
      "modelo": "estacional ingenuo",
      "decision": "Sin faltantes ni fechas duplicadas; se conservan los valores extremos observados",
      "RMSE": "2181.36",
      "MAE": "1904.4",
      "MAPE": "2.44"
    },
    {
      "modelo": "ingenuo",
      "decision": "Sin faltantes ni fechas duplicadas; se conservan los valores extremos observados",
      "RMSE": "8601.76",
      "MAE": "6875.18",
      "MAPE": "8.66"
    }
  ],
  "adf": [
    {
      "version": "Original",
      "estadistico": "-3.128227420192094",
      "p_valor": "0.09967459434978015",
      "rezagos": "14"
    },
    {
      "version": "Diferencia regular",
      "estadistico": "-3.6385162603578567",
      "p_valor": "0.005065964010936593",
      "rezagos": "13"
    },
    {
      "version": "Diferencia estacional",
      "estadistico": "-4.527515730406494",
      "p_valor": "0.00017531320881537967",
      "rezagos": "16"
    },
    {
      "version": "Ambas diferencias",
      "estadistico": "-5.690754977410129",
      "p_valor": "8.081711466049416e-07",
      "rezagos": "14"
    }
  ],
  "aic": [
    {
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6286.642274303555"
    },
    {
      "orden": "(2, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6288.052398439946"
    },
    {
      "orden": "(1, 0, 2)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6290.324946662842"
    },
    {
      "orden": "(2, 0, 2)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6290.725045483079"
    },
    {
      "orden": "(2, 0, 1)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6303.876573945704"
    },
    {
      "orden": "(2, 0, 1)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6308.672435522287"
    },
    {
      "orden": "(1, 0, 1)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6311.07069494253"
    },
    {
      "orden": "(1, 0, 1)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6315.2453742184325"
    },
    {
      "orden": "(2, 0, 2)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6324.976285136119"
    },
    {
      "orden": "(2, 0, 1)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6328.02742658394"
    },
    {
      "orden": "(2, 0, 0)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6342.950161046283"
    },
    {
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6350.471844416398"
    },
    {
      "orden": "(1, 0, 1)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6359.620905803149"
    },
    {
      "orden": "(2, 0, 0)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6362.264556736476"
    },
    {
      "orden": "(2, 0, 0)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6374.847255501561"
    },
    {
      "orden": "(1, 0, 0)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6455.133975087301"
    },
    {
      "orden": "(1, 0, 0)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6460.236123311197"
    },
    {
      "orden": "(1, 0, 0)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6467.602378304817"
    },
    {
      "orden": "(0, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6520.570000674819"
    },
    {
      "orden": "(1, 0, 2)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6534.419195932133"
    },
    {
      "orden": "(2, 0, 2)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6535.979562988065"
    },
    {
      "orden": "(2, 0, 1)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6567.888499559526"
    },
    {
      "orden": "(0, 0, 2)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6575.082681397615"
    },
    {
      "orden": "(1, 0, 1)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6579.949145851855"
    },
    {
      "orden": "(2, 0, 0)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6587.501157568562"
    },
    {
      "orden": "(0, 0, 2)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6625.36437757356"
    },
    {
      "orden": "(0, 0, 1)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6639.061602212006"
    },
    {
      "orden": "(0, 0, 1)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6640.490183098879"
    },
    {
      "orden": "(0, 0, 1)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6670.0784127812585"
    },
    {
      "orden": "(1, 0, 0)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6684.869615192245"
    },
    {
      "orden": "(0, 0, 0)",
      "estacional": "(1, 1, 1, 12)",
      "AIC": "6701.952383687678"
    },
    {
      "orden": "(0, 0, 0)",
      "estacional": "(1, 1, 0, 12)",
      "AIC": "6783.675806367377"
    },
    {
      "orden": "(0, 0, 2)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6786.952340412643"
    },
    {
      "orden": "(0, 0, 0)",
      "estacional": "(0, 1, 1, 12)",
      "AIC": "6797.293373826476"
    },
    {
      "orden": "(0, 0, 1)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "6897.495478791772"
    },
    {
      "orden": "(0, 0, 0)",
      "estacional": "(0, 1, 0, 12)",
      "AIC": "7060.500183433452"
    }
  ],
  "ljung": [
    {
      "rezago": "12",
      "lb_stat": "36.80058210120489",
      "lb_pvalue": "5.116744292016922e-06",
      "model_df": "5",
      "residuos_excluidos": "27"
    },
    {
      "rezago": "24",
      "lb_stat": "89.82256594590113",
      "lb_pvalue": "3.5661444725921036e-11",
      "model_df": "5",
      "residuos_excluidos": "27"
    }
  ],
  "convergencia": [
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 0)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "2",
      "AIC": "7060.500183433452"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 0)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "19",
      "AIC": "6797.293373826476"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 0)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "0",
      "AIC": "6783.675806367377"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 0)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6701.952383687678"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 1)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "5",
      "AIC": "6897.495478791772"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 1)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "24",
      "AIC": "6640.490183098879"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 1)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "25",
      "AIC": "6670.0784127812585"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 1)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6639.061602212006"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 2)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "24",
      "AIC": "6786.952340412643"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 2)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "26",
      "AIC": "6575.082681397615"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 2)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "27",
      "AIC": "6625.36437757356"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(0, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "49",
      "AIC": "6520.570000674819"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 0)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "1",
      "AIC": "6684.869615192245"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 0)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "7",
      "AIC": "6460.236123311197"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 0)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "7",
      "AIC": "6467.602378304817"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 0)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "11",
      "AIC": "6455.133975087301"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 1)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "9",
      "AIC": "6579.949145851855"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 1)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "11",
      "AIC": "6315.2453742184325"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 1)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "12",
      "AIC": "6359.620905803149"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 1)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "12",
      "AIC": "6311.07069494253"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "8",
      "AIC": "6534.419195932133"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "12",
      "AIC": "6290.324946662842"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "13",
      "AIC": "6350.471844416398"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6286.642274303555"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 0)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "1",
      "AIC": "6587.501157568562"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 0)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "6",
      "AIC": "6374.847255501561"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 0)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "10",
      "AIC": "6362.264556736476"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 0)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "12",
      "AIC": "6342.950161046283"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 1)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6567.888499559526"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 1)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6308.672435522287"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 1)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6328.02742658394"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 1)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "20",
      "AIC": "6303.876573945704"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 2)",
      "estacional": "(0, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6535.979562988065"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 2)",
      "estacional": "(0, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "21",
      "AIC": "6290.725045483079"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 2)",
      "estacional": "(1, 1, 0, 12)",
      "convergio": "True",
      "iteraciones": "21",
      "AIC": "6324.976285136119"
    },
    {
      "etapa": "rejilla",
      "origen": "2024-08",
      "orden": "(2, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "23",
      "AIC": "6288.052398439946"
    },
    {
      "etapa": "diagnostico",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6286.642274303555"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6286.642274303555"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2024-09",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "14",
      "AIC": "6303.030536384082"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2024-10",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "13",
      "AIC": "6319.354698149415"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2024-11",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6337.319570178638"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2024-12",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6353.9977669677755"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-01",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6370.781892289434"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-02",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6391.1718491632"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-03",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6408.19811152429"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-04",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6426.891507133795"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-05",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6443.3361691717555"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-06",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6460.0358770372995"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-07",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6476.195524408296"
    },
    {
      "etapa": "backtest SARIMA",
      "origen": "2025-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6492.8863798951625"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2024-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6271.829577745973"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2024-09",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6288.309360322199"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2024-10",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6305.0552241046935"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2024-11",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6322.365087890274"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2024-12",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6338.928269672881"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-01",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "14",
      "AIC": "6355.925845244853"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-02",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6377.32238741912"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-03",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6394.154056632651"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-04",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "18",
      "AIC": "6413.086584562574"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-05",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "17",
      "AIC": "6429.326242657797"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-06",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "16",
      "AIC": "6445.887133713339"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-07",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "13",
      "AIC": "6462.0441429806"
    },
    {
      "etapa": "backtest SARIMAX",
      "origen": "2025-08",
      "orden": "(1, 0, 2)",
      "estacional": "(1, 1, 1, 12)",
      "convergio": "True",
      "iteraciones": "15",
      "AIC": "6478.397416023842"
    }
  ],
  "fuentes": {
    "miniproyecto.py:preparar": {
      "archivo": "miniproyecto.py",
      "funcion": "preparar",
      "linea": 50,
      "codigo": "def preparar(serie):\n    serie = serie.copy()\n\n    if serie.isna().any():\n        raise ValueError(\n            \"Se encontraron valores faltantes no previstos\"\n        )\n\n    if not np.isfinite(serie.to_numpy()).all():\n        raise ValueError(\"Existen valores no finitos\")\n\n    return serie"
    },
    "miniproyecto.py:graficar_serie": {
      "archivo": "miniproyecto.py",
      "funcion": "graficar_serie",
      "linea": 63,
      "codigo": "def graficar_serie(serie):\n    figura, eje = plt.subplots(figsize=(9, 3.4))\n    eje.plot(serie.index, serie.to_numpy())\n    eje.set_title(f\"{VALOR}: serie mensual\")\n    eje.set_ylabel(VALOR)\n    figura.tight_layout()\n    figura.savefig(FIGURAS / \"serie.png\", dpi=120)\n    plt.close(figura)"
    },
    "miniproyecto.py:descomponer": {
      "archivo": "miniproyecto.py",
      "funcion": "descomponer",
      "linea": 76,
      "codigo": "def descomponer(serie):\n    \"\"\"Descomposición STL robusta con periodo estacional 12.\"\"\"\n\n    resultado = STL(\n        serie,\n        period=PERIODO,\n        robust=True\n    ).fit()\n\n    figura = resultado.plot()\n    figura.set_size_inches(11, 8)\n    figura.suptitle(\n        \"Descomposición STL de ventas mensuales\",\n        fontsize=14\n    )\n    figura.tight_layout()\n    figura.savefig(FIGURAS / \"stl.png\", dpi=150)\n    plt.close(figura)\n\n    estacional = resultado.seasonal\n    tendencia = resultado.trend\n    residuos = resultado.resid\n\n    promedio_mensual = estacional.groupby(\n        estacional.index.month\n    ).mean()\n\n    mes_alto = promedio_mensual.idxmax()\n    mes_bajo = promedio_mensual.idxmin()\n\n    fecha_residuo = residuos.abs().idxmax()\n\n    print(\"\\n--- DESCOMPOSICIÓN STL ---\")\n    print(f\"Tendencia inicial: {tendencia.iloc[0]:.2f}\")\n    print(f\"Tendencia final: {tendencia.iloc[-1]:.2f}\")\n    print(\n        f\"Mes estacional más alto: {mes_alto}, \"\n        f\"efecto: {promedio_mensual.loc[mes_alto]:.2f}\"\n    )\n    print(\n        f\"Mes estacional más bajo: {mes_bajo}, \"\n        f\"efecto: {promedio_mensual.loc[mes_bajo]:.2f}\"\n    )\n    print(\n        f\"Mayor residuo: {fecha_residuo:%Y-%m}, \"\n        f\"valor: {residuos.loc[fecha_residuo]:.2f}\"\n    )\n\n    return resultado"
    },
    "miniproyecto.py:estacionariedad": {
      "archivo": "miniproyecto.py",
      "funcion": "estacionariedad",
      "linea": 129,
      "codigo": "def estacionariedad(serie):\n    \"\"\"ADF de cuatro versiones y análisis ACF/PACF.\"\"\"\n\n    versiones = {\n        \"Original\": serie,\n        \"Diferencia regular\": serie.diff().dropna(),\n        \"Diferencia estacional\": serie.diff(12).dropna(),\n        \"Ambas diferencias\": (\n            serie.diff(12).diff().dropna()\n        )\n    }\n\n    print(\"\\n--- PRUEBAS ADF ---\")\n\n    resultados = []\n\n    for nombre, datos in versiones.items():\n\n        # La serie original puede presentar tendencia.\n        # En las diferencias usamos constante.\n        regression = \"ct\" if nombre == \"Original\" else \"c\"\n\n        prueba = adfuller(\n            datos,\n            regression=regression,\n            autolag=\"AIC\"\n        )\n\n        resultados.append({\n            \"version\": nombre,\n            \"estadistico\": prueba[0],\n            \"p_valor\": prueba[1],\n            \"rezagos\": prueba[2]\n        })\n\n        print(\n            f\"{nombre}: \"\n            f\"ADF={prueba[0]:.4f}, \"\n            f\"p={prueba[1]:.6f}, \"\n            f\"rezagos={prueba[2]}\"\n        )\n\n    tabla_adf = pd.DataFrame(resultados)\n    tabla_adf.to_csv(\n        RESULTADOS / \"adf.csv\",\n        index=False\n    )\n\n    # Selección provisional que debe contrastarse\n    # con ADF, ACF/PACF y la forma de la serie.\n    d = 0\n    D = 1\n\n    transformada = serie.diff(12).dropna()\n\n    figura, ejes = plt.subplots(\n        2, 1, figsize=(11, 7)\n    )\n\n    plot_acf(\n        transformada,\n        lags=36,\n        ax=ejes[0],\n        alpha=0.05\n    )\n\n    plot_pacf(\n        transformada,\n        lags=36,\n        ax=ejes[1],\n        alpha=0.05,\n        method=\"ywm\"\n    )\n\n    ejes[0].set_title(\"ACF - Diferencia estacional (D=1)\")\n    ejes[1].set_title(\"PACF - Diferencia estacional (D=1)\")\n\n    figura.tight_layout()\n    figura.savefig(\n        FIGURAS / \"acf_pacf.png\",\n        dpi=150\n    )\n    plt.close(figura)\n\n    print(f\"\\nOrden provisional: d={d}, D={D}\")\n    print(\"Revisar ADF y ACF/PACF antes de confirmar.\")\n\n    return d, D"
    },
    "miniproyecto.py:ajustar": {
      "archivo": "miniproyecto.py",
      "funcion": "ajustar",
      "linea": 222,
      "codigo": "def ajustar(modelo, etapa, origen):\n    \"\"\"Comprueba convergencia sin ocultar advertencias ni omitir orígenes.\"\"\"\n    ajuste = modelo.fit(disp=False, maxiter=100)\n    convergio = bool(ajuste.mle_retvals.get(\"converged\", False))\n    REGISTRO_AJUSTES.append({\n        \"etapa\": etapa, \"origen\": f\"{origen:%Y-%m}\",\n        \"orden\": modelo.order, \"estacional\": modelo.seasonal_order,\n        \"convergio\": convergio,\n        \"iteraciones\": ajuste.mle_retvals.get(\"iterations\"),\n        \"AIC\": ajuste.aic,\n    })\n    pd.DataFrame(REGISTRO_AJUSTES).to_csv(\n        RESULTADOS / \"convergencia.csv\", index=False\n    )\n    if not convergio and etapa != \"rejilla\":\n        raise RuntimeError(\n            f\"{etapa} no convergió en {origen:%Y-%m}; se detiene la ejecución \"\n            \"sin descartar el origen ni sustituir el modelo.\"\n        )\n    return ajuste"
    },
    "miniproyecto.py:elegir_sarima": {
      "archivo": "miniproyecto.py",
      "funcion": "elegir_sarima",
      "linea": 244,
      "codigo": "def elegir_sarima(serie, d, D):\n    \"\"\"Selecciona SARIMA por AIC y diagnostica residuos.\"\"\"\n\n    resultados = []\n\n    for p, q, P, Q in product(\n        [0, 1, 2], [0, 1, 2], [0, 1], [0, 1]\n    ):\n        orden = (p, d, q)\n        estacional = (P, D, Q, PERIODO)\n\n        try:\n            modelo = SARIMAX(\n                serie,\n                order=orden,\n                seasonal_order=estacional,\n                trend=\"n\",\n                enforce_stationarity=False,\n                enforce_invertibility=False\n            )\n\n            ajuste = ajustar(modelo, \"rejilla\", serie.index[-1])\n\n            if not ajuste.mle_retvals.get(\"converged\", False):\n                continue\n\n            if not np.isfinite(ajuste.aic):\n                continue\n\n            resultados.append({\n                \"orden\": orden,\n                \"estacional\": estacional,\n                \"AIC\": ajuste.aic\n            })\n\n        except (ValueError, np.linalg.LinAlgError) as error:\n            warnings.warn(f\"Rejilla {orden}{estacional}: {error}\", RuntimeWarning)\n            continue\n\n    if not resultados:\n        raise RuntimeError(\"Ningún SARIMA convergió.\")\n\n    tabla = pd.DataFrame(resultados).sort_values(\"AIC\")\n    tabla.to_csv(RESULTADOS / \"aic_sarima.csv\", index=False)\n\n    print(\"\\n--- MEJORES SARIMA POR AIC ---\")\n    print(tabla.head(10).to_string(index=False))\n\n    mejor = tabla.iloc[0]\n    orden = mejor[\"orden\"]\n    estacional = mejor[\"estacional\"]\n\n    modelo = SARIMAX(\n        serie,\n        order=orden,\n        seasonal_order=estacional,\n        trend=\"n\",\n        enforce_stationarity=False,\n        enforce_invertibility=False\n    )\n    ajuste = ajustar(modelo, \"diagnostico\", serie.index[-1])\n\n    # Se excluyen residuos de inicialización para\n    # no confundirlos con errores de pronóstico.\n    inicio = max(\n        int(ajuste.filter_results.nobs_diffuse),\n        int(ajuste.loglikelihood_burn)\n    )\n    residuos = ajuste.resid.iloc[inicio:].dropna()\n\n    model_df = orden[0] + orden[2] + estacional[0] + estacional[2]\n    print(f\"Residuos iniciales excluidos: {inicio}; model_df={model_df}\")\n    prueba = acorr_ljungbox(\n        residuos,\n        lags=[12, 24],\n        model_df=model_df,\n        return_df=True\n    )\n    prueba.index.name = \"rezago\"\n    prueba.assign(model_df=model_df, residuos_excluidos=inicio).to_csv(\n        RESULTADOS / \"ljung_box.csv\"\n    )\n\n    print(\"\\n--- LJUNG-BOX ---\")\n    print(prueba.to_string())\n\n    figura, ejes = plt.subplots(2, 1, figsize=(10, 7))\n\n    ejes[0].plot(residuos.index, residuos)\n    ejes[0].axhline(0, color=\"black\", linestyle=\"--\")\n    ejes[0].set_title(\"Residuos SARIMA\")\n\n    plot_acf(residuos, lags=36, ax=ejes[1])\n\n    figura.tight_layout()\n    figura.savefig(FIGURAS / \"residuos.png\", dpi=150)\n    plt.close(figura)\n\n    return orden, estacional"
    },
    "miniproyecto.py:modelo_sarima": {
      "archivo": "miniproyecto.py",
      "funcion": "modelo_sarima",
      "linea": 344,
      "codigo": "def modelo_sarima(orden, orden_estacional):\n    \"\"\"SARIMA ajustado exclusivamente con el entrenamiento.\"\"\"\n\n    def pronosticar(entrenamiento, h):\n        modelo = SARIMAX(\n            entrenamiento,\n            order=orden,\n            seasonal_order=orden_estacional,\n            trend=\"n\",\n            enforce_stationarity=False,\n            enforce_invertibility=False\n        )\n\n        ajuste = ajustar(modelo, \"backtest SARIMA\", entrenamiento.index[-1])\n\n        return ajuste.forecast(steps=h).to_numpy()\n\n    return pronosticar"
    },
    "miniproyecto.py:exogenas": {
      "archivo": "miniproyecto.py",
      "funcion": "exogenas",
      "linea": 363,
      "codigo": "def exogenas(serie):\n    \"\"\"Variable de calendario conocida anticipadamente.\"\"\"\n\n    fechas = pd.date_range(\n        start=serie.index.min(),\n        end=serie.index.max() + pd.DateOffset(months=12),\n        freq=\"MS\"\n    )\n\n    dias = []\n\n    for fecha in fechas:\n        inicio = fecha.date()\n        fin = (fecha + pd.offsets.MonthBegin(1)).date()\n\n        cantidad = np.busday_count(inicio, fin)\n        dias.append(cantidad)\n\n    x = pd.DataFrame(\n        {\"dias_lunes_viernes\": dias},\n        index=fechas\n    )\n\n    x.index.name = \"fecha\"\n\n    return x"
    },
    "miniproyecto.py:modelo_sarimax": {
      "archivo": "miniproyecto.py",
      "funcion": "modelo_sarimax",
      "linea": 389,
      "codigo": "def modelo_sarimax(orden, orden_estacional, x):\n    \"\"\"SARIMAX con exógena de calendario, sin fuga.\"\"\"\n\n    def pronosticar(entrenamiento, h):\n\n        x_entrenamiento = x.loc[\n            entrenamiento.index\n        ]\n\n        fechas_futuras = fechas_siguientes(\n            entrenamiento, h\n        )\n\n        x_futuro = x.loc[fechas_futuras]\n\n        modelo = SARIMAX(\n            entrenamiento,\n            exog=x_entrenamiento,\n            order=orden,\n            seasonal_order=orden_estacional,\n            trend=\"n\",\n            enforce_stationarity=False,\n            enforce_invertibility=False\n        )\n\n        ajuste = ajustar(modelo, \"backtest SARIMAX\", entrenamiento.index[-1])\n\n        pronostico = ajuste.forecast(\n            steps=h,\n            exog=x_futuro\n        )\n\n        return pronostico.to_numpy()\n\n    return pronosticar"
    },
    "miniproyecto.py:fila": {
      "archivo": "miniproyecto.py",
      "funcion": "fila",
      "linea": 429,
      "codigo": "def fila(nombre, serie, modelo):\n    _, promedio = backtest(serie, modelo)\n    return {\"modelo\": nombre, \"decision\": DECISION,\n            \"RMSE\": round(promedio[\"RMSE\"], 2), \"MAE\": round(promedio[\"MAE\"], 2),\n            \"MAPE\": round(promedio[\"MAPE\"], 2)}"
    },
    "miniproyecto.py:pendiente": {
      "archivo": "miniproyecto.py",
      "funcion": "pendiente",
      "linea": 436,
      "codigo": "def pendiente(parte, error):\n    print(f\"  pendiente: {parte} ({error})\")"
    },
    "miniproyecto.py:main": {
      "archivo": "miniproyecto.py",
      "funcion": "main",
      "linea": 440,
      "codigo": "def main():\n    REGISTRO_AJUSTES.clear()\n    cruda = cargar_serie(ARCHIVO, FECHA, VALOR)\n    print(f\"Serie: {len(cruda)} meses, de {cruda.index[0]:%Y-%m} a \"\n          f\"{cruda.index[-1]:%Y-%m}, {cruda.isna().sum()} vacíos\")\n    serie = preparar(cruda)\n    serie_seleccion = serie.iloc[:-24]\n    print(f\"Selección: {len(serie_seleccion)} meses hasta {serie_seleccion.index[-1]:%Y-%m}\")\n    graficar_serie(serie)\n\n    filas = [fila(\"ingenuo\", serie, ingenuo),\n             fila(\"estacional ingenuo\", serie,\n                  lambda t, h: estacional_ingenuo(t, h, PERIODO))]\n\n    try:\n        descomponer(serie)\n    except NotImplementedError as error:\n        pendiente(\"parte 2\", error)\n\n    try:\n        d, D = estacionariedad(serie_seleccion)\n    except NotImplementedError as error:\n        pendiente(\"parte 3\", error)\n        d = D = None\n\n    if d is not None:\n        try:\n            orden, estacional = elegir_sarima(\n                serie_seleccion, d, D\n            )\n            filas.append(fila(f\"SARIMA{orden}{estacional}\", serie,\n                              modelo_sarima(orden, estacional)))\n            x = exogenas(serie)\n            filas.append(fila(f\"SARIMAX{orden}{estacional} + exógenas\", serie,\n                              modelo_sarimax(orden, estacional, x)))\n        except NotImplementedError as error:\n            pendiente(\"parte 4\", error)\n\n    tabla = pd.DataFrame(filas).sort_values(\"RMSE\")\n    tabla.to_csv(RESULTADOS / \"metricas.csv\", index=False)\n    print(tabla.drop(columns=\"decision\").to_string(index=False))\n    print(\"Mejor modelo por RMSE:\", tabla.iloc[0][\"modelo\"])"
    },
    "comun.py:cargar_serie": {
      "archivo": "comun.py",
      "funcion": "cargar_serie",
      "linea": 16,
      "codigo": "def cargar_serie(archivo, fecha, valor):\n    \"\"\"Serie mensual con índice de fechas; los meses sin dato quedan en NaN.\"\"\"\n    tabla = pd.read_csv(RAIZ / archivo)\n    tabla.index = pd.to_datetime(tabla[fecha])\n    serie = tabla[valor].astype(float).asfreq(\"MS\")\n    serie.name = valor\n    return serie"
    },
    "comun.py:fechas_siguientes": {
      "archivo": "comun.py",
      "funcion": "fechas_siguientes",
      "linea": 25,
      "codigo": "def fechas_siguientes(entrenamiento, h):\n    \"\"\"Las h fechas mensuales que siguen al último dato de entrenamiento.\"\"\"\n    return pd.date_range(entrenamiento.index[-1], periods=h + 1, freq=\"MS\")[1:]"
    },
    "comun.py:mae": {
      "archivo": "comun.py",
      "funcion": "mae",
      "linea": 32,
      "codigo": "def mae(y, y_hat):\n    y, y_hat = np.asarray(y), np.asarray(y_hat)\n    return np.mean(np.abs(y - y_hat))"
    },
    "comun.py:rmse": {
      "archivo": "comun.py",
      "funcion": "rmse",
      "linea": 37,
      "codigo": "def rmse(y, y_hat):\n    y, y_hat = np.asarray(y), np.asarray(y_hat)\n    return np.sqrt(np.mean((y - y_hat) ** 2))"
    },
    "comun.py:mape": {
      "archivo": "comun.py",
      "funcion": "mape",
      "linea": 42,
      "codigo": "def mape(y, y_hat):\n    y, y_hat = np.asarray(y), np.asarray(y_hat)\n    return 100 * np.mean(np.abs((y - y_hat) / y))"
    },
    "comun.py:ingenuo": {
      "archivo": "comun.py",
      "funcion": "ingenuo",
      "linea": 49,
      "codigo": "def ingenuo(entrenamiento, h):\n    \"\"\"Repite el último valor observado durante h meses.\"\"\"\n    return np.repeat(entrenamiento.iloc[-1], h)"
    },
    "comun.py:estacional_ingenuo": {
      "archivo": "comun.py",
      "funcion": "estacional_ingenuo",
      "linea": 54,
      "codigo": "def estacional_ingenuo(entrenamiento, h, m=12):\n    \"\"\"Repite el mismo mes del último año observado.\"\"\"\n    ultimo_anio = entrenamiento.iloc[-m:].to_numpy()\n    return np.resize(ultimo_anio, h)"
    },
    "comun.py:backtest": {
      "archivo": "comun.py",
      "funcion": "backtest",
      "linea": 62,
      "codigo": "def backtest(serie, modelo, n_prueba=24, h=12):\n    \"\"\"Origen móvil sobre los últimos n_prueba meses, horizonte de 1 a h.\n\n    `modelo(entrenamiento, h)` recibe solo los datos hasta el origen y\n    devuelve h pronósticos. Nada posterior al origen entra al modelo.\n    Devuelve las métricas por origen y su promedio.\n    \"\"\"\n    filas = []\n    primero = len(serie) - n_prueba\n    for corte in range(primero, len(serie) - h + 1):\n        entrenamiento = serie.iloc[:corte]\n        real = serie.iloc[corte:corte + h].to_numpy()\n        pronostico = np.asarray(modelo(entrenamiento, h))\n        filas.append({\"origen\": serie.index[corte - 1],\n                      \"RMSE\": rmse(real, pronostico),\n                      \"MAE\": mae(real, pronostico),\n                      \"MAPE\": mape(real, pronostico)})\n    por_origen = pd.DataFrame(filas)\n    return por_origen, por_origen[[\"RMSE\", \"MAE\", \"MAPE\"]].mean()"
    }
  },
  "sha256": {
    "miniproyecto.py": "8c5fc1ec62a54b00e31dbe325b649ff515a7c07405ad4122f9f08d73e36b8789",
    "comun.py": "2f0745122a6e14dc4c7f544156127efeb26df401c143a393d5f419adf1609467",
    "docs/informe.md": "6422126004477cdb48eeb8eb3be4472d90dd3ce798d8bdf7b5cb36d8f6fd7fb4",
    "datos/ventas_mensuales.csv": "d4f474efdc5107797ce85e348bdb0588d036f3d8dded90588cbbf37a34ffd5fe",
    "resultados/metricas.csv": "ab7193950d1e6c9954558fa76e6906d087762085f169fc6c0c2a7843b5b2dc27",
    "resultados/adf.csv": "6fde62919d928bf631469586355fe48ab8b9ec1da54df896022e6c491489bbbb",
    "resultados/aic_sarima.csv": "d1b273b20da4f4e6ae346a0aad1eade03bb996b803041424222c61771f7bde12",
    "resultados/ljung_box.csv": "9fecc69de7c45562f33067f9160c1c2e37078dcdb924f345df2b097c2a427cf0",
    "resultados/convergencia.csv": "e6e295b086a0a4e40a89ae87b31c2d86e2ea8d77a41023b932c62065e95b5ff6",
    "figuras/serie.png": "f139e92b90cb2f526aecb880bc9231363b032a4e426838743a1612941e97b480",
    "figuras/stl.png": "1efede3cafca62e40f40e71465d12a4e881a89aa3c0d968927acdd55f5acbdda",
    "figuras/acf_pacf.png": "8368299dd73dcf527edaf2dccb652709ef6fcdf6342071711bc7d1274a91dc5b",
    "figuras/residuos.png": "1f9651f23202ce6f28552c4d8c1786ac3a8653115b76b015df810659d83ad333"
  }
};
