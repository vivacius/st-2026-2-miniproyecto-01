"use strict";
const D = window.DATOS;
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num = (value, digits = 2) => Number(value).toLocaleString('es-CO', {minimumFractionDigits: digits, maximumFractionDigits: digits});
const pvalue = value => Number(value) < .000001 ? Number(value).toExponential(6).replace('.', ',') : num(value, 6);
const labels = D.metricas.map(r => r.modelo.startsWith('SARIMAX') ? 'SARIMAX' : r.modelo.startsWith('SARIMA') ? 'SARIMA' : r.modelo === 'ingenuo' ? 'Ingenuo' : 'Estacional ingenuo');
const mx = D.metricas.find(r => r.modelo.startsWith('SARIMAX'));
const ma = D.metricas.find(r => r.modelo.startsWith('SARIMA'));
const baseline = D.metricas.find(r => r.modelo === 'estacional ingenuo');
const mejora = 100 * (1 - Number(mx.RMSE) / Number(baseline.RMSE));
const incremental = 100 * (1 - Number(mx.RMSE) / Number(ma.RMSE));
const fig = (file, title, wide = false) => `<figure class="figure ${wide ? 'wide' : ''}"><button data-figure="${file}" data-title="${title}" aria-label="Ampliar ${title}"><img src="../figuras/${file}.png" alt="${title}"></button><figcaption><span>Python · ${file}.png</span><span>Ampliar ↗</span></figcaption></figure>`;
const source = (file, fn) => `<button data-source="${file}:${fn}">${file} · ${fn}() ↗</button>`;
const table = (headers, rows) => `<table><thead><tr>${headers.map(h=>`<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map((r,i)=>`<tr class="${i===0?'highlight':''}">${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
const literal = (file, fn, first, last) => {
  const lines = D.fuentes[`${file}:${fn}`].codigo.split('\n');
  const start = lines.findIndex(l => l.includes(first));
  const end = lines.findIndex((l,i) => i>=start && l.includes(last));
  if(start<0 || end<0) throw new Error('Fragmento no encontrado en el código real');
  return esc(lines.slice(start,end+1).join('\n'));
};
const slides = [
 {name:'Introducción', time:'0:45', kicker:'Miniproyecto 1 · Pronóstico mensual', title:'De las líneas base<br>al mejor modelo clásico.', hero:true,
 body:`<p class="subtitle">Una comparación reproducible sobre ventas de tiendas de mercancías generales en Estados Unidos.</p><div class="hero-flow"><span>Ingenuos</span><span>→</span><span>SARIMA</span><span>→</span><b>SARIMAX</b></div><div class="stats"><div class="stat"><div class="big">416</div><small>observaciones mensuales</small></div><div class="stat"><div class="big">4</div><small>modelos · un mismo backtest</small></div><div class="stat"><div class="big green">${num(mejora,1)} %</div><small>menos RMSE frente a la mejor línea base</small></div></div><div class="author"><strong>Santiago Correa Campaña</strong><br><span class="muted">UAO · Maestría en IA y Ciencia de Datos · 2026-II</span><br><span class="micro">Serie MRTSSM452USN · apoyo a la demostración del código</span></div>`,
 sources:[['miniproyecto.py','main']], notes:'Objetivo: comparar métodos, no forzar un ganador. Este recorrido suma 10:40 y deja margen para una demostración breve. La guía original reserva 7 minutos de exposición y 8 de preguntas: si se mantiene ese formato, resume cada pantalla a 40–45 segundos. Inicia el cronómetro al empezar.'},
 {name:'Datos y serie',time:'1:10',kicker:'01 / Datos',title:'Una serie larga, con un ciclo visible.',
 body:`${fig('serie','Ventas mensuales de mercancías generales',true)}<div class="stats"><div class="stat"><strong>Ene. 1992 → ago. 2026</strong><small>416 meses · millones de USD · sin ajuste estacional</small></div><div class="stat"><strong class="green">0 faltantes · 0 duplicados</strong><small>No se imputaron observaciones.</small></div><div class="stat"><strong>Extremos conservados</strong><small>No hay evidencia de errores de medición.</small></div></div><p class="micro">Fuente: <a href="https://fred.stlouisfed.org/series/MRTSSM452USN" target="_blank" rel="noopener">FRED / U.S. Census Bureau</a> · Public Domain: Citation Requested.</p>`,
 sources:[['comun.py','cargar_serie'],['miniproyecto.py','preparar']],notes:'Explica la unidad: ventas nominales, no crecimiento real. Señala los picos anuales y el tramo 2020–2024. Un dato extremo no es necesariamente un error. La lectura del CSV y su frecuencia mensual se realizan en cargar_serie; preparar rechaza faltantes y valores no finitos.'},
 {name:'Descomposición STL',time:'1:15',kicker:'02 / Componentes',title:'Tendencia creciente. Diciembre destaca.',
 body:`<div class="grid figure-first">${fig('stl','Descomposición STL robusta, periodo 12')}<div class="stack"><div class="formula">Yₜ = Tₜ + Sₜ + Rₜ</div><div><p class="big green">+18.857,60</p><p class="muted">Diciembre · efecto estacional medio</p></div><div><p class="big blue">−6.592,12</p><p class="muted">Febrero · efecto estacional medio</p></div><div class="callout">Mayor residuo absoluto:<br><strong>diciembre de 2020 · −5.850,21</strong></div><p class="micro">Millones de USD. STL robusta, periodo 12. Análisis descriptivo de la muestra completa; no alimenta la selección de modelos.</p></div></div>`,
 sources:[['miniproyecto.py','descomponer']],notes:'Amplía la figura y recorre tendencia, estacionalidad y residuo. La tendencia pasa de 20.015,40 a 80.982,93. Los efectos por mes son promedios del componente estacional, no ventas. robust=True reduce la influencia de observaciones inusuales; no elimina datos ni demuestra su causa.'},
 {name:'Estacionariedad',time:'1:25',kicker:'03 / Identificación',title:'La identificación termina en agosto de 2024.',
 body:`<div class="grid equal"><div class="stack"><div class="panel">${table(['Transformación','ADF','Valor p'], D.adf.map(r=>[esc(r.version),num(r.estadistico,4),pvalue(r.p_valor)]))}</div><div class="callout"><strong>d = 0 · D = 1 · s = 12</strong><br>Wₜ = Yₜ − Yₜ₋₁₂</div><p class="micro">H₀: raíz unitaria. Original con constante y tendencia; diferencias con constante. ADF no prueba por sí solo todas las raíces estacionales.</p></div><div class="stack">${fig('acf_pacf','ACF y PACF de la diferencia estacional sobre 392 meses')}<div class="range-labels"><strong class="blue">392 meses: identificación y AIC</strong><strong class="green">24 meses: evaluación</strong></div><p class="micro">ADF rechaza la raíz unitaria tras diferenciar estacionalmente. La dependencia restante se modela con términos AR y MA.</p></div></div>`,
 sources:[['miniproyecto.py','estacionariedad'],['miniproyecto.py','main']],notes:'La original tiene p≈0,0997; la diferencia estacional p≈0,000175. Mantengo provisionalmente d=0 y D=1: añadir otra diferencia no es obligatorio. ACF inicial ≈0,64, 0,64, 0,67; PACF ≈0,64, 0,39, 0,33. Estacionariedad no equivale a ruido blanco. Los 24 meses finales no eligen los órdenes.'},
 {name:'Selección SARIMA',time:'1:05',kicker:'04 / Selección',title:'Una rejilla pequeña, una comparación por AIC.',
 body:`<div class="grid"><div class="panel">${table(['Orden (p,d,q)','Estacional (P,D,Q,s)','AIC'],D.aic.slice(0,5).map(r=>[esc(r.orden),esc(r.estacional),num(r.AIC)]))}<p class="micro" style="margin-top:16px">Los cinco mejores de ${D.aic.length} candidatos convergentes · resultados/aic_sarima.csv</p></div><div class="stack"><span class="tag">p,q ∈ {0,1,2} · P,Q ∈ {0,1}</span><h3>SARIMA(1,0,2)(1,1,1)₁₂</h3><div><p class="big green">${num(D.aic[0].AIC)}</p><p class="muted">menor AIC de la rejilla</p></div><div class="formula">AIC = 2k − 2 log L</div><p class="subtitle">Equilibra ajuste y complejidad. Un AIC menor no garantiza mejores pronósticos ni residuos blancos.</p></div></div>`,
 sources:[['miniproyecto.py','elegir_sarima']],notes:'La rejilla contiene 3×3×2×2=36 combinaciones. d y D quedan fijos y todos se ajustan con los primeros 392 meses. El segundo candidato está muy cerca: no interpretes esta elección como certeza de un modelo verdadero. El backtest es la evaluación predictiva independiente.'},
 {name:'Diagnóstico residual',time:'1:10',kicker:'05 / Diagnóstico',title:'Buen pronóstico no significa residuos blancos.',
 body:`<div class="grid figure-first">${fig('residuos','Residuos SARIMA y su autocorrelación')}<div class="stack"><div class="panel">${table(['Rezago','Ljung–Box','Valor p'],D.ljung.map(r=>[r.rezago,num(r.lb_stat,6),Number(r.lb_pvalue).toExponential(6)]))}</div><p><strong>model_df = 5</strong><br><span class="muted">p + q + P + Q = 1 + 2 + 1 + 1</span></p><p class="micro">27 residuos de inicialización excluidos. Diagnóstico sobre el periodo de selección: 365 residuos.</p><div class="callout amber">Se rechaza la ausencia de autocorrelación.<br><strong>El SARIMA todavía deja dependencia sin explicar.</strong></div></div></div>`,
 sources:[['miniproyecto.py','elegir_sarima'],['miniproyecto.py','ajustar']],notes:'H₀ de Ljung–Box: ausencia conjunta de autocorrelación hasta el rezago elegido. Los grados de libertad son 12−5=7 y 24−5=19. Se excluye el máximo entre loglikelihood_burn y nobs_diffuse. No cambié el modelo para conseguir p>0,05. Este diagnóstico corresponde a SARIMA, no permite concluir que SARIMAX tenga residuos blancos.'},
 {name:'SARIMAX y backtest',time:'1:30',kicker:'06 / Evaluación',title:'Solo el pasado; el calendario sí se conoce.',
 body:`<div class="grid equal"><div class="stack"><div class="panel"><h3>13 orígenes · horizonte de 12 meses</h3><label for="origen" class="micro">Explorar el origen de pronóstico</label><input id="origen" type="range" min="0" max="12" value="0"><div class="timeline" aria-hidden="true"><div class="train" id="train"></div><div class="test" id="test"></div><div class="unused" id="unused"></div></div><p id="ventana" aria-live="polite"></p><p class="micro" style="margin-top:12px">Azul: entrenamiento disponible · verde: 12 meses evaluados · gris: meses posteriores. Las métricas se promedian sobre los 13 orígenes.</p></div><pre class="code-inline">${literal('comun.py','backtest','for corte in range','pronostico = np.asarray')}</pre></div><div class="stack"><div class="callout"><strong>Exógena: días de lunes a viernes</strong><br>Determinada por calendario. No descuenta festivos ni requiere ventas futuras.</div><pre class="code-inline">${literal('miniproyecto.py','exogenas','for fecha in fechas','dias.append')}</pre><pre class="code-inline">${literal('miniproyecto.py','modelo_sarimax','x_entrenamiento =','x_futuro =')}</pre></div></div>`,
 sources:[['comun.py','backtest'],['miniproyecto.py','exogenas'],['miniproyecto.py','modelo_sarimax']],notes:'Mueve el control: primer origen agosto de 2024 y último agosto de 2025. En cada paso se reajusta el modelo; se incorporan ventas ya observadas, nunca las futuras al origen. Los órdenes permanecen fijos. Las ventanas se solapan: 13 orígenes no son 13 muestras independientes. Abre el código y muestra x.loc con índices de entrenamiento y fechas futuras.'},
 {name:'Resultados',time:'1:20',kicker:'07 / Resultados',title:'SARIMAX obtiene el menor error.',
 body:`<div class="grid equal"><div class="panel"><p class="micro">RMSE · millones de USD · menor es mejor</p>${D.metricas.map((r,i)=>`<div class="bar-row ${r===mx?'winner':''}"><span>${labels[i]}</span><div class="bar-track"><div class="bar-fill" style="width:${100*Number(r.RMSE)/Math.max(...D.metricas.map(x=>Number(x.RMSE)))}%"></div></div><strong>${num(r.RMSE)}</strong></div>`).join('')}<p class="micro">Barras proporcionales desde cero, calculadas con metricas.csv.</p></div><div class="stack"><div class="panel">${table(['Modelo','RMSE','MAE','MAPE %'],D.metricas.map((r,i)=>[labels[i],num(r.RMSE),num(r.MAE),num(r.MAPE)]))}</div><div class="stats" style="grid-template-columns:1fr 1fr"><div class="stat"><div class="big green">−${num(mejora,1)} %</div><small>RMSE vs. estacional ingenuo</small></div><div class="stat"><div class="big blue">−${num(incremental)} %</div><small>RMSE vs. SARIMA</small></div></div><p class="micro">RMSE y MAE: millones de USD. Mejora relativa calculada con las métricas redondeadas del CSV.</p></div></div>`,
 sources:[['miniproyecto.py','fila'],['comun.py','rmse'],['comun.py','backtest']],notes:'Primero compara con la mejor línea base, no solo con el ingenuo. El salto principal viene de modelar la estructura temporal; añadir calendario mejora modestamente el SARIMA. No afirmes significancia estadística de la diferencia: aquí se compara el desempeño observado en este backtest.'},
 {name:'Conclusiones',time:'1:00',kicker:'08 / Cierre',title:'Una referencia clásica, con límites explícitos.',
 body:`<div class="grid"><div><div class="conclusion"><span class="ordinal">01</span><div><h3>SARIMAX es la referencia predictiva</h3><p>Menor RMSE en la ventana evaluada; ${num(mejora,1)} % de mejora frente al estacional ingenuo.</p></div></div><div class="conclusion"><span class="ordinal">02</span><div><h3>El calendario aporta una mejora modesta</h3><p>${num(incremental)} % menos RMSE frente a SARIMA. No equivale a una ventaja universal.</p></div></div><div class="conclusion"><span class="ordinal">03</span><div><h3>El diagnóstico deja una tarea abierta</h3><p>Persiste autocorrelación en SARIMA. El Miniproyecto 2 deberá superar esta referencia con el mismo protocolo.</p></div></div></div><div class="stack"><div class="panel"><span class="eyebrow">Demostración en el editor</span><h3 style="margin:18px 0">Del dato al resultado</h3><p class="subtitle">1. Separación temporal en main()<br>2. Exógena de calendario<br>3. Ventanas en backtest()<br>4. CSV y control de convergencia</p></div><div class="callout"><strong>python miniproyecto.py</strong><br>El HTML acompaña la explicación; no ejecuta ni sustituye el código Python.</div><p class="micro">La entrega evaluable continúa siendo docs/informe.md. Esta presentación es un apoyo para la sustentación.</p></div></div>`,
 sources:[['miniproyecto.py','main'],['miniproyecto.py','ajustar'],['comun.py','backtest']],notes:'Cierra distinguiendo desempeño predictivo y diagnóstico. Muestra el comando de ejecución si el docente lo solicita; todos los ajustes del backtest convergieron en la validación registrada. Evita prometer resultados fuera del periodo evaluado. Deja tiempo para preguntas sobre d/D, exógenas y fuga de información.'}
];
const main = document.querySelector('#contenido');
main.innerHTML = slides.map((s,i)=>`<section class="slide ${s.hero?'hero':''}" id="pantalla-${i+1}" ${i?'hidden':''} aria-labelledby="titulo-${i}"><div class="eyebrow">${s.kicker}</div><div class="title-row"><${s.hero?'h1':'h2'} id="titulo-${i}" tabindex="-1">${s.title}</${s.hero?'h1':'h2'}><span class="tag">${s.time} sugeridos</span></div>${s.body}<div class="source-row"><small>VER CÓDIGO REAL</small>${s.sources.map(x=>source(...x)).join('')}</div><aside class="notes" hidden><strong>Notas del expositor · ${s.time}</strong><p>${s.notes}</p></aside></section>`).join('');
const menu = document.querySelector('#menu');
menu.innerHTML = slides.map((s,i)=>`<button data-slide="${i}">${String(i+1).padStart(2,'0')} &nbsp; ${s.name}</button>`).join('');
let current = 0, notes = false;
const sections = [...document.querySelectorAll('.slide')];
function show(index, focus=true) {
 current = Math.max(0,Math.min(slides.length-1,index));
 sections.forEach((s,i)=>s.hidden=i!==current);
 document.querySelector('#numero').textContent=`${String(current+1).padStart(2,'0')} / 09`;
 document.querySelector('#tema').textContent=slides[current].name;
 document.querySelector('#progreso').value=current+1;
 document.querySelector('#anterior').disabled=current===0;
 document.querySelector('#siguiente').disabled=current===slides.length-1;
 menu.querySelectorAll('button').forEach((b,i)=>b.setAttribute('aria-current',i===current?'step':'false'));
 location.hash=`${current+1}`;
 if(focus) document.querySelector(`#titulo-${current}`).focus({preventScroll:true});
 window.scrollTo(0,0);
}
document.querySelector('#anterior').onclick=()=>show(current-1);
document.querySelector('#siguiente').onclick=()=>show(current+1);
const indexButton=document.querySelector('#indice');
indexButton.onclick=()=>{menu.hidden=!menu.hidden;indexButton.setAttribute('aria-expanded',String(!menu.hidden));};
menu.onclick=e=>{const b=e.target.closest('[data-slide]');if(b){show(Number(b.dataset.slide));menu.hidden=true;indexButton.setAttribute('aria-expanded','false');}};
document.querySelector('#notas').onclick=()=>{notes=!notes;document.querySelectorAll('.notes').forEach(n=>n.hidden=!notes);document.querySelector('#notas').setAttribute('aria-pressed',String(notes));};
document.querySelector('#pantalla').onclick=async()=>{try{if(document.fullscreenElement) await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{document.querySelector('#pantalla').textContent='Usa F11';}};
let elapsed=0,started=null;
const timeButton=document.querySelector('#reloj');
function tick(){const seconds=Math.floor((elapsed+(started===null?0:performance.now()-started))/1000);document.querySelector('#tiempo').textContent=`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`;document.querySelector('.clock').classList.toggle('warn',seconds>=720);document.querySelector('.clock').classList.toggle('over',seconds>=900);}
timeButton.onclick=()=>{if(started===null){started=performance.now();timeButton.textContent='Pausar';}else{elapsed+=performance.now()-started;started=null;timeButton.textContent='Continuar';}tick();};
document.querySelector('#reiniciar').onclick=()=>{elapsed=0;started=null;timeButton.textContent='Iniciar';tick();};
setInterval(tick,250);
const imageModal=document.querySelector('#figuraModal'), codeModal=document.querySelector('#codigoModal');
main.addEventListener('click',e=>{
 const figure=e.target.closest('[data-figure]');
 if(figure){const image=document.querySelector('#figuraGrande');image.src=`../figuras/${figure.dataset.figure}.png`;image.alt=figure.dataset.title;image.classList.remove('zoomed');document.querySelector('#zoom').textContent='Zoom 150 %';document.querySelector('#figuraTitulo').textContent=figure.dataset.title;imageModal.showModal();}
 const button=e.target.closest('[data-source]');
 if(button){const f=D.fuentes[button.dataset.source];document.querySelector('#codigoTitulo').textContent=`${f.archivo} · ${f.funcion}() · línea ${f.linea}`;document.querySelector('#codigoTexto').textContent=f.codigo;document.querySelector('#codigoArchivo').href=`../${f.archivo}`;codeModal.showModal();}
});
document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>b.closest('dialog').close());
document.querySelector('#zoom').onclick=()=>{const zoomed=document.querySelector('#figuraGrande').classList.toggle('zoomed');document.querySelector('#zoom').textContent=zoomed?'Ajustar figura':'Zoom 150 %';};
document.addEventListener('keydown',e=>{
 if(document.querySelector('dialog[open]')||e.altKey||e.ctrlKey||e.metaKey||['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName))return;
 if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();show(current+1);}
 if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();show(current-1);}
 if(e.key.toLowerCase()==='n')document.querySelector('#notas').click();
 if(e.key.toLowerCase()==='f')document.querySelector('#pantalla').click();
 if(e.key==='Escape'){menu.hidden=true;indexButton.setAttribute('aria-expanded','false');}
});
const month = offset => new Date(Date.UTC(2024,7+offset,1)).toLocaleDateString('es-CO',{month:'short',year:'numeric',timeZone:'UTC'});
function windowUpdate(){const offset=Number(document.querySelector('#origen').value);document.querySelector('#train').style.width=`${100*(392+offset)/416}%`;document.querySelector('#test').style.width=`${100*12/416}%`;document.querySelector('#unused').style.width=`${100*(12-offset)/416}%`;document.querySelector('#ventana').textContent=`Origen ${offset+1}/13: ${month(offset)} · ${392+offset} meses disponibles. Evaluación: ${month(offset+1)} → ${month(offset+12)}.`;}
document.querySelector('#origen').oninput=windowUpdate;windowUpdate();
window.addEventListener('hashchange',()=>{const n=Number(location.hash.slice(1));if(Number.isInteger(n)&&n>=1&&n<=9&&n-1!==current)show(n-1);});
const initial=Number(location.hash.slice(1));show(Number.isInteger(initial)&&initial>=1&&initial<=9?initial-1:0,false);
