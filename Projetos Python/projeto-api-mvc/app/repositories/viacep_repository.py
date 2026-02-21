import requests


class ViaCepRepository:

    @staticmethod
    def buscar_endereco(cep):
        """
        Busca o endereço no ViaCep.
        Retorna: Dicionário com dados (Se achar) OU None (Se der qualquer erro).
        """
        try:
            # 1. Tenta buscar (mantive o seu timeout de 3s, que é ótimo!)
            url = f"https://viacep.com.br/ws/{cep}/json/"
            response = requests.get(url, timeout=3)

            # 2. Se o site do ViaCep der erro 404 ou 500, isso aqui avisa
            response.raise_for_status()

            dados = response.json()

            # 3. Se o CEP for válido mas não existir (ex: 99999-999)
            if "erro" in dados:
                return None

            # 4. Devolve os dados limpos
            return dados

        except requests.exceptions.Timeout:
            # Se demorar demais, apenas retornamos None (o Motoboy voltou vazio)
            print(f"Erro: Timeout ao buscar CEP {cep}")  # Log no terminal pra você ver
            return None

        except Exception as e:
            # Qualquer outro erro
            print(f"Erro no ViaCep: {e}")
            return None