from django.urls import path
from . import views

urlpatterns = [
    path('', views.DetalhesIndex.as_view(), name='detalhes'),
    path('Detalhe/<int:pk>', views.DetalheIndex.as_view(), name='detalhe'),
    path('Busca/', views.PostBusca.as_view(), name='post_busca'),
    path('aprovar/<int:pk>', views.Aprovar.as_view(), name='aprovar'),
    path('reprovar/<int:pk>', views.Reprovar.as_view(), name='reprovar'),
]