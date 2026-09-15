
from pathlib import Path
import pandas as pd
base=Path(__file__).resolve().parent
assert (base/"app.py").exists()
assert (base/"assets"/"plano_campus_unt_referencia.png").exists()
ed=pd.read_csv(base/"data"/"edificios_demo.csv")
am=pd.read_csv(base/"data"/"ambientes_demo.csv")
print("OK", len(ed), "edificios;", len(am), "ambientes")
