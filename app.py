from flask import Flask, render_template, request, jsonify
import re
from decimal import Decimal, ROUND_HALF_UP

app = Flask(__name__)

class RegrasPortabilidadeINSS:
    def __init__(self):
        # Bancos disponíveis para portabilidade
        self.bancos = [
            "Banco do Brasil", "Caixa Econômica Federal", "Bradesco", "Itaú", 
            "Santander", "Banrisul", "Sicredi", "Sicoob", "BRB", "Bancoob",
            "Cresol", "Unicred", "Ailos", "Sicredi Pioneira", "Sicoob Credisul",
            "Sicredi Norte", "Sicredi Centro", "Sicredi Sul", "Sicoob Credisul",
            "Sicredi Pioneira", "Sicoob Credisul", "Sicredi Norte", "Sicoob Centro"
        ]
        
        # Regras de portabilidade baseadas no documento
        self.regras = {
            "idade_limite": 85,
            "parcelas_minimas": {
                "geral": 12,
                "invalidez": 6
            },
            "bancos_bloqueados": ["BRB"],  # BRB não aceita portabilidade
            "saldo_minimo": 500.00,
            "troco_minimo": 100.00,
            "taxa_maxima": 2.99
        }
        
        # Regras específicas por banco
        self.regras_bancos = {
            "Banco do Brasil": {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Caixa Econômica Federal": {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Bradesco": {
                "idade_maxima": 85,
                "parcelas_minimas": 15,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Itaú": {
                "idade_maxima": 85,
                "parcelas_minimas": 15,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Santander": {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Banrisul": {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Sicredi": {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            },
            "Sicoob": {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            }
        }

    def validar_dados(self, dados):
        """Valida os dados de entrada"""
        erros = []
        
        if not dados.get('nome') or len(dados['nome'].strip()) < 3:
            erros.append("Nome deve ter pelo menos 3 caracteres")
            
        if not dados.get('cpf') or not self.validar_cpf(dados['cpf']):
            erros.append("CPF inválido")
            
        idade = dados.get('idade')
        if not idade or not str(idade).isdigit() or int(idade) < 18 or int(idade) > 120:
            erros.append("Idade deve ser entre 18 e 120 anos")
            
        if not dados.get('codigo_beneficio'):
            erros.append("Código do benefício é obrigatório")
            
        parcelas = dados.get('parcelas_pagas')
        if not parcelas or not str(parcelas).isdigit() or int(parcelas) < 0:
            erros.append("Quantidade de parcelas pagas deve ser um número positivo")
            
        if not dados.get('banco_atual'):
            erros.append("Banco atual é obrigatório")
            
        try:
            valor_parcela = Decimal(str(dados.get('valor_parcela', 0)))
            if valor_parcela <= 0:
                erros.append("Valor da parcela deve ser maior que zero")
        except:
            erros.append("Valor da parcela inválido")
            
        try:
            saldo_devedor = Decimal(str(dados.get('saldo_devedor', 0)))
            if saldo_devedor <= 0:
                erros.append("Saldo devedor deve ser maior que zero")
        except:
            erros.append("Saldo devedor inválido")
            
        try:
            valor_total = Decimal(str(dados.get('valor_total', 0)))
            if valor_total <= 0:
                erros.append("Valor total deve ser maior que zero")
        except:
            erros.append("Valor total inválido")
            
        try:
            taxa = Decimal(str(dados.get('taxa', 0)))
            if taxa < 0 or taxa > 100:
                erros.append("Taxa deve ser entre 0 e 100%")
        except:
            erros.append("Taxa inválida")
            
        return erros

    def validar_cpf(self, cpf):
        """Valida formato do CPF"""
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11:
            return False
        if cpf == cpf[0] * 11:
            return False
        return True

    def consultar_portabilidade(self, dados):
        """Consulta portabilidade baseada nas regras"""
        resultados = []
        
        # Verificar se é benefício por invalidez
        is_invalidez = "invalidez" in dados.get('codigo_beneficio', '').lower()
        
        for banco in self.bancos:
            if banco in self.regras['bancos_bloqueados']:
                continue
                
            # Aplicar regras específicas do banco
            regras_banco = self.regras_bancos.get(banco, {
                "idade_maxima": 85,
                "parcelas_minimas": 12,
                "aceita_invalidez": True,
                "taxa_padrao": 2.49
            })
            
            # Verificar idade
            if int(dados['idade']) > regras_banco['idade_maxima']:
                continue
                
            # Verificar parcelas mínimas
            parcelas_minimas = regras_banco['parcelas_minimas']
            if is_invalidez:
                parcelas_minimas = self.regras['parcelas_minimas']['invalidez']
                
            if int(dados['parcelas_pagas']) < parcelas_minimas:
                continue
                
            # Verificar se aceita invalidez
            if is_invalidez and not regras_banco['aceita_invalidez']:
                continue
                
            # Verificar saldo mínimo
            if Decimal(str(dados['saldo_devedor'])) < self.regras['saldo_minimo']:
                continue
                
            # Verificar troco mínimo
            troco = Decimal(str(dados['valor_total'])) - Decimal(str(dados['saldo_devedor']))
            if troco < self.regras['troco_minimo']:
                continue
                
            # Determinar tipo de operação
            tipo_operacao = "Portabilidade"
            if troco > 0:
                tipo_operacao = "Port+Refin"
                
            # Calcular taxa aplicável
            taxa_aplicavel = min(regras_banco['taxa_padrao'], 
                               Decimal(str(dados['taxa'])) + Decimal('0.5'))
            
            # Observações
            observacoes = []
            if is_invalidez:
                observacoes.append("Benefício por invalidez")
            if troco > 0:
                observacoes.append(f"Refinanciamento de R$ {troco:.2f}")
            if int(dados['parcelas_pagas']) >= parcelas_minimas + 5:
                observacoes.append("Cliente com histórico positivo")
                
            resultados.append({
                'banco': banco,
                'tipo_operacao': tipo_operacao,
                'taxa_aplicavel': float(taxa_aplicavel),
                'observacoes': '; '.join(observacoes) if observacoes else "Regras atendidas"
            })
            
        return resultados

# Instância global das regras
regras = RegrasPortabilidadeINSS()

@app.route('/')
def index():
    return render_template('index.html', bancos=regras.bancos)

@app.route('/consultar', methods=['POST'])
def consultar():
    dados = request.form.to_dict()
    
    # Validar dados
    erros = regras.validar_dados(dados)
    if erros:
        return jsonify({'erro': True, 'mensagens': erros})
    
    # Consultar portabilidade
    resultados = regras.consultar_portabilidade(dados)
    
    return jsonify({
        'erro': False,
        'resultados': resultados,
        'total_bancos': len(resultados)
    })

if __name__ == '__main__':
    app.run(debug=True)
