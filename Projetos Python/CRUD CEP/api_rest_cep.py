import requests
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- BANCO DE DADOS SIMULADO ---
banco_de_dados = {}


# --- CLASSE 1: O "Fiscal" (Validador) ---
class Validador:

    @staticmethod
    def limpar_texto(texto):
        """Remove sujeira (pontos, traços, espaços, barras)"""
        if not texto:
            return ""
        return str(texto).replace(".", "").replace("-", "").replace(" ", "").replace("/", "")

    @staticmethod
    def validar_nome_sobrenome(texto, tipo="Nome"):
        """Valida tamanho e se tem apenas letras"""
        texto = str(texto).strip()

        # Aceita nomes curtos como "Sá" ou "Ana" (mínimo 2)
        if len(texto) < 2:
            return f"{tipo} muito curto. Digite pelo menos 2 letras."

        # Regex: Aceita letras e acentos
        if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', texto):
            return f"{tipo} inválido (use apenas letras)."
        return None

    @staticmethod
    def validar_cpf(cpf_limpo):
        """Valida formato do CPF"""
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
        """Valida formato do CEP"""
        if not cep_limpo.isdigit() or len(cep_limpo) != 8:
            return "CEP Inválido. Deve conter 8 dígitos numéricos."
        return None


# --- CLASSE 2: O "Mensageiro" (Serviço Externo) ---
class ViaCepService:

    @staticmethod
    def buscar_endereco(cep):
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=3)
            response.raise_for_status()
            dados = response.json()

            if "erro" in dados:
                return None, "CEP não encontrado na base dos Correios."

            return dados, None

        except requests.exceptions.Timeout:
            return None, "O serviço de CEP está demorando."
        except Exception as e:
            return None, f"Erro ao buscar CEP: {str(e)}"


# --- ROTAS (CONTROLLERS) ---

# 1. CADASTRAR (POST)
@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    try:
        dados = request.get_json()
    except:
        return jsonify({"erro": "JSON inválido."}), 400

    # Validação de Campos Obrigatórios
    campos = ['nome', 'sobrenome', 'cpf', 'cep']
    for campo in campos:
        if campo not in dados or dados[campo] is None:
            return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

    # Limpeza e Validação
    nome = str(dados['nome']).strip()
    sobrenome = str(dados['sobrenome']).strip()

    erro_nome = Validador.validar_nome_sobrenome(nome, "Nome")
    if erro_nome: return jsonify({"erro": erro_nome}), 400

    erro_sobrenome = Validador.validar_nome_sobrenome(sobrenome, "Sobrenome")
    if erro_sobrenome: return jsonify({"erro": erro_sobrenome}), 400

    cpf_limpo = Validador.limpar_texto(dados['cpf'])
    erro_cpf = Validador.validar_cpf(cpf_limpo)
    if erro_cpf: return jsonify({"erro": erro_cpf}), 400

    cep_limpo = Validador.limpar_texto(dados['cep'])
    erro_cep = Validador.validar_cep(cep_limpo)
    if erro_cep: return jsonify({"erro": erro_cep}), 400

    # Regra de Negócio: Duplicidade
    if cpf_limpo in banco_de_dados:
        return jsonify({"erro": f"O CPF {dados['cpf']} já está cadastrado!"}), 409

    # Busca Endereço
    dados_endereco, erro_api = ViaCepService.buscar_endereco(cep_limpo)
    if erro_api:
        status = 404 if "não encontrado" in erro_api else 503
        return jsonify({"erro": erro_api}), status

    # Sucesso - Montagem do Objeto
    nome_completo = f"{nome.title()} {sobrenome.title()}"

    novo_usuario = {
        "nome_completo": nome_completo,
        "cpf": cpf_limpo,
        "endereco": {
            "rua": dados_endereco.get('logradouro', 'N/A'),
            "bairro": dados_endereco.get('bairro', 'N/A'),
            "cidade": dados_endereco.get('localidade', 'N/A'),
            "uf": dados_endereco.get('uf', 'N/A')
        }
    }

    banco_de_dados[cpf_limpo] = novo_usuario

    # Mensagem Final
    endereco_str = f"{novo_usuario['endereco']['rua']}, {novo_usuario['endereco']['bairro']} - {novo_usuario['endereco']['cidade']}/{novo_usuario['endereco']['uf']}"
    mensagem_final = f"Usuário {nome_completo} cadastrado! Endereço: {endereco_str}"

    print(f"--- NOVO USUÁRIO: {nome_completo} ---")

    return jsonify({
        "mensagem": mensagem_final,
        "dados": novo_usuario
    }), 201


