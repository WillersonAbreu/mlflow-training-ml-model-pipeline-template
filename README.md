# Template de treinamento de modelo 

- [Introdução](#introdução)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Como rodar o projeto](#como-rodar-o-projeto)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Primeiros passos](#primeiros-passos)
- [Explicação dos módulos](#explicação-dos-módulos)
- [Arquivos importantes no projeto](#arquivos-importantes)
## Introdução
O projeto em questão, foi desenvolvido utilizando as ferramentas que o time já tem experiência com a principal finalidade de economizar tempo
para iniciar o desenvolvimento de novos projetos de treinamento de modelo.

## Tecnologias utilizadas
* Mlflow
* Python 3.8
* Pandas
* Conda

## Como rodar o projeto
Partindo do pressuposto que já esteja em um ambiente virtual com as dependências instaladas, execute os comandos abaixo:
       
```bash
#Executando o wokflow completo: 
mlflow run . -P environment_type=DEVELOPMENT
```

Também é possível rodar um entrypoint específico:
```bash
#Executando o entrypoint que executa o script de extração: 
mlflow run . -e extract -P environment_type=DEVELOPMENT
```

**Observação:** é possível usar chamar cada etapa da esteira de treinamento utilizando os entrypoints que estão definidos no arquivo _`MLproject`_.

## Estrutura do projeto
```bash
├── pipelines
│   ├── azure-pipelines.yaml
│   ├── build.py
│   └── requirements.txt
├── src
│   ├── core
│   │   ├── contexts
│   │   │   └── extract_context
│   │   │       └── data_extraction_by_environment.py
│   │   ├── enum
│   │   │   └── data_extraction_strategy_by_context_enum.py
│   │   ├── services
│   │   │   └── wine_quality_extract_service.py
│   │   └── strategies
│   │       └── extraction_strategies
│   │           ├── abstract_extraction_strategy.py
│   │           ├── development_extraction_strategy.py
│   │           ├── production_extraction_strategy.py
│   │           └── test_extraction_strategy.py
│   ├── notebook
│   │   └── train-projects-local.ipynb
│   ├── scripts
│   │   ├── decorators
│   │   └── utils
│   │       └── test_welcome_utils.py
│   └── tests
│       └── __init__.py
├── temp
│   └── dataset
│       └── .gitkeep
├── .gitignore
├── conda.yaml
├── MLproject
└── README.md
```

## Primeiros passos
O template atual contém um padrão de hierarquia de módulos já utilizadas em outras pipelines de treinamento de modelo no time. 

### Explicação dos módulos
* **_`pipelines`_**
    1. O arquivo _`yaml`_ da pipeline do _`Azure DevOps`_ com as etapas que são costumeiras nas _`pipelines`_ de **CI** dos projetos de treinamento de modelo que temos; 
    2. O módulo contém também, o _`script build.py`_ que é executado pela esteira de **CI** a fim de disparar um experimento com um fluxo de trabalho a ser executado através do _`Mlflow`_ dentro do _`Azure ML`_; 
    3. Por fim, tem o arquivo de pacotes que são requisitos para rodar a aplicação.

* **_`temp/dataset`_**
    1. É um diretório que deve ser usado para manter o arquivo do _`dataset baseline`_, salvar os arquivos do _`dataset baseline`_ processado (preparado/dividido)

* **_`src/core`_**
    1. É um diretório que pode ser usado para manter o core do treinamento do modelo, pode-se alocar aqui classes do treinamento de modelo, services para buscar dados que estão em ambientes externos ao da pipeline de treinamento e também, implementação de design-patterns (Assim como o Strategy que implementei para manipular de onde deve ser extraído o _`dataset baseline`_), mas não é obrigatório usar esse módulo, ou seja, você pode excluí-lo e trabalhar de uma forma mais flexível para você.

* **_`src/notebook`_**
    1. Diretório para alocar _`notebooks jupyter`_ onde geralmente os cientistas costumam fazer vários testes em relação ao treinamento de modelos.

* **_`src/scripts`_**
    1. _`Script main.py`_ é um orquestrador de _`entrypoints`_ do _`Mlflow`_ que executa um fluxo de trabalho para garantir que todas as etapas da esteira de treinamento sejam executadas em ordem e garantindo uma melhor manutenção e leitura com as etapas separadas;
    2. _`Script extract.py`_ é o _`entrypoint`_ que faz a extração do _`dataset baseline`_ no exemplo do template, ele usa o parâmetro _`environment\_type`_ para fazer a escolha da estratégia correta para a extração;
    3. _`Script prepare.py`_ é o _`entrypoint`_ que faz a preparação de dados utilizando o _`dataset baseline`_ extraído no passo anterior e salva um ou mais arquivos que são produtos da preparação dos dados;
    4. _`Script train.py`_ é o _`entrypoint`_ que faz o uso do arquivo (ou arquivos) gerados no passo anterior para realizar o treino do modelo;
    5. _`Script validate.py`_ é o _`entrypoint`_ que recebe o **ID** do _Job_ que o _`Mlflow`_ gerou ao disparar o passo anterior, busca e valida as métricas geradas na etapa anterior;
    6. _`Script model_registry.py`_ é o _`entrypoint`_ que recebe o **ID** do _Job_ que o _`Mlflow`_ gerou ao disparar o passo **4** e registra um modelo candidato a ser produtizado através de APIs Rest caso a etapa anterior não falhe.
* **_`src/scripts/decorators`_**
    1. O módulo _`load_path_context.py`_ é um módulo que faz o uso do pacote _`libcontext built-in no Python`_ para abrir contextos, pode-se perceber que em vários entrypoints é utilizada a classe _`PathLoadContext`_ junto com o _`with`_ que é usado para iniciar os jobs do _`Mlflow`_.
* **_`src/tests`_** é o modulo que contém testes unitários (Geralmente para testar os scripts dos _`entrypoints`_).

### Arquivos importantes
Como já dito anteriormente, este template (e todas as esteiras de treinamento de modelo aqui no time) utiliza o _`Mlflow`_ para fazer um melhor gerenciamento do ciclo de vida dos modelos de machine learning, portanto, segue abaixo arquivos que são necessários para que o _`Mlflow`_ possa ser executado corretamente.

* O **_`conda.yaml`_** é utilizado pelo _`Mlflow`_ para poder criar os ambientes virtuais para rodar os entrypoints, nele, deve-se alocar todas as dependências necessárias para preparar dados e treinar o modelo;
* O **_`MLproject`_** é exclusivo do _`Mlflow`_, nele são descritos todos os _`entrypoints`_, seus respectivos parâmetros e comandos que executam scripts específicos de cada etapa.