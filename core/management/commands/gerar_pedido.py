import os
import django



os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "transcript.settings"
)
django.setup()

from datetime import timedelta
from django.utils import timezone

from core.models import Fornecedor, Rede, Oferta, Pedido, Ncm

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Gera pedidos"

    def handle(self, *args, **options):
        print("Executando...")


    def gerar_oferta(ean, percentual_limite):

        try:
            fornecedor = Fornecedor.objects.get(ean=ean)
            rede = Rede.objects.get(ean=fornecedor)

        except (Fornecedor.DoesNotExist, Rede.DoesNotExist):
            return False

        # Ajuste este campo para o nome real no seu model
        preco_base = fornecedor.preco_fornecedor

        preco_oferta = preco_base * 1.10

        oferta = Oferta.objects.create(
            ean=fornecedor,
            preco_oferta=preco_oferta
        )

        diferenca_percentual = (
            (rede.preco_venda_r - preco_oferta)
            / rede.preco_venda_r
        ) * 100

        aceito = diferenca_percentual > percentual_limite

        if aceito:

            Pedido.objects.create(
                preco_pedido=preco_oferta,
                data_ped=timezone.now().date() + timedelta(days=7)
            )

        return aceito