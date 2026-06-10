# 📚 REFERÊNCIA RÁPIDA - Prova SAEP API

## ⚡ COMANDOS ESSENCIAIS

### Instalar dependências
```bash
pip install -r requirements
```

### Executar aplicação
```bash
uvicorn main:app --reload
```

### Acessar documentação
- **Swagger (recomendado)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔐 O QUE CADA COISA FAZ

### **config.py** - Segurança
- `obter_hash_senha()` → Criptografa senha com bcrypt
- `verificar_senha()` → Compara senha digitada com hash armazenado
- `criar_access_token()` → Gera token JWT válido por 30 minutos
- `verificar_token()` → Valida e extrai dados do token JWT
- `get_current_user_email()` → Dependency para proteger endpoints

### **schemas.py** - Validação de dados
- `ClienteRegistro` → Dados para novo usuário (com senha)
- `ClienteResposta` → Retorna dados do usuário (SEM senha)
- `Login` → Credenciais (email + senha)
- `Token` → Resposta com JWT
- `ProdutoBase/Resposta/Atualizar` → Validação de produtos

### **models/model.py** - Banco de dados
- `Cliente` → Usuários (tem email, CPF, senha_hash)
- `Produto` → Produtos (nome, preço, validade)
- `Registro` → Transações (cliente_id + produto_id)

### **auth_router.py** - Autenticação
- `/auth/registro` (POST) → Registra novo usuário
- `/auth/login` (POST) → Faz login
- `/auth/me` (GET) → Obter dados do usuário autenticado ⚠️ REQUER TOKEN
- `/auth/listar_usuario` (GET) → Lista todos ⚠️ REQUER TOKEN
- `/auth/criar_user` (POST) → Criar usuário (admin) ⚠️ REQUER TOKEN

### **prod_router.py** - Produtos
- `/produto/listar_produtos` (GET) → Lista pública ✅ SEM TOKEN
- `/produto/produtos/{id}` (GET) → Detalhes ✅ SEM TOKEN
- `/produto/criar_produto` (POST) → Criar ⚠️ REQUER TOKEN
- `/produto/atualizar_produto/{id}` (PUT) → Atualizar ⚠️ REQUER TOKEN
- `/produto/deletar_produto/{id}` (DELETE) → Deletar ⚠️ REQUER TOKEN

---

## 📋 TABELAS DO BANCO

### Cliente
```
id (PK) | nome | email (UNIQUE) | telefone | cpf (UNIQUE) | senha_hash | vip
```

### Produto
```
id (PK) | nome | preco | validade
```

### Registro
```
id (PK) | cliente_id (FK) | produto_id (FK) | data
```

---

## 🔄 FLUXO DE AUTENTICAÇÃO

```
Usuário digita: email + senha
        ↓
POST /auth/login ou /auth/registro
        ↓
Aplicação criptografa senha com bcrypt
        ↓
Compara com hash no banco
        ↓
✅ Válido → Cria JWT token
        ↓
Cliente recebe token
        ↓
Cliente envia token em header: "Authorization: Bearer <token>"
        ↓
App verifica token (não expirou? assinatura correta?)
        ↓
✅ Válido → Acesso ao endpoint
❌ Inválido → Erro 401
```

---

## 🛡️ SEGURANÇA IMPLEMENTADA

| Feature | Implementado | Detalhes |
|---------|-------------|----------|
| **Criptografia de Senha** | ✅ bcrypt | Irreversível, com salt aleatório |
| **JWT Token** | ✅ HS256 | Expira em 30 min, SECRET_KEY no .env |
| **Email Único** | ✅ | Não pode haver 2 usuários com mesmo email |
| **CPF Único** | ✅ | Não pode haver 2 usuários com mesmo CPF |
| **Bearer Token** | ✅ | Extrai token do header Authorization |
| **Validação de Dados** | ✅ Pydantic | Email, comprimento mínimo, tipos |

---

## 🚨 POSSÍVEIS ERROS E SOLUÇÕES

| Erro | Causa | Solução |
|------|-------|---------|
| `401 Token inválido` | Token expirou ou errado | Fazer login novamente |
| `400 Email já cadastrado` | Email duplicado | Use outro email |
| `400 CPF já cadastrado` | CPF duplicado | Use outro CPF |
| `404 Usuário não encontrado` | Email não existe no banco | Registre novo usuário |
| `500 Database connection error` | Banco offline ou credenciais erradas | Verifique .env |
| `Invalid authentication credentials` | Sem token no header | Adicione: `Authorization: Bearer <token>` |

---

## 🧪 TESTE RÁPIDO (3 minutos)

### 1. Registrar
```bash
curl -X POST "http://localhost:8000/auth/registro" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","email":"teste@test.com","telefone":"11999999999","cpf":"12345678901","senha":"Senha123!"}'
```

### 2. Guardar o token da resposta

### 3. Criar produto
```bash
curl -X POST "http://localhost:8000/produto/criar_produto" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome":"Produto Teste","preco":99.99,"validade":"31/12/2025"}'
```

### 4. Listar produtos
```bash
curl -X GET "http://localhost:8000/produto/listar_produtos"
```

**Pronto! Aplicação funcionando! ✅**

---

## 📞 RESUMO: O QUE FAZER PRIMEIRO

1. ✅ Instalar dependências: `pip install -r requirements`
2. ✅ Configurar .env com credenciais do banco
3. ✅ Criar tabelas no MySQL (via Alembic ou criação manual)
4. ✅ Executar: `uvicorn main:app --reload`
5. ✅ Abrir: http://localhost:8000/docs (Swagger)
6. ✅ Testar endpoints na interface visual

---

**Desenvolvido com ❤️ - Todas as informações em comentários nos arquivos**
