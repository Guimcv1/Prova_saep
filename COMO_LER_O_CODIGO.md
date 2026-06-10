# 📖 COMO LER O CÓDIGO - Guia Interativo

Este documento te guia **passo a passo** sobre como ler e entender todo o código do projeto.

---

## 🎯 ANTES DE COMEÇAR

✅ Certifique-se de:
1. Ter Python instalado
2. Ter lido o [INDEX.md](INDEX.md)
3. Ter o projeto aberto no VS Code
4. Ter a extensão Python instalada (para syntax highlighting)

---

## 📚 ORDEM RECOMENDADA DE LEITURA

### FASE 1: ESTRUTURA BÁSICA (15 minutos)

#### 1. Leia: `main.py`
**Tempo:** 5 minutos
**Objetivo:** Entender como a aplicação é criada

```python
# O que procurar:
# - Como FastAPI é criado
# - Como os routers são incluídos
# - Qual é o endpoint raiz
```

**Depois de ler, você deve ser capaz de:**
- Explicar o que `app = FastAPI()` faz
- Entender por que incluem-se routers
- Saber em que ordem os routers são incluídos

---

#### 2. Leia: `schemas.py` - Apenas `ClienteBase` e `Login`
**Tempo:** 5 minutos
**Objetivo:** Entender validação Pydantic

```python
# O que procurar:
# - Como Pydantic valida dados
# - O que significa 'Field(...)'
# - Como 'EmailStr' funciona
```

**Depois de ler, você deve ser capaz de:**
- Explicar o que é um schema
- Entender a diferença entre ClienteBase, ClienteRegistro e ClienteResposta
- Saber por que validação é importante

---

#### 3. Leia: `models/model.py`
**Tempo:** 5 minutos
**Objetivo:** Entender o banco de dados

```python
# O que procurar:
# - Como se conecta ao MySQL
# - Estrutura da tabela Cliente
# - Significado de 'nullable=False' e 'unique=True'
```

**Depois de ler, você deve ser capaz de:**
- Explicar como SQLAlchemy conecta ao banco
- Entender cada coluna da tabela Cliente
- Saber por que email e cpf são UNIQUE

---

### FASE 2: SEGURANÇA (20 minutos) ⭐ IMPORTANTE

#### 4. Leia: `config.py` - Funções de criptografia
**Tempo:** 10 minutos
**Objetivo:** Entender como bcrypt funciona

```python
# Leia estas funções em ordem:
# 1. obter_hash_senha()
# 2. verificar_senha()
# Ignore JWT por enquanto
```

**Perguntas para testar compreensão:**
- Como é possível verificar senha se o hash é irreversível?
- Por que bcrypt é melhor que MD5?
- O que é salt aleatório?

**Respuestas esperadas:**
- (Salt + Senha → Hash) - cada vez diferente, bcrypt compara com a função verify
- Bcrypt é intencionalmente lento (contra brute force), MD5 é rápido
- Impede ataques rainbow table

---

#### 5. Leia: `config.py` - Funções de JWT
**Tempo:** 10 minutos
**Objetivo:** Entender como JWT funciona

```python
# Leia estas funções em ordem:
# 1. criar_access_token()
# 2. verificar_token()
# 3. get_current_user_email()
```

**Perguntas para testar compreensão:**
- Por que JWT não precisa de banco de dados para validar?
- O que significa "stateless authentication"?
- Qual é o risco de JWT ser visível no header?

**Respuestas esperadas:**
- Porque JWT é assinado com SECRET_KEY - é verificável
- O servidor não precisa guardar estado/sessão
- Nenhum risco se for HTTPS (criptografado em trânsito)

---

### FASE 3: AUTENTICAÇÃO (20 minutos)

#### 6. Leia: `routers/auth_router.py` - POST /auth/registro
**Tempo:** 10 minutos
**Objetivo:** Entender fluxo completo de registro

```python
# Siga o fluxo:
# 1. Entrada: ClienteRegistro (Pydantic)
# 2. Validação: email único? cpf único?
# 3. Criptografia: obter_hash_senha()
# 4. Salvamento: session.add() + session.commit()
# 5. Token: criar_access_token()
# 6. Retorno: Token response model
```

**Trace o código:**
- De onde vem o endpoint?
- Como Pydantic valida?
- Qual função criptografa?
- Como se salva no banco?
- Como é gerado o token?

---

#### 7. Leia: `routers/auth_router.py` - POST /auth/login
**Tempo:** 5 minutos
**Objetivo:** Entender autenticação

```python
# Siga o fluxo:
# 1. Entrada: Login (email + senha)
# 2. Busca: Cliente no banco por email
# 3. Verificação: verificar_senha()
# 4. Token: criar_access_token()
# 5. Retorno: Token response model
```

**Teste compreensão:**
- O que acontece se email não existe?
- O que acontece se senha está errada?
- Por que retorna erro genérico?

---

#### 8. Leia: `routers/auth_router.py` - GET /auth/me
**Tempo:** 5 minutos
**Objetivo:** Entender endpoints protegidos

```python
# Procure por:
# - email: str = Depends(get_current_user_email)
# - Como o email é extraído
# - Como é usado para buscar usuário
```

**Teste compreensão:**
- Qual é a mágica de `Depends()`?
- O que acontece se token for inválido?
- Como o email chega até a função?

---

### FASE 4: PRODUTOS (15 minutos)

#### 9. Leia: `routers/prod_router.py` - GET endpoints
**Tempo:** 5 minutos
**Objetivo:** Entender endpoints públicos

