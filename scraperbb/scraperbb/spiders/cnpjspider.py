import scrapy


class CnpjSpider(scrapy.Spider):
    name = 'cnpj'

    # Garante que os caracteres vao sair corretos no JSON
    custom_settings = {'FEED_EXPORT_ENCODING': 'UTF-8'}

    # page = '0'
    base_url = 'https://cp.trf5.jus.br'
    processos = []

    # Url preechida com o cnpj manualmente, descomente e comente o init para usar
    # start_urls = [f'{base_url}/processo/cpf/porData/ativos/00000000000191/0']

    # def do init nescessario para o scrapy funcionar aceitando argumentos na linha de comando. exemplo: scrapy crawl cnpj -a numero=00000000000191
    def __init__(self, numero=None, *args, **kwargs):
        super(CnpjSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"{self.base_url}/processo/cpf/porData/ativos/{numero}/0"]

    def parse(self, response):
        position = 1
        numero_processo = response.css(
            f'.consulta_resultados > tbody:nth-child(2) > tr:nth-child({position}) > td:nth-child(2) > a:nth-child(1)::text').get()
        while numero_processo is not None:
            position += 2
            self.processos.append(numero_processo)
            numero_processo = response.css(
                f'.consulta_resultados > tbody:nth-child(2) > tr:nth-child({position}) > td:nth-child(2) > a:nth-child(1)::text').get()

        next_page = response.xpath('//a[contains(text(), ">")]/@href').get()

        if next_page is not None:
            yield response.follow(self.base_url + next_page, callback=self.parse)
        else:
            yield {
                'processos': self.processos
            }