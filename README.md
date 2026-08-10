# CanonForge

> **Evidence-driven research, knowledge extraction and learning for fictional universes.**

CanonForge é uma plataforma open-source projetada para investigar profundamente uma obra ficcional, construir uma base de conhecimento estruturada e rastreável e transformar essa informação em um sistema de aprendizagem.

Seu objetivo não é simplesmente responder:

> "O que acontece nessa obra?"

O objetivo é responder:

> **"O que sabemos, de onde sabemos, por que consideramos isso verdadeiro e quão confiável é essa conclusão?"**

---

## 🎯 Visão

Obras como animes, mangás, novels, jogos e universos compartilhados podem possuir:

* centenas ou milhares de capítulos;
* múltiplas adaptações;
* databooks e materiais complementares;
* entrevistas;
* traduções diferentes;
* retcons;
* informações contraditórias;
* teorias;
* interpretações;
* fanon;
* enormes quantidades de conteúdo produzido pela comunidade.

Isso cria um problema:

**quanto mais informação existe, mais difícil se torna distinguir conhecimento verdadeiro de informação repetida, interpretada ou inventada pelo fandom.**

O CanonForge pretende resolver esse problema através de uma combinação de:

* pesquisa automatizada;
* fontes rastreáveis;
* extração de afirmações;
* validação de evidências;
* classificação de continuidade;
* detecção de contradições;
* construção de conhecimento estruturado;
* análise narrativa;
* treinamento adaptativo.

---

# 🧠 Princípio Central

CanonForge segue uma regra fundamental:

> **Uma afirmação não deve ser considerada verdadeira apenas porque uma IA a conhece. Ela deve possuir evidência rastreável.**

Portanto:

```text
Informação
    ↓
Afirmação (Claim)
    ↓
Fonte
    ↓
Evidência
    ↓
Validação
    ↓
Classificação
    ↓
Conhecimento
```

A quantidade de sites repetindo uma informação não determina sua veracidade.

> **50 fontes copiando a mesma afirmação continuam podendo representar apenas uma única origem.**

CanonForge procura rastrear essa origem.

---

# 🔎 O Problema Canon ≠ Fanon

CanonForge não utiliza apenas duas categorias.

O sistema trabalha com uma taxonomia mais detalhada:

```text
CANON
├── Primário
├── Complementar
├── Adaptação
└── Ambíguo

INTERPRETAÇÃO
├── Fortemente sustentada
├── Plausível
└── Especulativa

FANDOM
├── Teoria
├── Headcanon
└── Fanon

NÃO CONFIRMADO

CONTRADITÓRIO

DESMENTIDO
```

Isso permite representar situações complexas sem forçar uma informação para dentro de apenas "verdadeiro" ou "falso".

---

# 🏗️ Arquitetura Conceitual

```text
                         ┌──────────────────┐
                         │      OBRA        │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ IDENTIFICAÇÃO    │
                         │ obra / versão /  │
                         │ continuidade     │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │    RESEARCHER    │
                         │ coleta fontes    │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ CLAIM EXTRACTOR  │
                         │ extrai afirmações│
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ EVIDENCE ENGINE  │
                         │ procura provas   │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │    VALIDATOR     │
                         │ verifica contexto│
                         └────────┬─────────┘
                                  ↓
                    ┌─────────────┴─────────────┐
                    ↓                           ↓
             ┌──────────────┐           ┌──────────────┐
             │ CLASSIFIER   │           │ CONTRADICTION│
             │ canon/fanon  │           │   DETECTOR   │
             └──────┬───────┘           └──────┬───────┘
                    └─────────────┬─────────────┘
                                  ↓
                         ┌──────────────────┐
                         │ KNOWLEDGE GRAPH  │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │  DOSSIER ENGINE  │
                         └────────┬─────────┘
                                  ↓
                    ┌─────────────┴─────────────┐
                    ↓                           ↓
             ┌──────────────┐           ┌──────────────┐
             │  ANALYSIS    │           │   LEARNING   │
             │ lore/themes  │           │    ENGINE    │
             └──────────────┘           └──────┬───────┘
                                               ↓
                                      ┌──────────────────┐
                                      │ EXAM / PROGRESS  │
                                      └──────────────────┘
```

