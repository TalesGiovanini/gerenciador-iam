from flask import Flask, request, jsonify

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Simulação de um banco de dados em memória
users_db = {}

# Rota raiz para exibir uma mensagem inicial
@app.route('/')
def home():
    return "Bem-vindo ao Gerenciador de IAM! Utilize as rotas disponíveis para interagir com o sistema."

# Função para criar um usuário
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Função padrão: 'user'

    if username in users_db:
        return jsonify({'error': 'Usuário já existe!'}), 400

    users_db[username] = {'password': password, 'role': role}
    return jsonify({'message': f'Usuário {username} criado com sucesso!'}), 201

# Função para listar usuários
@app.route('/users', methods=['GET'])
def list_users():
    return jsonify({'users': list(users_db.keys())}), 200

# Função para autenticar um usuário
@app.route('/auth', methods=['POST'])
def authenticate_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Credenciais inválidas!'}), 401

    return jsonify({'message': f'Usuário {username} autenticado com sucesso!'}), 200

# Função para verificar permissões de um usuário
@app.route('/permissions', methods=['GET'])
def get_permissions():
    username = request.args.get('username')

    user = users_db.get(username)
    if not user:
        return jsonify({'error': 'Usuário não encontrado!'}), 404

    # Permissões baseadas no papel (role)
    permissions = {
        'admin': ['create_user', 'delete_user', 'view_reports'],
        'user': ['view_profile', 'update_profile']
    }
    return jsonify({'permissions': permissions.get(user['role'], [])}), 200

if __name__ == '__main__':
    app.run(debug=True)

