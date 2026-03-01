class UsuarioRepository:
    # O Banco de Dados fica aqui agora (Protegido)
    _banco_de_dados = {}

    @classmethod
    def salvar(cls, usuario_dict):
        """Salva ou atualiza um usuário"""
        # A chave é o CPF
        cls._banco_de_dados[usuario_dict['cpf']] = usuario_dict

    @classmethod
    def buscar_por_cpf(cls, cpf):
        """Busca um usuário pelo CPF. Retorna None se não achar."""
        return cls._banco_de_dados.get(cpf)

    @classmethod
    def listar_todos(cls):
        """Devolve todos os usuários"""
        return cls._banco_de_dados

    @classmethod
    def deletar(cls, cpf):
        """Remove um usuário se ele existir"""
        if cpf in cls._banco_de_dados:
            del cls._banco_de_dados[cpf]
            return True
        return False