---

# 🤖 Agentes

O sistema será modular.

## Researcher

Responsável pela descoberta de informações.

Pesquisa:

* fontes primárias;
* fontes oficiais;
* entrevistas;
* materiais complementares;
* wikis;
* artigos;
* comunidades;
* discussões.

O Researcher **não determina sozinho o canon**.

---

## Claim Extractor

Transforma documentos em afirmações verificáveis.

Exemplo:

```text
Fonte:
Jujutsu Kaisen — Capítulo X

Claim:
"Gojo possui os Six Eyes."

Contexto:
[...]

Localização:
[...]

Fonte primária:
true
```

---

## Evidence Engine

Procura evidências que sustentem ou contradigam uma Claim.

```text
CLAIM
  ↓
Evidence A
Evidence B
Evidence C
  ↓
Support / Contradiction
```

---

## Validator

Verifica se a fonte realmente sustenta a afirmação.

Pergunta:

> "A fonte diz isso ou estamos interpretando a fonte?"

Essa distinção é fundamental.

---

## Canon Classifier

Determina o status da informação considerando:

* tipo da fonte;
* continuidade;
* contexto;
* autoridade;
* evidência;
* contradições;
* material posterior;
* adaptação;
* intenção editorial quando verificável.

---

## Contradiction Detector

Procura conflitos entre informações.

Exemplo:

```text
CLAIM A
Databook:
"X nasceu em 1980."

CLAIM B
Mangá:
"X nasceu em 1982."

↓

CONTRADICTION

Mangá:
fonte primária

Databook:
fonte complementar

↓

Conclusão:
1982 possui prioridade para a continuidade principal.
```

O sistema não deve simplesmente apagar uma das informações.

Ele deve **preservar o conflito e explicar sua resolução**.

---

# 📚 Knowledge Graph

As informações não devem existir apenas como texto.

CanonForge pretende representar relações:

```text
        Gojo
         │
         ├── possui → Six Eyes
         │
         ├── utiliza → Limitless
         │
         ├── pertence → Jujutsu Society
         │
         ├── conhece → Geto
         │
         └── enfrenta → Sukuna
```

Isso permite investigar perguntas complexas:

* Quem conhece determinado personagem?
* Quais eventos levaram a outro evento?
* Quais poderes possuem determinada propriedade?
* Quais personagens participaram de determinada guerra?
* Quais informações possuem a mesma fonte?
* Quais teorias dependem de determinada premissa?

---

# 🗓️ Timeline Engine

O sistema também constrói cronologias.

```text
Evento A
   ↓
Evento B
   ↓
Evento C
   ↓
Evento D
```

Mas não apenas uma lista temporal.

Quando possível, registra:

```text
EVENTO

Data:
...

Local:
...

Participantes:
...

Causa:
...

Consequência:
...

Fontes:
...

Canon:
...

Confiança:
...
```

Isso permite construir uma **timeline causal**, não apenas cronológica.

---

# 🔬 Analysis Engine

Depois que os fatos são consolidados, o sistema pode analisar:

### Lore

* história do mundo;
* política;
* religiões;
* culturas;
* organizações;
* geografia;
* sistemas de poder.

### Personagens

* objetivos;
* desenvolvimento;
* relações;
* conflitos;
* decisões;
* arcos narrativos.

### Narrativa

* temas;
* simbolismos;
* foreshadowing;
* paralelos;
* estrutura;
* construção de mundo.

### Produção

* autor;
* estúdio;
* adaptação;
* mudanças;
* entrevistas;
* decisões editoriais.

Importante:

> **Análise não deve ser confundida com canon.**

Uma interpretação excelente continua sendo uma interpretação.

---

# ⚠️ Controle de Incerteza

CanonForge nunca deve transformar incerteza em certeza artificial.

Exemplos:

```text
CANON CONFIRMADO
████████████████████ 100%
```

```text
FORTEMENTE SUSTENTADO
██████████████████░░ 90%
```

```text
PLAUSÍVEL
██████████████░░░░░░ 70%
```

```text
ESPECULATIVO
████████░░░░░░░░░░░░ 40%
```

