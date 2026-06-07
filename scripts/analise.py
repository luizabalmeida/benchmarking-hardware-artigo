"""
Análise Estatística — Benchmarking de Hardware (Arquitetura UMA)
Artigo: Benchmarking de CPU, Memória e Armazenamento em Sistemas com
        Arquitetura de Memória Unificada: Uma Avaliação Experimental
Autora: Luiza Barbosa Almeida da Silva — CESAR School, 2025
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

os.makedirs("figuras", exist_ok=True)

# ── Funções utilitárias ────────────────────────────────────────────────────

def estatisticas(data, nome):
    """Calcula e imprime estatísticas descritivas completas."""
    a = np.array(data)
    n = len(a)
    media = np.mean(a)
    dp = np.std(a, ddof=1) if n > 1 else 0.0
    mediana = np.median(a)
    cv = (dp / media * 100) if media != 0 else 0
    if n > 1:
        ci = stats.t.interval(0.95, df=n-1, loc=media, scale=stats.sem(a))
    else:
        ci = (media, media)

    print(f"\n{'='*50}")
    print(f"  {nome}")
    print(f"{'='*50}")
    print(f"  N             : {n}")
    print(f"  Média         : {media:.2f}")
    print(f"  Desvio Padrão : {dp:.2f}")
    print(f"  Mediana       : {mediana:.2f}")
    print(f"  Mín / Máx     : {a.min():.2f} / {a.max():.2f}")
    print(f"  CV            : {cv:.2f}%")
    print(f"  IC 95%        : [{ci[0]:.2f}, {ci[1]:.2f}]")
    return {"media": media, "dp": dp, "mediana": mediana, "cv": cv, "ci": ci}

# ── Leitura dos dados ──────────────────────────────────────────────────────

cb  = pd.read_csv("dados/cinebench_r23.csv")
dsk = pd.read_csv("dados/disk_speed.csv")
mem = pd.read_csv("dados/sysbench_memory.csv")

print("\n>>> CINEBENCH R23")
sc_stats = estatisticas(cb["single_core_pts"], "Single-Core (pts)")
mc_stats = estatisticas(cb["multi_core_pts"],  "Multi-Core (pts)")

print("\n>>> BLACKMAGIC DISK SPEED TEST")
dr_stats = estatisticas(dsk["leitura_mbs"], "Leitura Sequencial (MB/s)")
dw_stats = estatisticas(dsk["escrita_mbs"], "Escrita Sequencial (MB/s)")

print("\n>>> SYSBENCH MEMORY")
print(mem.to_string(index=False))

# ── Gráfico 1: Cinebench R23 ───────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Cinebench R23 — Apple M4 (3 execuções)", fontsize=13, fontweight="bold")

for ax, col, label, st in zip(
    axes,
    ["single_core_pts", "multi_core_pts"],
    ["Single-Core (pts)", "Multi-Core (pts)"],
    [sc_stats, mc_stats]
):
    ax.bar(cb["execucao"], cb[col], color="#4C72B0", alpha=0.8, zorder=2)
    ax.axhline(st["media"], color="red", linestyle="--", linewidth=1.5, label=f'Média: {st["media"]:.0f}')
    ax.fill_between(
        [0.5, 3.5],
        st["ci"][0], st["ci"][1],
        alpha=0.15, color="red", label=f'IC 95%'
    )
    ax.set_title(label)
    ax.set_xlabel("Execução")
    ax.set_ylabel("Pontuação (pts)")
    ax.set_xticks([1, 2, 3])
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3, zorder=1)

plt.tight_layout()
plt.savefig("figuras/cinebench_r23.png", dpi=150, bbox_inches="tight")
print("\n[✓] Figura salva: figuras/cinebench_r23.png")

# ── Gráfico 2: Disk Speed ──────────────────────────────────────────────────

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle("Blackmagic Disk Speed Test — Apple SSD NVMe (3 execuções)", fontsize=13, fontweight="bold")

for ax, col, label, st, cor in zip(
    axes,
    ["leitura_mbs", "escrita_mbs"],
    ["Leitura Sequencial (MB/s)", "Escrita Sequencial (MB/s)"],
    [dr_stats, dw_stats],
    ["#2ca02c", "#ff7f0e"]
):
    ax.bar(dsk["execucao"], dsk[col], color=cor, alpha=0.8, zorder=2)
    ax.axhline(st["mediana"], color="black", linestyle="--", linewidth=1.5,
               label=f'Mediana: {st["mediana"]:.0f} MB/s')
    ax.set_title(label)
    ax.set_xlabel("Execução")
    ax.set_ylabel("MB/s")
    ax.set_xticks([1, 2, 3])
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3, zorder=1)

plt.tight_layout()
plt.savefig("figuras/disk_speed.png", dpi=150, bbox_inches="tight")
print("[✓] Figura salva: figuras/disk_speed.png")

# ── Gráfico 3: Memória ─────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(7, 4))
ops = mem["operacao"]
bw  = mem["bandwidth_mbs"] / 1000  # converter para GB/s
bars = ax.bar(ops, bw, color=["#4C72B0", "#DD8452"], alpha=0.85, width=0.4, zorder=2)
ax.bar_label(bars, fmt="%.1f GB/s", padding=4, fontsize=10)
ax.set_title("sysbench Memory — Unified Memory Apple M4", fontsize=12, fontweight="bold")
ax.set_ylabel("Largura de Banda (GB/s)")
ax.set_ylim(0, 40)
ax.grid(axis="y", alpha=0.3, zorder=1)
plt.tight_layout()
plt.savefig("figuras/memoria.png", dpi=150, bbox_inches="tight")
print("[✓] Figura salva: figuras/memoria.png")

print("\n[✓] Análise concluída.")
