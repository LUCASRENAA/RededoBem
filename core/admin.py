from django.contrib import admin

from core.models import Publicacao
from core.models import Imagens_publicacao,tipoConta,Perfil,Conquista,Conquista_Usuario



admin.site.register(Publicacao)
admin.site.register(Imagens_publicacao)
admin.site.register(tipoConta)
admin.site.register(Perfil)


admin.site.register(Conquista)

admin.site.register(Conquista_Usuario)




# Register your modelpythos here.
