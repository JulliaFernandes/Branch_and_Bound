import time
import sys
from scipy.optimize import linprog
from copy import deepcopy

def ler_problema(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.read().strip().split(';')

    variaveis = {}
    objetivo_tipo = None
    objetivo = {}
    restricoes = []

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith('//'):
            continue
        if linha.startswith('var'):
            partes = linha.replace('var ', '').split()
            nome = partes[0]
            tipo = 'real'
            limite = 'livre'
            if 'integer' in linha:
                tipo = 'inteira'
            if '>=' in linha:
                limite = '>=0'
            elif '<=' in linha:
                limite = '<=0'
            variaveis[nome] = {'tipo': tipo, 'limite': limite}

        elif linha.startswith('maximize') or linha.startswith('minimize'):
            if linha.startswith('maximize'):
                objetivo_tipo = 'max'
            else:
                objetivo_tipo = 'min'
            expr = linha.split(':')[1].strip()
            termos = expr.split('+')
            for termo in termos:
                termo = termo.strip()
                if termo == '':
                    continue
                partes_termo = termo.split('*')
                if len(partes_termo) == 2:
                    coef = partes_termo[0]
                    var = partes_termo[1]
                    objetivo[var.strip()] = float(coef.strip())
                elif len(partes_termo) == 1:
                    var = partes_termo[0]
                    objetivo[var.strip()] = 1.0

        elif linha.startswith('subject to'):
            conteudo = linha.split(':')[1].strip()
            if '<=' in conteudo:
                lado_esq, lado_dir = conteudo.split('<=', 1)
                tipo = '<='
            elif '>=' in conteudo:
                lado_esq, lado_dir = conteudo.split('>=', 1)
                tipo = '>='
            elif '=' in conteudo:
                lado_esq, lado_dir = conteudo.split('=', 1)
                tipo = '='
            else:
                continue
            lado_esq = lado_esq.strip()
            restricao = {}
            termos = lado_esq.split('+')
            for termo in termos:
                termo = termo.strip()
                if termo == '':
                    continue
                partes_termo = termo.split('*')
                if len(partes_termo) == 2:
                    coef = partes_termo[0]
                    var = partes_termo[1]
                    restricao[var.strip()] = float(coef.strip())
                elif len(partes_termo) == 1:
                    var = partes_termo[0]
                    restricao[var.strip()] = 1.0
            restricoes.append((restricao, tipo, float(lado_dir.strip())))

    print("Variáveis lidas:", variaveis)
    return variaveis, objetivo_tipo, objetivo, restricoes

def montar_lp(variaveis, objetivo_tipo, objetivo, restricoes):
    nomes = []
    for var in variaveis:
        nomes.append(var)
    c = []
    for var in nomes:
        if var in objetivo:
            c.append(objetivo[var])
        else:
            c.append(0)
    if objetivo_tipo == 'max':
        for i in range(len(c)):
            c[i] = -c[i]

    A_ub = []
    b_ub = []
    A_eq = []
    b_eq = []
    for restricao, tipo, valor in restricoes:
        linha = []
        for var in nomes:
            if var in restricao:
                linha.append(restricao[var])
            else:
                linha.append(0)
        if tipo == '<=':
            A_ub.append(linha)
            b_ub.append(valor)
        elif tipo == '>=':
            linha_neg = []
            for v in linha:
                linha_neg.append(-v)
            A_ub.append(linha_neg)
            b_ub.append(-valor)
        elif tipo == '=':
            A_eq.append(linha)
            b_eq.append(valor)

    bounds = []
    for var in nomes:
        lim = variaveis[var]['limite']
        if lim == '>=0':
            bounds.append((0, None))
        elif lim == '<=0':
            bounds.append((None, 0))
        else:
            bounds.append((None, None))

    if len(A_eq) == 0:
        A_eq_final = None
        b_eq_final = None
    else:
        A_eq_final = A_eq
        b_eq_final = b_eq

    if len(A_ub) == 0:
        A_ub_final = None
        b_ub_final = None
    else:
        A_ub_final = A_ub
        b_ub_final = b_ub

    return nomes, c, A_ub_final, b_ub_final, A_eq_final, b_eq_final, bounds

def eh_solucao_inteira(solucao, variaveis, nomes):
    for i in range(len(nomes)):
        var = nomes[i]
        if variaveis[var]['tipo'] == 'inteira':
            if abs(solucao[i] - round(solucao[i])) > 1e-5:
                return False
    return True

def branch_and_bound(variaveis, objetivo_tipo, objetivo, restricoes):
    inicio = time.time()
    fila = [([], [])] 
    if objetivo_tipo == 'max':
        melhor_valor = float('-inf')
    else:
        melhor_valor = float('inf')
    melhor_solucao = None
    iteracao = 0
    restricoes_originais = restricoes.copy()

    while len(fila) > 0:
        restricoes_atual, historico = fila.pop(0)
        nomes, c, A_ub, b_ub, A_eq, b_eq, bounds = montar_lp(
            variaveis, objetivo_tipo, objetivo, restricoes_originais + restricoes_atual
        )
        resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
        iteracao = iteracao + 1
        tempo = time.time() - inicio

        marcador = ''
        if not resultado.success:
            acao = 'I'
            z_lp = '---'
        elif resultado.status == 3:
            acao = 'L'
            z_lp = '---'
        else:
            solucao = resultado.x
            if objetivo_tipo == 'max':
                valor_obj = resultado.fun * -1
            else:
                valor_obj = resultado.fun
            z_lp = "{:.4f}".format(valor_obj)
            if eh_solucao_inteira(solucao, variaveis, nomes):
                viavel = True
                todas_restricoes = restricoes_originais + restricoes_atual
                for restricao, tipo, valor in todas_restricoes:
                    soma = 0
                    for var, coef in restricao.items():
                        soma = soma + solucao[nomes.index(var)] * coef
                    if tipo == '<=' and soma > valor + 1e-5:
                        viavel = False
                        break
                    elif tipo == '>=' and soma < valor - 1e-5:
                        viavel = False
                        break
                    elif tipo == '=' and abs(soma - valor) > 1e-5:
                        viavel = False
                        break
                if viavel:
                    if (objetivo_tipo == 'max' and valor_obj > melhor_valor) or (objetivo_tipo == 'min' and valor_obj < melhor_valor):
                        melhor_valor = valor_obj
                        melhor_solucao = solucao.copy()
                        acao = 'O'
                        marcador = '*'
                    else:
                        acao = 'O'
                        marcador = ''
                else:
                    acao = 'I'
                    z_lp = '---'
            else:
                acao = 'D'
                marcador = ''
                for i in range(len(nomes)):
                    var = nomes[i]
                    if variaveis[var]['tipo'] == 'inteira':
                        if abs(solucao[i] - round(solucao[i])) > 1e-5:
                            baixo = deepcopy(restricoes_atual)
                            cima = deepcopy(restricoes_atual)
                            baixo.append(({var: 1}, '<=', int(solucao[i])))
                            cima.append(({var: 1}, '>=', int(solucao[i]) + 1))
                            fila.append((baixo, historico + [(var, 'baixo')]))
                            fila.append((cima, historico + [(var, 'cima')]))
                            break

        if melhor_solucao is not None:
            z_melhor = "{:.4f}".format(melhor_valor) + marcador
        else:
            z_melhor = "---"

        # Poda por bound
        if melhor_solucao is not None:
            if (objetivo_tipo == 'max' and valor_obj <= melhor_valor + 1e-5) or \
               (objetivo_tipo == 'min' and valor_obj >= melhor_valor - 1e-5):
                acao = 'P'
                z_lp = "{:.4f}".format(valor_obj)
                marcador = ''
                print("{:03d} | avaliados: {:02d} | fila: {:02d} | z (LP): {} | acao: {} | z* = {} | tempo: {:.4f}s".format(
                    iteracao, iteracao, len(fila), z_lp, acao, melhor_valor, tempo))
                continue

        print("{:03d} | avaliados: {:02d} | fila: {:02d} | z (LP): {} | acao: {} | z* = {} | tempo: {:.4f}s".format(
            iteracao, iteracao, len(fila), z_lp, acao, z_melhor, tempo))

    if melhor_solucao is not None:
        print("\nSolução ótima encontrada: z = {:.4f}".format(melhor_valor))
        for i in range(len(nomes)):
            print("{} = {}".format(nomes[i], round(melhor_solucao[i], 4)))
    else:
        print("\nProblema inviável ou solução ilimitada")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python main.py caminho/para/arquivo.txt")
        sys.exit(1)

    caminho = sys.argv[1]
    vars_, tipo, obj, restrs = ler_problema(caminho)
    branch_and_bound(vars_, tipo, obj, restrs)