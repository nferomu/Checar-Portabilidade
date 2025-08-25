#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arquivo de configuração do sistema de portabilidade INSS
Centraliza todos os parâmetros e configurações do sistema
"""

# Configurações da aplicação Flask
FLASK_CONFIG = {
    'DEBUG': True,
    'HOST': '0.0.0.0',
    'PORT': 5000,
    'SECRET_KEY': 'consigacred-portabilidade-inss-2025'
}

# Configurações de regras de negócio
REGRAS_NEGOCIO = {
    # Limites gerais
    'IDADE_LIMITE': 85,
    'IDADE_MINIMA': 18,
    'IDADE_MAXIMA': 120,
    
    # Parcelas mínimas
    'PARCELAS_MINIMAS': {
        'GERAL': 12,
        'INVALIDEZ': 6
    },
    
    # Valores mínimos
    'SALDO_MINIMO': 500.00,
    'TROCO_MINIMO': 100.00,
    'TAXA_MAXIMA': 2.99,
    'TAXA_PADRAO': 2.49
}

# Configurações de bancos
BANCOS_CONFIG = {
    # Bancos que não aceitam portabilidade
    'BLOQUEADOS': ['BRB'],
    
    # Regras específicas por banco
    'REGRAS_ESPECIFICAS': {
        'Banco do Brasil': {
            'idade_maxima': 85,
            'parcelas_minimas': 12,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Banco público com regras flexíveis'
        },
        'Caixa Econômica Federal': {
            'idade_maxima': 85,
            'parcelas_minimas': 12,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Banco público com regras flexíveis'
        },
        'Bradesco': {
            'idade_maxima': 85,
            'parcelas_minimas': 15,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Banco privado com regras mais rigorosas'
        },
        'Itaú': {
            'idade_maxima': 85,
            'parcelas_minimas': 15,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Banco privado com regras mais rigorosas'
        },
        'Santander': {
            'idade_maxima': 85,
            'parcelas_minimas': 12,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Banco privado com regras intermediárias'
        },
        'Banrisul': {
            'idade_maxima': 85,
            'parcelas_minimas': 12,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Banco estadual do RS'
        },
        'Sicredi': {
            'idade_maxima': 85,
            'parcelas_minimas': 12,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Cooperativa de crédito'
        },
        'Sicoob': {
            'idade_maxima': 85,
            'parcelas_minimas': 12,
            'aceita_invalidez': True,
            'taxa_padrao': 2.49,
            'observacoes': 'Cooperativa de crédito'
        }
    }
}

# Configurações de validação
VALIDACAO_CONFIG = {
    'CPF': {
        'min_length': 11,
        'max_length': 14,
        'pattern': r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    },
    'NOME': {
        'min_length': 3,
        'max_length': 100
    },
    'IDADE': {
        'min': 18,
        'max': 120
    },
    'CODIGO_BENEFICIO': {
        'min_length': 1,
        'max_length': 50
    },
    'PARCELAS_PAGAS': {
        'min': 0,
        'max': 999
    },
    'VALORES': {
        'min': 0.01,
        'max': 999999.99,
        'decimals': 2
    },
    'TAXA': {
        'min': 0.00,
        'max': 100.00,
        'decimals': 2
    }
}

# Configurações de interface
UI_CONFIG = {
    'TITULO': 'Consulta de Portabilidade INSS - ConsigaCred',
    'DESCRICAO': 'Sistema de consulta para empréstimos consignados do INSS',
    'EMPRESA': 'ConsigaCred',
    'ANO': '2025',
    'VERSION': '1.0.0',
    
    # Cores do tema
    'CORES': {
        'PRIMARIA': '#3498db',
        'SECUNDARIA': '#2ecc71',
        'SUCESSO': '#27ae60',
        'ERRO': '#e74c3c',
        'AVISO': '#f39c12',
        'INFO': '#9b59b6'
    }
}

# Configurações de exportação
EXPORT_CONFIG = {
    'CSV': {
        'encoding': 'utf-8',
        'delimiter': ',',
        'filename_prefix': 'portabilidade_inss_',
        'date_format': '%Y%m%d_%H%M%S'
    },
    'EXCEL': {
        'sheet_name': 'Portabilidade INSS',
        'filename_prefix': 'portabilidade_inss_',
        'date_format': '%Y%m%d_%H%M%S'
    }
}

# Configurações de log
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'portabilidade_inss.log',
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Configurações de cache
CACHE_CONFIG = {
    'enabled': True,
    'ttl': 300,  # 5 minutos
    'max_size': 1000
}

# Configurações de segurança
SECURITY_CONFIG = {
    'rate_limit': {
        'enabled': True,
        'max_requests': 100,
        'window': 3600  # 1 hora
    },
    'input_sanitization': True,
    'xss_protection': True,
    'csrf_protection': False  # Desabilitado para simplicidade
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'max_concurrent_requests': 10,
    'request_timeout': 30,  # segundos
    'enable_compression': True,
    'enable_caching': True
}

# Função para obter configuração completa
def get_config():
    """Retorna todas as configurações do sistema"""
    return {
        'flask': FLASK_CONFIG,
        'regras': REGRAS_NEGOCIO,
        'bancos': BANCOS_CONFIG,
        'validacao': VALIDACAO_CONFIG,
        'ui': UI_CONFIG,
        'export': EXPORT_CONFIG,
        'log': LOG_CONFIG,
        'cache': CACHE_CONFIG,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG
    }

# Função para obter configuração específica
def get_config_section(section):
    """Retorna configuração de uma seção específica"""
    config = get_config()
    return config.get(section, {})

# Função para validar configurações
def validate_config():
    """Valida se todas as configurações estão corretas"""
    errors = []
    
    # Validar regras de negócio
    if REGRAS_NEGOCIO['IDADE_LIMITE'] <= 0:
        errors.append("IDADE_LIMITE deve ser maior que zero")
    
    if REGRAS_NEGOCIO['SALDO_MINIMO'] <= 0:
        errors.append("SALDO_MINIMO deve ser maior que zero")
    
    if REGRAS_NEGOCIO['TAXA_MAXIMA'] <= 0:
        errors.append("TAXA_MAXIMA deve ser maior que zero")
    
    # Validar configurações Flask
    if FLASK_CONFIG['PORT'] < 1 or FLASK_CONFIG['PORT'] > 65535:
        errors.append("PORT deve estar entre 1 e 65535")
    
    return errors

if __name__ == "__main__":
    # Testar configurações
    print("🔧 Testando configurações do sistema...")
    
    errors = validate_config()
    if errors:
        print("❌ Erros encontrados:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Todas as configurações estão válidas!")
    
    # Mostrar configurações principais
    print(f"\n📋 Configurações principais:")
    print(f"   - Porta: {FLASK_CONFIG['PORT']}")
    print(f"   - Idade limite: {REGRAS_NEGOCIO['IDADE_LIMITE']} anos")
    print(f"   - Saldo mínimo: R$ {REGRAS_NEGOCIO['SALDO_MINIMO']:.2f}")
    print(f"   - Taxa máxima: {REGRAS_NEGOCIO['TAXA_MAXIMA']}%")
    print(f"   - Bancos bloqueados: {', '.join(BANCOS_CONFIG['BLOQUEADOS'])}")
