from app.models.usuario_model import UsuarioModel
from app.repositories.viacep_repository import ViaCepRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.utils.validadores import Validador


class UsuarioService:

    @staticmethod
    def criar_usuario(dados):
        # --- (CÓDIGO DE CRIAÇÃO IGUAL AO ANTERIOR) ---
        campos = ['nome', 'sobrenome', 'cpf', 'cep']
        for campo in campos:
            if campo not in dados or not dados[campo]:
                return {"erro": f"O campo '{campo}' é obrigatório."}, 400

        nome = str(dados['nome']).strip()
        sobrenome = str(dados['sobrenome']).strip()

        erro_nome = Validador.validar_nome_sobrenome(nome, "Nome")
        if erro_nome: return {"erro": erro_nome}, 400
        erro_sobrenome = Validador.validar_nome_sobrenome(sobrenome, "Sobrenome")
        if erro_sobrenome: return {"erro": erro_sobrenome}, 400

        cpf_limpo = Validador.limpar_texto(dados['cpf'])
        erro_cpf = Validador.validar_cpf(cpf_limpo)
        if erro_cpf: return {"erro": erro_cpf}, 400

        cep_limpo = Validador.limpar_texto(dados['cep'])
        erro_cep = Validador.validar_cep(cep_limpo)
        if erro_cep: return {"erro": erro_cep}, 400

        if UsuarioRepository.buscar_por_cpf(cpf_limpo):
            print(f"❌ Tentativa de cadastro duplicado: CPF {cpf_limpo}")
            return {"erro": f"O CPF {dados['cpf']} já está cadastrado!"}, 409

        dados_endereco = ViaCepRepository.buscar_endereco(cep_limpo)
        if not dados_endereco:
            print(f"⚠️ Erro ao buscar CEP: {cep_limpo}")
            return {"erro": "CEP não encontrado ou serviço indisponível."}, 404

        nome_completo = f"{nome.title()} {sobrenome.title()}"

        novo_usuario = UsuarioModel(
            nome_completo=nome_completo,
            cpf=cpf_limpo,
            cep=cep_limpo,
            logradouro=dados_endereco.get('logradouro', 'N/A'),
            bairro=dados_endereco.get('bairro', 'N/A'),
            cidade=dados_endereco.get('localidade', 'N/A'),
            uf=dados_endereco.get('uf', 'N/A')
        )

        UsuarioRepository.salvar(novo_usuario.to_dict())

        print(f"--- NOVO USUÁRIO CADASTRADO: {nome_completo} ---")
        print(f"📍 Endereço: {novo_usuario.endereco['rua']} - {novo_usuario.endereco['cidade']}")
        print("------------------------------------------------")

        endereco_str = f"{novo_usuario.endereco['rua']}, {novo_usuario.endereco['bairro']} - {novo_usuario.endereco['cidade']}/{novo_usuario.endereco['uf']}"

        return {
            "mensagem": f"Usuário {nome_completo} cadastrado! Endereço: {endereco_str}",
            "dados": novo_usuario.to_dict()
        }, 201

    @staticmethod
    def listar_todos():
        usuarios = UsuarioRepository.listar_todos()
        print(f"📋 Listagem solicitada. Total de usuários: {len(usuarios)}")
        return usuarios, 200

    # --- NOVO: ATUALIZAR (PUT) ---
    @staticmethod
    def atualizar_usuario(cpf, dados):
        cpf_limpo = Validador.limpar_texto(cpf)
        usuario_atual = UsuarioRepository.buscar_por_cpf(cpf_limpo)

        if not usuario_atual:
            return {"erro": "Usuário não encontrado."}, 404

        # Prepara dados atuais
        novo_nome_completo = usuario_atual['nome_completo']
        novo_endereco_obj = usuario_atual['endereco']
        novo_cep = usuario_atual['cep']

        # Se mandou NOME e SOBRENOME novos
        if 'nome' in dados and 'sobrenome' in dados:
            nome = str(dados['nome']).strip()
            sobrenome = str(dados['sobrenome']).strip()

            erro1 = Validador.validar_nome_sobrenome(nome, "Nome")
            erro2 = Validador.validar_nome_sobrenome(sobrenome, "Sobrenome")

            if erro1: return {"erro": erro1}, 400
            if erro2: return {"erro": erro2}, 400

            novo_nome_completo = f"{nome.title()} {sobrenome.title()}"

        # Se mandou CEP novo
        if 'cep' in dados:
            cep_novo = Validador.limpar_texto(dados['cep'])
            erro_cep = Validador.validar_cep(cep_novo)
            if erro_cep: return {"erro": erro_cep}, 400

            dados_endereco = ViaCepRepository.buscar_endereco(cep_novo)
            if not dados_endereco:
                return {"erro": "Novo CEP não encontrado."}, 404

            novo_cep = cep_novo
            novo_endereco_obj = {
                "rua": dados_endereco.get('logradouro', 'N/A'),
                "bairro": dados_endereco.get('bairro', 'N/A'),
                "cidade": dados_endereco.get('localidade', 'N/A'),
                "uf": dados_endereco.get('uf', 'N/A')
            }

        # Atualiza o objeto na memória
        usuario_atual['nome_completo'] = novo_nome_completo
        usuario_atual['endereco'] = novo_endereco_obj
        usuario_atual['cep'] = novo_cep

        # Salva (Atualiza) no Repository
        UsuarioRepository.salvar(usuario_atual)

        print(f"🔄 Usuário atualizado: {cpf_limpo}")

        return {
            "mensagem": "Dados atualizados com sucesso!",
            "dados_novos": usuario_atual
        }, 200

    # --- NOVO: DELETAR (DELETE) ---
    @staticmethod
    def deletar_usuario(cpf):
        cpf_limpo = Validador.limpar_texto(cpf)
        usuario_atual = UsuarioRepository.buscar_por_cpf(cpf_limpo)

        if not usuario_atual:
            return {"erro": "Usuário não encontrado."}, 404

        nome_removido = usuario_atual['nome_completo']
        UsuarioRepository.deletar(cpf_limpo)

        print(f"🗑️ Usuário removido: {nome_removido} (CPF: {cpf_limpo})")

        return {"mensagem": f"O usuário {nome_removido} foi removido com sucesso!"}, 200