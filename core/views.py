import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from datetime import  datetime, timezone, timedelta
from core.models import Publicacao, Imagens_publicacao, tipoConta, Perfil, Conquista, Conquista_Usuario, Curtida, \
    Sugestao, Reportar

import time

# Create your views here.



# Create your views here
#from core.models import Produto


def login_user(request):
    return render(request,'login.html')


def registro(request):
    return render(request,'registro.html')



def logout_user(request):
    logout(request)
    return redirect('/')
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        print(username)
        print(password)
        print(usuario)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request,"Usuário ou senha invalido")


    return  redirect('/')

def submit_registro(request):
    print(request.POST)
    if request.POST:
        senha = request.POST.get('senha')
        usuario = request.POST.get ( 'username' )
        email =   request.POST.get ( 'email' )
        print(senha)
        print(usuario)
        print(email)
        try:
            print("e aqui?")
            user = User.objects.create_user ( str(usuario), str(email) ,  str(senha) )

            tipo = tipoConta.objects.create(usuario = user,tipo=0)





        except:

            User.objects.get(username = usuario)



            return HttpResponse('<h1> Usuario já cadastrado </h1>')

        print("hey")
        return redirect('/')
    return HttpResponse('<h1> faça um post </h1>')



@login_required(login_url='/login/')
def inicio(request):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        dados = {"nome": request.user,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all()
                 }
    except:
        dados = {"nome": request.user,
                 "fotos": Perfil.objects.all(),
                 "publicacao": Publicacao.objects.all(),
                 "foto": "/static/img/perfil.jpg",
                 "imagens": Imagens_publicacao.objects.all()
                 }
    return render(request,'inicio.html',dados)

@login_required(login_url='/login/')
def conquista(request):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        dados = {"nome": request.user,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all(),
                 "conquistas": Conquista_Usuario.objects.all()

                 }
    except:


        dados = {"nome": request.user,
                 "fotos": Perfil.objects.all(),
                 "publicacao": Publicacao.objects.all(),
                 "foto":"/static/img/perfil.jpg",
                 "imagens": Imagens_publicacao.objects.all(),
                 "conquistas": Conquista_Usuario.objects.all()

                 }
    return render(request,'conquista.html',dados)


@login_required(login_url='/login/')
def home(request):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        dados = {"nome": request.user,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all()
                 }
    except:


        dados = {"nome": request.user,
                 "fotos": Perfil.objects.all(),
                 "publicacao": Publicacao.objects.all(),
                 "foto":"/static/img/perfil.jpg",
                 "imagens": Imagens_publicacao.objects.all()
                 }
    return render(request,'home.html',dados)

@login_required(login_url='/login/')
def submit_postagem(request):
    if request.POST:
        print(request.POST.get ( 'publicacao' ))
        texto =  request.POST.get ( 'publicacao' )
        data_evento = request.POST.get ( 'data_evento' )
        Publicacao.objects.create(texto =texto,
                                  curtidas=0,nao_gostei = 0,data_evento = data_evento,
                                  pretende_ir = 0,confirmados = 0,usuario = User.objects.get(username = request.user),
                                  tipo = tipoConta.objects.get(usuario = User.objects.get(username = request.user)).tipo)


    return redirect('/')


@login_required(login_url='/login/')
def submit_postagem_imagem(request):
    if request.POST:
        print(request.POST.get ( 'publicacao' ))
        texto =  request.POST.get ( 'publicacao' )
        id =  request.POST.get ( 'id' )

        arquivo = request.FILES['file']
        Imagens_publicacao.objects.create(texto =texto,
                                          imagem=arquivo,
                                          publicacao=Publicacao.objects.get(id=id),
                               usuario = User.objects.get(username = request.user))


    return redirect('/')
def verPostagens(request):
    dlist = []

    for publicacao in Publicacao.objects.all():
        d = {}
        print(str(publicacao.texto))
        d["texto"] = str(publicacao.texto)
        d["data_evento"] = str(publicacao.get_data_evento())
        d["data_criacao"] = str(publicacao.get_data_criacao())
        d["curtidas"] = str(publicacao.curtidas)
        d["odiei"] = str(publicacao.nao_gostei)
        d["prentedeIr"] = str(publicacao.pretende_ir)
        d["confirmados"] = str(publicacao.confirmados)
        d["usuario"] = str(publicacao.usuario)
        if int(publicacao.tipo) == 0:
            d["tipo"] = "Comum"
        if int(publicacao.tipo) == 1:
                d["tipo"] = "Empresas"
        if int(publicacao.tipo) == 2:
                d["tipo"] = "Administrativa"


        d["id"] = str(publicacao.id)

        dlist.append(d)

    sorted_list = sorted(dlist, key=lambda k: (k['id']), reverse=True)
    jsonresultado = json.dumps(sorted_list)
    return HttpResponse(jsonresultado)
def verPostagensImagens(request):
    dlist = []

    for publicacao in Imagens_publicacao.objects.all():
        d = {}
        d["texto"] = str(publicacao.texto)
        d["imagem"] = str(publicacao.imagem)

        d["usuario"] = str(publicacao.usuario)


        d["id"] = str(publicacao.id)

        dlist.append(d)

    sorted_list = sorted(dlist, key=lambda k: (k['id']), reverse=True)
    jsonresultado = json.dumps(sorted_list)
    return HttpResponse(jsonresultado)


