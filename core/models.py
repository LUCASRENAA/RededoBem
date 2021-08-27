from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

class Preferencias(models.Model):
    preferencia = models.CharField(max_length=100)

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

    class modo(models.IntegerChoices):
        Presencial = 0
        NaoPresencial = 1
    modo = models.IntegerField(choices=modo.choices)

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y')
    def get_usuario(self):
        return str(self.usuario)
    def get_data_criacao(self):
        return self.data_criacao.strftime('%d/%m/%Y')
class Conquista(models.Model):
    texto = models.CharField(max_length=1000)
    imagem = models.ImageField(upload_to='static/img')

    def get_data_evento(self):
        return self.data_criacao.strftime('%d/%m/%Y')

class Conquista_Usuario(models.Model):
    conquista =  models.ForeignKey(Conquista,models.CASCADE)
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



class Preferencia_publicacao(models.Model):
    publicacao =  models.ForeignKey(Preferencias,models.CASCADE)

    usuario =  models.ForeignKey(User,models.CASCADE)
    def get_data_evento(self):
        return self.data_criacao.strftime('%d/%m/%Y')
class Perfil(models.Model):
    imagem = models.ImageField(upload_to='static/img')
    usuario =  models.ForeignKey(User,models.CASCADE)

class Perfil_nome(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    data_nascimento = models.DateTimeField()
    endereco = models.CharField(max_length=50)
    cartão = models.CharField(max_length=50)
    usuario =  models.ForeignKey(User,models.CASCADE)




class Curtida(models.Model):
    publicacao =  models.ForeignKey(Publicacao,models.CASCADE)
    usuario =  models.ForeignKey(User,models.CASCADE)
    gostou = models.IntegerField()

class Respostas(models.Model):
    texto = models.CharField(max_length=1000)
    publicacao =  models.ForeignKey(Publicacao,models.CASCADE)
    curtidas = models.IntegerField()
    nao_gostei = models.IntegerField()
    usuario = models.ForeignKey(User, models.CASCADE)
    data_criacao = models.DateTimeField(auto_now=True)
    pra_quem     = models.IntegerField()


class Sugestao(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=1000)
    usuario = models.ForeignKey(User, models.CASCADE)


class Reportar(models.Model):
    titulo = models.CharField(max_length=50)
    texto = models.CharField(max_length=1000)
    usuario = models.ForeignKey(User, models.CASCADE)



class Local(models.Model):
    publicacao =  models.ForeignKey(Publicacao,models.CASCADE)
    texto = models.CharField(max_length=1000)
