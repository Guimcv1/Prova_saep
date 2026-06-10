# 🔐 Prova SAEP - Aplicação com JWT e Autenticação

Aplicação FastAPI com autenticação JWT, criptografia de senhas e gestão de clientes e produtos.

## 📋 Funcionalidades Implementadas

### ✅ Autenticação e Segurança
- ✔️ Registro de novos usuários com criptografia de senha (bcrypt)
- ✔️ Login com geração de token JWT
- ✔️ Autenticação via Bearer Token
- ✔️ Proteção de endpoints com verificação de token
- ✔️ Validação de email único e CPF único

### ✅ Schemas (Pydantic Models)
- ✔️ ClienteRegistro - Para registro de novos usuários
- ✔️ ClienteResposta - Para retorno de dados do cliente
- ✔️ Login - Para credenciais de login
- ✔️ Token - Para resposta de autenticação
- ✔️ ProdutoBase, ProdutoResposta, ProdutoAtualizar
- ✔️ RegistroResposta

### ✅ Endpoints de Autenticação
- **POST** `/auth/registro` - Registrar novo usuário
- **POST** `/auth/login` - Fazer login
- **GET** `/auth/me` - Obter dados do usuário autenticado (protegido)
- **GET** `/auth/listar_usuario` - Listar todos os usuários (protegido)
- **POST** `/auth/criar_user` - Criar novo usuário (protegido)

### ✅ Endpoints de Produtos
- **GET** `/produto/listar_produtos` - Listar todos os produtos
- **GET** `/produto/produtos/{produto_id}` - Obter produto específico
- **POST** `/produto/criar_produto` - Criar novo produto (protegido)
- **PUT** `/produto/atualizar_produto/{produto_id}` - Atualizar produto (protegido)
- **DELETE** `/produto/deletar_produto/{produto_id}` - Deletar produto (protegido)

## 🚀 Como Instalar e Usar

### 1. Instalar Dependências
```bash
pip install -r requirements
```

### 2. Configurar o Arquivo .env
```env
DB_NAME = seu_banco
DB_HOST = 2dsmoca.tech
DB_USER = root
DB_PASSWORD = sua_senha
DB_PORT = 3301
SECRET_KEY = sua-chave-secreta-super-segura
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 3. Criar as Tabelas no Banco de Dados
```bash
# Execute o seguinte comando para criar as migrações
alembic revision --autogenerate -m "Initial migration"

# Apply as migrações
alembic upgrade head
```

### 4. Executar a Aplicação
```bash
uvicorn main:app --reload
```

A aplicação estará disponível em: **http://localhost:8000**

## 📚 Documentação Interativa

Acesse a documentação Swagger em: **http://localhost:8000/docs**

## 🔑 Como Usar a API

### 1. Registro (sem autenticação)
```bash
curl -X POST "http://localhost:8000/auth/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "cpf": "12345678901",
    "senha": "Senha123!"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "cpf": "12345678901",
    "vip": false,
    "id": 1
  }
}
```

### 2. Login (sem autenticação)
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "senha": "Senha123!"
  }'
```

### 3. Usar Endpoints Protegidos
Copie o token JWT da resposta e use no header Authorization:

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer SEU_TOKEN_JWT_AQUI"
```

### 4. Criar Produto (protegido)
```bash
curl -X POST "http://localhost:8000/produto/criar_produto" \
  -H "Authorization: Bearer SEU_TOKEN_JWT_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Produto Exemplo",
    "preco": 99.99,
    "validade": "31/12/2025"
  }'
```

## 🔒 Segurança Implementada

### Criptografia de Senhas
- Utiliza **bcrypt** para hash de senhas
- Senhas nunca são armazenadas em texto plano
- Verificação segura de senha usando `passlib`

### JWT (JSON Web Token)
- Token com expiração (30 minutos por padrão)
- Algoritmo: HS256
- Chave secreta configurável via .env
- Autenticação via Bearer Token

### Validações
- Email único no banco de dados
- CPF único no banco de dados
- Senhas com mínimo de 8 caracteres
- Validação de formato de email com EmailStr

## 📁 Estrutura do Projeto

```
Prova_saep/
├── main.py              # Aplicação principal
├── config.py            # Configuração de JWT e criptografia
├── schemas.py           # Modelos Pydantic
├── .env                 # Variáveis de ambiente
├── requirements         # Dependências
├── models/
│   └── model.py         # Modelos SQLAlchemy
├── routers/
│   ├── auth_router.py   # Endpoints de autenticação
│   └── prod_router.py   # Endpoints de produtos
└── alembic/            # Migrações de banco de dados
```

## 🐛 Troubleshooting

### Erro: "FOREIGN KEY constraint failed"
Certifique-se de que as tabelas são criadas na ordem correta. Use Alembic para gerenciar migrações.

### Erro: "Token inválido ou expirado"
Verifique se:
- O token foi copiado corretamente
- O token não expirou (padrão: 30 minutos)
- A SECRET_KEY no .env está correta

### Erro: "Email já cadastrado"
O email já existe no banco de dados. Use outro email para registrar.

## 📝 Notas Importantes

1. **Segurança:** Altere a `SECRET_KEY` no `.env` para uma chave segura em produção
2. **Tokens:** Os tokens JWT expiram em 30 minutos. Implemente refresh token para melhor UX
3. **Banco de Dados:** Certifique-se de que o banco de dados existe e está acessível
4. **CORS:** Se precisar de CORS, adicione ao main.py

## 🔄 Próximas Melhorias Sugeridas

- [ ] Implementar Refresh Token
- [ ] Adicionar roles e permissões (admin, user)
- [ ] Implementar rate limiting
- [ ] Adicionar logs de auditoria
- [ ] Testes unitários
- [ ] Documentação de erros mais detalhada

---

**Desenvolvido com ❤️ usando FastAPI**
