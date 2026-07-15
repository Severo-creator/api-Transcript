from pathlib import Path

import pandas as pd

from core.models import Base, Categoria, Fornecedor, Ncm, Oferta, Opera, Rede


def _resolver_caminho(caminho):
    arquivo = Path(str(caminho).strip().strip('"'))
    if not arquivo.is_absolute():
        arquivo = Path.cwd() / arquivo
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {arquivo}")
    return arquivo


def _valor_linha(row, *nomes):
    for nome in nomes:
        if nome in row and pd.notna(row[nome]):
            return row[nome]
    return None


def _texto(valor):
    if valor is None or pd.isna(valor):
        return ""
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor).strip()


def _numero(valor, padrao=0):
    if valor is None or pd.isna(valor):
        return padrao
    return float(valor)


def importar_fornecedor_rede(caminho_fornecedor, caminho_rede):
    arquivo_fornecedor = _resolver_caminho(caminho_fornecedor)
    arquivo_rede = _resolver_caminho(caminho_rede)

    df_fon = pd.read_excel(arquivo_fornecedor)
    df_rede = pd.read_excel(arquivo_rede)

    df_fon.columns = df_fon.columns.str.strip()
    df_rede.columns = df_rede.columns.str.strip()

    df_fon = df_fon.drop_duplicates(subset=["EAN"])
    df_rede = df_rede.drop_duplicates(subset=["EAN"])

    categorias = list(Categoria.objects.order_by("categoria"))
    if not categorias:
        categorias = [
            Categoria.objects.create(
                categoria=1001,
                desc_categoria="Categoria demonstracao",
                mark_categoria=10,
                prioridade="Media",
            )
        ]

    fornecedores_importados = 0
    bases_importadas = 0
    redes_importadas = 0
    sem_fornecedor = 0

    for indice, row in df_fon.iterrows():
        ean = _texto(_valor_linha(row, "EAN"))
        if not ean:
            continue

        ncm_valor = _texto(_valor_linha(row, "NCM"))
        descricao = _texto(_valor_linha(row, "Descricao", "Descrição", "DescriÃ§Ã£o"))
        preco = _numero(
            _valor_linha(
                row,
                "Preco Medio Atacado (R$)",
                "Preço Médio Atacado (R$)",
                "PreÃ§o MÃ©dio Atacado (R$)",
            )
        )
        embalagem = int(_numero(_valor_linha(row, "Qtde Caixa"), 1) or 1)
        categoria_obj = categorias[indice % len(categorias)]

        fornecedor, _ = Fornecedor.objects.update_or_create(
            ean=ean,
            defaults={
                "ncm": ncm_valor,
                "descricao_f": descricao,
                "preco_venda_embalagem_f": preco,
                "embalagem_f": embalagem,
                "preco_unitario_f": preco / embalagem if embalagem else None,
                "estoque_f": 100,
                "industria": "Industria demonstracao",
                "marca": "Marca demonstracao",
            },
        )
        fornecedores_importados += 1

        Ncm.objects.update_or_create(
            ncm=ncm_valor,
            defaults={
                "descricao_n": "Descricao demonstracao",
                "tributo_n": 2.5,
            },
        )

        Base.objects.update_or_create(
            ean=fornecedor,
            defaults={
                "ncm": ncm_valor,
                "sku_f": ncm_valor,
                "descricao_f": descricao,
                "categoria": categoria_obj,
                "industria": "Industria demonstracao",
                "marca": "Marca demonstracao",
                "preco_custo_embalagem_f": preco * 0.8,
                "preco_venda_embalagem_f": preco,
                "embalagem_f": embalagem,
                "preco_unitario_f": preco / embalagem if embalagem else None,
                "estoque_f": 100,
            },
        )
        bases_importadas += 1

    for _, row in df_rede.iterrows():
        ean = _texto(_valor_linha(row, "EAN"))
        if not ean:
            continue

        try:
            fornecedor = Fornecedor.objects.get(ean=ean)
        except Fornecedor.DoesNotExist:
            sem_fornecedor += 1
            continue

        Rede.objects.update_or_create(
            ean=fornecedor,
            defaults={
                "descricao_r": _texto(_valor_linha(row, "Descricao", "Descrição", "DescriÃ§Ã£o")),
                "sku_r": _texto(_valor_linha(row, "NCM")),
                "preco_venda_r": _numero(
                    _valor_linha(
                        row,
                        "Preco Medio Atacado (R$)",
                        "Preço Médio Atacado (R$)",
                        "PreÃ§o MÃ©dio Atacado (R$)",
                    )
                ),
                "contrato_r": _numero(_valor_linha(row, "Dif %")),
                "preco_ultima_compra": _numero(_valor_linha(row, "COMPRA")),
            },
        )
        redes_importadas += 1

    return {
        "mensagem": "Planilhas importadas com sucesso.",
        "fornecedores_importados": fornecedores_importados,
        "bases_importadas": bases_importadas,
        "redes_importadas": redes_importadas,
        "redes_ignoradas_sem_fornecedor": sem_fornecedor,
        "arquivo_fornecedor": str(arquivo_fornecedor),
        "arquivo_rede": str(arquivo_rede),
    }


def gerar_ofertas_validas(taxa=0.2, qtd_ped=20):
    bases = Base.objects.all()

    ofertas_criadas = 0
    produtos_validos = []
    ignorados = {
        "sem_cadastro_completo": 0,
        "estoque_insuficiente": 0,
        "dados_invalidos": 0,
        "fora_da_taxa": 0,
    }

    for base in bases:
        try:
            rede = Rede.objects.get(ean=base.ean)
            opera = Opera.objects.get(categoria=base.categoria)
            ncm = Ncm.objects.get(ncm=base.ncm)
        except (Rede.DoesNotExist, Opera.DoesNotExist, Ncm.DoesNotExist):
            ignorados["sem_cadastro_completo"] += 1
            continue

        if base.estoque_f is not None and base.estoque_f < qtd_ped:
            ignorados["estoque_insuficiente"] += 1
            continue

        valor_produto = base.preco_venda_embalagem_f
        preco_rede = rede.preco_venda_r
        embalagem = base.embalagem_f

        if valor_produto is None or preco_rede in [None, 0] or embalagem in [None, 0]:
            ignorados["dados_invalidos"] += 1
            continue

        tributo = (opera.total_opera or 0) + (ncm.tributo_n or 0)
        preco_oferta = valor_produto * (1 + tributo / 100)
        diferenca_percentual = abs((preco_oferta / preco_rede) - 1)

        if diferenca_percentual > taxa:
            ignorados["fora_da_taxa"] += 1
            continue

        Oferta.objects.update_or_create(
            ean=base,
            defaults={
                "sku_f": base.sku_f,
                "sku_r": rede.sku_r,
                "descricao_r": rede.descricao_r,
                "preco_embalagem_oferta": preco_oferta,
                "preco_unitario_oferta": preco_oferta / embalagem,
                "embalagem_f": embalagem,
            },
        )

        produtos_validos.append(
            {
                "ean": base.ean.ean,
                "descricao": rede.descricao_r or base.descricao_f,
                "preco_rede": round(preco_rede, 2),
                "preco_oferta": round(preco_oferta, 2),
                "diferenca_percentual": round(diferenca_percentual * 100, 2),
            }
        )
        ofertas_criadas += 1

    return {
        "mensagem": "Produtos validos adicionados em Oferta.",
        "ofertas_criadas_ou_atualizadas": ofertas_criadas,
        "produtos_analisados": bases.count(),
        "produtos_validos": produtos_validos,
        "ignorados": ignorados,
    }
