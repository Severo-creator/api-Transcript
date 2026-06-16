import os
import django
import uuid



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')
django.setup()

from datetime import timedelta
from django.utils import timezone

from core.models import Fornecedor, Rede, Oferta, Pedido


def gerar_oferta(ean, percentual_limite):

    try:
        fornecedor = Fornecedor.objects.get(ean=ean)
        rede = Rede.objects.get(ean=fornecedor)

    except (Fornecedor.DoesNotExist, Rede.DoesNotExist):
        print("false")
        return False

    # Ajuste este campo para o nome real no seu model
    preco_base = fornecedor.preco_venda_embalagem_f

    preco_oferta = preco_base * 1.10

    oferta = Oferta.objects.get_or_create(
        id=uuid.uuid4().hex[:13],
        ean=fornecedor,
        preco_embalagem_oferta=preco_oferta
    )

    diferenca_percentual = (
        (rede.preco_venda_r - preco_oferta)
        / rede.preco_venda_r
    ) * 100
    print(diferenca_percentual, percentual_limite)

    aceito = abs(diferenca_percentual) > percentual_limite

    if aceito:
        print("Aceito")
        data_entrega = timezone.now() + timedelta(days=7)
        Pedido.objects.get_or_create(
            ean=fornecedor,
            preco_tab=preco_oferta,
            data_ped=data_entrega
        )

    return aceito
print("gogogo")
gerar_oferta("7899706100001", 10.0)