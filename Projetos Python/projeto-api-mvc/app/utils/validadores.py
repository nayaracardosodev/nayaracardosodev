import re


class Validador:

    @staticmethod
    def limpar_texto(texto):
        """Remove sujeira (pontos, traços, espaços, barras)"""
        if not texto:
            return ""
        return str(texto).replace(".", "").replace("-", "").replace(" ", "").replace("/", "")

    @staticmethod
    def validar_nome_sobrenome(texto, tipo="Nome"):
        """
        Valida se o nome tem tamanho suficiente e apenas letras.
        Recuperamos o seu Regex original!
        """
        texto = str(texto).strip()

        # 1. Tamanho mínimo (ex: "Sá" ou "Ana")
        if len(texto) < 2:
            return f"{tipo} muito curto. Digite pelo menos 2 letras."

        # 2. Regex: Aceita letras e acentos (ex: "João", "Renée")
        # Se tiver número ou símbolo estranho, reprova.
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', texto):
            return f"{tipo} inválido (use apenas letras)."

        return None

    @staticmethod
    def validar_cpf(cpf_limpo):
        """Valida formato e dígitos repetidos do CPF"""
        if not cpf_limpo.isdigit():
            return "CPF deve conter apenas números."

        if len(cpf_limpo) != 11:
            return "CPF inválido. Deve ter 11 dígitos."

        # Bloqueia 111.111.111-11
        if cpf_limpo == cpf_limpo[0] * 11:
            return "CPF inválido. Dígitos repetidos não são permitidos."

        return None

    @staticmethod
    def validar_cep(cep_limpo):
        """Valida se o CEP tem 8 dígitos numéricos"""
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            return "CEP Inválido. Deve conter 8 dígitos numéricos."
        return None