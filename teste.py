from readline import redisplay
import pandas as pd

df = pd.read_csv('https://storage.googleapis.com/my-bucket-soulcode/dfs_brutos/alunos_matriculados.csv')

redisplay(df)