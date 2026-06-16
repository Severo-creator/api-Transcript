import os
import django
import pandas as pd
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')
django.setup()

from core.models import Base
from core.models import Pedido
from core.models import Rede
from core.models import Categoria
from core.models import Opera
from core.models import Oferta
from core.models import Ncm

def gerar_oferta(ean):
    
    base = Base.objects.get(ean=ean)
    rede = Rede.objects.get(ean=ean)

    opera = Opera.objects.get(
        categoria=base.categoria
    )
    ncm = Ncm.objects.get(
        ncm=base.ncm
    )

    tributo = opera.total_opera + ncm.tributo_n
    valorprod = base.preco_venda_embalagem_f

    precoferta = valorprod * (1 + tributo  / 100)
    print("Base:", base)
    print("Base PK:", base.pk)
    print("EAN:", base.ean)

    oferta, criada = Oferta.objects.get_or_create(    
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

    print(oferta.preco_embalagem_oferta)
    print(rede.preco_venda_r)

    if abs((oferta.preco_embalagem_oferta  / rede.preco_venda_r) -1)<= 0.4:
        print("pedido")
        pedido = Pedido.objects.get_or_create(
            ean=rede,
        defaults={
            'sku_f': base.sku_f,
            'sku_r': rede.sku_r,
            'descricao_r': rede.descricao_r,
            'valortotal_ped': oferta.preco_embalagem_oferta,
        }
        )

gerar_oferta('7899706100001')