# Implementação do Algoritmo Branch and Bound para Problemas de Programação Linear Inteira

Este projeto implementa o algoritmo Branch and Bound para resolver problemas de Programação Linear Inteira Mista (MILP), desenvolvido como parte da disciplina de Pesquisa Operacional.

## 📋 Descrição do Projeto

O algoritmo Branch and Bound é uma técnica de otimização que resolve problemas de programação linear inteira através da divisão do espaço de soluções em subproblemas menores. A implementação utiliza a biblioteca SciPy para resolver os problemas relaxados e implementa a estratégia de busca em profundidade (DFS) para explorar a árvore de soluções.

## 🚀 Funcionalidades

- **Leitura de arquivos**: Parser customizado para arquivos de entrada no formato específico
- **Relaxação Linear**: Resolve problemas relaxados usando o método Simplex
- **Estratégia de Branching**: Implementa a regra da variável mais fracionária
- **Bound Pruning**: Elimina nós que não podem levar a soluções ótimas
- **Suporte a diferentes tipos de problema**: Maximização e minimização
- **Relatórios detalhados**: Exibe o progresso da busca e estatísticas

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **SciPy**: Para resolver problemas de programação linear
- **NumPy**: Para operações matriciais
- **Bibliotecas padrão**: time, sys, copy, math

## 📁 Estrutura do Projeto

```
Trabalho2/
├── main.py                 # Arquivo principal com implementação do algoritmo
├── entrada/               # Diretório com arquivos de teste
│   ├── MIP_01.txt
│   ├── MIP_02.txt
│   ├── MIP_03.txt
│   ├── MIP_04.txt
│   └── MIP_05.txt
└── README.md
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)

### Instalação das Dependências

```bash
pip install scipy numpy
```

## 💻 Como Executar

### Execução Básica

```bash
python main.py entrada/MIP_01.txt
```

### Exemplos de Uso

```bash
# Executar problema pequeno
python main.py entrada/MIP_01.txt

# Executar problema médio
python main.py entrada/MIP_03.txt

# Executar problema grande (pode demorar)
python main.py entrada/MIP_05.txt
```

## 📊 Formato dos Arquivos de Entrada

Os arquivos de entrada seguem o formato:

```
var x1 integer >= 0;
var x2 integer >= 0;
maximize: 3*x1 + 2*x2;
subject to: x1 + x2 <= 4;
subject to: 2*x1 + x2 <= 6;
```

### Elementos do Formato:

- **var**: Declaração de variáveis com tipo (integer/real) e limites
- **maximize/minimize**: Função objetivo
- **subject to**: Restrições do problema

## 🎯 Algoritmo Implementado

### Branch and Bound

1. **Inicialização**: Resolve o problema relaxado inicial
2. **Seleção de Nó**: Usa estratégia DFS (pilha)
3. **Bound**: Calcula limite superior/inferior através da relaxação
4. **Branching**: Divide usando a variável mais fracionária
5. **Pruning**: Elimina nós com bounds piores que a melhor solução

### Estratégias de Otimização

- **Regra de Branching**: Variável mais fracionária
- **Bound Pruning**: Comparação com melhor solução conhecida
- **Busca em Profundidade**: Explora soluções rapidamente

## 📈 Exemplos de Saída

```
Variáveis lidas: {'x1': {'tipo': 'inteira', 'limite': '>=0'}, 'x2': {'tipo': 'inteira', 'limite': '>=0'}}
001 | avaliados: 01 | fila: 02 | z (LP): 6.0000 | acao: D | z* = --- | tempo: 0.0120s
002 | avaliados: 02 | fila: 01 | z (LP): 5.0000 | acao: O | z* = 5.0000* | tempo: 0.0250s
003 | avaliados: 03 | fila: 00 | z (LP): 4.0000 | acao: P | z* = 5.0000 | tempo: 0.0380s

Solução ótima encontrada: z = 5.0000
x1 = 1.0
x2 = 2.0
```

## 📋 Problemas de Teste

| Arquivo | Variáveis | Tipo | Descrição |
|---------|-----------|------|-----------|
| MIP_01.txt | 2 | Pequeno | Problema básico para validação |
| MIP_02.txt | 5 | Pequeno | Problema com mais variáveis |
| MIP_03.txt | 10 | Médio | Problema de complexidade média |
| MIP_04.txt | 20 | Médio | Teste de eficiência |
| MIP_05.txt | 100 | Grande | Problema de mochila 0-1 |

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.

## 📞 Contato
<div>
 <br><p align="justify"> Jullia Fernandes</p>
 <a href="https://t.me/JulliaFernandes">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:julliacefet@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>julliacefet@gmail.com</i>
</a>

<div>
 <br><p align="justify"> Lucas Lima de Oliveira</p>
 <a href="https://t.me/oilucaslima">
 <img align="center" src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/> 
 </div>
<a style="color:black" href="mailto:lucaslimadeoliveira80@gmail.com?subject=[GitHub]%20Source%20Dynamic%20Lists">
✉️ <i>lucaslimadeoliveira80@gmail.com</i>
</a>
   
---

**Desenvolvido para a disciplina de Pesquisa Operacional - 7º Período**
