import pandas as pd
from apps.manpower.models import Personal  

def cargar_datos_personal(archivo_excel):
    df = pd.read_excel(archivo_excel)

    for _, row in df.iterrows():
        # Verifica si 'Nss' no es nulo antes de convertirlo a entero
        inss = str(int(row['INSS'])).strip() if pd.notna(row['INSS']) else ""

        # Obtén los datos de las otras columnas con verificación de nulos
        cedula = str(row['Cédula']).strip() if pd.notna(row['Cédula']) else ""
        nombre = str(row['Nombre']).strip() if pd.notna(row['Nombre']) else ""
        Personal.objects.update_or_create(
            cedula=cedula,
            defaults={'nombre': nombre, 'inss': inss}
        )

    print("Datos cargados exitosamente")
