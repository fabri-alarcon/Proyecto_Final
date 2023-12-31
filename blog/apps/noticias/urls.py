from django.urls import path
from . import views
from .views import *


app_name = "noticias"

# urls de app noticias
urlpatterns = [
    path("", views.inicio, name= "inicio"),
     # url para el detalle de la noticia por pk
    path('detalle<int:pk>', views.Detalle_Noticias, name='detalle'),

    # url del formulario de contacto
    path('contacto', views.contacto, name="contacto"),

      # URL COMENTARIO
    path('comentario', views.Comentar_Noticia, name='comentar'),

    # path('editnoticia', views.editnoticia, name='editar'),

    path('post/edit/<int:pk>/', views.editnoticia.as_view(), name="post-edit"),
    path('post/delete/<int:pk>', views.deletnoticia.as_view(), name="post-delete"),
]