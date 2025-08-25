// Configurações globais
const CONFIG = {
    API_URL: '/consultar',
    CPF_MASK: '000.000.000-00',
    CURRENCY_MASK: '000.000.000,00',
    PERCENTAGE_MASK: '00,00'
};

// Classe principal da aplicação
class PortabilidadeINSS {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupMasks();
    }

    // Inicializar elementos do DOM
    initializeElements() {
        this.form = document.getElementById('formConsulta');
        this.resultsSection = document.getElementById('resultsSection');
        this.loading = document.getElementById('loading');
        this.errorMessages = document.getElementById('errorMessages');
        this.errorList = document.getElementById('errorList');
        this.resultsTable = document.getElementById('resultsTable');
        this.resultsTableBody = document.getElementById('resultsTableBody');
        this.noResults = document.getElementById('noResults');
        this.totalBancos = document.getElementById('totalBancos');
        this.statusConsulta = document.getElementById('statusConsulta');
    }

    // Vincular eventos
    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.form.addEventListener('reset', () => this.handleReset());
        
        // Validação em tempo real
        this.form.querySelectorAll('input, select').forEach(field => {
            field.addEventListener('blur', () => this.validateField(field));
            field.addEventListener('input', () => this.clearFieldError(field));
        });
    }

    // Configurar máscaras de entrada
    setupMasks() {
        // Máscara para CPF
        const cpfField = document.getElementById('cpf');
        if (cpfField) {
            cpfField.addEventListener('input', (e) => this.formatCPF(e.target));
        }

        // Máscaras para campos monetários
        const currencyFields = ['valor_parcela', 'saldo_devedor', 'valor_total'];
        currencyFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', (e) => this.formatCurrency(e.target));
            }
        });

        // Máscara para taxa
        const taxaField = document.getElementById('taxa');
        if (taxaField) {
            taxaField.addEventListener('input', (e) => this.formatPercentage(e.target));
        }
    }

    // Formatar CPF
    formatCPF(field) {
        let value = field.value.replace(/\D/g, '');
        if (value.length > 11) value = value.slice(0, 11);
        
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d)/, '$1.$2');
        value = value.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        
        field.value = value;
    }

    // Formatar campo monetário
    formatCurrency(field) {
        let value = field.value.replace(/\D/g, '');
        if (value.length === 0) {
            field.value = '';
            return;
        }
        
        // Converter para centavos
        value = (parseInt(value) / 100).toFixed(2);
        field.value = value;
    }

    // Formatar campo de porcentagem
    formatPercentage(field) {
        let value = field.value.replace(/[^\d,]/g, '');
        value = value.replace(',', '.');
        
        if (value && !isNaN(value)) {
            const numValue = parseFloat(value);
            if (numValue > 100) {
                field.value = '100.00';
            } else {
                field.value = numValue.toFixed(2);
            }
        }
    }

    // Validar campo individual
    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        
        // Remover classes de erro anteriores
        this.clearFieldError(field);
        
        let isValid = true;
        let errorMessage = '';
        
        switch (fieldName) {
            case 'nome':
                if (value.length < 3) {
                    isValid = false;
                    errorMessage = 'Nome deve ter pelo menos 3 caracteres';
                }
                break;
                
            case 'cpf':
                if (!this.isValidCPF(value)) {
                    isValid = false;
                    errorMessage = 'CPF inválido';
                }
                break;
                
            case 'idade':
                const idade = parseInt(value);
                if (isNaN(idade) || idade < 18 || idade > 120) {
                    isValid = false;
                    errorMessage = 'Idade deve ser entre 18 e 120 anos';
                }
                break;
                
            case 'codigo_beneficio':
                if (value.length === 0) {
                    isValid = false;
                    errorMessage = 'Código do benefício é obrigatório';
                }
                break;
                
            case 'parcelas_pagas':
                const parcelas = parseInt(value);
                if (isNaN(parcelas) || parcelas < 0) {
                    isValid = false;
                    errorMessage = 'Quantidade de parcelas deve ser um número positivo';
                }
                break;
                
            case 'banco_atual':
                if (value === '') {
                    isValid = false;
                    errorMessage = 'Banco atual é obrigatório';
                }
                break;
                
            case 'valor_parcela':
            case 'saldo_devedor':
            case 'valor_total':
                const valor = parseFloat(value);
                if (isNaN(valor) || valor <= 0) {
                    isValid = false;
                    errorMessage = 'Valor deve ser maior que zero';
                }
                break;
                
            case 'taxa':
                const taxa = parseFloat(value);
                if (isNaN(taxa) || taxa < 0 || taxa > 100) {
                    isValid = false;
                    errorMessage = 'Taxa deve ser entre 0 e 100%';
                }
                break;
        }
        
        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.showFieldSuccess(field);
        }
        
        return isValid;
    }

    // Validar CPF
    isValidCPF(cpf) {
        cpf = cpf.replace(/\D/g, '');
        
        if (cpf.length !== 11) return false;
        if (cpf === cpf[0].repeat(11)) return false;
        
        // Validação do primeiro dígito verificador
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf[i]) * (10 - i);
        }
        let remainder = sum % 11;
        let digit1 = remainder < 2 ? 0 : 11 - remainder;
        
        if (parseInt(cpf[9]) !== digit1) return false;
        
        // Validação do segundo dígito verificador
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf[i]) * (11 - i);
        }
        remainder = sum % 11;
        let digit2 = remainder < 2 ? 0 : 11 - remainder;
        
        return parseInt(cpf[10]) === digit2;
    }

    // Mostrar erro no campo
    showFieldError(field, message) {
        field.classList.add('error');
        field.title = message;
        
        // Criar tooltip de erro
        const tooltip = document.createElement('div');
        tooltip.className = 'field-error-tooltip';
        tooltip.textContent = message;
        tooltip.style.cssText = `
            position: absolute;
            background: #e74c3c;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            margin-top: 5px;
        `;
        
        field.parentNode.style.position = 'relative';
        field.parentNode.appendChild(tooltip);
        
        // Remover tooltip após 3 segundos
        setTimeout(() => {
            if (tooltip.parentNode) {
                tooltip.parentNode.removeChild(tooltip);
            }
        }, 3000);
    }

    // Mostrar sucesso no campo
    showFieldSuccess(field) {
        field.classList.add('success');
        setTimeout(() => {
            field.classList.remove('success');
        }, 2000);
    }

    // Limpar erro do campo
    clearFieldError(field) {
        field.classList.remove('error');
        field.title = '';
        
        // Remover tooltip de erro se existir
        const tooltip = field.parentNode.querySelector('.field-error-tooltip');
        if (tooltip) {
            tooltip.remove();
        }
    }

    // Validar formulário completo
    validateForm() {
        const fields = this.form.querySelectorAll('input, select');
        let isValid = true;
        
        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    // Manipular envio do formulário
    async handleSubmit(e) {
        e.preventDefault();
        
        // Validar formulário
        if (!this.validateForm()) {
            this.showError('Por favor, corrija os erros no formulário antes de continuar.');
            return;
        }
        
        // Mostrar loading
        this.showLoading();
        this.hideResults();
        this.hideErrors();
        
        try {
            // Preparar dados do formulário
            const formData = new FormData(this.form);
            const dados = Object.fromEntries(formData.entries());
            
            // Fazer requisição para a API
            const response = await fetch(CONFIG.API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(dados)
            });
            
            const result = await response.json();
            
            if (result.erro) {
                this.showErrors(result.mensagens);
            } else {
                this.showResults(result);
            }
            
        } catch (error) {
            console.error('Erro na consulta:', error);
            this.showError('Erro ao conectar com o servidor. Tente novamente.');
        } finally {
            this.hideLoading();
        }
    }

    // Manipular reset do formulário
    handleReset() {
        this.hideResults();
        this.hideErrors();
        this.clearFieldErrors();
        
        // Limpar tooltips
        document.querySelectorAll('.field-error-tooltip').forEach(tooltip => {
            tooltip.remove();
        });
    }

    // Limpar erros dos campos
    clearFieldErrors() {
        this.form.querySelectorAll('input, select').forEach(field => {
            field.classList.remove('error', 'success');
            field.title = '';
        });
    }

    // Mostrar loading
    showLoading() {
        this.loading.style.display = 'block';
    }

    // Ocultar loading
    hideLoading() {
        this.loading.style.display = 'none';
    }

    // Mostrar resultados
    showResults(data) {
        this.totalBancos.textContent = data.total_bancos;
        this.statusConsulta.textContent = data.total_bancos > 0 ? 'Consulta realizada com sucesso' : 'Nenhum banco encontrado';
        
        if (data.total_bancos > 0) {
            this.populateResultsTable(data.resultados);
            this.resultsSection.style.display = 'block';
            this.noResults.style.display = 'none';
        } else {
            this.noResults.style.display = 'block';
            this.resultsSection.style.display = 'block';
        }
        
        // Scroll para resultados
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Ocultar resultados
    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    // Preencher tabela de resultados
    populateResultsTable(resultados) {
        this.resultsTableBody.innerHTML = '';
        
        resultados.forEach(resultado => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${resultado.banco}</strong></td>
                <td><span class="operation-type">${resultado.tipo_operacao}</span></td>
                <td><span class="taxa-value">${resultado.taxa_aplicavel.toFixed(2)}%</span></td>
                <td>${resultado.observacoes}</td>
            `;
            this.resultsTableBody.appendChild(row);
        });
    }

    // Mostrar erros
    showErrors(mensagens) {
        this.errorList.innerHTML = '';
        
        mensagens.forEach(mensagem => {
            const li = document.createElement('li');
            li.textContent = mensagem;
            this.errorList.appendChild(li);
        });
        
        this.errorMessages.style.display = 'block';
        this.errorMessages.scrollIntoView({ behavior: 'smooth' });
    }

    // Mostrar erro único
    showError(mensagem) {
        this.showErrors([mensagem]);
    }

    // Ocultar erros
    hideErrors() {
        this.errorMessages.style.display = 'none';
    }

    // Exportar resultados para CSV
    exportToCSV() {
        const table = this.resultsTable;
        const rows = table.querySelectorAll('tr');
        
        let csv = [];
        rows.forEach(row => {
            const cols = row.querySelectorAll('td, th');
            const rowData = [];
            cols.forEach(col => {
                rowData.push(`"${col.textContent.trim()}"`);
            });
            csv.push(rowData.join(','));
        });
        
        const csvContent = csv.join('\n');
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', 'portabilidade_inss.csv');
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

// Inicializar aplicação quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new PortabilidadeINSS();
    
    // Adicionar botão de exportar CSV se houver resultados
    const exportButton = document.createElement('button');
    exportButton.className = 'btn-exportar';
    exportButton.innerHTML = '📊 Exportar CSV';
    exportButton.style.cssText = `
        background: linear-gradient(135deg, #9b59b6, #8e44ad);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 20px;
        font-weight: 600;
    `;
    
    exportButton.addEventListener('click', () => {
        const app = window.portabilidadeApp;
        if (app) {
            app.exportToCSV();
        }
    });
    
    // Adicionar botão após a tabela de resultados
    const resultsSection = document.querySelector('.results-section');
    if (resultsSection) {
        resultsSection.appendChild(exportButton);
    }
});

// Utilitários adicionais
window.utils = {
    // Formatar número para moeda brasileira
    formatCurrency: (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },
    
    // Formatar número para porcentagem
    formatPercentage: (value) => {
        return `${value.toFixed(2)}%`;
    },
    
    // Validar se é um número válido
    isValidNumber: (value) => {
        return !isNaN(value) && isFinite(value);
    },
    
    // Debounce para otimizar validações
    debounce: (func, wait) => {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};
