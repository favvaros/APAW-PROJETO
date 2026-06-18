# Sistema de Controle de Faturamento

Trabalho prático desenvolvido para a disciplina de Análise e Projeto de Aplicações Web (APAW). 

## 1. Sobre o Sistema
* **Descrição do sistema:** Uma aplicação web para gestão de clientes e acompanhamento de faturas emitidas.
* **Problema resolvido:** Elimina o controle manual e descentralizado de faturamentos, centralizando o status financeiro (pendente/pago/cancelado) e os dados fiscais em uma única plataforma.
* **Público-alvo:** Pequenas e médias empresas, profissionais autônomos e analistas de faturamento.

## 2. Requisitos
* **Requisitos Funcionais:**
  * Autenticação de usuários (Login/Logout/Registro).
  * CRUD completo de Clientes (Nome, Email, CPF/CNPJ).
  * CRUD completo de Faturas (Cliente, Data, Valor, Status, Observações).
  * Dashboard com indicadores e totalizadores de faturas.
* **Requisitos Não Funcionais:**
  * Interface responsiva utilizando Bootstrap 5.
  * Senha mínima de 8 caracteres para segurança.
  * Validação de dados (ex: valores estritamente positivos).

## 3. Aspectos Técnicos
* **Modelo de Dados:** Entidades relacionais `Cliente` (1) e `Fatura` (N), onde uma fatura pertence obrigatoriamente a um cliente.
* **Arquitetura da Aplicação:** Padrão MVT (Model-View-Template) nativo do framework.
* **Tecnologias Utilizadas:** * Backend: Python 3 com Django
  * Banco de Dados: SQLite
  * Frontend: HTML5, CSS3, JavaScript e Bootstrap 5

## 4. Instruções de Execução (Local)
1. Clone o repositório: `git clone <url-do-repositorio>`
2. Crie um ambiente virtual: `python -m venv venv` e ative-o.
3. Instale as dependências: `pip install -r requirements.txt` (ou instale o Django manualmente).
4. Aplique as migrações: `python manage.py migrate`
5. Inicie o servidor: `python manage.py runserver`
6. Acesse `http://127.0.0.1:8000/` no navegador.