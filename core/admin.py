from django.contrib import admin

from core.models import Publicacao, Sugestao, Reportar
from core.models import Imagens_publicacao,tipoConta,Perfil,Conquista,Conquista_Usuario,Curtida,Perfil_nome



admin.site.register(Publicacao)
admin.site.register(Imagens_publicacao)
admin.site.register(tipoConta)
admin.site.register(Perfil)


admin.site.register(Conquista)

admin.site.register(Conquista_Usuario)
admin.site.register(Curtida)
admin.site.register(Sugestao)
admin.site.register(Reportar)

admin.site.register(Perfil_nome)



# Register your modelpythos here.