```text
NÃO CONFIRMADO
░░░░░░░░░░░░░░░░░░░░ 0%
```

A pontuação representa **confiança da evidência**, não "probabilidade de uma teoria virar canon".

---

# 🚫 Ausência de Evidência

Uma regra importante:

```text
"Não encontramos evidência de X."
```

não significa:

```text
"X é falso."
```

Portanto:

```text
FALSO
≠
NÃO CONFIRMADO
```

CanonForge deve preservar essa distinção.

---

# 🔗 Rastreamento de Origem

Uma informação pode aparecer em centenas de lugares.

O sistema deve tentar descobrir:

```text
YouTube
   ↓
Reddit
   ↓
Wiki
   ↓
Blog
   ↓
Entrevista
   ↓
Fonte primária
```

Isso evita:

> **contagem falsa de evidências.**

Dez páginas copiando uma informação não equivalem a dez fontes independentes.

---

# 📖 Dossiê Automático

Ao finalizar uma investigação, o sistema pode gerar uma estrutura como:

```text
WORK DOSSIER

00 — Overview
01 — Canon & Continuities
02 — Timeline
03 — World
04 — Geography
05 — Factions
06 — Characters
07 — Relationships
08 — Power Systems
09 — Events
10 — Mysteries
11 — Foreshadowing
12 — Themes
13 — Symbolism
14 — Production
15 — Adaptations
16 — Supplementary Material
17 — Contradictions
18 — Theories
19 — Fandom Claims
20 — Debunked Claims
21 — Glossary
22 — Sources
```

---

# 🧑‍🏫 Learning Engine

O conhecimento coletado não serve apenas para consulta.

CanonForge também pode ensinar o usuário.

### Níveis

```text
NOVATO
↓
CONHECEDOR
↓
FÃ INFORMADO
↓
ESPECIALISTA
↓
ANALISTA
↓
GURU
```

O sistema gera perguntas baseadas na própria Knowledge Base.

### Memória

> Quem é X?

### Compreensão

> Por que X tomou essa decisão?

### Relação

> Como X influencia Y?

### Aplicação

> Como a habilidade X funciona sob determinada condição?

### Análise

> Qual evidência sustenta essa interpretação?

### Investigação

> A afirmação X é realmente canon?

### Guru

> Compare as evidências conflitantes e determine qual interpretação possui maior suporte.

---

# 📊 Avaliação

O sistema acompanha:

```text
Memória
████████████████░░░░

Compreensão
██████████████████░░

Lore
██████████████░░░░░░

Cronologia
████████████████░░░░

Análise
███████████████████░

Precisão
█████████████████░░░
```

E utiliza os erros para determinar o que revisar.

---

# 🔁 Pipeline Completo

```text
INPUT
  ↓
IDENTIFY
  ↓
DISCOVER SOURCES
  ↓
COLLECT
  ↓
EXTRACT CLAIMS
  ↓
TRACE ORIGINS
  ↓
GATHER EVIDENCE
  ↓
VALIDATE
  ↓
CLASSIFY
  ↓
DETECT CONTRADICTIONS
  ↓
BUILD KNOWLEDGE GRAPH
  ↓
BUILD TIMELINE
  ↓
ANALYZE
  ↓
GENERATE DOSSIER
  ↓
GENERATE STUDY MATERIAL
  ↓
TEST USER
  ↓
IDENTIFY KNOWLEDGE GAPS
  ↓
TARGETED REVIEW
  ↓
REASSESS
```

O sistema deve poder retornar ao estágio de pesquisa quando detectar lacunas importantes.

---

# 🧱 Filosofia de Desenvolvimento

CanonForge deve seguir alguns princípios:

### 1. Evidence First

Informações importantes precisam de evidências.

### 2. Source Traceability

Toda informação deve ser rastreável à sua origem.

### 3. Uncertainty Preservation

Incerteza nunca deve ser escondida.

### 4. Canon Separation

Canon, interpretação e fandom devem permanecer separados.

### 5. No Hallucinated Lore

A IA não deve inventar informações para preencher lacunas.

### 6. Contradictions Are Data

