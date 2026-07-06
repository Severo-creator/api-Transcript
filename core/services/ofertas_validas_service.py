from core.models import Base, Ncm, Oferta, Opera, Rede


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
