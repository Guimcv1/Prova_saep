# 📖 ÍNDICE - COMECE AQUI

Bem-vindo ao projeto **Prova SAEP** com **JWT, Criptografia e Autenticação**!

Escolha um ponto de entrada abaixo:

---

## 🚀 QUERO COMEÇAR RÁPIDO (5 minutos)

1. **Instalar dependências:**
   ```bash
   pip install -r requirements
   ```

2. **Executar a aplicação:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Abrir documentação:**
   - 🔗 http://localhost:8000/docs (Swagger - recomendado!)
   - 📄 http://localhost:8000/redoc

4. **Fazer primeiro teste:**
   - Clique em "Authorize" (cadeado no Swagger)
   - Clique em um endpoint verde (GET /produto/listar_produtos)
   - Clique em "Try it out"
   - Clique em "Execute"

✅ **Pronto! Você viu a API funcionando!**

---

## 🎓 QUERO ENTENDER O PROJETO

| Documento | Tempo | O que contém |
|-----------|-------|-------------|
| 📘 [README.md](README.md) | 10 min | Visão geral, funcionalidades, como instalar |
| 🏗️ [ESTRUTURA_VISUAL.md](ESTRUTURA_VISUAL.md) | 15 min | Diagramas visuais da arquitetura |
| 📚 [GUIA_ARQUIVOS.md](GUIA_ARQUIVOS.md) | 20 min | O que faz cada arquivo, função por função |
| ⚡ [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md) | 5 min | Consulta rápida, tabelas, erros comuns |
| ✅ [CHECKLIST.md](CHECKLIST.md) | 10 min | O que foi implementado |

---

## 🧪 QUERO TESTAR A API

👉 [TESTES.md](TESTES.md) - Guia passo a passo com exemplos de cURL

### Resumo rápido:

1. **Registrar novo usuário:**
   ```bash
   curl -X POST "http://localhost:8000/auth/registro" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "João",
       "email": "joao@test.com",
       "telefone": "11999999999",
       "cpf": "12345678901",
       "senha": "Senha123!"
     }'
   ```

2. **Guardar o token da resposta:**
   ```
   SEU_TOKEN_AQUI: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

3. **Criar produto com token:**
   ```bash
   curl -X POST "http://localhost:8000/produto/criar_produto" \
     -H "Authorization: Bearer SEU_TOKEN_AQUI" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "Notebook",
       "preco": 2999.99,
       "validade": "31/12/2025"
     }'
   ```

---

## 🔐 QUERO ENTENDER A SEGURANÇA

**Implementado:**
- ✅ Bcrypt - Criptografia irreversível de senhas
- ✅ JWT - Tokens com expiração (30 minutos)
- ✅ Bearer Token - Autenticação HTTP padrão
- ✅ Validação - Pydantic models
- ✅ Email Único - Constraint no banco
- ✅ CPF Único - Constraint no banco

**Documentos:**
1. Leia: [ESTRUTURA_VISUAL.md](ESTRUTURA_VISUAL.md) - Seção "Fluxo de Segurança"
2. Leia: [GUIA_ARQUIVOS.md](GUIA_ARQUIVOS.md) - Seção "config.py"
3. Veja o código: `config.py` (100% comentado)

---

## 📊 QUERO VER O QUE FOI IMPLEMENTADO

👉 [CHECKLIST.md](CHECKLIST.md) - Lista completa com ✅ tudo que foi feito

---

## 💻 QUERO ENTENDER O CÓDIGO

**Ordem recomendada de leitura:**

1. **main.py** (5 min)
   - Cria a app FastAPI
   - Inclui os routers

2. **config.py** (10 min) ⭐ IMPORTANTE
   - Bcrypt para criptografia
   - JWT para tokens
   - Dependencies para proteção

3. **schemas.py** (10 min)
   - Pydantic models
   - Validação de dados

4. **models/model.py** (5 min)
   - Tabelas do banco
   - Relacionamentos

5. **routers/auth_router.py** (15 min)
   - Endpoints de autenticação
   - Lógica de login/registro

6. **routers/prod_router.py** (10 min)
   - Endpoints de produtos
   - CRUD completo

**Todos os arquivos têm 100% de comentários explicativos!**

---

## 🎯 QUICK REFERENCE

### Endpoints principais

```
PÚBLICO (sem token):
GET  /produto/listar_produtos
GET  /produto/produtos/{id}
POST /auth/registro
POST /auth/login

