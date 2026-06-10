# 🧪 GUIA DE TESTES - Prova SAEP API

## 📌 Resumo das Funcionalidades

### 🔑 Autenticação (sem token necessário)
- **POST** `/auth/registro` - Registrar novo usuário (gera token JWT)
- **POST** `/auth/login` - Fazer login (gera token JWT)

### 👤 Usuários (REQUER TOKEN)
- **GET** `/auth/me` - Obter dados do usuário autenticado
- **GET** `/auth/listar_usuario` - Listar todos os usuários
- **POST** `/auth/criar_user` - Criar novo usuário (admin)

### 📦 Produtos (lista pública, criação requer token)
- **GET** `/produto/listar_produtos` - Listar produtos (público)
- **GET** `/produto/produtos/{id}` - Obter produto específico (público)
- **POST** `/produto/criar_produto` - Criar produto (REQUER TOKEN)
- **PUT** `/produto/atualizar_produto/{id}` - Atualizar produto (REQUER TOKEN)
- **DELETE** `/produto/deletar_produto/{id}` - Deletar produto (REQUER TOKEN)

---

## 🚀 PASSO A PASSO PARA TESTAR

### 1️⃣ Registrar Novo Usuário

**Endpoint:** `POST /auth/registro`

**Comando cURL:**
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

**Resposta (sucesso):**
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

✅ **SUCESSO!** Guarde o `access_token` para usar nos próximos testes!

---

### 2️⃣ Fazer Login

**Endpoint:** `POST /auth/login`

**Comando cURL:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "senha": "Senha123!"
  }'
```

**Resposta (sucesso):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "cpf": "12345678901",
    "vip": false
  }
}
```

---

### 3️⃣ Listar Produtos (Público)

**Endpoint:** `GET /produto/listar_produtos`

**Comando cURL:**
```bash
curl -X GET "http://localhost:8000/produto/listar_produtos"
```

**Resposta (sem autenticação necessária):**
```json
[
  {
    "id": 1,
    "nome": "Notebook",
    "preco": 2999.99,
    "validade": "31/12/2025"
  },
  {
    "id": 2,
    "nome": "Mouse",
    "preco": 49.99,
    "validade": "31/12/2026"
  }
]
```

---

### 4️⃣ Criar Produto (REQUER TOKEN)

**Endpoint:** `POST /produto/criar_produto`

**Comando cURL:**
```bash
curl -X POST "http://localhost:8000/produto/criar_produto" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Teclado Mecânico",
    "preco": 350.00,
    "validade": "31/12/2025"
  }'
```

**Resposta (sucesso):**
```json
{
  "id": 3,
  "nome": "Teclado Mecânico",
  "preco": 350.0,
  "validade": "31/12/2025"
}
```

✅ **PERFEITO!** Produto criado com sucesso!

---

### 5️⃣ Obter Dados do Usuário Autenticado (REQUER TOKEN)

**Endpoint:** `GET /auth/me`

**Comando cURL:**
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta (sucesso):**
```json
{
  "id": 1,
  "nome": "João Silva",
  "email": "joao@example.com",
  "telefone": "11999999999",
  "cpf": "12345678901",
  "vip": false
}
```

---

### 6️⃣ Atualizar Produto (REQUER TOKEN)

**Endpoint:** `PUT /produto/atualizar_produto/{id}`

**Comando cURL:**
```bash
curl -X PUT "http://localhost:8000/produto/atualizar_produto/3" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "preco": 399.99
  }'
```

**Resposta (sucesso):**
```json
{
  "id": 3,
  "nome": "Teclado Mecânico",
  "preco": 399.99,
  "validade": "31/12/2025"
}
```

---

### 7️⃣ Deletar Produto (REQUER TOKEN)

**Endpoint:** `DELETE /produto/deletar_produto/{id}`

**Comando cURL:**
```bash
curl -X DELETE "http://localhost:8000/produto/deletar_produto/3" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta (sucesso):**
```json
{
  "mensagem": "Produto deletado com sucesso"
}
```

---

## 🔒 SEGURANÇA - Testes de Erro

### ❌ Tentar acessar endpoint protegido SEM token

**Comando:**
```bash
curl -X GET "http://localhost:8000/auth/me"
```

**Resposta (erro):**
```json
{
  "detail": "Invalid authentication credentials"
}
```

---

### ❌ Tentar login com senha errada

**Comando:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "senha": "SenhaErrada123"
  }'
```

**Resposta (erro):**
```json
{
  "detail": "Email ou senha inválidos"
}
```

---

### ❌ Tentar registrar com email que já existe

**Comando:**
```bash
curl -X POST "http://localhost:8000/auth/registro" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Outro Nome",
    "email": "joao@example.com",
    "telefone": "11988888888",
    "cpf": "98765432101",
    "senha": "Senha456!"
  }'
```

**Resposta (erro):**
```json
{
  "detail": "Email já cadastrado"
}
```

---

## 🧑‍💻 USANDO A DOCUMENTAÇÃO INTERATIVA (SWAGGER)

1. Inicie a aplicação: `uvicorn main:app --reload`
2. Abra no navegador: **http://localhost:8000/docs**
3. Clique em "Authorize" (cadeado no topo direito)
4. Copie e cole seu token JWT (sem "Bearer ")
5. Pronto! Você pode testar todos os endpoints clicando em "Try it out"

---

## 📊 FLUXO COMPLETO DE TESTE

```
1. POST /auth/registro
   ↓
   ✅ Obter token JWT
   ↓
2. POST /produto/criar_produto (com token)
   ↓
   ✅ Produto criado
   ↓
3. GET /produto/listar_produtos
   ↓
   ✅ Ver produto na lista
   ↓
4. PUT /produto/atualizar_produto/{id} (com token)
   ↓
   ✅ Produto atualizado
   ↓
5. DELETE /produto/deletar_produto/{id} (com token)
   ↓
   ✅ Produto deletado
```

---

## 💡 DICAS IMPORTANTES

✅ **O token JWT expira em 30 minutos** - após isso, é necessário fazer login novamente

✅ **Sempre use "Bearer " antes do token** no header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

✅ **Senhas são criptografadas com bcrypt** - nunca são armazenadas em texto plano

✅ **Email e CPF são únicos** - não é possível registrar dois usuários com o mesmo email ou CPF

✅ **Use a documentação Swagger** em `/docs` para interface visual amigável

---

**Pronto para testar! 🚀**
