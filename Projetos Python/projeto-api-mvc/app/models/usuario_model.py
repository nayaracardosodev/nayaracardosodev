class UsuarioModel:
    def __init__(self, nome_completo, cpf, cep, logradouro=None, bairro=None, cidade=None, uf=None):
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.cep = cep
        # Dados do ViaCep (opcionais no início)
        self.endereco = {
            "rua": logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "uf": uf
        }

    def to_dict(self):
        return {
            "nome_completo": self.nome_completo,
            "cpf": self.cpf,
            "cep": self.cep,
            "endereco": self.endereco
        }