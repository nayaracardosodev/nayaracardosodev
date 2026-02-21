from flask import Flask
from app.controllers.usuario_controller import usuario_bp  # <--- Importamos a Recepcionista

app = Flask(__name__)

# Registramos o Blueprint (Damos o crachá pra ela trabalhar)
app.register_blueprint(usuario_bp)

# Rota de teste só pra saber se tá ligado
@app.route('/')
def hello():
    return "API MVC Rodando! 🚀 Use o Postman em /cadastro"

if __name__ == '__main__':
    app.run(debug=True)