@login_required(login_url='/login/')
def submit_perfil(request):
    if request.POST:
        arquivo = request.FILES['imagem']
        print(arquivo)
        try:
            perfil = Perfil.objects.get(usuario = User.objects.get(username = request.user))
            perfil.imagem = arquivo
            perfil.save()
        except:
            Perfil.objects.create(usuario = User.objects.get(username = request.user),imagem = arquivo)

        return redirect('/inicio')

def room(request, room_name,nome):
    lista = []
    lista.append(room_name)
    lista.append(nome)
    if str(room_name) == str(request.user):
        return render(request, 'room.html', {
            'room_name': room_name + str(nome) ,
            'username': str(request.user)
        })
    if str(nome) == str(request.user):
        return render(request, 'room.html', {
            'room_name': room_name + str(nome) ,
            'username': str(request.user)

        })

@login_required(login_url='/login/')
def perfil(request):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        dados = {"nome": request.user,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all()
                 }
    except:
        dados = {"nome":request.user,
             "foto":"/static/img/perfil.jpg"}

    return render(request,'perfil.html',dados)





def perfil_nome(request,nome):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=nome))
        dados = {"nome": nome,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all(),
                 "conquistas": Conquista_Usuario.objects.all()
                 }
    except:
        dados = {"nome":nome,
             "foto":"/static/img/perfil.jpg"}

    return render(request,'perfil.html',dados)

@login_required ( login_url = '/login/' )
def curtir(request, id_publicacao):

                conversa = Publicacao.objects.get ( id = id_publicacao )
                usuario = request.user


                try:
                    curtida = Curtida.objects.get ( usuario = usuario,
                                                 publicacao = conversa
                                                 )
                    validar = 0
                    if int(curtida.gostou) == 1:
                        conversa.curtidas = conversa.curtidas - 1
                        curtida.gostou = 3
                        curtida.save()
                        conversa.save()
                        validar = 1
                    if int(curtida.gostou) == 3:
                        if validar != 1:
                            conversa.curtidas = conversa.curtidas + 1
                            conversa.save()
                            curtida.gostou = 1
                            curtida.save()

                    if int(curtida.gostou) == 2:
                        conversa.curtidas = conversa.curtidas + 1
                        conversa.nao_gostei = conversa.nao_gostei - 1
                        curtida.gostou = 1
                        curtida.save()
                        conversa.save()
                    return redirect('/inicio')
                except:
                        conversa.curtidas = conversa.curtidas + 1
                        conversa.save ()
                        Curtida.objects.create(usuario = usuario,
                                               publicacao=conversa,
                        gostou = 1)


                        return redirect ( '/inicio' )
@login_required ( login_url = '/login/' )
def descurtir(request, id_publicacao):
                conversa = Publicacao.objects.get(id=id_publicacao)
                usuario = request.user



                try:
                    curtida = Curtida.objects.get(usuario=usuario,
                                                  publicacao=conversa
                                                  )
                    print("curtida")
                    print(curtida.gostou)
                    validar = 0
                    if int(curtida.gostou) == 3:
                        conversa.nao_gostei = conversa.nao_gostei + 1
                        conversa.save()
                        curtida.gostou = 2
                        curtida.save()
                        validar = 1
                    if int(curtida.gostou) == 2:
                        if validar != 1:
                            curtida.gostou = 3
                            curtida.save()
                            conversa.nao_gostei = conversa.nao_gostei - 1
                            conversa.save()

                    if int ( curtida.gostou ) == 1:
                        conversa.curtidas = conversa.curtidas - 1
                        curtida.gostou = 2
                        curtida.save()
                        conversa.nao_gostei = conversa.nao_gostei + 1
                        conversa.save()



                    return redirect('/inicio')
                except:
                        conversa.nao_gostei = conversa.nao_gostei + 1
                        conversa.save ()
                        Curtida.objects.create(usuario = usuario,
                                               publicacao = conversa,
                                               gostou = 2)

                        return redirect ( '/inicio' )


def Dados(request,dados):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        dados = {"nome": request.user,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all(),
                 "reportados": dados
                 }
    except:
        dados = {"nome": request.user,
                 "fotos": Perfil.objects.all(),
                 "publicacao": Publicacao.objects.all(),
                 "foto": "/static/img/perfil.jpg",
                 "imagens": Imagens_publicacao.objects.all(),
                 "reportados": dados
                 }


def reportar(request):
    usuario = request.user
    dados = Reportar.objects.filter(usuario=User.objects.get(username=usuario))

    dados = Dados(request,dados)

    return render(request, "reclamacao.html", dados)


def sugestao(request):
    usuario = request.user
    dados = Sugestao.objects.filter(usuario = User.objects.get(username = usuario))
    dados2 = Dados(request,dados)
    try:
        dados2["sugestoes"] = dados
    except:
        pass
    return render(request, "sugestao.html",dados2)



def sugestao_submit(request):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        texto = request.POST.get('publicacao')

        print(titulo)
        print(texto)
        Sugestao.objects.create(titulo = titulo, texto=texto, usuario=    User.objects.get(username = usuario))


    return redirect('/sugestao')

def reportar_submit(request):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        texto = request.POST.get('publicacao')


        print(titulo)
        print(texto)
        Reportar.objects.create(titulo = titulo, texto=texto, usuario=    User.objects.get(username = usuario))


    return redirect('/reportar')
