import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcript.settings')
django.setup()

from core.models import Base, Fornecedor, Categoria

fornecedor = Fornecedor.objects.get(ean="7899706100001")

categoria = Categoria.objects.get(categoria=1001)

Base.objects.create(
    ean=fornecedor,
    ncm="3305.90.00",
    sku_f="SKU123",
    descricao_f="L'Oréal Paris SKU 01",
    categoria=categoria,
    industria="Industria X",
    marca="Marca Y",
    preco_custo_embalagem_f=10.50,
    preco_venda_embalagem_f=12.0,
    embalagem_f=12,
    preco_unitario_f=1.325,
    estoque_f=100
)