```python
# Leia:
# - GET /produto/listar_produtos
# - GET /produto/produtos/{id}

# Procure por:
# - Como listar todos?
# - Como buscar por ID?
# - Como tratar erro 404?
```

---

#### 10. Leia: `routers/prod_router.py` - POST, PUT, DELETE
**Tempo:** 10 minutos
**Objetivo:** Entender CRUD protegido

```python
# Siga cada operação:
# - POST: criar novo produto
# - PUT: atualizar (parcial!)
# - DELETE: remover (irreversível!)

# Procure por:
# - Uso de Depends() para proteção
# - Validação com ProdutoBase/ProdutoAtualizar
# - Tratamento de erro 404
```

---

## 🧪 EXERCÍCIOS DE COMPREENSÃO

Depois de ler cada fase, tente responder:

### Fase 1 - Estrutura:
- [ ] Qual é o nome da aplicação FastAPI criada em main.py?
- [ ] Quantos routers existem?
- [ ] Qual router gerencia autenticação?

### Fase 2 - Segurança:
- [ ] Qual algoritmo é usado para criptografar senhas?
- [ ] Qual algoritmo é usado para assinar JWT?
- [ ] Por quanto tempo o token é válido?

### Fase 3 - Autenticação:
- [ ] Como é garantido que um email é único?
- [ ] O que impede alguém de usar outro token?
- [ ] Como se extrai o email do token?

### Fase 4 - Produtos:
- [ ] Qual endpoint pode ser acessado sem token?
- [ ] Como se trata atualização parcial?
- [ ] Qual operação não pode ser desfeita?

---

## 🔍 TÉCNICAS DE LEITURA

### 1. Leia de Cima para Baixo
```
Comece pelo começo do arquivo
    ↓
Entenda a lógica geral
    ↓
Entre em funções específicas
    ↓
Leia os comentários
```

### 2. Trace o Fluxo
```
Entrada (request)
    ↓
Validação (schema)
    ↓
Lógica (função)
    ↓
Banco de dados
    ↓
Saída (response)
```

### 3. Use Find (Ctrl+F)
Procure por:
- `def ` - encontra funções
- `@router.` - encontra endpoints
- `Depends` - encontra proteções
- `raise HTTPException` - encontra erros

### 4. Leia os Comentários Primeiro
Cada arquivo tem comentários explicando:
- O que faz
- Por que faz assim
- Exemplos de uso

---

## 💡 DICAS IMPORTANTES

### ✅ Faça:
- Leia de verdade o código (não só escancar)
- Tente entender o "por quê"
- Teste mudanças pequenas
- Use o Swagger para testar
- Leia os comentários

### ❌ Não faça:
- Não decore o código
- Não tente entender tudo de uma vez
- Não ignore os comentários
- Não pule a documentação
- Não copy-paste sem entender

---

## 🎬 TESTE NA PRÁTICA

Depois de ler, faça isso:

### 1. Execute a Aplicação
```bash
uvicorn main:app --reload
```

### 2. Abra o Swagger
```
http://localhost:8000/docs
```

### 3. Registre um Usuário
- Click em `/auth/registro`
- Click "Try it out"
- Preencha os dados
- Execute

### 4. Copie o Token
Da resposta, copie o `access_token`

### 5. Faça um Teste Autenticado
- Click em "Authorize" (cadeado)
- Cole o token
- Click em outro endpoint protegido
- Execute

**Viu?! Você entendeu o fluxo inteiro! 🎉**

---

## 📊 MAPA MENTAL

```
ENTRADA
  │
  ▼
SCHEMA (Pydantic)
  │ Valida tipo, email, comprimento
  ▼
FUNÇÃO DO ROUTER
  │ - Valida lógica
  │ - Usa config.py (segurança)
  ▼
BANCO DE DADOS
  │ - Salva/busca dados
  ▼
RESPONSE MODEL
  │ - Formata resposta
  ▼
SAÍDA (JSON)
```

---

## 🎓 CONHECIMENTOS ADQUIRIDOS

Depois de ler tudo, você saberá:

✅ Como FastAPI funciona  
✅ Como Pydantic valida dados  
✅ Como SQLAlchemy conecta ao banco  
✅ Como bcrypt criptografa senhas  
✅ Como JWT funciona  
✅ Como Bearer Token funciona  
✅ Como Dependency Injection funciona  
✅ Como CRUD funciona  
✅ Como tratar erros HTTP  
✅ Como estruturar uma API segura  

---

## 🎯 PRÓXIMO PASSO

Depois de ler o código inteiro, você pode:

1. **Modificar e experimentar**
   - Mude alguns campos
   - Adicione novas validações
   - Crie novos endpoints

2. **Escrever testes**
   - Crie testes unitários
   - Teste segurança
   - Teste validações

3. **Deploy**
   - Coloque em produção
   - Monitore segurança
   - Implemente logs

4. **Aprender mais**
   - Leia documentação oficial
   - Estude padrões REST
   - Aprenda DevOps

---

## ❓ SE FICAR COM DÚVIDA

1. **Leia o comentário** no código
2. **Leia a documentação** ([README.md](README.md), [GUIA_ARQUIVOS.md](GUIA_ARQUIVOS.md))
3. **Consulte a referência** ([REFERENCIA_RAPIDA.md](REFERENCIA_RAPIDA.md))
4. **Procure por exemplo** ([TESTES.md](TESTES.md))
5. **Use o debugger** do VS Code

---

**Boa leitura! 📖 Você consegue! 💪**

Tempo total estimado: **1-2 horas** para entender tudo completamente.
