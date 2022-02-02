import scrapy


class ProcessoSpider(scrapy.Spider):
    name = 'processo'

    # Garante que os caracteres especiais vao sair corretos no JSON
    custom_settings = {'FEED_EXPORT_ENCODING': 'UTF-8'}

    base_url = 'https://cp.trf5.jus.br/processo/'

    # Url preechida com o numero do processo manualmente, descomente e comente o init para usar
    # start_urls = [
    #   f"{base_url}0015648-78.1999.4.05.0000",
    #   f"{base_url}0012656-90.2012.4.05.0000",
    #   f"{base_url}0043753-74.2013.4.05.0000",
    #   f"{base_url}0002098-07.2011.4.05.8500",
    #   f"{base_url}0460674-33.2019.4.05.0000",
    #   f"{base_url}0000560-67.2017.4.05.0000",
    #   ]

    # def do init nescessario para o scrapy funcionar aceitando argumentos na linha de comando. exemplo: scrapy crawl processo -a numero=0015648-78.1999.4.05.0000
    def __init__(self, numero=None, *args, **kwargs):
        super(ProcessoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://cp.trf5.jus.br/processo/{numero}"]

    def parse(self, response):
        numero_legado = response.xpath('/html/body/p[3]/text()').get()
        if numero_legado is None:
            numero_legado = ""
        else:
            numero_legado = numero_legado.replace("(", "").replace(")", "")

        numero_processo = response.xpath('/html/body/p[2]/text()').get()
        if numero_processo is None:
            numero_processo = numero_legado
        else:
            numero_processo = numero_processo.replace("\n      PROCESSO Nº ", "")

        data_autuacao = response.xpath('/html/body/table[1]/tr[1]/td[2]/div/text()').get().replace("AUTUADO EM ", "")

        envolvidos_papel = response.xpath('/html/body/table[3]/tr/td[1]/text()').getall()
        envolvidos_nome = response.xpath('/html/body/table[3]/tr/td/b/text()').getall()
        envolvidos_papel.pop()
        relator = envolvidos_nome.pop().replace(": ", "")
        envolvidos = [{papel: nome} for papel, nome in zip(envolvidos_papel, envolvidos_nome)]

        def descricaoPorTable(table):
            descricao = None
            texto = response.xpath(f"/html/body/table[{table}]/tr[2]/td[2]/text()").get()
            complemento = response.xpath(f"/html/body/table[{table}]/tr[3]/td[2]/text()").get()

            if texto is not None:
                movimentacao_data = response.xpath(f"/html/body/table[{table}]/tr[1]/td/ul/li/a/text()").get().replace(
                    'Em ', '')
                if complemento == '\n':
                    descricao = {movimentacao_data: texto}
                else:
                    descricao = {movimentacao_data: f"{texto} {complemento}"}
            return descricao

        table = 6
        descricoes = []
        descricao = descricaoPorTable(table)
        while descricao is not None:
            table += 1
            descricoes.append(descricao)
            descricao = descricaoPorTable(table)

        yield {
            'numero_processo': numero_processo,
            'numero_legado': numero_legado,
            "data_autuacao": data_autuacao,
            "envolvidos": envolvidos,
            "relator": relator,
            "movimentacoes": descricoes
        }