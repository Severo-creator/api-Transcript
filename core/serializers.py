from rest_framework import serializers
from .models import *

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class RedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rede
        fields = '__all__'

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'

class OperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opera
        fields = '__all__'

class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Base
        fields = '__all__'

class NcmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ncm
        fields = '__all__'