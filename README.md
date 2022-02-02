# DESAFIO TÉCNICO SCRAPING

## Teste prático de Scrapping

## **Target**: [http://www5.trf5.jus.br/cp/]

### **Objetivos**
- Construir um scrapy que permita consulta pública de processos utilizando o Scrapy
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


### **Instruções para Execução**
- Navegar até o diretório raiz do projeto
- executar o comando **scrapy crawl cnpj -a numero=00000000000191 -O processos_por_cnpj.jl** para executar o spider que busca todos os processos referentes ao CNPJ passado como parâmetro e gravar o resultado em um arquivo .jl
- executar o comando **scrapy crawl processo -a numero=0000560-67.2017.4.05.0000 -O processos.jl** para executar o spider que busca as informações do processo cujo número foi passado como parâmetro e gravar o resultado em um arquivo .jl

### **Considerações**
- A maior dificuldade encontrada na implementação, foi o fato do site do TRF5 não possuir classes em seus elementos. Em um primeiro momento, foi tentado fazer os SELECTORS com response.css, porém sem sucesso. Utilizou-se, então, o XPATH para que os SELECTORS pudessem ser feitos.
- Pensando no aspecto da escalabilidade de código, permitindo uma ampliação no poder de busca do spider, tomei a decisão de criar o **init** e passar o número do processo na chamada do raspador. Desta forma, será possível a busca em outros números de processos, além dos que o cliente já passou.
- Salienta-se que, no próprio código do spider supra citado, há a possibilidade de "desativar" o **init** e fazer o raspador buscar, de uma só vez, por todos os números de processos já passados pelo cliente.
- o -a numero=00000000000191, é o argumento que vc passa com o numero do cnpj o qual quer buscar os processos OU o número do processo o qual quer buscar seus dados.
- o -O processos_por_cnpj.jl é a parte do comando que salva o output em um arquivo json line (processos.jl para o spider do número do processo)
- Utilizando o -O irá sobrescrever o arquivo do output, e utilizando o -o será feito um append no arquivo de saída.