# 2. LISTAR TODOS (GET)
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(banco_de_dados), 200


# 3. ATUALIZAR (PUT) - Mágica acontece aqui!
@app.route('/usuarios/<cpf>', methods=['PUT'])
def atualizar_usuario(cpf):
    # Limpa o CPF da URL
    cpf_limpo = Validador.limpar_texto(cpf)

    # Verifica se existe
    if cpf_limpo not in banco_de_dados:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    try:
        dados = request.get_json()
    except:
        return jsonify({"erro": "JSON inválido."}), 400

    # Pega o usuário atual do banco
    usuario_atual = banco_de_dados[cpf_limpo]

    # --- PREPARAÇÃO (Não salvamos nada ainda) ---
    novo_nome_completo = usuario_atual['nome_completo']
    novo_endereco_obj = usuario_atual['endereco']

    # Se mandou NOME e SOBRENOME novos
    if 'nome' in dados and 'sobrenome' in dados:
        nome = str(dados['nome']).strip()
        sobrenome = str(dados['sobrenome']).strip()

        erro1 = Validador.validar_nome_sobrenome(nome, "Nome")
        erro2 = Validador.validar_nome_sobrenome(sobrenome, "Sobrenome")

        if erro1: return jsonify({"erro": erro1}), 400
        if erro2: return jsonify({"erro": erro2}), 400

        # Se passou, prepara o novo nome
        novo_nome_completo = f"{nome.title()} {sobrenome.title()}"

    # Se mandou CEP novo
    if 'cep' in dados:
        cep_novo = Validador.limpar_texto(dados['cep'])
        erro_cep = Validador.validar_cep(cep_novo)
        if erro_cep: return jsonify({"erro": erro_cep}), 400

        dados_endereco, erro_api = ViaCepService.buscar_endereco(cep_novo)
        if erro_api: return jsonify({"erro": erro_api}), 404  # Se o CEP não existir, para tudo.

        # Se passou, prepara o novo endereço
        novo_endereco_obj = {
            "rua": dados_endereco.get('logradouro', 'N/A'),
            "bairro": dados_endereco.get('bairro', 'N/A'),
            "cidade": dados_endereco.get('localidade', 'N/A'),
            "uf": dados_endereco.get('uf', 'N/A')
        }

    # --- COMMIT (Agora salvamos tudo de uma vez) ---
    usuario_atual['nome_completo'] = novo_nome_completo
    usuario_atual['endereco'] = novo_endereco_obj

    # Devolvemos os dados atualizados
    return jsonify({
        "mensagem": "Dados atualizados com sucesso!",
        "dados_novos": usuario_atual
    }), 200


# 4. DELETAR (DELETE)
@app.route('/usuarios/<cpf>', methods=['DELETE'])
def deletar_usuario(cpf):
    cpf_limpo = Validador.limpar_texto(cpf)

    if cpf_limpo not in banco_de_dados:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    nome_removido = banco_de_dados[cpf_limpo]['nome_completo']
    del banco_de_dados[cpf_limpo]

    return jsonify({"mensagem": f"O usuário {nome_removido} foi removido com sucesso!"}), 200


if __name__ == '__main__':
    app.run(debug=True)