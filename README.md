# Creche Pet    |   Coragem

> Desenvolvimento de um Sistema de Administração de Serviços especializado para atender às necessidades específicas da área de creche pet. 
Este projeto visa otimizar a gestão operacional e administrativa de estabelecimentos dedicados ao cuidado de animais de estimação, proporcionando uma solução eficiente e personalizada. Com funcionalidades adaptadas às demandas únicas de uma creche pet, o sistema abrange desde o controle de agendamentos e registros de atividades diárias até a gestão financeira, garantindo uma operação organizada e centrada no bem-estar dos animais. Esta iniciativa busca melhorar a eficiência operacional e a experiência do cliente em estabelecimentos que oferecem serviços de creche para pets, elevando a qualidade dos cuidados prestados e impulsionando o sucesso do negócio.





## Autores

- [@MichellyNonatto](https://github.com/MichellyNonatto)
- [@paulaandrezza](https://github.com/paulaandrezza)
- [@St4rThabs](https://github.com/St4rThabs)


### Contribuintes

- [@MarceloHribeiro](https://github.com/MarceloHribeiro)
- [@Bea-Querubim](https://github.com/Bea-Querubim)


# Instalação
> A instalação de dependências serão necessárias para o uso local do sistema;

> Para acessar o projeto, é necessário ter o Python3 versão 3.9 ou superior instalado no computador.

***

### Instalação e Acesso Local
* Inicie baixando o repositório através do terminal, seja utilizando o `git bash`, `cmd`, `conda` ou o de sua preferência
```bash
 git clone https://github.com/MichellyNonatto/Coragem.git
```

* Com a utilização do Framework Django é necessário que criemos um novo ambiente virtual para não ocorrer conflito de versões
```bash
 python -m venv env
```
 `env` é nome do ambiente virtual, você pode modificar para qualquer outro nome.

* Após a instalação abra o prompt de comando e ative o ambiente virtual criado no passo anterior.
```bash
 ./venv/Scripts/Activate.ps1
```
* O passo a seguir pode demorar um pouco para ser concluído, isso irá variar das configurações do computador.
O código abaixo quando executado irá baixar todas a dependências necessárias para o funcionamento do projeto.
```bash
 pip install -r requirements.txt
```
* A base de dados já está funcionando com a conexão do Railway, então não é necessário fazer o `python manage.py migrate`.
* Pronto! Agora é só utilizar o projeto e explora-lo.
```bash
 python manage.py runserver
```
* Caso queira alterar algum estilo utilize esse comando para recarregamento das classes Tailwind do projeto.
```bash
 npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```

***

## Informações para Manutenção 
#### Versões dos softwares dependentes

* Python `v3.9.13`
* Django `4.2.6`

```bash
    pip freeze > requirements.txt #  Utilizar sempre antes de fazer o deploy do projeto
```
```
    python manage.py collectstatic # Atualizar a pasta responsável por realizar o POST em produção dos arquivos estáticos
```
* Requirements
  - amqp '5.2.0'
  - asgiref '3.7.2'
  - billiard '4.2.0'
  - celery '5.3.5'
  - click '8.1.7'
  - click-didyoumean '0.3.0'
  - click-plugins '1.1.1'
  - click-repl '0.3.0'
  - colorama '0.4.6'
  - Django '4.2.7'
  - gunicorn '21.2.0'
  - holidays '0.35'
  - kombu '5.3.4'
  - packaging '23.2'
  - Pillow '10.1.0'
  - prompt-toolkit '3.0.41'
  - psycopg2 '2.9.9'
  - python-dateutil '2.8.2'
  - six '1.16.0'
  - sqlparse '0.4.4'
  - typing_extensions '4.8.0'
  - tzdata '2023.3'
  - Unidecode '1.3.7'
  - vine '5.1.0'
  - wcwidth '0.2.12'
  - whitenoise '6.6.0'

***
### Estrutura de Pastas
```
projeto/
├── coragem/                # Aplicação principal
│   ├── migrations/        # Migrações do banco de dados
│   ├── static/            # Arquivos estáticos específicos do aplicativo
│   ├── templates/         # Modelos HTML específicos do aplicativo
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── media/                  # Uploads de mídia
├── static/                 # Arquivos estáticos comuns a várias aplicações
├── servicos/               # Possíveis serviços do projeto
├── usuarios/               # Aplicação de usuários
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── celerybeat-schedule.bak # Extensão para agendar tarefas periódicas em uma aplicação Django.
├── celerybeat-schedule.dat
├── celerybeat-schedule.dir
├── manage.py               # Script de gerenciamento do Django
├── Procfile                # Arquivo de configuração para ambientes de implantação
├── README.md               # Documentação do projeto
├── requirements.txt        # Dependências do projeto
├── runtime.txt             # Especificação da versão do Python a ser usada
```
***
### Estrutura de Classes

Cada classe tem objetivo de realizar um método CRUD com base ao dados salvos no sistema. 
As classes informadas abaixo é referente a classe de vizualisação do Django, ou seja estão localizadas em `views.py` do app indicado.


| Nome   | App       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `CustomLoginView`      | `usuarios` | Retorna um formulário de autenticação de login. Classe principal de funcionamento do sistema, consistendo na regra de negócio `acesso em horários comerciais`. |
|`RecuperarConta`|`usuarios`| Retorna um formulário de autenticação por e-mail. |
|`Autenticacao`|`usuarios`|Faz autenticação da validade do e-mail e usuário com base na regra de autenticação do arquivo `form` tenho a herança de `AutenticacaoContaForm`.|
|`AtualizarSenha`|`usuarios`|Retorna um formulário de update de senha, fazendo a criptográfia do mesmo antes de retornar a informação para o banco de dados.|
|`Dashboard`|`usuarios`|Retorna informações básicas do usuário autenticado.|
|`EditarPerfilUsuario`|`usuarios`|Retorna um formulário de update de informações do usuário autenticado, podendo modificar dados que estão permitido na regra desenvolvida na classe.|
|`EditarPerfilEndereco`|`usuarios`|Retorna um formulário de update de informações do endereço do usuário autenticado, podendo quaisquer dado implantado na modelagem da tabela.|
|`ListaFuncionarios`|`usuarios`|Retorna informações permitidas pela classe de todos os usuários com vinculo a tabela funcionário existente no sistema|
|`PesquisaFuncionario`|`usuarios`|Retorna perfis com base na informação enviada pelo método GET.|
|`VerFuncionario`|`usuarios`|Retorna informações encapsulada conforme a regra de privacidade de informações.|
|`EditarFuncionario`|`usuarios`|Retorna informações encapsulada e editáveis conforme a regra de privacidade de informações.|
|`DeletarFuncionario`|`usuarios`|Deleta um usuário com base em seu id e permissão de administrador, se concedida.|
|`AdicionarFuncionario`|`usuarios`|Adiciona um novo usuário vinculado há categoria `funcionário` e herda a classe do arquivo form `CriarContaForm`. |
|`AutenticacaoClienteView`|`usuarios`|Verifica o e-mail e documento cadastrados do tutor, realizando a validade do uso para pagamento do mesmo.|
|`CriarNovoPagamento`|`usuarios`|Formulário que retorna ao cliente qual tipo de pagamento quer realizar e cria uma nova instancia em pagamento__cliente ao ser realizado com sucesso. Essa classe é puramento ilustrativa, não é realizado nenhum tipo de pagamaneto real.|
|`ListaPagamentos`|`usuarios`|Retorna os pagamento pendentes e a quantidade de dias que ele está vencido.|
|`PesquisarPagamento`|`usuarios`|Retorna perfis de pagamento com base na informação enviada pelo método GET.|
|`DeletarCliente`|`usuarios`|Realiza o delete do usuário com a categoria `Tutor`|
|`ListaPets`|`servicos`|Retorna informações permitidas pela classe de todos os pets cadastrado no banco de dados|
|`PesquisaPet`|`servicos`|Retorna perfis de pets com base na informação enviada pelo método GET.|
|`VerPet`|`servicos`|Retorna informações encapsulada conforme a regra de privacidade de informações.|
|`AdicionarVacinaPet`|`servico`|Vincula uma vacina cadastrada no banco de dados ao pet.|
|`VincularTutor`|`servico`|Retorna uma lista de tutores existentes na base de dados para vincular ao novo pet.|
|`AdicionarPet`|`servico`|Cria uma nova instância pet.|
|`PesquisarTutor`|`servico`||
|``|`servico`|Retorna perfis de tutores com base na informação enviada pelo método GET.|
|`AdicionarTutor`|`servico`|Cria uma nova instância para tutor|
|`ListaServicos`|`servico`|Retorna uma lista de serviços dispoiníveis pelo comércio.|
|`PesquisarServico`|`servico`|Retorna serviços com base na informação enviada pelo método GET.|
|`VerServicos`|`servico`|Retorna uma lista de pets cadastrados no serviço|
|`EditarGrade`|`servico`|Atualiza as informações do pet há grade, servindo como meio de presença do pet ao serviço.|
|`AdicionarPetServico`|`servico`|Vincula um pet ao serviço.|
|`DeletarPetServico`|`servico`|deleta a instancia pet__servico da grade|
***
### Mensagem de ``Error``

- 503 (Service Unavailable): Indica que o servidor não está disponível para lidar com a solicitação.
- 204 (No Content): A solicitação foi bem-sucedida, mas não há conteúdo para retornar.
- 403 (Forbidden): Acesso restrito pelo servidor.

<div align="center">
  <a href="https://github.com/MichellyNonatto">
   <img height="100em" src="https://github.com/MichellyNonatto/CPCoragem/assets/101263547/6ae7fead-5d91-4f46-9e10-1e973e5095b9"/>
  </a>
</div>

<div align="center">

## &copy; Creche Pet Coragem | <a href="https://bra.ifsp.edu.br">IFSP - Campus Bragança Paulista<a/>

Para entrar em contato com os desenvolvedores do projeto retorne até a aba de `Autores` em `Introdução`

</div>
