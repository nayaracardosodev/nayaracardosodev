# 🐍 API de Gestão de Usuários (CRUD) - Python & Clean Architecture

Este projeto é uma API RESTful robusta desenvolvida em Python para a gestão de usuários, aplicando princípios de **Arquitetura Limpa** e separação de responsabilidades. O objetivo é demonstrar práticas de engenharia de software voltadas para manutenção, escalabilidade e resiliência.

---

### 🏗️ Arquitetura do Projeto

A aplicação segue a divisão em camadas para garantir o desacoplamento:

- **`Models`**: Define a estrutura e integridade dos dados (Entidades).
- **`Controllers`**: Gerencia as rotas HTTP, validação inicial da entrada e retorno de respostas.
- **`Services`**: Contém o "cérebro" da aplicação. É onde residem as regras de negócio e orquestração dos dados.
- **`Repositories`**: Camada de persistência e gateway de APIs externas (como a integração com ViaCEP).
- **`Utils`**: Conjunto de ferramentas utilitárias para higienização e validação (Regex de CPF, nomes e CEP).

---

### 🚀 Principais Funcionalidades

- **CRUD Completo:** Criação, leitura, listagem, atualização e deleção de perfis.
- **Integração ViaCEP:** Busca automatizada de logradouro, bairro e cidade a partir do CEP informado.
- **Resiliência:** Implementação de timeouts estratégicos em chamadas externas e tratamento global de exceções.
- **Higienização de Dados:** Sanitização proativa de strings e validação rigorosa de documentos via Expressões Regulares (Regex).

---

### 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework:** Flask (API REST)
- **Integrações:** Requests (Consumo de API ViaCEP)
- **Padrões:** MVC + Service Layer / Repository Pattern

---

### 🏁 Como Executar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)

2. **Configurar Ambiente Virtual (Recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instalar Dependências:**
   ```bash
   pip install -r requirements.txt

4. **Rodar a Aplicação:**
   ```bash
   python run.py