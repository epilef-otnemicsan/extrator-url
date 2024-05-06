import re

class ExtratorURL:
    def __init__(self, url):
        self.url = self.sanitiza_url(url)
        self.valida_url()

    def sanitiza_url(self, url):
        """
            Faz a verificação SE o tipo da URL é igual a uma String.
            SE for, será feito uma limpeza dos espaços em branco ou caracteres especiais da URL.
            SE não, será feito o retorno de uma string vazia.
        """
        if type(url) == str:
            return url.strip()
        else:
            return ""
    
    def valida_url(self):
        """
            Faz a validação para saber se é uma URL válida.
            SE não for uma URL (uma string), o retorno será de uma URL vazia.
            SE for uma uma string, a variável match serve para saber se a URL passada como parâmetro
            corresponde com a variável padrao_url.
            SE não corresponder, o retorno será que a URL é inválida. 
        """
        if not self.url:
            raise ValueError("A URL está VAZIA")
        
        padrao_url = re.compile("(http(s)?://)?(www.)?metalbank.com(.br)?/cambio")
        match = padrao_url.match(url)
        if not match:
            raise ValueError("A URL é inválida.")
        
    def get_url_base(self):
        """
            Separa a base de uma URL, que é tudo que está ANTES da interrogação.
            A variável indice_interrogacao procura o caractere de interrogação (?) dentro da URL.
            A variável url_base irá fatiar tudo que estiver ANTES da interrogação.
        """
        indice_interrogacao = self.url.find('?')
        url_base = self.url[:indice_interrogacao]
        return url_base

    def get_url_parametros(self):
        """
            Separa os parâmetros de uma URL, que é tudo que está DEPOIS da interrogação.
            A variável indice_interrogacao procura o caractere de interrogação (?) dentro da URL. 
            A variável url_parametros irá fatiar tudo que estiver DEPOIS da interrogação.
        """
        indice_interrogacao = self.url.find('?')
        url_parametros = self.url[indice_interrogacao+1:]
        return url_parametros

    def get_valor_parametro(self, parametro_busca):
        """
            Busca o valor de um parâmetro de uma URL.
            A variável indice_parametro irá definir qual foi o parâmetro escolhido. 
            A váriavel indice_valor irá buscar aonde começa aquele valor dentro da URL para fazer o fatiamento.

            A váriavel indice_e_comercial irá procurar se tem um & comercial após a variável indice_valor. 
            SE não achar, será feito o fatiamento da URL desde o ínicio de indice_valor até o final da URL.
            SE exister um & comercial após indice_valor, o fatiamento será feito até o indice_e_comercial.
            Por último, será feito o retorno apenas do valor do parâmetro.
        """
        indice_parametro = self.get_url_parametros().find(parametro_busca)
        indice_valor = indice_parametro + len(parametro_busca) + 1
        indice_e_comercial = self.get_url_parametros().find('&', indice_valor)
        if indice_e_comercial == -1:
            valor_parametro = self.get_url_parametros()[indice_valor:] 
        else:
            valor_parametro = self.get_url_parametros()[indice_valor:indice_e_comercial] 
        return valor_parametro
    
    def __len__(self):
        return len(self.url)
    
    def __str__(self):
        return f"URL: {self.url} \nURL Base: {self.get_url_base()} \nURL Parâmetros: {self.get_url_parametros()}"
    
    def __eq__(self, other):
        return self.url == other.url


url = "https://metalbank.com/cambio?moedaDestino=real&quantidade=100&moedaOrigem=dollar"
extrator_url = ExtratorURL(url)

quantidade = extrator_url.get_valor_parametro("quantidade")
moeda_destino = extrator_url.get_valor_parametro("moedaDestino")
moeda_origem = extrator_url.get_valor_parametro("moedaOrigem")
dollar = 5.10

if moeda_origem == "real" and moeda_destino == "dollar":
    conversao = (int(quantidade)) / dollar
    print(f"O valor de R${quantidade} reais é igual a U${conversao:.2f} dólares")
elif moeda_origem == "dollar" and moeda_destino == "real":
    conversao = (int(quantidade)) * dollar
    print(f"O valor de U${quantidade} dólares é igual a R${conversao:.2f} reais")
else:
    print("Câmbio não disponível")
    