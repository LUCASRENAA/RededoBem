"""controle_estoque URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/', views.registro),


                  path('registro/submit', views.submit_registro),
                  path('logout/', views.logout_user),

                  #path('inicio/',views.inicio),
                  path('conquista/', views.conquista),
                  path('home/', views.home),

                  path('inicio/perfil/submit', views.submit_perfil),
                  path('inicio/publicacao/curtir/<id_publicacao>', views.curtir),
                  path('inicio/publicacao/pretendoir/<id_publicacao>', views.pretender),

                  path('inicio/publicacao/descurtir/<id_publicacao>', views.descurtir),
                  path('inicio/publicacao/<id_publicacao>', views.editar),
                  path('inicio/publicacao/<id_publicacao>/submit', views.editarSubmit),

                  path('inicio/publicacao/submit', views.submit_postagem),
                  path('inicio/publicacao_imagem/submit', views.submit_postagem_imagem),
                  path('postagens', views.verPostagens),
                  path('postagensImagens', views.verPostagensImagens),


                  path('login/', views.login_user),
    path('login/submit',views.submit_login),
                  path('chat/<str:room_name>/<nome>', views.room, name='room'),
                  path('perfil', views.perfil),
                  path('perfil/<nome>', views.perfil_nome),
                  path('perfil/<nome>/submit', views.perfil_nome_submit),

                  path('reportar', views.reportar),
                  path('reportar/submit', views.reportar_submit),

                  path('sugestao', views.sugestao),
                  path('sugestao/submit', views.sugestao_submit),
                  path('inicio/', RedirectView.as_view(url='/home/')),

                  path('',RedirectView.as_view(url='home/'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
