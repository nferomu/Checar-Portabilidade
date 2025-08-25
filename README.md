# 🏦 Sistema de Consulta de Portabilidade INSS - ConsigaCred

Sistema web desenvolvido em Python (Flask) para consulta de portabilidade de empréstimos consignados do INSS, baseado nas regras de negócio específicas do setor.

## ✨ Funcionalidades

- **Formulário completo** para coleta de dados do cliente
- **Validação em tempo real** de todos os campos
- **Consulta automática** de portabilidade baseada em regras de negócio
- **Resultados detalhados** com tabela de bancos elegíveis
- **Interface responsiva** e moderna
- **Exportação para CSV** dos resultados
- **Validação de CPF** com algoritmo oficial
- **Máscaras de entrada** para melhor experiência do usuário

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. **Clone ou baixe o projeto**
   ```bash
   git clone <url-do-repositorio>
   cd ConsigaCred
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # No Windows
   venv\Scripts\activate
   
   # No Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Como usar

### 1. Iniciar o servidor
```bash
python app.py
```

### 2. Acessar a aplicação
Abra seu navegador e acesse: `http://localhost:5000`

### 3. Preencher o formulário
- **Nome**: Nome completo do cliente
- **CPF**: CPF válido (formato automático: 000.000.000-00)
- **Idade**: Idade entre 18 e 120 anos
- **Código do Benefício**: Código do benefício INSS
- **Parcelas Pagas**: Quantidade de parcelas já pagas
- **Banco Atual**: Banco onde está o empréstimo atual
- **Valor da Parcela**: Valor da parcela mensal
- **Saldo Devedor**: Saldo restante do empréstimo
- **Valor Total**: Valor total do empréstimo
- **Taxa**: Taxa de juros atual (%)

### 4. Consultar portabilidade
Clique no botão **"Consultar Portabilidade"** para processar a consulta.

### 5. Visualizar resultados
O sistema retornará uma tabela com:
- Bancos elegíveis para portabilidade
- Tipo de operação (Portabilidade ou Port+Refin)
- Taxa aplicável
- Observações específicas

## 📋 Regras de Negócio Implementadas

### Critérios Gerais
- **Idade máxima**: 85 anos
- **Parcelas mínimas**: 12 parcelas (6 para invalidez)
- **Saldo mínimo**: R$ 500,00
- **Troco mínimo**: R$ 100,00

### Bancos Bloqueados
- **BRB**: Não aceita portabilidade

### Regras Específicas por Banco
- **Bradesco e Itaú**: Mínimo de 15 parcelas pagas
- **Demais bancos**: Mínimo de 12 parcelas pagas
- **Benefícios por invalidez**: Regras especiais aplicadas

### Cálculo de Taxa
- Taxa base: 2,49% ao mês
- Ajuste baseado na taxa atual do cliente
- Limite máximo: 2,99% ao mês

## 🏗️ Estrutura do Projeto

```
ConsigaCred/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── templates/            # Templates HTML
│   └── index.html       # Página principal
└── static/              # Arquivos estáticos
    ├── style.css        # Estilos CSS
    └── script.js        # JavaScript da aplicação
```

## 🔧 Configuração e Personalização

### Adicionar Novos Bancos
Edite o arquivo `app.py` e adicione novos bancos na lista `self.bancos` da classe `RegrasPortabilidadeINSS`.

### Modificar Regras de Negócio
As regras estão centralizadas na classe `RegrasPortabilidadeINSS`. Para alterar:
- Limites de idade
- Quantidade de parcelas mínimas
- Taxas aplicáveis
- Critérios específicos por banco

### Personalizar Interface
- **CSS**: Edite `static/style.css`
- **JavaScript**: Edite `static/script.js`
- **HTML**: Edite `templates/index.html`

## 🧪 Testando o Sistema

### Dados de Exemplo
```
Nome: João Silva
CPF: 123.456.789-00
Idade: 65
Código do Benefício: 123456789
Parcelas Pagas: 18
Banco Atual: Banco do Brasil
Valor da Parcela: 150.00
Saldo Devedor: 5000.00
Valor Total: 8000.00
Taxa: 2.49
```

### Resultado Esperado
O sistema deve retornar uma lista de bancos elegíveis para portabilidade, considerando as regras implementadas.

## 🚨 Solução de Problemas

### Erro de Porta em Uso
Se a porta 5000 estiver ocupada, altere no arquivo `app.py`:
```python
app.run(debug=True, port=5001)
```

### Problemas de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Erro de Template não Encontrado
Verifique se a estrutura de pastas está correta:
- `templates/` deve estar no mesmo nível de `app.py`
- `static/` deve estar no mesmo nível de `app.py`

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (até 767px)

## 🔒 Segurança

- Validação de entrada em todos os campos
- Sanitização de dados
- Validação de CPF com algoritmo oficial
- Proteção contra XSS básica

## 🚀 Deploy em Produção

Para produção, recomenda-se:
- Usar WSGI server (Gunicorn, uWSGI)
- Configurar proxy reverso (Nginx, Apache)
- Implementar HTTPS
- Configurar variáveis de ambiente
- Desabilitar modo debug

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Consulte os comentários no código
3. Verifique os logs do console
4. Abra uma issue no repositório

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e comerciais. Consulte as licenças das dependências utilizadas.

---

**Desenvolvido com ❤️ para ConsigaCred**
