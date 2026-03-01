from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

# 1. CADASTRAR (POST)
@usuario_bp.route('/cadastro', methods=['POST'])
def cadastrar():
    try:
        dados = request.get_json()
    except:
        return jsonify({"erro": "JSON inválido."}), 400

    resposta, status_code = UsuarioService.criar_usuario(dados)
    return jsonify(resposta), status_code

# 2. LISTAR (GET)
@usuario_bp.route('/usuarios', methods=['GET'])
def listar():
    resposta, status_code = UsuarioService.listar_todos()
    return jsonify(resposta), status_code

# 3. ATUALIZAR (PUT) - NOVO!
@usuario_bp.route('/usuarios/<cpf>', methods=['PUT'])
def atualizar(cpf):
    try:
        dados = request.get_json()
    except:
        return jsonify({"erro": "JSON inválido."}), 400

    resposta, status_code = UsuarioService.atualizar_usuario(cpf, dados)
    return jsonify(resposta), status_code

# 4. DELETAR (DELETE) - NOVO!
@usuario_bp.route('/usuarios/<cpf>', methods=['DELETE'])
def deletar(cpf):
    resposta, status_code = UsuarioService.deletar_usuario(cpf)
    return jsonify(resposta), status_code