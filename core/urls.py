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

urlpatterns = router.urls