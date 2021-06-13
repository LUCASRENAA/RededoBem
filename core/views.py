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
from core.models import Publicacao, Imagens_publicacao,tipoConta,Perfil

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
        senha = request.POST.get('password')
        usuario = request.POST.get ( 'username' )
        email =   request.POST.get ( 'email' )
        try:
            print("e aqui?")
            user = User.objects.create_user ( str(usuario), str(email) ,  str(senha) )
            tipo = tipoConta.objects.create(usuario = user,tipo=0)





        except:
            User.objects.get(username = usuario)
            User.objects.get(email = email)


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
        dados = {"nome":request.user,
             "foto":"/static/img/perfil.jpg"}
    return render(request,'inicio.html',dados)

@login_required(login_url='/login/')
def inicio2(request):
    return render(request,'inicio2.html')

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
