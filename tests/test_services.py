from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from services import leer_academico,filtrar,resumen,tendencia,word_informe,pdf_informe,validar

def test_derecho():
    d=leer_academico();validar(d)
    part=filtrar(d,facultad='Derecho y Ciencias Políticas',indicadores=['Postulantes'])
    year=resumen(part)
    assert int(year[year.anio==2026].valor.iloc[0])==1958
    assert len(part[part.anio==2026].programa.unique())==2

def test_export():
    data=filtrar(leer_academico(),facultad='Derecho y Ciencias Políticas',indicadores=['Postulantes','Ingresantes'])
    assert word_informe(data,'Informe de prueba','Derecho')[:2]==b'PK'
    assert pdf_informe(data,'Informe de prueba','Derecho')[:4]==b'%PDF'

def test_tendencia():
    data=resumen(filtrar(leer_academico(),facultad='Derecho y Ciencias Políticas',indicadores=['Postulantes']))
    assert len(tendencia(data,3))==3
