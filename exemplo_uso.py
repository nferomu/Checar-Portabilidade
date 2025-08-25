#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso do sistema de portabilidade INSS
Este arquivo demonstra como usar as regras de portabilidade programaticamente
"""

from app import RegrasPortabilidadeINSS

def exemplo_consulta_portabilidade():
    """Exemplo de como usar o sistema de portabilidade"""
    
    # Criar instância das regras
    regras = RegrasPortabilidadeINSS()
    
    # Dados de exemplo de um cliente
    dados_cliente = {
        'nome': 'João Silva',
        'cpf': '12345678900',
        'idade': '65',
        'codigo_beneficio': '123456789',
        'parcelas_pagas': '18',
        'banco_atual': 'Banco do Brasil',
        'valor_parcela': '150.00',
        'saldo_devedor': '5000.00',
        'valor_total': '8000.00',
        'taxa': '2.49'
    }
    
    print("🏦 Sistema de Consulta de Portabilidade INSS - ConsigaCred")
    print("=" * 60)
    
    # Validar dados
    print("\n📋 Validando dados do cliente...")
    erros = regras.validar_dados(dados_cliente)
    
    if erros:
        print("❌ Erros encontrados:")
        for erro in erros:
            print(f"   - {erro}")
        return
    
    print("✅ Dados válidos!")
    
    # Consultar portabilidade
    print("\n🔍 Consultando portabilidade...")
    resultados = regras.consultar_portabilidade(dados_cliente)
    
    # Exibir resultados
    print(f"\n📊 Resultados da consulta:")
    print(f"Total de bancos elegíveis: {len(resultados)}")
    print("-" * 60)
    
    if resultados:
        for i, resultado in enumerate(resultados, 1):
            print(f"\n{i}. {resultado['banco']}")
            print(f"   Tipo de Operação: {resultado['tipo_operacao']}")
            print(f"   Taxa Aplicável: {resultado['taxa_aplicavel']:.2f}%")
            print(f"   Observações: {resultado['observacoes']}")
    else:
        print("❌ Nenhum banco atende aos critérios de portabilidade")
    
    print("\n" + "=" * 60)
    print("✅ Consulta concluída!")

def exemplo_diferentes_cenarios():
    """Exemplo com diferentes cenários de clientes"""
    
    regras = RegrasPortabilidadeINSS()
    
    cenarios = [
        {
            'nome': 'Maria Santos (Idade Limite)',
            'idade': '87',
            'parcelas_pagas': '20',
            'saldo_devedor': '10000.00',
            'valor_total': '15000.00'
        },
        {
            'nome': 'Pedro Costa (Poucas Parcelas)',
            'idade': '45',
            'parcelas_pagas': '8',
            'saldo_devedor': '8000.00',
            'valor_total': '12000.00'
        },
        {
            'nome': 'Ana Silva (Benefício Invalidez)',
            'idade': '52',
            'codigo_beneficio': 'INV123456',
            'parcelas_pagas': '8',
            'saldo_devedor': '6000.00',
            'valor_total': '10000.00'
        }
    ]
    
    print("\n🧪 Testando diferentes cenários:")
    print("=" * 60)
    
    for cenario in cenarios:
        # Dados base
        dados = {
            'nome': cenario['nome'],
            'cpf': '11122233344',
            'idade': cenario['idade'],
            'codigo_beneficio': cenario.get('codigo_beneficio', '123456789'),
            'parcelas_pagas': cenario['parcelas_pagas'],
            'banco_atual': 'Banco do Brasil',
            'valor_parcela': '200.00',
            'saldo_devedor': cenario['saldo_devedor'],
            'valor_total': cenario['valor_total'],
            'taxa': '2.49'
        }
        
        print(f"\n👤 Cliente: {cenario['nome']}")
        print(f"   Idade: {cenario['idade']} anos")
        print(f"   Parcelas pagas: {cenario['parcelas_pagas']}")
        
        # Validar e consultar
        erros = regras.validar_dados(dados)
        if not erros:
            resultados = regras.consultar_portabilidade(dados)
            print(f"   Bancos elegíveis: {len(resultados)}")
            
            if resultados:
                bancos = [r['banco'] for r in resultados[:3]]  # Primeiros 3 bancos
                print(f"   Exemplos: {', '.join(bancos)}")
            else:
                print("   ❌ Nenhum banco elegível")
        else:
            print(f"   ❌ Dados inválidos: {erros[0]}")

def exemplo_regras_bancos():
    """Exemplo mostrando as regras implementadas"""
    
    regras = RegrasPortabilidadeINSS()
    
    print("\n📋 Regras implementadas no sistema:")
    print("=" * 60)
    
    print(f"\n🏦 Total de bancos cadastrados: {len(regras.bancos)}")
    print(f"🚫 Bancos bloqueados: {', '.join(regras.regras['bancos_bloqueados'])}")
    print(f"📊 Idade limite geral: {regras.regras['idade_limite']} anos")
    print(f"💰 Saldo mínimo: R$ {regras.regras['saldo_minimo']:.2f}")
    print(f"💸 Troco mínimo: R$ {regras.regras['troco_minimo']:.2f}")
    
    print(f"\n📈 Parcelas mínimas:")
    print(f"   - Geral: {regras.regras['parcelas_minimas']['geral']} parcelas")
    print(f"   - Invalidez: {regras.regras['parcelas_minimas']['invalidez']} parcelas")
    
    print(f"\n🏛️ Regras específicas por banco:")
    for banco, regras_banco in regras.regras_bancos.items():
        print(f"   - {banco}:")
        print(f"     * Idade máxima: {regras_banco['idade_maxima']} anos")
        print(f"     * Parcelas mínimas: {regras_banco['parcelas_minimas']}")
        print(f"     * Aceita invalidez: {'Sim' if regras_banco['aceita_invalidez'] else 'Não'}")
        print(f"     * Taxa padrão: {regras_banco['taxa_padrao']}%")

if __name__ == "__main__":
    print("🚀 Iniciando exemplos do sistema de portabilidade INSS...")
    
    try:
        # Exemplo principal
        exemplo_consulta_portabilidade()
        
        # Exemplos de diferentes cenários
        exemplo_diferentes_cenarios()
        
        # Exemplo das regras implementadas
        exemplo_regras_bancos()
        
        print("\n🎉 Todos os exemplos executados com sucesso!")
        print("\n💡 Para usar o sistema web, execute: python app.py")
        print("🌐 Acesse: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {e}")
        print("💡 Verifique se o Flask está instalado e se o arquivo app.py está correto")
