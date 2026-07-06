import os
import django
import pandas as pd
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')
django.setup()

from core.models import Fornecedor, Rede, Base, Categoria, Opera, Oferta, Ncm


def importar_fornecedor_rede():
    dfFon = pd.read_excel('planilhasfontes/FORN_050626.xlsx')
    dfRede = pd.read_excel('planilhasfontes/REDE_050626.xlsx')

    dfFon.columns = dfFon.columns.str.strip()
    dfRede.columns = dfRede.columns.str.strip()

    dfFon = dfFon.drop_duplicates(subset=['EAN'])
    dfRede = dfRede.drop_duplicates(subset=['EAN'])

    print(dfFon.columns.tolist())
    print(dfRede.columns.tolist())

    categorias_disponiveis = [1001, 1002, 1003, 1004, 1005]

    for _, row in dfFon.iterrows():
        ean = str(row['EAN'])
        ncm_valor = str(row['NCM'])
        preco = row['Preço Médio Atacado (R$)']
        embalagem = row['Qtde Caixa']

        fornecedor, _ = Fornecedor.objects.update_or_create(
            ean=ean,
            defaults={
                'ncm': ncm_valor,
                'descricao_f': row['Descrição'],
                'preco_venda_embalagem_f': preco,
                'embalagem_f': embalagem,
                'preco_unitario_f': preco / embalagem if embalagem else None,
                'estoque_f': 100,
                'industria': 'Industria Arbitraria',
                'marca': 'Marca Arbitraria'
            }
        )

        Ncm.objects.get_or_create(
            ncm=ncm_valor,
            defaults={
                'descricao_n': 'Descricao arbitraria',
                'tributo_n': 2.5
            }
        )

        categoria_obj = Categoria.objects.get(
            categoria=random.choice(categorias_disponiveis)
        )

        Base.objects.update_or_create(
            ean=fornecedor,
            defaults={
                'ncm': ncm_valor,
                'sku_f': ncm_valor,
                'descricao_f': row['Descrição'],
                'categoria': categoria_obj,
                'industria': 'Industria Arbitraria',
                'marca': 'Marca Arbitraria',
                'preco_custo_embalagem_f': preco * 0.8,
                'preco_venda_embalagem_f': preco,
                'embalagem_f': embalagem,
                'preco_unitario_f': preco / embalagem if embalagem else None,
                'estoque_f': 100
            }
        )

    for _, row in dfRede.iterrows():
        fornecedor = Fornecedor.objects.get(ean=str(row['EAN']))

        Rede.objects.update_or_create(
            ean=fornecedor,
            defaults={
                'descricao_r': row['Descrição'],
                'sku_r': row['NCM'],
                'preco_venda_r': row['Preço Médio Atacado (R$)'],
                'contrato_r': row['Dif %'],
                'preco_ultima_compra': row['COMPRA']
            }
        )


def gerar_ofertas_validas(taxa=0.2, qtd_ped=20):
    bases = Base.objects.all()

    ofertas_criadas = 0
    produtos_validos = []

    for base in bases:
        try:
            rede = Rede.objects.get(ean=base.ean)
            opera = Opera.objects.get(categoria=base.categoria)
            ncm = Ncm.objects.get(ncm=base.ncm)

            if base.estoque_f is not None and base.estoque_f < qtd_ped:
                continue

            tributo = opera.total_opera + ncm.tributo_n
            valorprod = base.preco_venda_embalagem_f

            if valorprod is None or rede.preco_venda_r is None or base.embalagem_f in [None, 0]:
                continue

            precoferta = valorprod * (1 + tributo / 100)

            print(base.ean)
            print(precoferta)

            # Produto válido: preço da oferta dentro da taxa aceita em relação à rede
            if abs((precoferta / rede.preco_venda_r) - 1) <= taxa:
                Oferta.objects.update_or_create(
                    ean=base,
                    defaults={
                        'sku_f': base.sku_f,
                        'sku_r': rede.sku_r,
                        'descricao_r': rede.descricao_r,
                        'preco_embalagem_oferta': precoferta,
                        'preco_unitario_oferta': precoferta / base.embalagem_f,
                        'embalagem_f': base.embalagem_f
                    }
                )

                produtos_validos.append(base.ean.ean)
                ofertas_criadas += 1

        except (Rede.DoesNotExist, Opera.DoesNotExist, Ncm.DoesNotExist):
            continue

    return {
        "mensagem": "Produtos válidos adicionados em Oferta.",
        "ofertas_criadas_ou_atualizadas": ofertas_criadas,
        "produtos_validos": produtos_validos
    }


if __name__ == "__main__":
    importar_fornecedor_rede()

    resultado = gerar_ofertas_validas(
        taxa=0.2,
        qtd_ped=20
    )

    print(resultado)