import pandas as pd

data = pd.read_csv("indeed_jobs.csv")["url"]



data = data[ data.str.contains("bmw") == False ]

print(data)
print("huh")