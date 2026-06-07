# Benchmarking de Hardware — Arquitetura de Memória Unificada

Repositório de dados brutos, scripts de análise e instruções de reprodução do artigo científico:

> **Benchmarking de CPU, Memória e Armazenamento em Sistemas com Arquitetura de Memória Unificada: Uma Avaliação Experimental**
> Luiza Barbosa Almeida da Silva



## Estrutura do Repositório

```
benchmarking-hardware-artigo/
├── README.md
├── dados/
│   ├── cinebench_r23.csv       # Resultados brutos do Cinebench R23
│   ├── disk_speed.csv          # Resultados brutos do Blackmagic Disk Speed Test
│   └── sysbench_memory.csv     # Resultados brutos do sysbench
├── artigo/
│   ├── artigo_sbc.tex          # Fonte LaTeX do artigo
│   └── referencias.bib         # Referências bibliográficas
└── scripts/
    └── analise.py              # Script de análise estatística
```


## Como Reproduzir os Experimentos

### 1. Cinebench R23
- Clique em **CPU (Multi Core)** → aguarde → anote o resultado
- Clique em **CPU (Single Core)** → aguarde → anote o resultado
- Repita 3 vezes com intervalo de 2 minutos entre execuções

### 2. Blackmagic Disk Speed Test
- Abra o app → clique em **Start**
- Anote os valores de **Write** e **Read** (MB/s)
- Repita 3 vezes com intervalo de 2 minutos

### 3. sysbench (memória)
Instale via Homebrew:
```bash
brew install sysbench
```

Execute o benchmark de **escrita**:
```bash
sysbench memory --memory-block-size=1M --memory-total-size=10G run
```

Execute o benchmark de **leitura**:
```bash
sysbench memory --memory-block-size=1M --memory-total-size=10G --memory-oper=read run
```

Anote o valor de **MiB/sec** de cada execução.


## Como Rodar a Análise Estatística

```bash
pip install pandas scipy matplotlib
python scripts/analise.py
```

O script gera as estatísticas completas (média, desvio-padrão, IC 95%).

---

## Citação

```
SILVA, Luiza Barbosa Almeida da. Benchmarking de CPU, Memória e Armazenamento
em Sistemas com Arquitetura de Memória Unificada: Uma Avaliação Experimental.
```