PRIVADO (com token):
GET  /auth/me
GET  /auth/listar_usuario
POST /auth/criar_user
POST /produto/criar_produto
PUT  /produto/atualizar_produto/{id}
DELETE /produto/deletar_produto/{id}
```

### Credenciais padrão para teste

Use os dados que quiser para registrar um novo usuário:
- Email: qualquer email válido (ex: teste@example.com)
- Senha: mínimo 8 caracteres (ex: Senha123!)
- CPF: 11 caracteres (ex: 12345678901)
- Telefone: 10-15 caracteres (ex: 11999999999)

---

## ❓ FAQ RÁPIDO

**P: Como faço login?**  
R: POST `/auth/login` com email e senha → você recebe um token JWT

**P: Como faço um teste protegido?**  
R: Copie o token que recebeu e adicione no header: `Authorization: Bearer seu_token`

**P: Quanto tempo o token dura?**  
R: 30 minutos. Após isso, faça login novamente.

**P: Posso mudar a expiração do token?**  
R: Sim! Altere `ACCESS_TOKEN_EXPIRE_MINUTES` no `.env`

**P: Onde está a senha armazenada?**  
R: Nunca em texto plano! Sempre como hash bcrypt no banco.

**P: Posso deletar um produto?**  
R: Sim, com DELETE `/produto/deletar_produto/{id}` (requer token)

**P: Posso editar apenas alguns campos do produto?**  
R: Sim! PUT permite atualização parcial (campos opcionais)

---

## 📁 ESTRUTURA RESUMIDA

```
Prova_saep/
├── main.py              ← Aplicação principal
├── config.py            ← Segurança (JWT + bcrypt)
├── schemas.py           ← Validação (Pydantic)
├── models/model.py      ← Banco de dados
├── routers/
│   ├── auth_router.py   ← Login/Registro
│   └── prod_router.py   ← Produtos CRUD
├── .env                 ← Configuração
├── requirements         ← Dependências
└── Documentação/
    ├── README.md
    ├── TESTES.md
    ├── ESTRUTURA_VISUAL.md
    ├── GUIA_ARQUIVOS.md
    ├── REFERENCIA_RAPIDA.md
    ├── CHECKLIST.md
    └── INDEX.md (este arquivo)
```

---

## 🚨 IMPORTANTE

⚠️ **Em Produção:**
- Mude `SECRET_KEY` no `.env` para algo seguro e aleatório
- Use variáveis de ambiente seguras (não hardcode)
- Ative HTTPS/TLS
- Implemente rate limiting
- Adicione logs de auditoria

---

## 🎉 PARABÉNS!

Você tem uma **API REST completa, segura e funcional** com:
- ✅ Registro e Login
- ✅ JWT Tokens
- ✅ Criptografia Bcrypt
- ✅ CRUD de Produtos
- ✅ Autenticação Bearer
- ✅ Validação com Pydantic
- ✅ Banco de Dados MySQL
- ✅ Documentação Interativa (Swagger)

---

## 📞 PRÓXIMOS PASSOS

Escolha o que fazer:

1. **Testar a API** → [TESTES.md](TESTES.md)
2. **Entender o código** → [GUIA_ARQUIVOS.md](GUIA_ARQUIVOS.md)
3. **Ver estrutura visual** → [ESTRUTURA_VISUAL.md](ESTRUTURA_VISUAL.md)
4. **Consulta rápida** → [REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md)
5. **Rodar agora:** `uvicorn main:app --reload`

---

**Desenvolvido com ❤️ - Tudo comentado e pronto para aprender!**

🚀 **Pronto para começar? Execute: `uvicorn main:app --reload`**
