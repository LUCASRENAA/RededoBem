# Rede do bem

### Sobre:
#### Rede do bem é um projeto para disponibilizar uma rede social voltada para ações sociais, "O bem gera o bem", com essa frase, com esse intuito, desenvolvemos a noção e a estrutura de como seria essa rede social.

# Instalação:
### Rode o git clone ou pegue o zip do projeto, mas vamos presumir que vocês vão com o git clone
```
git clone https://github.com/LUCASRENAA/RededoBem.git
cd RededoBem
```

#### Instale uma env ou continue do jeito que quiser, depois de escolher se vai usar uma env ou não, rode o comando

```
python manage.py migrate
python manage.py createsuperuser --username admin
```

#### Para funcioanr o websocket, utilize
```
docker run -p 6379:6379 -d redis:5
```
#### E depois rode

```
python manage.py runserver
```

E depois é só se divertir :D, ainda estamos atualizando algumas coisinhas


- [x] Login básico
- [x] Registro básico
- [x] Chat online funcionar brevemente
- [x] Construção dos models
- [x] Construção das views
- [x] Construção dos templates
- [x] Sistema funcional(Construção dos models,views e dos templates funcional)
- [ ] Web socket com diversos usuarios na mesma página 
- [x] Login com layout melhorado
- [x] Registro com layout melhorado
- [x] Inicio com visualização das postagens
- [ ] Inicio com publicação
- [x] Tela de Conquistas
- [x] Tela de Sugestão
- [x] Tela de Reclamação
- [ ] Tela para definir as preferencias por eventos;
- [ ] Tela de feedback e comentários para os eventos.

