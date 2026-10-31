from pathlib import Path
import ast, csv, hashlib, json, math, textwrap
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
TMP=Path(__file__).resolve().parent
OUT=ROOT/'docs/guia_estudio_sustentacion.docx'
def csvread(name):
    with (ROOT/'resultados'/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
metrics=csvread('metricas.csv'); adf=csvread('adf.csv'); aic=csvread('aic_sarima.csv'); lb=csvread('ljung_box.csv'); conv=csvread('convergencia.csv')
protected=[ROOT/'miniproyecto.py',ROOT/'comun.py',ROOT/'docs/informe.md',*list((ROOT/'datos').glob('*')),*list((ROOT/'figuras').glob('*.png')),*list((ROOT/'resultados').glob('*.csv'))]
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
(TMP/'hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
def fmt(x,n=2):return f'{float(x):,.{n}f}'.replace(',','@').replace('.',',').replace('@','.')
def short(name):return 'SARIMAX' if name.startswith('SARIMAX') else 'SARIMA' if name.startswith('SARIMA') else name.capitalize()
mx,ma,base,naive=metrics
improvements={m:100*(1-float(mx[m])/float(base[m])) for m in ['RMSE','MAE','MAPE']}
inc=100*(1-float(mx['RMSE'])/float(ma['RMSE']))
source={}
for name in ['miniproyecto.py','comun.py']:
    raw=(ROOT/name).read_text(encoding='utf-8')
    for n in ast.parse(raw).body:
        if isinstance(n,ast.FunctionDef):source[name,n.name]=(n.lineno,ast.get_source_segment(raw,n))

doc=Document(); sec=doc.sections[0]
sec.page_width=Cm(21); sec.page_height=Cm(29.7)
sec.top_margin=Cm(1.8);sec.bottom_margin=Cm(1.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
sec.header_distance=Cm(.8);sec.footer_distance=Cm(.8)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Heading 3','Caption']:
    st=doc.styles[name];st.font.name='Calibri';st.font.color.rgb=RGBColor(0,0,0)
normal=doc.styles['Normal'];normal.font.size=Pt(10.5);normal.paragraph_format.space_after=Pt(7);normal.paragraph_format.line_spacing=1.12
for name,size in [('Title',26),('Heading 1',19),('Heading 2',13),('Heading 3',11),('Subtitle',13),('Caption',9)]:doc.styles[name].font.size=Pt(size)
for name in ['Heading 1','Heading 2','Heading 3']:
    doc.styles[name].paragraph_format.space_before=Pt(12);doc.styles[name].paragraph_format.space_after=Pt(8)
    doc.styles[name].paragraph_format.keep_with_next=True
sec.header.paragraphs[0].text='SERIES TEMPORALES    |    GUÍA DE ESTUDIO Y SUSTENTACIÓN'
sec.header.paragraphs[0].runs[0].font.size=Pt(8)
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('Santiago Correa Campaña   ·   ')
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
for r in footer.runs:r.font.size=Pt(8)
doc.core_properties.title='Guía de estudio y sustentación del Miniproyecto 1 de Series Temporales'
doc.core_properties.author='Santiago Correa Campaña'
doc.core_properties.subject='Explicación del código y defensa de resultados verificables'

def p(text='',boldlead=None):
    par=doc.add_paragraph()
    if boldlead and text.startswith(boldlead):par.add_run(boldlead).bold=True;par.add_run(text[len(boldlead):])
    else:par.add_run(text)
    return par
def h(text,level=2):doc.add_heading(text,level)
def page(title,level=1):
    doc.add_page_break();h(title,level)
def bullets(items):
    for item in items:
        par=doc.add_paragraph(style='List Bullet');par.add_run(item)
def table(headers,rows,widths=None):
    t=doc.add_table(rows=1,cols=len(headers));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    widths=widths or [17/len(headers)]*len(headers)
    for c,w in zip(t.columns,widths):c.width=Cm(w)
    for i,v in enumerate(headers):t.rows[0].cells[i].text=str(v)
    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
    for row in rows:
        cells=t.add_row().cells
        for c,v in zip(cells,row):c.text=str(v)
    for ri,row in enumerate(t.rows):
        pr=row._tr.get_or_add_trPr();pr.append(OxmlElement('w:cantSplit'))
        for ci,c in enumerate(row.cells):
            c.width=Cm(widths[ci]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            tc=c._tc.get_or_add_tcPr()
            borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right']:
                el=OxmlElement('w:'+edge);el.set(qn('w:val'),'single');el.set(qn('w:sz'),'4');el.set(qn('w:color'),'D9D9D9');borders.append(el)
            tc.append(borders)
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'20364D' if ri==0 else ('EEF3F7' if ri%2 else 'FFFFFF'));tc.append(shade)
            margins=OxmlElement('w:tcMar')
            for edge in ['top','left','bottom','right']:
                el=OxmlElement('w:'+edge);el.set(qn('w:w'),'85');el.set(qn('w:type'),'dxa');margins.append(el)
            tc.append(margins)
            for par in c.paragraphs:
                par.paragraph_format.space_after=Pt(3);par.paragraph_format.space_before=Pt(3)
                if ci>0:par.alignment=WD_ALIGN_PARAGRAPH.CENTER
                for run in par.runs:
                    run.font.size=Pt(9.5)
                    if ri==0:run.bold=True;run.font.color.rgb=RGBColor(255,255,255)
    p()
    return t
def picture(path,caption,width=17):
    par=doc.add_paragraph();par.paragraph_format.keep_with_next=True
    shape=par.add_run().add_picture(str(path),width=Cm(width));shape._inline.docPr.set('descr',caption)
    doc.add_paragraph(caption,style='Caption')
def code(file,fn,start=None,end=None):
    line,raw=source[file,fn];lines=raw.splitlines()
    if start:
        lo=next(i for i,l in enumerate(lines) if start in l);hi=next(i for i in range(lo,len(lines)) if end in lines[i])+1 if end else len(lines)
        raw='\n'.join(lines[lo:hi]);line+=lo
    doc.add_paragraph(f'Código real · {file} · {fn}() · desde la línea {line}',style='Caption')
    par=doc.add_paragraph();par.paragraph_format.space_after=Pt(8);par.paragraph_format.line_spacing=1
    for i,l in enumerate(raw.splitlines()):
        run=par.add_run(('\n' if i else '')+l);run.font.name='Consolas';run.font.size=Pt(8)
    return raw
def equation(text):
    par=doc.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    om=OxmlElement('m:oMath');mr=OxmlElement('m:r');mt=OxmlElement('m:t');mt.text=text;mr.append(mt);om.append(mr);par._p.append(om)
def qa(q,a):h(q,3);p(a)

# Figures created solely from CSV values and the existing backtest protocol.
fontpath='C:/Windows/Fonts/arial.ttf'
def font(n):return ImageFont.truetype(fontpath,n)
im=Image.new('RGB',(1600,780),'white');draw=ImageDraw.Draw(im)
draw.text((45,25),'RMSE por modelo',font=font(38),fill='#152e46')
x0,x1,y0=360,1430,120
for tick in [0,2000,4000,6000,8000]:
    x=x0+(x1-x0)*tick/9000;draw.line((x,100,x,650),fill='#d9e1e8',width=2);draw.text((x-25,670),str(tick),font=font(24),fill='#415266')
for i,r in enumerate(metrics):
    y=y0+i*125;v=float(r['RMSE']);draw.text((35,y+19),short(r['modelo']),font=font(28),fill='#172b3e')
    end=x0+(x1-x0)*v/9000;draw.rectangle((x0,y,end,y+75),fill='#257e71' if i==0 else '#4e759b');draw.text((end+12,y+21),fmt(v),font=font(25),fill='#172b3e')
draw.text((640,724),'Millones de dólares · menor es mejor',font=font(26),fill='#415266');im.save(TMP/'rmse.png')
im=Image.new('RGB',(1600,1000),'white');draw=ImageDraw.Draw(im)
draw.text((30,15),'Trece orígenes sobre los últimos veinticuatro meses',font=font(34),fill='#152e46')
draw.text((30,65),'Entrenamiento previo: enero de 1992 a agosto de 2024 en el primer origen',font=font(23),fill='#415266')
startx,step,starty=280,51,175
for j in range(24):
    month=(8+j)%12+1;year=2024+(8+j)//12
    draw.text((startx+j*step+5,120),f'{month:02d}',font=font(18),fill='black')
    if j in [0,4,16]:draw.text((startx+j*step,92),str(year),font=font(18),fill='#415266')
for i in range(13):
    month=(7+i)%12+1;year=2024+(7+i)//12;y=starty+i*52
    draw.text((30,y+9),f'{i+1:02d}  {year}-{month:02d}',font=font(23),fill='#152e46')
    for j in range(24):
        color='#7699b9' if j<i else '#319385' if j<i+12 else '#e6ebef'
        draw.rectangle((startx+j*step,y,startx+(j+1)*step-4,y+35),fill=color)
for k,(color,label) in enumerate([('#7699b9','Ya observado'),('#319385','12 meses evaluados'),('#e6ebef','Posterior a la ventana')]):
    x=40+k*500;draw.rectangle((x,900,x+25,925),fill=color);draw.text((x+38,895),label,font=font(24),fill='#152e46')
draw.text((30,955),'Columnas: septiembre de 2024 a agosto de 2026. Cada fila reajusta con todo el pasado disponible.',font=font(22),fill='#415266');im.save(TMP/'backtest.png')

doc.add_paragraph('Guía de estudio y sustentación del Miniproyecto 1 de Series Temporales',style='Title')
doc.add_paragraph('Comprender el código y defender los resultados',style='Subtitle')
p('Santiago Correa Campaña · 551476\nMaestría en Inteligencia Artificial y Ciencia de Datos\nUniversidad Autónoma de Occidente · 2026 II')
h('Propósito de esta guía')
p('Esta guía prepara una explicación con Python abierto en VS Code. Recorre el problema, las decisiones estadísticas y la evaluación real del repositorio. No sustituye docs/informe.md ni es un documento adicional exigido para la entrega.')
p(f'El resultado principal es que SARIMAX obtuvo el menor RMSE del backtest: {fmt(mx["RMSE"])} millones de dólares. La mejora frente al estacional ingenuo fue {fmt(improvements["RMSE"])} %. Esa ventaja convive con una limitación: el SARIMA seleccionado conserva autocorrelación residual. Son conclusiones distintas y ambas deben defenderse.')
h('Cómo estudiar')
bullets(['Primera lectura: capítulos 1 a 9 para entender cada decisión y relacionarla con una función real.','Ensayo con el editor: capítulo 10, con un recorrido de 12 minutos y margen antes de 15.','Preparación de preguntas: capítulo 11. Responde primero sin leer y contrasta después.','Repaso final: la hoja del capítulo 12 reúne cifras, decisiones y errores que evitar.'])
p('La guía original del curso distribuye los 15 minutos en 7 de exposición y 8 de preguntas. El guion de 12 minutos solicitado aquí sirve para ensayar; si esa distribución sigue vigente, usa la variante abreviada indicada en el capítulo 10.')
h('Trazabilidad')
p('Fuentes exclusivas del caso: miniproyecto.py, comun.py, docs/informe.md, datos/README.md, datos/ventas_mensuales.csv, las cuatro figuras originales y los cinco CSV de resultados. Las nuevas ilustraciones representan las métricas guardadas y las ventanas que define el código; no contienen nuevos pronósticos. Los ejemplos de cálculo se identifican expresamente como didácticos.')
p('Los coeficientes estimados, sus intervalos y los errores individuales de cada pronóstico no se guardan en los CSV disponibles. No se inventan ni se infieren a partir de las métricas agregadas.')

page('Capítulo 1 Comprender el problema')
p('Se pronostican las ventas mensuales de tiendas de mercancías generales de Estados Unidos, serie MRTSSM452USN. Cada observación resume las ventas de un mes, en millones de dólares, sin ajuste estacional. La fuente es U.S. Census Bureau a través de FRED; la ficha local documenta la etiqueta Public Domain: Citation Requested.')
picture(ROOT/'figuras/serie.png','Figura 1 · Serie original · figuras/serie.png')
h('Concepto y lectura de los ejes')
p('Una serie temporal ordena mediciones de una variable según el tiempo. El orden importa: el dato de un mes puede estar relacionado con los meses anteriores y con el mismo mes de años previos. Aquí la frecuencia mensual significa un valor por mes, no doce observaciones independientes por año.')
bullets(['Eje X: fechas de observación, desde enero de 1992 hasta agosto de 2026. La marca 2028 es espacio del eje, no un dato ni un pronóstico.','Eje Y: ventas en millones de dólares. Un valor de 80.000 equivale a 80.000 millones, no a 80.000 dólares.','Cada punto de la línea corresponde al total mensual registrado; la línea une observaciones, no mediciones diarias.'])
h('Interpretación de nuestra serie')
p('La muestra tiene 416 meses. Se observa un nivel creciente y oscilaciones anuales con picos recurrentes, especialmente en diciembre. La STL permite cuantificar ese patrón. La amplitud y el nivel no son constantes a lo largo de toda la historia; también aparecen cambios locales alrededor de 2020–2024.')
p('Pronosticar exige distinguir el nivel de largo plazo, el ciclo del calendario y las variaciones no explicadas. Repetir el último mes falla cuando ese mes pertenece a otra fase estacional. Repetir el mismo mes del año anterior atiende el calendario, pero puede quedarse atrás si el nivel cambia.')
p('Límite: la figura no prueba que un evento económico específico haya causado una subida o caída. El código no deflacta la serie, de modo que no debe presentarse el aumento como crecimiento real del volumen de ventas.')
p('En VS Code: comun.py → cargar_serie(); miniproyecto.py → preparar() y graficar_serie().')

page('Capítulo 2 Preparación y descomposición STL')
p('La revisión del CSV identificó cero faltantes y cero fechas duplicadas. cargar_serie() convierte las fechas en índice mensual MS; preparar() rechaza faltantes y valores no finitos. No imputa, recorta ni sustituye observaciones. La ausencia de duplicados es una propiedad comprobada del archivo, no una rutina explícita de deduplicación en preparar().')
picture(ROOT/'figuras/stl.png','Figura 2 · Cuatro paneles de STL robusta · figuras/stl.png')
h('Qué hace STL')
p('STL separa tendencia y estacionalidad mediante suavizados locales LOESS. El modelo descriptivo es aditivo: observado = tendencia + estacionalidad + residuo. period=12 indica un ciclo anual de doce observaciones mensuales. robust=True repondera observaciones inusuales para reducir su influencia en los suavizados; no las borra ni las convierte automáticamente en errores.')
equation('Yₜ = Tₜ + Sₜ + Rₜ')
p('La descomposición usa toda la serie para describirla. Sus componentes no entran al SARIMA, no determinan la rejilla ni se usan para transformar los datos del backtest.')

page('Lectura detallada de los cuatro paneles',2)
table(['Panel','Qué representa','Resultado del proyecto'],[
['Observado','Ventas tal como se cargan','416 meses sin ajuste estacional'],
['Tendencia','Nivel suavizado de largo plazo','20.015,40 al inicio; 80.982,93 al final'],
['Estacionalidad','Desviación periódica respecto a la tendencia','Diciembre +18.857,60; febrero −6.592,12'],
['Residuo','Parte restante tras quitar tendencia y estacionalidad','Diciembre de 2020: −5.850,21']], [3,6.2,7.8])
h('Interpretación de los componentes')
p('Observado. El panel superior reproduce las ventas originales: combina nivel, calendario y otras variaciones. Los picos altos no son por sí solos anomalías; algunos son parte del patrón recurrente.')
p('Tendencia. La curva suave crece de 20.015,40 a 80.982,93 millones. Es una estimación local del nivel y no un pronóstico. Sus extremos pueden ser sensibles al suavizado y a la información disponible al borde de la muestra.')
p('Estacionalidad. El código agrupa el componente estacional por número de mes y calcula su promedio. Por eso +18.857,60 en diciembre es el efecto medio de diciembre en la descomposición, no el valor de ventas de todos los diciembres ni un coeficiente fijo del SARIMA. Febrero queda en promedio 6.592,12 millones por debajo de la tendencia.')
p('Residuo. Se obtiene restando tendencia y estacionalidad al observado. En diciembre de 2020 el residuo es −5.850,21 millones: las ventas quedaron por debajo de lo que suman esos dos componentes. No significa ventas negativas. Es el mayor residuo absoluto de esta STL, no necesariamente el mayor error de un pronóstico SARIMA.')
h('Decisión sobre los extremos')
p('Se conservaron los extremos porque no existe evidencia en el archivo que permita clasificarlos como errores. Quitarlos por ser grandes alteraría la señal que se pretende pronosticar. STL robusta facilita separar componentes sin exigir esa eliminación; no garantiza que los residuos sean normales ni independientes.')
code('miniproyecto.py','descomponer','resultado = STL',').fit()')
p('Para explicarlo: “La descomposición me ayuda a describir qué parte parece nivel y qué parte parece calendario. No uso esta figura como prueba causal ni como pronóstico”.')

page('Capítulo 3 Estacionariedad y pruebas ADF')
h('Conceptos desde cero')
p('La estacionariedad débil supone media y varianza constantes en el tiempo y una covarianza que depende de la distancia entre observaciones, no del mes concreto de la historia. No significa que la serie sea plana ni que no tenga autocorrelación: puede fluctuar con dependencia alrededor de un nivel estable.')
p('Una raíz unitaria es una forma de persistencia no estacionaria. En el ejemplo conceptual Yₜ = Yₜ₋₁ + εₜ, un choque se acumula en el nivel y no se disipa rápidamente. Diferenciar produce ΔYₜ = εₜ. Este ejemplo explica la idea; no afirma que nuestras ventas sigan exactamente un paseo aleatorio.')
p('ADF es la prueba aumentada de Dickey–Fuller. Su hipótesis nula es que existe una raíz unitaria en la especificación evaluada. Incluye rezagos de la diferencia para atender dependencia en los errores; el código selecciona su número con autolag="AIC". Ese AIC pertenece a la regresión de la prueba, no es la tabla de selección SARIMA.')
h('Cómo interpretar el valor p')
p('El valor p mide qué tan incompatible es el estadístico observado con la hipótesis nula, bajo los supuestos de la prueba. No es la probabilidad de que la nula sea verdadera ni la probabilidad de que la serie sea estacionaria. Con un umbral de 0,05, p menor que ese umbral lleva a rechazar la nula; p mayor lleva a no rechazarla, no a demostrarla.')
p('Para la serie original se incluye constante y tendencia, regression="ct". Así, la alternativa permite estacionariedad alrededor de una tendencia determinista. Para las series diferenciadas se usa constante, regression="c". La especificación determinista afecta al resultado y debe declararse.')
h('Qué hacen las diferencias')
equation('ΔYₜ = Yₜ − Yₜ₋₁     Δ₁₂Yₜ = Yₜ − Yₜ₋₁₂')
equation('ΔΔ₁₂Yₜ = Yₜ − Yₜ₋₁ − Yₜ₋₁₂ + Yₜ₋₁₃')
p('d cuenta las diferencias regulares entre meses consecutivos; D cuenta las diferencias estacionales entre meses separados por doce posiciones. No son los rezagos AR o MA. Una diferencia estacional también incorpora un factor de diferencia regular: 1−B¹² = (1−B)(1+B+…+B¹¹). Por eso d=0 no significa ausencia total de diferenciación.')

page('Resultados ADF y decisión de diferenciación',2)
table(['Versión','ADF','Valor p','Rezagos'],[[r['version'],fmt(r['estadistico'],4),f'{float(r["p_valor"]):.6g}'.replace('.',','),r['rezagos']] for r in adf],[6.2,3.2,4,3.6])
p('Fuente: resultados/adf.csv. Las cuatro pruebas usan únicamente los primeros 392 meses, enero de 1992 a agosto de 2024. Al diferenciar se pierden observaciones iniciales; las cuatro regresiones ADF no tienen idéntico número efectivo de filas.')
h('Interpretación de nuestros resultados')
p('Original: ADF −3,1282 y p=0,099675. No rechazo la raíz unitaria al 5 %. No afirmo que la probé, ni cambio el umbral al 10 % después de ver el resultado para obtener una conclusión conveniente.')
p('Diferencia regular: ADF −3,6385 y p=0,005066. Rechaza la nula, pero eso no demuestra por sí solo que ya se representó adecuadamente el ciclo anual.')
p('Diferencia estacional: ADF −4,5275 y p=0,000175. También rechaza. Junto con la estructura anual y la ACF/PACF de la transformada, permite mantener provisionalmente d=0 y D=1.')
p('Ambas diferencias: ADF −5,6908 y p=8,081711×10⁻⁷. A seis decimales aparece como 0,000001. Que el valor p sea menor no significa que esta transformación produzca mejores pronósticos: la prueba no es una competición para minimizar p.')
h('Por qué no se añade d igual a uno')
p('La diferencia estacional ya aporta evidencia contra la raíz unitaria; una diferencia regular adicional no es necesaria solo para conseguir rechazo. Sobrediferenciar puede amplificar ruido e introducir dependencia artificial. La decisión es provisional: el experimento no comparó por backtest todas las parejas posibles de d y D.')
p('Límite: ADF no prueba específicamente todas las raíces estacionales, no garantiza varianza constante y puede verse afectada por cambios estructurales. Las decisiones se justifican combinando prueba, gráficos y alcance del experimento, no con un único número.')
code('miniproyecto.py','estacionariedad','regression =','        )')
p('En VS Code: estacionariedad() define las cuatro versiones; main() le entrega serie_seleccion, no los 416 meses.')

page('Capítulo 4 ACF y PACF')
picture(ROOT/'figuras/acf_pacf.png','Figura 3 · ACF y PACF de la diferencia estacional sobre la muestra de selección · figuras/acf_pacf.png')
h('Cómo leer cada barra')
p('ACF significa función de autocorrelación. La barra de rezago k mide la asociación lineal entre Wₜ y Wₜ₋ₖ. PACF significa función de autocorrelación parcial: resume la asociación lineal restante al controlar los rezagos intermedios. El eje horizontal muestra meses de separación y el vertical correlaciones entre −1 y 1. La barra cero vale uno por construcción; no se usa para elegir el orden.')
table(['Rezago','Distancia temporal','Lectura'],[['1','Un mes','Relación con el mes anterior'],['2','Dos meses','Relación a dos meses de distancia'],['12','Un año','Mismo mes del año anterior'],['24','Dos años','Mismo mes dos años antes']],[2,5,10])
p('Las bandas azules son intervalos aproximados del 95 % representados alrededor de cero. Una barra fuera de ellas es evidencia puntual contra correlación cero bajo el cálculo usado. No es una regla simultánea para las 36 barras: examinar muchas aumenta la posibilidad de picos aislados por azar.')

page('Interpretación de las barras de nuestra gráfica',2)
p('La variable graficada es Wₜ = Yₜ−Yₜ₋₁₂, no las ventas originales ni los residuos del SARIMA. Se dispone de 380 valores tras quitar los primeros doce de los 392 meses de selección.')
table(['Aspecto','Lo observado','Qué sugiere'],[
['ACF inicial','Rezagos 1, 2 y 3 ≈ 0,64; 0,64; 0,67','Dependencia positiva que requiere modelarse'],
['ACF posterior','Rezagos 1–8 fuera de bandas; luego se atenúa','No hay corte nítido de MA puro en 1 o 2'],
['PACF inicial','Rezagos 1, 2 y 3 ≈ 0,64; 0,39; 0,33','Componentes AR plausibles'],
['PACF posterior','Picos positivos y negativos aislados','No corresponde a un AR puro claramente truncado']],[3.3,6.8,6.9])
p('Entre los rezagos 1 y 36, la PACF sobrepasa las bandas en 1, 2, 3, 9, 10, 12, 13, 14, 16, 22, 23, 26, 27 y 36. En particular, el rezago 12 es negativo y sale de la banda; el 24 está dentro. En la ACF, los rezagos 12 y 24 están dentro de sus bandas. La ausencia de un gran pico en 12 no elimina el interés de los términos estacionales: ya se aplicó una diferencia anual y el modelo es mixto.')
h('Relación con los órdenes')
p('En casos ideales de procesos puros, una PACF que se corta después de p orienta un AR(p), y una ACF que se corta después de q orienta un MA(q). Para términos estacionales, se observan los múltiplos de 12: P cuenta términos AR estacionales y Q términos MA estacionales. En datos finitos y modelos mixtos esas pautas son orientaciones, no un algoritmo infalible.')
p('Aquí la PACF de rezago 3 es visible, pero la rejilla elegida solo explora p hasta 2. AIC seleccionó (1,0,2)(1,1,1)₁₂ dentro de ese conjunto; no se puede decir que descartó p=3, porque no se ensayó. El residuo autocorrelacionado es otra señal para revisar el alcance de la rejilla en una extensión futura.')
h('Cómo explicarlo sin sobreinterpretar')
p('“Las gráficas me orientaron hacia una estructura con memoria regular y estacional. No leí el modelo exacto de una sola barra. Comparé una rejilla pequeña por AIC y después comprobé el comportamiento predictivo y residual”.')
p('En VS Code: estacionariedad() → transformada, plot_acf(..., lags=36) y plot_pacf(..., method="ywm").')

page('Capítulo 5 SARIMA y selección por AIC')
p('ARIMA combina autorregresión, integración mediante diferencias y media móvil de innovaciones. SARIMA añade esos mecanismos en los rezagos de un ciclo estacional. La implementación usa la clase SARIMAX de statsmodels también para el SARIMA: si no se pasa exog, no hay regresora externa.')
table(['Orden','Valor','Significado en el modelo'],[
['p','1','Un término AR regular sobre la serie diferenciada'],['d','0','Ninguna diferencia regular adicional'],['q','2','Dos términos MA regulares de innovaciones'],['P','1','Un término AR estacional a 12 meses'],['D','1','Una diferencia estacional anual'],['Q','1','Un término MA estacional a 12 meses'],['s','12','Doce observaciones por ciclo anual']],[2,2,13])
h('Qué hace cada componente')
p('Autorregresión: utiliza valores pasados de la serie transformada para explicar el presente. Media móvil: utiliza innovaciones o errores de predicción pasados estimados por el modelo; no es un promedio aritmético de las últimas ventas. Diferenciar: resta niveles separados por un rezago para transformar la persistencia del nivel.')
p('La forma multiplicativa contiene interacciones entre términos regulares y estacionales. Por eso no debe describirse como si solo usara los meses 1, 2 y 12 sin términos cruzados. La configuración trend="n" excluye una tendencia determinista añadida.')
equation('(1−φ₁B)(1−Φ₁B¹²)(1−B¹²)Yₜ =')
equation('(1+θ₁B+θ₂B²)(1+Θ₁B¹²)εₜ')
p('B desplaza una observación hacia el pasado; B¹² desplaza doce. Los signos de los coeficientes dependen de la convención del polinomio. Los CSV no incluyen los valores estimados de φ, Φ, θ o Θ; no puedo asignarles magnitudes ni significancia.')

page('La rejilla y el criterio de selección',2)
code('miniproyecto.py','elegir_sarima','for p, q, P, Q in product','estacional =')
code('miniproyecto.py','elegir_sarima','ajuste = ajustar','if not np.isfinite(ajuste.aic):')
p('product recorre 3×3×2×2=36 combinaciones de p,q∈{0,1,2} y P,Q∈{0,1}. d=0 y D=1 permanecen fijos. ajustar() limita a 100 iteraciones y registra convergencia; el código excluye candidatos no convergentes o con AIC no finito. En el CSV actual convergieron los 36.')
table(['Orden regular','Orden estacional','AIC'],[[r['orden'],r['estacional'],fmt(r['AIC'],6)] for r in aic[:5]],[4.5,6,6.5])
equation('AIC = −2 log L + 2k')
p('L es la verosimilitud maximizada y k el número de parámetros estimados contado por el ajuste. El primer término recompensa ajuste y el segundo penaliza complejidad. Entre candidatos comparables se prefiere menor AIC. No es un porcentaje, un error en dólares ni una prueba de ruido blanco.')
p(f'El ganador registra AIC {fmt(aic[0]["AIC"],6)}. El segundo está a {fmt(float(aic[1]["AIC"])-float(aic[0]["AIC"]),2)} unidades: la ventaja de AIC no es enorme ni demuestra unicidad. AIC se calcula dentro de la muestra de selección; RMSE evalúa errores fuera de cada entrenamiento.')
p('Límites del código: enforce_stationarity=False y enforce_invertibility=False no imponen esas restricciones al optimizador. Además, el descarte inicial de verosimilitud puede depender del orden del modelo. Antes de atribuir una interpretación fuerte a diferencias pequeñas de AIC, convendría auditar la comparabilidad de la muestra efectiva y las raíces estimadas. Los CSV no guardan esos detalles por candidato. Aquí se reporta fielmente el ranking implementado, no una búsqueda exhaustiva del mejor modelo posible.')

page('Capítulo 6 Diagnóstico de residuos')
picture(ROOT/'figuras/residuos.png','Figura 4 · Residuos del SARIMA seleccionado y su ACF · figuras/residuos.png')
h('Panel superior')
p('Un residuo del ajuste compara la observación con su predicción de un paso condicionada al pasado. Si es positivo, el observado supera la predicción; si es negativo, queda por debajo. No es el mismo objeto que el residuo STL ni que el error de horizonte doce del backtest.')
p('La gráfica muestra residuos alrededor de cero, con valores positivos y negativos, y mayor dispersión en el tramo posterior a 2020. La línea horizontal cero es una referencia, no una prueba de media exactamente nula. La figura sugiere variación de volatilidad; no se ejecutó aquí una prueba formal de heterocedasticidad.')
h('Panel inferior')
p('La ACF residual busca memoria que el modelo dejó sin explicar. Se ven, por ejemplo, picos positivos alrededor de los rezagos 3, 6 y 14, y negativos alrededor de 10 y 16. No hay una desaparición completa de la dependencia. La interpretación conjunta se apoya en Ljung–Box y no en contar barras individualmente.')
p('Ruido blanco débil tiene media cero, varianza constante y autocovarianzas nulas a rezagos distintos de cero. No exige normalidad ni equivale automáticamente a independencia. Un diagnóstico satisfactorio debería ser compatible con esas propiedades; un p alto en una sola prueba tampoco las demostraría todas.')

page('Ljung Box y residuos de inicialización',2)
code('miniproyecto.py','elegir_sarima','inicio = max','residuos = ajuste.resid')
code('miniproyecto.py','elegir_sarima','model_df =','return_df=True')
p('El inicio del filtro de estados depende de supuestos de inicialización; esos residuos pueden no ser comparables con los posteriores. El código toma el máximo entre nobs_diffuse y loglikelihood_burn. En este ajuste son 27 observaciones excluidas, no una constante universal que deba copiarse a todo SARIMA. Quedan 392−27=365 residuos.')
table(['Rezago','Estadístico Q','Valor p','Grados de libertad'],[[r['rezago'],fmt(r['lb_stat'],6),f'{float(r["lb_pvalue"]):.6e}',str(int(r['rezago'])-int(r['model_df']))] for r in lb],[2.3,4.4,5.5,4.8])
p('Ljung–Box contrasta la hipótesis nula de ausencia conjunta de autocorrelación hasta el rezago elegido. El ajuste model_df=5 descuenta p+q+P+Q=1+2+1+1 términos AR y MA. No suma d, D ni el periodo 12. Así, los grados de libertad de la aproximación son 7 y 19.')
p('Los valores p, 5,116744×10⁻⁶ y 3,566144×10⁻¹¹, son inferiores a 0,05. Rechazo la ausencia de autocorrelación y no describo los residuos como ruido blanco. No cambio la especificación solo para conseguir valores p superiores a 0,05: ese sería un objetivo distinto de la comparación predictiva realizada.')
p('Este diagnóstico corresponde al SARIMA ajustado sobre los 392 meses de selección. No se guardó un diagnóstico equivalente del SARIMAX. Una mejora de RMSE no autoriza a afirmar que la regresora resolvió la dependencia residual.')
p('Para explicarlo: “El modelo mejora los pronósticos frente a las líneas base, pero el diagnóstico señala estructura que no capturó. Esa limitación forma parte del resultado, no la oculto”.')

page('Capítulo 7 SARIMAX y variable exógena')
p('SARIMAX añade regresoras externas a la estructura de errores SARIMA. En este proyecto la única columna externa es dias_lunes_viernes: el número de fechas de lunes a viernes de cada mes. Mantiene los órdenes seleccionados para SARIMA; no se ejecuta una segunda rejilla de órdenes para SARIMAX.')
h('Calendario conocido anticipadamente')
p('numpy.busday_count cuenta días de lunes a viernes entre el inicio inclusivo del mes y el inicio exclusivo del siguiente. El código no proporciona un calendario de festivos; por eso “días hábiles oficiales” sería una descripción inexacta. Tampoco supone que una tienda solo venda entre semana.')
code('miniproyecto.py','exogenas')
p('date_range construye meses desde el inicio de la serie hasta doce meses después del último dato. Esa extensión solo crea fechas y no utiliza ventas futuras. El índice MS alinea la regresora con el índice mensual de las ventas. El número de días se conoce para cualquier horizonte futuro porque depende del calendario.')

page('Cómo entra el calendario en cada pronóstico',2)
code('miniproyecto.py','modelo_sarimax')
p('x.loc[entrenamiento.index] entrega exclusivamente las filas de calendario correspondientes a las ventas disponibles. fechas_siguientes(entrenamiento,h) calcula las fechas posteriores al origen; x_futuro suministra sus regresoras al método forecast. El coeficiente de la regresora se estima con entrenamiento, no con las ventas de la ventana evaluada.')
p('Fuga de información significa utilizar al ajustar o elegir un modelo datos que no se habrían conocido al emitir el pronóstico. La regresora futura es válida aquí porque no contiene ventas observadas después del origen. Una temperatura futura realizada o una tasa de cambio futura realizada serían distintas: habría que pronosticarlas o usar escenarios conocidos al origen.')
p('Límite: “exógena” en el código significa una entrada externa al historial de ventas; no prueba una relación causal. Los CSV no incluyen el coeficiente, su incertidumbre o una prueba de significancia de esta regresora.')

page('Capítulo 8 Backtest y métricas')
p('El backtest simula pronósticos históricos con origen móvil y entrenamiento expansivo. Se reservan los últimos 24 meses, septiembre de 2024 a agosto de 2026. Cada origen necesita doce valores posteriores observados; por eso hay 24−12+1=13 orígenes, de agosto de 2024 a agosto de 2025.')
picture(TMP/'backtest.png','Figura 5 · Diagrama del protocolo real de comun.py · no representa pronósticos nuevos')
p('Cada fila emite doce pronósticos simultáneamente, para horizontes 1 a 12. Al avanzar una fila se incorpora un mes ya conocido al entrenamiento y se vuelve a estimar el mismo orden de modelo. El primer ajuste tiene 392 meses y el último 404. Los parámetros se reestiman; los órdenes no se vuelven a seleccionar.')
table(['Origen','Entrenamiento hasta','Ventana evaluada'],[['1','Agosto de 2024','Septiembre de 2024 a agosto de 2025'],['7','Febrero de 2025','Marzo de 2025 a febrero de 2026'],['13','Agosto de 2025','Septiembre de 2025 a agosto de 2026']],[2.2,5,9.8])
p('Las ventanas se solapan: las 156 parejas origen–horizonte no son 156 meses diferentes ni observaciones independientes. Los meses centrales aparecen en más ventanas. El protocolo común determina esa ponderación y no se modifica.')

page('Cómo se ejecuta y agrega el backtest',2)
code('comun.py','backtest','filas = []')
h('Lectura paso a paso')
p('primero=416−24=392. range(392,405) genera cortes del 392 al 404 inclusive. serie.iloc[:corte] excluye la posición corte: todo lo que se ajusta queda antes del primer mes objetivo. real contiene los doce valores siguientes y solo se usa para evaluar. modelo recibe entrenamiento y h, no real.')
p('En cada origen se calculan RMSE, MAE y MAPE sobre sus doce horizontes. Finalmente se promedia cada columna de métricas sobre los trece orígenes. fila() conserva esos promedios y los redondea a dos decimales para escribir metricas.csv.')
equation('M final = (1/13) Σⱼ₌₁¹³ Mⱼ')
p('Promediar los trece RMSE no equivale, en general, a calcular una sola raíz del promedio de los 156 errores cuadrados. La raíz es una transformación no lineal. MAE y MAPE sí equivalen al promedio de los 156 términos porque cada origen tiene el mismo horizonte, pero con repetición de meses y diferentes pronósticos para ellos.')
h('Las dos líneas base')
p('Ingenuo: repite el último valor observado en los doce horizontes. Estacional ingenuo: repite los últimos doce meses, alineados con los meses futuros. Son referencias simples pero necesarias para saber si la complejidad añadida aporta valor. Ambas usan exactamente el mismo backtest.')
p('Fuente: comun.py → ingenuo(), estacional_ingenuo(), backtest(); miniproyecto.py → fila(). El archivo común permanece intacto.')

page('Interpretación y límites de las tres métricas',2)
p('Sea eᵢ = yᵢ−ŷᵢ, el observado menos el pronóstico. En cada origen, n=12. Las siguientes fórmulas son las que implementa comun.py.')
equation('MAE = (1/n) Σᵢ₌₁ⁿ |yᵢ − ŷᵢ|')
p('MAE es el error absoluto medio. Tiene las mismas unidades que las ventas: millones de dólares. Un MAE de 890,76 indica una magnitud media de error absoluto de 890,76 millones bajo la agregación del protocolo. Menor es mejor; no conserva el signo, no muestra sesgo y resume en un número errores que pueden variar mucho por mes.')
equation('RMSE = √[(1/n) Σᵢ₌₁ⁿ (yᵢ − ŷᵢ)²]')
p('RMSE eleva al cuadrado, promedia y extrae la raíz. También se expresa en millones de dólares. Penaliza más los errores grandes que MAE, por lo que un fallo importante puede influir mucho. Menor es mejor dentro de la misma serie y protocolo; su escala impide comparar directamente series de tamaños muy distintos.')
equation('MAPE = (100/n) Σᵢ₌₁ⁿ |(yᵢ − ŷᵢ) / yᵢ|')
p('MAPE es el error porcentual absoluto medio respecto al valor observado. Un 1,16 % no significa que cada predicción tenga ese error ni que exista una garantía de precisión del 98,84 %. Los valores reales pequeños reciben más peso relativo y un cero hace indefinida la división. La serie local tiene valores positivos; comun.py no incorpora protección especial contra ceros.')
h('Ejemplo didáctico que no pertenece a los resultados')
p('Supón dos observaciones de 100 y 200 millones y pronósticos de 90 y 220. Los errores son 10 y −20; los absolutos son 10 y 20. MAE=(10+20)/2=15 millones. RMSE=√[(100+400)/2]=√250≈15,81 millones. MAPE=100×[(10/100+20/200)/2]=10 %. Este ejemplo ilustra el cálculo; el proyecto usa doce horizontes por origen.')
p('En VS Code: abre mae(), rmse() y mape(). Señala np.abs, el cuadrado antes de la raíz y la división por y. Ninguna de estas métricas prueba causalidad, independencia residual ni significancia de diferencias entre modelos.')

page('Capítulo 9 Resultados y comparación')
picture(TMP/'rmse.png','Figura 6 · Barras calculadas exclusivamente con resultados/metricas.csv')
table(['Modelo','RMSE','MAE','MAPE'],[[short(r['modelo']),fmt(r['RMSE']),fmt(r['MAE']),fmt(r['MAPE'])+' %'] for r in metrics],[5.8,3.8,3.8,3.6])
p('RMSE y MAE se expresan en millones de dólares. El gráfico parte de cero para mantener proporciones honestas. Las cifras son los promedios por origen ya redondeados que guarda el guion, no estimaciones nuevas.')
h('Qué explica razonablemente el orden observado')
p('El ingenuo ignora el ciclo anual: prolonga el nivel del último mes incluso cuando se aproxima diciembre o febrero. Esa debilidad es compatible con su mayor error. El estacional ingenuo reconoce el calendario y reduce marcadamente el error; aun así, reutiliza niveles de hace un año.')
p('SARIMA permite representar cambios respecto al año anterior y dependencia AR/MA, por lo que puede adaptarse mejor que repetir un año completo. SARIMAX añade variación de calendario que podría aportar información adicional. Lo demostrado es que su error fue menor aquí; sin analizar coeficientes e incertidumbre no puede atribuirse causalmente toda la diferencia a un mecanismo específico.')

page('Cuánto mejora y qué no puede concluirse',2)
equation('Mejora porcentual = 100 × (M base − M modelo) / M base')
table(['Comparación','RMSE','MAE','MAPE'],[
['SARIMAX frente a estacional ingenuo',*[fmt(improvements[m])+' %' for m in ['RMSE','MAE','MAPE']]],
['SARIMAX frente a SARIMA',*[fmt(100*(1-float(mx[m])/float(ma[m])))+' %' for m in ['RMSE','MAE','MAPE']]],
['Estacional ingenuo frente a ingenuo',*[fmt(100*(1-float(base[m])/float(naive[m])))+' %' for m in ['RMSE','MAE','MAPE']]]],[6.5,3.5,3.5,3.5])
p('Los porcentajes se calculan con los valores de metricas.csv, que ya están redondeados. Por eso el porcentaje de mejora de MAPE es aproximado. Frente al estacional ingenuo, la diferencia de MAPE es 2,44−1,16=1,28 puntos porcentuales; su reducción relativa es 52,46 %. No son la misma unidad.')
p(f'La reducción de RMSE frente a SARIMA es {fmt(inc)} %, equivalente a {fmt(float(ma["RMSE"])-float(mx["RMSE"]))} millones. La estructura temporal explica la mayor parte de la ventaja frente a las bases en esta comparación; la ganancia adicional del calendario es modesta.')
h('Convergencia y reproducibilidad')
p('convergencia.csv registra 36 ajustes de rejilla, uno de diagnóstico, 13 SARIMA y 13 SARIMAX: 63 registros, todos con convergio=True. Converger significa que el optimizador reporta su criterio de parada, no que se haya probado un óptimo global ni que el modelo sea estadísticamente adecuado. Fuera de la rejilla, ajustar() detiene la ejecución si no hay convergencia; no elimina orígenes ni sustituye modelos silenciosamente.')
p('El entorno local documentado fue Python 3.11 con NumPy 2.4.2, pandas 2.3.3, matplotlib 3.10.8 y statsmodels 0.14.6. requirements.txt no fija versiones. Esta guía verifica archivos guardados y no reentrena modelos; no certifica una ejecución nueva en otro entorno.')
h('Límites de la evidencia')
bullets(['No hay prueba de significancia de la diferencia SARIMAX–SARIMA ni diagnóstico residual guardado del SARIMAX.','No se guardan errores por horizonte ni predicciones por fecha: no puede localizarse desde metricas.csv el peor mes de pronóstico.','El ganador se elige tras comparar resultados en esta ventana: una validación futura independiente es necesaria para evaluar generalización.','El CSV es una descarga histórica; no hay archivo de versiones de publicación. El backtest respeta cortes por fecha, pero no demuestra evaluación en tiempo real con datos disponibles antes de futuras revisiones del proveedor.'])

page('Capítulo 10 Guion de exposición de doce minutos')
p('Ten abiertos miniproyecto.py, comun.py, metricas.csv y las cuatro figuras. Practica las transiciones sin leer el documento en voz alta. Usa Ctrl+F con los nombres de función; las líneas pueden cambiar si se edita el código. No cuentes con que un entrenamiento completo termine dentro del tiempo de explicación.')
table(['Tiempo','Abrir','Idea central','Cifra'],[
['0:00–1:00','ARCHIVO y serie.png','Qué se pronostica y en qué unidades','416 meses'],
['1:00–2:20','preparar y descomponer','Decisiones de datos y componentes','Diciembre +18.857,60'],
['2:20–3:50','main y estacionariedad','Separar identificación de evaluación','392 / 24'],
['3:50–5:00','acf_pacf.png y elegir_sarima','Gráficos orientan; AIC compara','6.286,64'],
['5:00–6:20','residuos.png y Ljung–Box','Dependencia no explicada','model_df=5'],
['6:20–7:40','exogenas y modelo_sarimax','Calendario futuro sin ventas futuras','Lunes a viernes'],
['7:40–9:20','comun.py → backtest','Ventanas y agregación común','13 orígenes × 12'],
['9:20–10:40','metricas.csv','Ganador y magnitud de mejora','RMSE 1.082,02'],
['10:40–12:00','ajustar y cierre','Convergencia, límites y siguiente paso','Mejora 50,40 %']],[2.5,5.2,6.3,3])
h('Primer tramo con palabras naturales')
p('0:00–1:00. Señala ARCHIVO, FECHA y VALOR y abre serie.png. “Estoy pronosticando ventas mensuales, en millones de dólares. Elegí una historia larga y con estacionalidad visible para comparar métodos simples y clásicos bajo el mismo protocolo”. Con el cursor muestra el eje Y y los picos anuales.')
p('1:00–2:20. En preparar() señala las validaciones y después period=12 y robust=True. En stl.png recorre de arriba abajo. “No imputé porque no había huecos y conservé los extremos porque no tenía evidencia de error. Diciembre queda por encima de la tendencia; el residuo negativo de 2020 significa estar por debajo de lo que explica la descomposición”.')
p('2:20–3:50. Señala serie.iloc[:-24] y la llamada estacionariedad(serie_seleccion). “La identificación usa solo 392 meses. La diferencia estacional rechaza la raíz unitaria, por eso mantengo d=0 y D=1 de forma provisional”. Recuerda p≈0,000175; no hace falta recitar los cuatro estadísticos.')

page('Segundo tramo y cierre del ensayo',2)
p('3:50–5:00. En acf_pacf.png apunta a rezagos 1–3 y a las bandas; después abre la rejilla product. “Las gráficas muestran memoria, pero no dictan un único modelo. Entre 36 combinaciones, este orden produjo el menor AIC”. Señala el orden ganador y aclara que AIC no es error de pronóstico.')
p('5:00–6:20. Abre residuos.png y el bloque acorr_ljungbox. Con el cursor alterna entre la mayor dispersión posterior a 2020 y los picos de la ACF. “Excluí la inicialización y desconté cinco términos AR/MA. Los valores p son muy pequeños, así que reconozco autocorrelación residual en SARIMA”.')
p('6:20–7:40. En exogenas() señala busday_count; en modelo_sarimax() señala x_entrenamiento y x_futuro. “La regresora cuenta lunes a viernes, no festivos. Puedo conocer ese calendario al pronosticar. El coeficiente se estima solo con ventas pasadas”.')
p('7:40–9:20. En backtest() señala primero, range y los dos cortes iloc. “Cada origen ajusta con todo lo conocido y pronostica doce meses. Como la ventana final tiene 24, resultan trece orígenes. Evalúo los doce horizontes y promedio las métricas por origen”. Si preguntan, explica por qué el promedio de RMSE no es un RMSE global.')
p('9:20–10:40. Abre metricas.csv. Compara primero SARIMAX con estacional ingenuo, luego con SARIMA. “El RMSE baja de 2.181,36 a 1.082,02, aproximadamente 50,40 %. La ganancia adicional frente a SARIMA es solo 1,85 %”. No presentes esa diferencia como estadísticamente significativa.')
p('10:40–12:00. Señala el chequeo converged de ajustar(). “Los 26 ajustes del backtest convergieron. Eso no elimina la limitación residual. Este SARIMAX queda como referencia para el siguiente proyecto, con el mismo protocolo”. Deja preparada la terminal para ejecutar python miniproyecto.py si el profesor lo solicita.')
h('Si solo hay siete minutos de exposición')
p('Dedica 45 segundos al problema, 50 a STL, 60 a identificación, 45 a AIC, 50 al diagnóstico, 55 a la exógena, 65 al backtest y 50 a resultados y cierre. Total: 7 minutos. Conserva las decisiones esenciales y omite derivaciones; las preguntas permiten profundizar. No amplíes a doce minutos sin confirmar que ese tiempo está disponible.')
h('Rutina de ensayo')
bullets(['Haz una pasada de 12 minutos con cronómetro sin leer; anota dónde buscas archivos demasiado tiempo.','Haz una segunda pasada de 7 minutos centrada en decisiones y cifras.','Practica tres preguntas difíciles sin pantalla: d/D, fuga y residuos.','Si algo falla en vivo, muestra los archivos guardados y explica el fallo; no presentes un resultado antiguo como una ejecución nueva exitosa.'])

page('Capítulo 11 Preguntas del profesor')
h('Nivel básico')
qa('1 Qué estás pronosticando','Las ventas mensuales de tiendas de mercancías generales de Estados Unidos, no el número de clientes ni el precio de una acción. La unidad es millones de dólares y la serie no está ajustada estacionalmente. Cada pronóstico corresponde a un mes.')
qa('2 Por qué sirve esta serie para el proyecto','Tiene 416 observaciones públicas, supera el mínimo de 60 y muestra un patrón anual visible. Permite evaluar una base estacional y modelos con periodo doce. Su extensión también exige reconocer que la economía puede cambiar durante la historia.')
qa('3 Qué significa frecuencia mensual','Hay una observación por mes y el rezago uno equivale a un mes. MS es la etiqueta de inicio de mes usada por pandas; no significa que la cifra sea una venta ocurrida únicamente ese día.')
qa('4 Qué es estacionalidad y cómo la distingues de tendencia','Estacionalidad es un patrón que se repite ligado al ciclo, aquí anual. Tendencia es el nivel que cambia a más largo plazo. En la STL, diciembre tiene un efecto medio positivo mientras la tendencia aumenta durante décadas.')
qa('5 Qué hiciste con huecos y extremos','No hubo faltantes ni duplicados en el CSV. preparar() exige valores finitos y sin faltantes; no hubo imputación. Conservé extremos porque no había evidencia de error de registro. Su tamaño por sí solo no justifica eliminarlos.')
qa('6 Qué significa robust True en STL','Hace que la descomposición reduzca la influencia de observaciones inusuales mediante reponderación. No elimina esos meses ni garantiza ausencia de errores; la serie utilizada por los modelos conserva sus valores originales.')
qa('7 El efecto de diciembre son sus ventas','No. +18.857,60 millones es el promedio del componente estacional de diciembre, una desviación respecto a la tendencia de la descomposición. Las ventas observadas incluyen tendencia, efecto estacional y residuo.')
qa('8 Un residuo negativo significa ventas negativas','No. Significa que el valor observado está por debajo de lo explicado o predicho. En STL se compara con tendencia más estacionalidad; en SARIMA se compara con su predicción condicionada al pasado. Son residuos de objetos diferentes.')

page('Preguntas de nivel intermedio',2)
qa('9 Qué significa p igual a 0 coma 099675 en ADF','Al 5 % no rechazo la hipótesis nula de raíz unitaria para la serie original con constante y tendencia. No significa una probabilidad de 9,97 % de que la serie sea estacionaria. Tampoco demuestra que necesariamente haya una raíz unitaria.')
qa('10 Por qué no utilizaste d igual a uno','La diferencia estacional por sí sola rechaza la raíz unitaria y la ACF se atenúa. No añado una diferencia regular solo para disminuir más el p. d=0,D=1 es una elección provisional; no he demostrado que todas las alternativas con d=1 pronostiquen peor.')
qa('11 Por qué no elegiste ambas diferencias si su p es menor','ADF contrasta una hipótesis, no selecciona el mejor pronosticador mediante el menor p. Añadir diferencias puede introducir ruido y sobrediferenciación. La variante con ambas tiene p≈8,08×10⁻⁷, pero eso no basta para preferirla.')
qa('12 Cuál es la diferencia entre ACF y PACF','ACF mide la asociación con un rezago incluyendo relaciones transmitidas por los intermedios. PACF controla linealmente esos intermedios. En nuestra transformada, ambas muestran dependencia inicial, pero ninguna identifica inequívocamente por sí sola el modelo final.')
qa('13 Por qué la PACF tiene un pico en tres y p termina en uno','Las reglas de corte son aproximaciones para casos puros. Se seleccionó por AIC entre una rejilla limitada a p≤2; p=3 no fue evaluado. Reconozco esa limitación en vez de decir que AIC lo descartó.')
qa('14 Media móvil significa promediar las últimas ventas','No en ARIMA. Un término MA modela dependencia respecto a innovaciones pasadas estimadas. Un promedio móvil descriptivo de ventas es otro procedimiento. q=2 cuenta términos de innovaciones a rezagos regulares, no una ventana de dos ventas para promediar.')
qa('15 Por qué AIC menor es preferible','Dentro de candidatos comparables, equilibra la verosimilitud lograda y el número de parámetros. Un valor menor favorece ese equilibrio; no tiene una escala de bueno o malo universal. 6.286,64 no se interpreta como un error de 6.286,64 dólares.')
qa('16 Por qué AIC no es RMSE','AIC deriva del ajuste probabilístico penalizado dentro de entrenamiento. RMSE resume magnitudes de error de pronóstico en la evaluación. Pueden ordenar modelos de forma distinta y ninguno reemplaza el diagnóstico residual.')

page('Preguntas intermedias y diagnóstico',2)
qa('17 Por qué RMSE es mayor que MAE en tu tabla','El cuadrado da más peso a errores grandes, por lo que RMSE suele ser mayor o igual a MAE para el mismo conjunto de errores. En cada origen se cumple esa desigualdad y se conserva al promediar. La diferencia no cuantifica por sí sola cuántos extremos hubo.')
qa('18 MAPE de 1 coma 16 implica precisión de 98 coma 84','No. MAPE es un promedio de errores absolutos relativos, con el protocolo de agregación usado. No es una probabilidad de acierto ni una garantía para cada mes. Tampoco es adecuado cuando hay observados cero o cercanos a cero.')
qa('19 Por qué AIC eligió un modelo con residuos autocorrelacionados','La regla de selección minimiza AIC entre los candidatos; no impone una restricción de aprobar Ljung–Box. La rejilla es limitada y puede quedar estructura sin representar. Conservo el resultado y reporto su limitación, sin elegir retrospectivamente otro modelo solo para mejorar p.')
qa('20 Qué significa model df igual a cinco','Descuenta los cinco términos AR y MA estimados: p+q+P+Q=1+2+1+1. No suma diferencias ni el periodo. Los rezagos 12 y 24 se contrastan con 7 y 19 grados de libertad, respectivamente.')
qa('21 Por qué quitaste exactamente veintisiete residuos','El ajuste indica un periodo de inicialización que el código obtiene del máximo entre nobs_diffuse y loglikelihood_burn. Para este ajuste resulta 27. No se eligió observando qué cantidad permitía obtener un valor p conveniente.')
qa('22 Puedes decir que SARIMAX tiene ruido blanco','No. El archivo ljung_box.csv viene del ajuste SARIMA de selección. No tengo un diagnóstico equivalente guardado para SARIMAX. Su menor RMSE no prueba que la exógena haya eliminado la autocorrelación ni otros problemas residuales.')
qa('23 Convergencia implica que el modelo es correcto','No. convergio=True informa el resultado del optimizador, no una prueba de veracidad, óptimo global, estabilidad o residuos blancos. En el registro hay 63 ajustes convergentes, incluidos los 26 del backtest, pero el diagnóstico sigue rechazando ausencia de autocorrelación.')

page('Preguntas avanzadas sobre evaluación',2)
qa('24 Por qué hay trece orígenes y no veinticuatro','Cada origen necesita doce observaciones futuras para evaluarse completamente. En una ventana de 24 meses caben 24−12+1=13 ventanas consecutivas de longitud doce. El primer origen es agosto de 2024 y el último agosto de 2025.')
qa('25 Los meses reservados nunca entran al entrenamiento','No entran a la identificación inicial ni a la búsqueda de órdenes. En los orígenes posteriores, los meses ya observados sí entran al entrenamiento expansivo; es lo que se conocería en ese momento. Lo prohibido es usar valores posteriores al origen vigente.')
qa('26 Por qué STL usa toda la serie e identificación solo trescientos noventa y dos meses','La STL completa es descriptiva y no suministra datos transformados ni reglas estimadas al pronosticador. Identificar d/D, leer ACF/PACF para elegir órdenes o seleccionar por AIC sí influye en los modelos, por lo que se limita al entrenamiento inicial. Si usara la STL completa para ajustar estacionalidad del backtest, habría fuga.')
qa('27 Existe sesgo por seleccionar una vez y mantener el orden','Fijar el orden con entrenamiento inicial evita consultar las ventas futuras y evalúa una estrategia válida de orden fijo con parámetros reestimados. No reproduce una estrategia que reelige órdenes cada mes. Puede adaptarse menos a cambios; para comparar esa otra estrategia habría que volver a seleccionar dentro de cada origen sin acceder a sus objetivos.')
qa('28 SARIMAX es significativamente mejor que SARIMA','Solo puedo afirmar que tiene menor error agregado observado: una reducción de RMSE de aproximadamente 1,85 %. No se realizó una prueba de significancia ni se guardaron errores individuales para aplicarla directamente. Las ventanas se solapan, por lo que tampoco sería correcto tratar los errores como independientes.')
qa('29 Por qué no usaste temperatura o tasa de cambio','Porque sus valores futuros realizados no se conocen con certeza al origen. Podrían usarse pronósticos disponibles entonces o escenarios, incorporando su incertidumbre. El calendario tiene disponibilidad anticipada verificable. No afirmo que esas otras variables sean irrelevantes; no se ensayaron.')
qa('30 Qué cambiaría con festivos oficiales','Habría que especificar el calendario del país y reglas de observancia, construir la regresora conocida al origen y volver a evaluar con el mismo backtest. Podría captar composición comercial mejor o peor, pero los resultados actuales no permiten anticipar una ganancia. busday_count sin holidays no los descuenta.')

page('Preguntas avanzadas sobre límites y extensiones',2)
qa('31 Cuál fue el peor mes de pronóstico','No puede determinarse a partir de metricas.csv: solo contiene promedios. El mayor residuo STL es diciembre de 2020, pero no es un error del backtest, cuya evaluación empieza en septiembre de 2024. Necesitaría guardar predicciones y errores por origen y horizonte para responder.')
qa('32 Cómo sabes que no hay fuga por revisiones del proveedor','El código evita utilizar fechas futuras al origen, pero el archivo es una descarga única y no conserva vintages de publicación. No puedo garantizar que cada cifra coincida con la conocida históricamente en ese mes. Una evaluación estrictamente en tiempo real necesitaría esas versiones y considerar retrasos de publicación.')
qa('33 El calendario causó la mejora','No lo demuestra este experimento. El modelo con esa regresora dio un error menor en la ventana analizada. No hay diseño causal ni coeficientes e intervalos guardados que permitan sostener una explicación causal o una significancia estadística del efecto.')
qa('34 El AIC de todos los candidatos es perfectamente comparable','Todos usan los mismos 392 meses de entrada y d/D fijos, lo cual favorece la comparación. Sin embargo, la inicialización y loglikelihood_burn pueden variar con el orden al relajar restricciones. Los CSV no guardan esa auditoría. Reporto el ranking obtenido y evitaría sobreinterpretar diferencias pequeñas sin revisar la muestra efectiva de verosimilitud.')
qa('35 Qué cambiarías para el Miniproyecto dos','Conservaría este benchmark y el protocolo. Guardaría errores por origen y horizonte, diagnosticaría SARIMAX, revisaría candidatos y la comparabilidad de AIC, y ensayaría alternativas de transformación o modelos sin mirar los objetivos de cada origen. Evaluaría intervalos e incertidumbre y usaría datos futuros independientes para validar las mejoras.')
qa('36 Qué sucede si un ajuste no converge en otra máquina','ajustar() escribe el estado en convergencia.csv y lanza un error fuera de la rejilla. No se sustituye el modelo ni se descarta el origen. Puede quedar un metricas.csv anterior en disco: habría que verificar que la ejecución terminó antes de atribuir ese archivo a la corrida nueva. Las versiones de dependencias pueden cambiar el ajuste.')
qa('37 Puedes comparar tu RMSE con el de otra serie','No directamente si cambian escala, unidad, periodo o protocolo. RMSE de ventas en millones no tiene la misma escala que pasajeros o temperatura. Incluso MAPE requiere cautela por valores pequeños, ceros y composición de la muestra.')
qa('38 Qué significa que ambos modelos usen la misma estructura SARIMA','El SARIMAX agrega una regresora y vuelve a estimar sus parámetros con exog, manteniendo los órdenes. No conserva necesariamente los coeficientes del SARIMA ni simplemente suma una cantidad fija al pronóstico. El código estima ambos por separado en cada origen.')

page('Capítulo 12 Resumen de estudio')
table(['Diez cifras y referencias que recordar','Valor'],[
['1 Muestra mensual','416 meses · ene. 1992 a ago. 2026'],['2 Separación temporal','392 identificación / 24 evaluación'],['3 Evaluación','13 orígenes × 12 horizontes'],['4 Diferenciación','d=0, D=1, s=12'],['5 ADF estacional','p=0,000175'],['6 Modelo y AIC','(1,0,2)(1,1,1)₁₂ · 6.286,64'],['7 Diagnóstico','27 excluidos · model_df=5'],['8 Ljung–Box','p₁₂≈5,12×10⁻⁶; p₂₄≈3,57×10⁻¹¹'],['9 SARIMAX','RMSE 1.082,02; MAE 890,76; MAPE 1,16 %'],['10 Mejora RMSE','50,40 % vs. base; 1,85 % vs. SARIMA']],[8.1,8.9])
h('Seis decisiones metodológicas')
p('1. Conservar extremos sin evidencia de error. 2. Usar STL robusta solo descriptivamente. 3. Identificar y seleccionar con 392 meses. 4. Mantener provisionalmente d=0,D=1. 5. Usar calendario conocido y el backtest común intacto. 6. Registrar convergencia y reportar autocorrelación residual sin ocultarla.')
h('Cinco errores que evitar')
p('1. Decir que p es la probabilidad de la hipótesis. 2. Confundir estacionariedad con ruido blanco. 3. Llamar festivos a lunes–viernes. 4. Confundir AIC con RMSE o media móvil con promedio de ventas. 5. Afirmar significancia, causalidad o residuos blancos de SARIMAX sin evidencia.')
h('Conclusión oral de treinta segundos')
p('“Comparé cuatro métodos con el mismo backtest. Identifiqué los modelos usando solo los primeros 392 meses y añadí una variable de calendario conocida anticipadamente. SARIMAX obtuvo el menor RMSE, 1.082,02 millones, cerca de 50,40 % menos que el estacional ingenuo. Su ventaja frente a SARIMA fue modesta y no prueba significancia. El SARIMA conserva autocorrelación residual. Esta es la referencia que buscaré superar con una evaluación temporal igualmente cuidadosa”.')

doc.save(OUT)
for path,digest in hashes.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
print(str(OUT));print('Parrafos',len(doc.paragraphs),'Tablas',len(doc.tables),'Imagenes',len(doc.inline_shapes))