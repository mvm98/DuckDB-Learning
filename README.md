🧪 Resultados da Comparação — DuckDB vs Pandas

Tamanho do arquivo CSV: 303.91 MB

⚙️ Resultados de Performance
Operação |	Tempo (s) |	Memória (MB)
Pandas - leitura CSV |	3.609 |	305.73
DuckDB - leitura CSV |	0.063 |	4.52
Pandas - filtro + groupby |	0.409 |	0.69
DuckDB - filtro + groupby |	1.022 |	2.80

📈 Resultado do Pandas
categoria  media_quantidade
A    25.006246
B    24.994971
C    25.004216
D    24.998633

📈 Resultado do DuckDB
  categoria  media_quantidade
D         24.998633
A         25.006246
C         25.004216
B         24.994971
