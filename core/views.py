from django.shortcuts import render



from .services import gerar_oferta

# Create your views here.
# core/views.py
from rest_framework import viewsets
from .models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .services import gerar_oferta

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer

class RedeViewSet(viewsets.ModelViewSet):
    queryset = Rede.objects.all()
    serializer_class = RedeSerializer

class OfertaViewSet(viewsets.ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class OperaViewSet(viewsets.ModelViewSet):
    queryset = Opera.objects.all()
    serializer_class = OperaSerializer

class BaseViewSet(viewsets.ModelViewSet):
    queryset = Base.objects.all()
    serializer_class = BaseSerializer

class NcmViewSet(viewsets.ModelViewSet):
    queryset = Ncm.objects.all()
    serializer_class = NcmSerializer

#from django.views import View
#from django.shortcuts import render

#class GerarOfertaView(APIView): 
#    def get(self, request): 
#        ean = request.GET.get("ean") 
 #       qtd_ped = int(request.GET.get("qtd_ped")) 
#        taxa = float(request.GET.get("taxa")) 
#
 #       resultado = gerar_oferta(ean, qtd_ped, taxa) 
#
 #       return Response(resultado)

#def oferta_page(request):
#    return render(request, "oferta.html")