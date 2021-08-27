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
    Sugestao, Reportar,Perfil_nome

import time

# Create your views here.



# Create your views here
#from core.models import Produto
#from RededoBem.core.models import Perfil_nome


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
        return redirect('/perfil/'+str(request.user))


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

        descricaoimagem = request.POST.get('publicacao')
        data_evento = request.POST.get('data_evento')
        a = Publicacao.objects.create(texto=texto,
                                  curtidas=0, nao_gostei=0, data_evento=data_evento,
                                  pretende_ir=0, confirmados=0, usuario=User.objects.get(username=request.user),
                                  tipo=tipoConta.objects.get(usuario=User.objects.get(username=request.user)).tipo)


        Imagens_publicacao.objects.create(texto =descricaoimagem,
                                          imagem=arquivo,
                                          publicacao=a,
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
            nome = request.POST.get('nome')
            sobrenome = request.POST.get('sobrenome')
            endereco = request.POST.get('endereco')
            data = request.POST.get('data')
            cartao = request.POST.get('cartao')
            arquivo = request.FILES['imagem']

            try:
                Perfil_nome.objects.get(usuario=User(id=request.user.id))
            except:

                Perfil_nome.objects.create(nome=nome,
                                           sobrenome=sobrenome,
                                           endereco=endereco,
                                           data_nascimento=data,
                                           cartão=cartao,
                                           usuario=User(request.user.id))

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
    """
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        dados = {"nome": request.user,
                 "foto": "/media/" + str(perfil.imagem),
                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all(),
                 "usuariologado": request.user
                 }
    except:
        try:
            perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
            perfil = "/media/" + str(perfil.imagem)
        except:
            perfil = "/static/img/perfil.jpg"
        dados = {"nome":request.user,
             "foto":perfil,
                 "atualizar":"1",
                 "usuariologado": request.user
                 }

    return render(request,'perfil.html',dados)
    """
    return redirect('/perfil/' + str(request.user))




def perfil_nome(request,nome):
    try:
        perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
        try:
            perfil2 = Perfil.objects.get(usuario=User.objects.get(username=nome))
            perfil2 = "/media/" + str(perfil2.imagem)
        except:
            perfil2 = "/static/img/perfil.jpg"



        dados = {"nome": nome,
                 "foto": "/media/" + str(perfil.imagem),
                 "foto_usuario": str(perfil2),

                 "publicacao": Publicacao.objects.all(),
                 "fotos": Perfil.objects.all(),
                 "imagens": Imagens_publicacao.objects.all(),
                 "conquistas": Conquista_Usuario.objects.all(),
                    "usuariologado":request.user
                 }
    except:
        try:
            perfil = Perfil.objects.get(usuario=User.objects.get(username=request.user))
            perfil = "/media/" + str(perfil.imagem)
        except:
            perfil = "/static/img/perfil.jpg"


        try:
            perfil2 = Perfil.objects.get(usuario=User.objects.get(username=nome))
            perfil2 = "/media/" + str(perfil.imagem)
        except:
            perfil2 = "/static/img/perfil.jpg"
        dados = {"nome":nome,
                 "foto_usuario": "/media/" + str(perfil2.imagem),

                 "foto":perfil,
                 "atualizar": 1,
                 "usuariologado": request.user,
                 "fotover":perfil2

                 }

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


@login_required(login_url='/login/')
def pretender(request, id_publicacao):

    return redirect('/inicio')
"""
@login_required ( login_url = '/login/' )
def pretender(request, id_publicacao):

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
"""
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
    #dados = Reportar.objects.filter(usuario=User.objects.get(username=usuario))

    #dados = Dados(request,dados)


    return render(request, "reclamacao.html", dados)


def sugestao(request):
    usuario = request.user
    dados = Sugestao.objects.filter(usuario = User.objects.get(username = usuario))
    dados2 = Dados(request,dados)
    try:
        dados2["sugestoes"] = dados
    except:
        pass

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
    return render(request, "sugestao.html",dados)



def sugestao_submit(request):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        texto = request.POST.get('publicacao')

        print(titulo)
        print(texto)
        Sugestao.objects.create(titulo = titulo, texto=texto, usuario=    User.objects.get(username = usuario))


    return redirect('/sugestao')

def perfil_nome_submit(request,nome):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        texto = request.POST.get('publicacao')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        endereco = request.POST.get('endereco')
        data =  request.POST.get('data')
        cartao = request.POST.get('cartao')
        arquivo = request.FILES['imagem']
        print(arquivo)


        try:
            Perfil_nome.objects.get(usuario=User(id=request.user.id))
        except:

            Perfil.objects.create(usuario=User.objects.get(username=request.user), imagem=arquivo)
            Perfil_nome.objects.create(nome=nome,
                                       sobrenome = sobrenome,
                                       endereco = endereco,
                                       data_nascimento = data,
                                       cartão = cartao,
                                       usuario = User(request.user.id))



    return redirect('/perfil/' + str(request.user))



def reportar_submit(request):
    if request.POST:
        usuario = request.user
        titulo = request.POST.get('titulo')
        texto = request.POST.get('publicacao')


        print(titulo)
        print(texto)
        Reportar.objects.create(titulo = titulo, texto=texto, usuario=    User.objects.get(username = usuario))


    return redirect('/reportar')
@login_required(login_url='/login/')
def editar(request,id_publicacao):
    if str(request.user) == str(Publicacao.objects.get(id = id_publicacao).usuario):
            print("asfsafsafsafsafsa")
            dados = {"variavel": "publicacao_texto.html",
                     "publicacao":Publicacao.objects.get(id = id_publicacao),
                     "id": id_publicacao
                     }


    else:
        return HttpResponse("não é tua publicação amigão")

    return render(request,"padraotela.html",dados)

@login_required(login_url='/login/')
def editarSubmit(request,id_publicacao):
    if str(request.user) == str(Publicacao.objects.get(id = id_publicacao).usuario):
            print("asfsafsafsafsafsa")
            texto = request.POST.get('publicacao')

            arquivo = request.FILES['file']

            descricaoimagem = request.POST.get('publicacao')
            data_evento = request.POST.get('data_evento')


            public = Publicacao.objects.get(id=id_publicacao)
            public.texto = texto
            public.data_evento = data_evento
            public.save()


    else:
        return HttpResponse("não é tua publicação amigão")

    return redirect('/')