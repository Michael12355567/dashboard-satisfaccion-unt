import json,re
import pandas as pd
import plotly.express as px
import streamlit as st
from services import BASE, leer_academico, filtrar, resumen, tendencia, word_informe, pdf_informe, validar

st.set_page_config(page_title='Portal Estadístico UNT',page_icon='🎓',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.stApp {background:#F7F9FC;} .block-container{padding-top:1.25rem;}
h1,h2,h3 {color:#092653;} [data-testid="stSidebar"]{background:#EEF2F8;}
div[data-testid="stMetric"]{background:white;padding:15px;border:1px solid #DDE5EF;border-radius:9px;}
</style>''',unsafe_allow_html=True)

@st.cache_data
def base():
    df=leer_academico();validar(df)
    return df

original=base()
st.sidebar.title('🎓 Estadística UNT')
st.sidebar.caption('2021–2026 · Prototipo local basado en registros institucionales')
if 'extra_df' not in st.session_state:st.session_state.extra_df=None
full=pd.concat([original,st.session_state.extra_df],ignore_index=True) if st.session_state.extra_df is not None else original

facultades=['Toda la UNT']+sorted(full[full.dimension=='Facultad'].grupo.dropna().unique().tolist())
fac=st.sidebar.selectbox('Facultad',facultades)
carlist=sorted(full[(full.dimension=='Facultad') & ((full.grupo==fac) if fac!='Toda la UNT' else True)].programa.unique().tolist())
car=st.sidebar.selectbox('Carrera profesional',['Todas']+carlist)
sedes=['Todas']+sorted(full[full.dimension=='Sede'].grupo.dropna().unique().tolist())
sede=st.sidebar.selectbox('Sede',sedes)
ind=st.sidebar.multiselect('Indicadores académicos',sorted(full.indicador.unique()),default=sorted(full.indicador.unique()))
years=st.sidebar.slider('Periodo',2021,2026,(2021,2026))
anios=list(range(years[0],years[1]+1))
st.sidebar.info('Porcentaje de crecimiento y proyecciones son resultados calculados. El sistema no atribuye automáticamente cifras institucionales a una facultad sin desglose.')

filtered=filtrar(full,fac,car,sede,anios,ind)
annual=resumen(filtered)
st.title('Portal de Información Estadística UNT')
st.caption('Consultas, análisis histórico, informes editables y proyecciones orientativas · No publicado en línea')
if fac!='Toda la UNT':st.subheader(fac if car=='Todas' else f'{fac} · {car}')

pan,consultar,informe,predecir,asistente,otras,administracion=st.tabs(['📊 Panorama','🔎 Explorador','📄 Informes Word/PDF','📈 Proyecciones','💬 Consultas guiadas','🏛 Otros indicadores','⚙️ Administración'])
with pan:
    if annual.empty:st.warning('No se encontraron registros para los filtros. Prueba ampliar los años, carreras o sedes.')
    else:
        latest=annual.anio.max()
        current=annual[annual.anio==latest]
        columns=st.columns(min(4,len(current)))
        for c,(_,r) in zip(columns,current.head(4).iterrows()):c.metric(r.indicador,f'{int(r.valor):,}'.replace(',',' '),help=f'Año {latest}')
        choosing=st.selectbox('Visualizar indicador',list(annual.indicador.unique()),key='chartind')
        dat=annual[annual.indicador==choosing]
        fig=px.line(dat,x='anio',y='valor',markers=True,title=f'{choosing}: evolución anual',labels={'anio':'Año','valor':'Cantidad'})
        fig.update_layout(plot_bgcolor='white',paper_bgcolor='white',font_color='#092653',xaxis=dict(dtick=1))
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(annual.pivot_table(index='indicador',columns='anio',values='valor',aggfunc='sum'),use_container_width=True)
with consultar:
    st.subheader('Detalle por carrera y año')
    if filtered.empty:st.warning('Sin registros para este filtro.')
    else:
        pivot=filtered.pivot_table(index=['indicador','programa'],columns='anio',values='valor',aggfunc='sum')
        st.dataframe(pivot,use_container_width=True,height=450)
        st.download_button('Descargar datos filtrados (CSV)',filtered.to_csv(index=False).encode('utf-8-sig'),'estadisticas_unt.csv','text/csv')
        with st.expander('Gráfico comparativo de carreras'):
            selected=st.selectbox('Indicador a comparar',sorted(filtered.indicador.unique()),key='compare')
            comp=filtered[filtered.indicador==selected]
            st.plotly_chart(px.bar(comp,x='anio',y='valor',color='programa',barmode='group',title=selected),use_container_width=True)
with informe:
    st.subheader('Generador automático de informes')
    st.write('El informe utiliza la selección de facultad, carrera, sede, años e indicadores del panel lateral y genera un archivo real para descargar.')
    tt='Informe estadístico UNT' if fac=='Toda la UNT' else f'Informe estadístico de la Facultad de {fac}'
    if car!='Todas':tt+=f' – {car}'
    tt+=f', {years[0]}–{years[1]}'
    st.text_input('Título del informe',tt,key='titulo_informe')
    extra=st.text_area('Nota metodológica opcional','')
    if filtered.empty:st.warning('Selecciona datos antes de generar el informe.')
    else:
        c1,c2=st.columns(2)
        with c1:
            try:st.download_button('📄 Descargar Word (.docx)',word_informe(filtered,st.session_state.titulo_informe,fac if car=='Todas' else car,extra),file_name='Informe_Estadistico_UNT.docx',mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',use_container_width=True)
            except Exception as e:st.error(f'No se pudo generar Word: {e}')
        with c2:
            try:st.download_button('📕 Descargar PDF (.pdf)',pdf_informe(filtered,st.session_state.titulo_informe,fac if car=='Todas' else car),file_name='Informe_Estadistico_UNT.pdf',mime='application/pdf',use_container_width=True)
            except Exception as e:st.error(f'No se pudo generar PDF: {e}')
        st.caption('Diseño institucional adaptable. No reproduce pixel a pixel la plantilla histórica; incluye carátula, resultados por indicador y tablas editables.')
with predecir:
    st.subheader('Proyecciones orientativas')
    if annual.empty:st.warning('Selecciona al menos un indicador.')
    else:
        which=st.selectbox('Serie a proyectar',sorted(annual.indicador.unique()),key='projind')
        horizon=st.slider('Años futuros',1,5,3)
        hist=annual[annual.indicador==which].sort_values('anio')
        forecast=tendencia(hist,horizon)
        if forecast.empty:st.warning('Se necesitan al menos tres años observados para proyectar.')
        else:
            histplot=hist.rename(columns={'valor':'cantidad'}).assign(tipo='Observado')
            fplot=forecast.rename(columns={'estimacion':'cantidad'}).assign(tipo='Proyección')
            merged=pd.concat([histplot[['anio','cantidad','tipo']],fplot[['anio','cantidad','tipo']]])
            st.plotly_chart(px.line(merged,x='anio',y='cantidad',color='tipo',markers=True,title='Tendencia lineal (demostrativa)'),use_container_width=True)
            st.dataframe(forecast.rename(columns={'estimacion':'Estimación','inferior':'Banda inferior ilustrativa','superior':'Banda superior ilustrativa'}),hide_index=True,use_container_width=True)
            st.warning('Proyección estadística simple, no pronóstico oficial. Las bandas son descriptivas, no intervalos de confianza calibrados. Un cambio de admisión o política puede invalidar la extrapolación.')
with asistente:
    st.subheader('Consultas en lenguaje natural — motor verificable')
    st.write('Ejemplos: «¿Cuántos postulantes hubo en 2026?», «Muestra ingresantes 2021 a 2026», «¿Cuántos matriculados tiene esta facultad?»')
    q=st.text_input('Escribe tu consulta')
    if q:
        low=q.casefold();available=sorted(annual.indicador.unique())
        selected=next((k for k in available if k.casefold() in low),None)
        # Sin interpretación generativa: solo patrones reconocidos sobre filtros actuales.
        if not selected:st.info('No reconozco un indicador inequívoco. Prueba indicar "postulantes", "ingresantes", "matriculados", "vacantes", "bachilleres" o "titulados".')
        else:
            selected_data=annual[annual.indicador==selected]
            foundyears=[int(y) for y in re.findall(r'20\d{2}',low)]
            if foundyears and len(foundyears)==1:selected_data=selected_data[selected_data.anio==foundyears[0]]
            if selected_data.empty:st.warning('No hay datos para ese año y selección.')
            else:
                st.success(f'{selected}: '+', '.join(f'{int(r.anio)}: {int(r.valor):,}'.replace(',',' ') for r in selected_data.itertuples()))
                st.caption('Respuesta calculada exclusivamente con los registros filtrados. No es un modelo generativo ni consulta fuentes externas.')
with otras:
    st.subheader('Tablas institucionales adicionales')
    st.write('Información complementaria nacional/institucional: posgrado, docentes, administrativos, RENACYT, innovación, movilidad, convenios, bienestar y presupuesto. No se atribuye automáticamente a una facultad.')
    tables=json.loads((BASE/'data'/'tablas_institucionales.json').read_text(encoding='utf8'))
    names={7:'Tasa de ingreso',8:'Matrícula anual',11:'Egresados UNT',16:'Posgrado',22:'Personal docente UNT',23:'Grados docentes',24:'Administrativos',25:'Regímenes administrativos',26:'RENACYT',27:'Investigadores por facultad',28:'Laboratorios por facultad',29:'Patentes',30:'Startups',31:'Movilidad nacional/internacional',36:'Movilidad por carrera',38:'Convenios internacionales',41:'Convenios nacionales',42:'Bienestar',43:'Atenciones mensuales',45:'Comedor por facultad',47:'Presupuesto UNT'}
    number=st.selectbox('Tabla a consultar',list(names),format_func=lambda n:f'Tabla {n}: {names[n]}')
    data=tables[number-1]
    st.dataframe(pd.DataFrame(data['filas'],columns=data['columnas']),use_container_width=True,hide_index=True)
    st.caption('Se presenta la tabla tal como consta en el documento institucional, sin imputar atribuciones a programas o facultades.')
with administracion:
    st.subheader('Incorporar nuevos datos académicos (durante esta sesión)')
    st.write('Carga un CSV con las columnas indicador, dimension, grupo, programa, anio, valor. Las filas se validan y no se guardan permanentemente ni se publican.')
    upload=st.file_uploader('Archivo CSV',type=['csv'])
    if upload is not None:
        try:
            nd=pd.read_csv(upload)
            required=['indicador','dimension','grupo','programa','anio','valor']
            assert all(k in nd for k in required),'Faltan columnas obligatorias.'
            nd=nd[required].copy();nd.anio=pd.to_numeric(nd.anio,errors='raise').astype(int);nd.valor=pd.to_numeric(nd.valor,errors='raise')
            assert nd.dimension.isin(['Facultad','Sede']).all(),'Dimensiones no reconocidas'
            assert nd.indicador.isin(original.indicador.unique()).all(),'Indicadores no reconocidos'
            assert (nd.valor>=0).all(),'Hay valores negativos'
            dupl=pd.concat([original,nd]).duplicated(subset=['indicador','dimension','grupo','programa','anio']).sum()
            assert not dupl,f'Existen {dupl} claves duplicadas. No se reemplazaron datos existentes.'
            st.success(f'Validado: {len(nd)} registros nuevos.')
            if st.button('Incorporar temporalmente'):
                st.session_state.extra_df=nd;st.rerun()
        except Exception as e:st.error(f'Archivo no válido: {e}')
    if st.session_state.extra_df is not None:
        st.info('Hay datos temporales cargados para esta sesión.')
        if st.button('Retirar datos temporales'):st.session_state.extra_df=None;st.rerun()
    st.markdown('**Control de acceso:** prototipo local. Antes de un despliegue institucional se requiere autenticación, permisos, bitácora, protección de datos personales y aprobación de publicación.')
