import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

happy_2023 = pd.read_csv("./WHR2023.csv")
continents2 = pd.read_csv("./continents2.csv")


# happy_2023['rank'] = happy_2023['Ladder score'].rank(ascending=False)
# happy_2023['rank'] = happy_2023['rank'].astype(int)

# print(happy_2023['rank'])
# continents2
print(continents2)