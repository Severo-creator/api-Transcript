import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')
django.setup()

dfFon = pd.read_excel('planilhasfontes/FORN_050626.xlsx')
dfFon = dfFon.drop_duplicates(subset=['EAN'])

dfRede = pd.read_excel('planilhasfontes/REDE_050626.xlsx')
dfRede = dfRede.drop_duplicates(subset=['EAN'])

from core.models import Fornecedor
from core.models import Rede

dfFon.columns = dfFon.columns.str.strip()
dfRede.columns = dfRede.columns.str.strip()

print(dfFon.columns.tolist())
print(dfRede.columns.tolist())

fornecedor = []

for _, row in dfFon.iterrows():
    Fornecedor.objects.get_or_create(
        ean=str(row['EAN']),
        defaults={
            'ncm': row['NCM'],
            'descricao_f' : row['Descrição'],
            'preco_venda_embalagem_f' : row['Preço Médio Atacado (R$)'],
            'embalagem_f' : row['Qtde Caixa']
        }
    )

    

for _, row in dfRede.iterrows():

    fornecedor = Fornecedor.objects.get(
        ean=str(row['EAN'])
    )

    Rede.objects.get_or_create(
        ean= fornecedor,
        defaults={
            'descricao_r': row['Descrição'],
            'sku_r': row['NCM'],
            'preco_venda_r': row['Preço Médio Atacado (R$)'],
            'contrato_r': row['Dif %'],
            'preco_ultima_compra': row['COMPRA']
        }
    )