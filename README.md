# Product Service - Componente B

Este repositório faz parte da entrega do MVP projeto final, sendo este o \*Componente B\*\*. A api externa usada foi a https://github.com/robvanbakel/gotiny-api, utilizada para reduzir o tamanho de URLS, licensa MIT. Ela foi utilizada apenas para a entrega do exercício de integração com uma API publica gratuita. A minha ideia era utilizar uma API para automatizar o envio de emails no momento em que fosse criado um novo pedido, mas todas as APIs que pesquisei ou eram pagas, ou necessitavam de um domínio.
Esta api faz a gestão de produtos e tem uma rota para a criação de um pedido

### Instalação

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---

### Executando o servidor

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5004
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 5004 --reload
```

---

### Acesso no browser

Abra o [http://localhost:5004/#/](http://localhost:5004/#/) no navegador para verificar o status da API em execução.

---

## Como executar através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t product-service .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5004:5004 product-service
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5004/#/](http://localhost:5004/#/) no navegador.

### Alguns comandos úteis do Docker

> **Para verificar se a imagem foi criada** você pode executar o seguinte comando:
>
> ```
> $ docker images
> ```
>
> Caso queira **remover uma imagem**, basta executar o comando:
>
> ```
> $ docker rmi <IMAGE ID>
> ```
>
> Subistituindo o `IMAGE ID` pelo código da imagem
>
> **Para verificar se o container está em exceução** você pode executar o seguinte comando:
>
> ```
> $ docker container ls --all
> ```
>
> Caso queira **parar um conatiner**, basta executar o comando:
>
> ```
> $ docker stop <CONTAINER ID>
> ```
>
> Subistituindo o `CONTAINER ID` pelo ID do conatiner
>
> Caso queira **destruir um conatiner**, basta executar o comando:
>
> ```
> $ docker rm <CONTAINER ID>
> ```
>
> Para mais comandos, veja a [documentação do docker](https://docs.docker.com/engine/reference/run/).
