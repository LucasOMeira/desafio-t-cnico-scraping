# DESAFIO TÉCNICO SCRAPING

## Teste prático de Scrapping

## **Target**: [http://www5.trf5.jus.br/cp/]

### **Objetivos**
- Construir um scraper que permita consulta pública de processos utilizando o Scrapy
- Consultar dados de processos cujo número já foi fornecido pelo cliente
- Permitir, também, que a busca seja realizada através do CNPJ do cliente

### **Campos Utilizados**
- numero_processo
- numero_legado
- data_autuacao
- envolvidos
- papel
- nome
- relator
- movimentações
- data
- texto

### **Setup do Ambiente**
- Instalar **Python 3**
- Instalar Scrapy 
- - pip install scrapy

### **Comandos Usados**
- scrapy startproject nome_projeto (para criação do projeto)
- scrapy genspider nome_spider url_target (para criação do spider)

### **Instruções para Execução**
- Navegar até o diretório **/spiders** dentro da pasta do projeto
- executar o comando **scrapy crawl cnpj -a numero=00000000000191 -O processos_por_cnpj.jl** para executar o scraper que busca todos os processos referentes ao CNPJ passado como parâmetro e gravar o resultado em um arquivo .jl
- executar o comando **scrapy crawl processo -a numero=0000560-67.2017.4.05.0000 -O processos.jl** para executar o scraper que busca as informações do processo cujo número foi passado como parâmetro e gravar o resultado em um arquivo .jl

### **Considerações**
- A maior dificuldade encontrada na implementação, foi o fato do site do TRF5 não possuir classes em seus elementos. Em um primeiro momento, foi tentado fazer os SELECTORS com responde.css, porém sem sucesso. Utilizou-se, então, o XPATH para que os SELECTORS pudessem ser feitos de forma mais clara.
- Pensando no aspecto da escalabilidade de código, permitindo uma ampliação no poder de busca do scraper, tomamos a decisão de criar o **init** e passar o número do processo na chamada do raspador. Desta forma, será possível a busca em outros números de processos, além dos que o cliente já passou.
- Salienta-se que, no próprio código do scraper supra citado, há a possibilidade de "desativar" o **init** e fazer o raspador buscar, de uma só vez, por todos os números de processos já passados pelo cliente.
