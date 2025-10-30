import duckdb
import pandas as pd
import psutil
import time
import os

# Caminho do arquivo CSV
csv_path = "dados.csv"

# Função para medir uso de memória (em MB)
def memoria_atual():
    processo = psutil.Process()
    return processo.memory_info().rss / (1024 * 1024)

# Tamanho do arquivo
tamanho_csv = os.path.getsize(csv_path) / (1024 * 1024)
print(f"Tamanho do arquivo CSV: {tamanho_csv:.2f} MB\n")


# Leitura com Pandas
mem_before = memoria_atual()
start = time.time()
df_pandas = pd.read_csv(csv_path)
tempo_pandas_leitura = time.time() - start
mem_after = memoria_atual()
mem_pandas_leitura = mem_after - mem_before

# Leitura com DuckDB
mem_before = memoria_atual()
start = time.time()
df_duckdb = duckdb.read_csv(csv_path)
tempo_duckdb_leitura = time.time() - start
mem_after = memoria_atual()
mem_duckdb_leitura = mem_after - mem_before

# Filtro + GroupBy (Pandas)
mem_before = memoria_atual()
start = time.time()
res_pandas = (
    df_pandas[df_pandas["valor"] > 500]
    .groupby("categoria")["quantidade"]
    .mean()
)
tempo_pandas_agg = time.time() - start
mem_after = memoria_atual()
mem_pandas_agg = mem_after - mem_before

# Filtro + GroupBy (DuckDB SQL)
mem_before = memoria_atual()
start = time.time()
res_duckdb = duckdb.query(f"""
    SELECT categoria, AVG(quantidade) AS media_quantidade
    FROM read_csv_auto('{csv_path}')
    WHERE valor > 500
    GROUP BY categoria
""").df()
tempo_duckdb_agg = time.time() - start
mem_after = memoria_atual()
mem_duckdb_agg = mem_after - mem_before

# Resultados
print("\n---------------------RESULTADOS DE PERFORMANCE---------------------\n")
print(f"Tamanho do CSV: {tamanho_csv:.2f} MB\n")

print(f"Pandas - leitura CSV: {tempo_pandas_leitura:.3f} s | Memória: {mem_pandas_leitura:.2f} MB")
print(f"DuckDB - leitura CSV: {tempo_duckdb_leitura:.3f} s | Memória: {mem_duckdb_leitura:.2f} MB")
print(f"Pandas - filtro + groupby: {tempo_pandas_agg:.3f} s | Memória: {mem_pandas_agg:.2f} MB")
print(f"DuckDB - filtro + groupby: {tempo_duckdb_agg:.3f} s | Memória: {mem_duckdb_agg:.2f} MB")

# Ganhos relativos
ganho_leitura = tempo_pandas_leitura / tempo_duckdb_leitura if tempo_duckdb_leitura > 0 else 0
ganho_agg = tempo_pandas_agg / tempo_duckdb_agg if tempo_duckdb_agg > 0 else 0

print("\n---------------------Comparativo---------------------\n")
print(f"DuckDB foi {ganho_leitura:.2f}x mais rápido na leitura")
print(f"DuckDB foi {ganho_agg:.2f}x mais rápido na agregação\n")


print("Resultado do Pandas:")
print(res_pandas)
print("\n--------------------\n")
print("Resultado do DuckDB:")
print(res_duckdb)
