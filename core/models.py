from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models



# Create your models here.
class tipoConta(models.Model):
    usuario =  models.ForeignKey(User,models.CASCADE)
    class tipo(models.IntegerChoices):
        Comum = 0
        Empresas = 1
        Administrativa = 2
    tipo = models.IntegerField()


class Publicacao(models.Model):
    texto = models.CharField(max_length=1000)
    curtidas = models.IntegerField()
    nao_gostei = models.IntegerField()
    data_evento = models.DateTimeField()
    pretende_ir = models.IntegerField()
    confirmados = models.IntegerField()
    usuario =  models.ForeignKey(User,models.CASCADE)
    data_criacao = models.DateTimeField(auto_now=True)

    class tipo(models.IntegerChoices):
        Comum = 0
        Empresas = 1
        Administrativa = 2
    tipo = models.IntegerField(choices=tipo.choices)

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y')
    def get_data_criacao(self):
        return self.data_criacao.strftime('%d/%m/%Y')
class Conquista(models.Model):
    texto = models.CharField(max_length=1000)
    imagem = models.ImageField(upload_to='static/img')

    usuario =  models.ForeignKey(User,models.CASCADE)
    def get_data_evento(self):
        return self.data_criacao.strftime('%d/%m/%Y')

class Imagens_publicacao(models.Model):
    texto = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='static/img')
    publicacao =  models.ForeignKey(Publicacao,models.CASCADE)

    usuario =  models.ForeignKey(User,models.CASCADE)
    def get_data_evento(self):
        return self.data_criacao.strftime('%d/%m/%Y')


class Perfil(models.Model):
    imagem = models.ImageField(upload_to='static/img')
    usuario =  models.ForeignKey(User,models.CASCADE)


