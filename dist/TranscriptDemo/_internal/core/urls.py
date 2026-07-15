from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'categorias', CategoriaViewSet)
router.register(r'fornecedores', FornecedorViewSet)
router.register(r'redes', RedeViewSet)
router.register(r'ofertas', OfertaViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'opera', OperaViewSet)
router.register(r'bases', BaseViewSet)
router.register(r'ncm', NcmViewSet)

urlpatterns = [
    path('importar-fornecedor-rede/', ImportarFornecedorRedeView.as_view()),
    path('gerar-ofertas-validas/', GerarOfertasValidasView.as_view()),
    path('', include(router.urls)),
]
