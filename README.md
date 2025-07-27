# 📄 Automação de Processos Documentais

Este projeto oferece uma solução automatizada e robusta para o processamento, validação e organização de documentos financeiros — com foco especial em informações relacionadas a **gravames de veículos**. Desenvolvido em **Python**, o sistema é ideal para manipular grandes volumes de dados estruturados e não estruturados, otimizando fluxos operacionais com **precisão, agilidade e confiabilidade**.

---

## 🚀 Como Começar

### ✅ Pré-requisitos

- Python 3.x instalado.
- Git (opcional, mas recomendado).
- Acesso à internet para instalação de dependências.

### 📥 Instalação

1. **Clone este repositório**
2. **Crie um ambiente virtual e ative-o:**

python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

3. **Instale as dependências:**
pip install -r requirements.txt

4. **Configuração do ambiente:**

Crie um arquivo .env na raiz do projeto com as variáveis necessárias:

TEAMS_WEBHOOK_LOG="SUA_URL_DO_WEBHOOK_DO_TEAMS"

## ⚙️ Uso

Coloque os arquivos .txt e .pdf a serem processados no diretório configurado (ex: ~/Downloads/pasta_designada).
Para iniciar o processamento:
python main.py

## ✨ Funcionalidades

📁 Monitoramento Inteligente de Diretórios
Detecta automaticamente arquivos .txt e .pdf, classificando e descartando arquivos irrelevantes.

🔍 Extração de Dados Estruturados
Captura informações financeiras e operacionais cruciais, como chassi, número de operação, juros e valores.

🛡️ Validação Avançada de Dados
Garante que todos os dados extraídos estejam completos e consistentes antes do próximo passo.

📎 Associação Inteligente de PDFs
Localiza e associa arquivos PDF a partir dos identificadores extraídos dos .txt.

📏 Verificação de Tamanho de Arquivo
Sinaliza automaticamente PDFs que ultrapassam o limite estabelecido.

📂 Organização Automatizada
Move e renomeia arquivos com base em identificadores únicos da operação, mantendo tudo organizado.

🧾 Exportação de Dados Estruturada
Gera arquivos .json com os dados extraídos para facilitar análises posteriores.

## 🚨 Tratamento de Erros e Notificações

Detecção de Erros Comuns
Falhas como dados ausentes, PDFs não localizados ou arquivos grandes são identificadas automaticamente.

Isolamento de Arquivos Inválidos
Arquivos problemáticos são movidos para a pasta "Lixo", sem afetar o restante do fluxo.

Alertas em Tempo Real
Notificações detalhadas são enviadas para o Microsoft Teams via Webhook para rápida ação da equipe.

## 🗂️ Estrutura do Projeto

Processamento_e_organizacao_de_documentos/

├── main.py # Arquivo principal de execução

├── core/ # Lógica principal de processamento

├── models/ # Módulos de extração, validação e organização

├── utils/ # Utilitários, incluindo envio de notificações

├── Docs/ # Documentação de regras e processos

└── .env # Variáveis de ambiente (não versionado)

## 🤝 Contribuindo

Contribuições são muito bem-vindas!

Abra uma issue para relatar bugs ou sugerir melhorias.

Envie um pull request com suas sugestões ou novas funcionalidades.

## 📬 Contato

Se tiver dúvidas ou quiser conversar sobre o projeto, fique à vontade para entrar em contato por meio das issues ou via LinkedIn.
