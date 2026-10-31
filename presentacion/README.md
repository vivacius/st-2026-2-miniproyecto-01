# Presentación local del Miniproyecto 1

Abre `index.html` con doble clic en Chrome, Edge o Firefox. No requiere servidor,
instalación ni conexión. Conserva esta carpeta dentro del repositorio: las cuatro
figuras se cargan desde `../figuras/`.

- Flechas izquierda/derecha, botones o índice: navegar.
- N: mostrar u ocultar notas del expositor (también son visibles al público).
- F: pantalla completa; F11 es la alternativa del navegador.
- Iniciar/Pausar/Continuar y ↺: controlar el cronómetro. No cambia al navegar.
- Clic sobre una figura: ampliar; Zoom 150 % permite explorar con desplazamiento.
- Esc: cerrar el visor de figuras o código.
- Botones de código: mostrar funciones literales con archivo y línea de origen.
- En la pantalla 7, el control deslizante recorre los 13 orígenes reales del protocolo;
  solo ilustra las ventanas temporales, no vuelve a entrenar modelos.

El tiempo sugerido por pantalla suma **10 minutos y 40 segundos**. El reloj cambia
de color a los 12 y 15 minutos. La guía original asigna 7 minutos a la exposición
y 8 a preguntas; adapta la exposición a esa distribución si el docente la mantiene.
El HTML es apoyo: la entrega evaluable sigue siendo `docs/informe.md`.

## Datos y trazabilidad

`datos.js` contiene una instantánea de los CSV reales de métricas, ADF, AIC,
Ljung–Box y convergencia, además de las funciones extraídas literalmente mediante
AST de los dos archivos Python. Las tablas y las barras de RMSE se construyen con
esa instantánea; las cifras STL proceden del informe validado. No se descargan
fuentes tipográficas ni librerías externas. No se usa `fetch`, evitando restricciones
de lectura de CSV al abrir mediante `file://`.

Si cambian los resultados, actualiza la instantánea sin entrenar modelos:

```powershell
python presentacion/generar_datos.py
```

Este script solo escribe `presentacion/datos.js`. Conserva hashes SHA-256 de los
archivos fuente para comprobar que la instantánea corresponde al repositorio.
Después de regenerar, revisa también los textos explicativos y cifras STL.

El botón para abrir un archivo `.py` puede mostrarlo o descargarlo según el navegador;
el visor interno de código funciona sin depender de esa asociación.