Contradições não devem ser apagadas.

### 7. Provider Agnostic

O sistema não deve depender de um único provedor de IA.

### 8. Modular Architecture

Cada componente deve poder evoluir independentemente.

### 9. Human Verifiability

O usuário deve conseguir verificar conclusões importantes.

### 10. Reproducible Research

Uma investigação deve poder ser repetida e atualizada.

---

# 🛠️ Stack Inicial

A stack definitiva ainda será definida durante a implementação.

Uma possibilidade:

```text
Frontend
└── React / Next.js

Backend
└── Python / FastAPI

AI Layer
└── Provider abstraction

Database
└── PostgreSQL

Knowledge Graph
└── PostgreSQL + graph representation
   ou Neo4j futuramente

Search
└── Web search abstraction

Vector Search
└── pgvector

Validation
└── Pydantic / JSON Schema

Testing
└── Pytest

CI/CD
└── GitHub Actions
```

A arquitetura deve permitir substituir componentes sem reescrever o sistema inteiro.

---

# 🔐 Segurança

Chaves de API nunca devem ser armazenadas no repositório.

```text
.env
```

deve permanecer fora do Git.

Para ambientes automatizados:

```text
GitHub Secrets
```

deve ser utilizado.

O repositório deve incluir um `.gitignore` apropriado desde o início.

---

# 🌐 Open Source

O objetivo é permitir que a comunidade contribua com:

* novos agentes;
* novos providers;
* novos conectores;
* novas fontes;
* novos classificadores;
* novos formatos de exportação;
* novas estratégias de validação;
* melhorias na Knowledge Base;
* ferramentas de aprendizagem.

---

# 🚧 Roadmap

## v0.1 — Foundation

* [x] Estrutura inicial do projeto
* [x] Configuração de providers
* [x] Modelo de Work
* [x] Modelo de Source
* [x] Modelo de Claim
* [x] Modelo de Evidence
* [x] Sistema básico de classificação
* [x] CLI inicial

## v0.2 — Research

* [ ] Pesquisa automatizada
* [ ] Coleta de fontes
* [ ] Extração de Claims
* [ ] Rastreamento de origem
* [ ] Validação básica

## v0.3 — Knowledge

* [ ] Personagens
* [ ] Eventos
* [ ] Relações
* [ ] Facções
* [ ] Localidades
* [ ] Timeline
* [ ] Knowledge Graph

## v0.4 — Verification

* [ ] Contradiction Engine
* [ ] Confidence system
* [ ] Source hierarchy
* [ ] Canon classifier
* [ ] Evidence chains

## v0.5 — Analysis

* [ ] Lore analysis
* [ ] Character analysis
* [ ] Narrative analysis
* [ ] Themes
* [ ] Symbolism
* [ ] Foreshadowing

## v0.6 — Learning

* [ ] Quiz generator
* [ ] Adaptive difficulty
* [ ] Knowledge tracking
* [ ] Spaced review
* [ ] Weakness detection

## v1.0 — CanonForge

* [ ] Interface web
* [ ] Full research pipeline
* [ ] Knowledge Base
* [ ] Evidence system
* [ ] Learning Engine
* [ ] Exportação de dossiês
* [ ] Multi-provider
* [ ] Documentação completa

---

# 🎯 Long-Term Vision

O objetivo final do CanonForge é permitir:

```text
"Investigue esta obra."
```

e produzir:

```text
                 CANONFORGE
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
     KNOWLEDGE                EVIDENCE
          │                       │
          └───────────┬───────────┘
                      ↓
                  ANALYSIS
                      ↓
                  DOSSIER
                      ↓
                  LEARNING
                      ↓
                  MASTERY
```

Não apenas uma resposta.

Não apenas um resumo.

Não apenas uma wiki.

Mas uma **infraestrutura de conhecimento verificável para universos ficcionais**.

---

# 📜 Status

**Projeto:** CanonForge
**Status:** 🟢 v0.1 Foundation — Concluído | 🟡 v0.2 Research — Em planejamento
**Versão:** 0.1.0

> The goal is not to know everything.
>
> **The goal is to know what is known, why it is known, where it came from, and what remains uncertain.**
