import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')
django.setup()

dfCat = pd.read_excel('planilhasfontes/Categoria.xlsx')
dfCat = dfCat.drop_duplicates(subset=['Categoria'])

dfOp = pd.read_excel('planilhasfontes/Opera.xlsx')
dfOp = dfOp.drop_duplicates(subset=['Categoria'])

from core.models import Categoria
from core.models import Opera

dfCat.columns = dfCat.columns.str.strip()
dfOp.columns = dfOp.columns.str.strip()

print(dfCat.columns.tolist())
print(dfOp.columns.tolist())

categoria = []

for _, row in dfCat.iterrows():
    Categoria.objects.get_or_create(
        categoria=int(row['Categoria']),
        defaults={
            'desc_categoria': row['Desc'],
            'mark_categoria' : row['Marca'],
            'prioridade' : row['prioridade']
        }
    )

    

for _, row in dfOp.iterrows():

    categoria = Categoria.objects.get(
        categoria=int(row['Categoria'])
    )

    Opera.objects.get_or_create(
        categoria= categoria,
        defaults={
            'log_opera': row['Log'],
            'mark_opera': row['Marca'],
            'tributo_opera': row['Tributo'],
            'promotor_opera': row['Promotor'],
            'total_opera': row['Total']
        }
    )