import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
happy_2023 = pd.read_csv("./WHR2023.csv")
continents2 = pd.read_csv("./continents2.csv")


happy_2023['rank'] = happy_2023['Ladder score'].rank(ascending=False)
happy_2023['rank'] = happy_2023['rank'].astype(int)

# # phân cụm theo các nhóm 
# kmeans = KMeans(n_clusters=3, random_state=0).fit(happy_2023[['Ladder score']])
# happy_2023['cluster'] = kmeans.labels_       # thêm cột cluster vào bảng happy_2023
# happy_2023['cluster'] = happy_2023['cluster'].astype(int)

# # tạo bảng mới gồm các cột: country, cluster, rank, Ladder score
# happy_2023_new = happy_2023[['Country name', 'cluster', 'rank', 'Ladder score']]
# happy_2023_new = happy_2023_new.sort_values(by=['rank'], ascending=True)
# happy_2023_new = happy_2023_new.reset_index(drop=True)
# # lưu bảng mới vào file csv 
# happy_2023_new.to_csv('happy_2023_new.csv', index=False)

# phân cụm dữ liệu bằng thuật toán kmeans và hiển thị kết quả và biểu đồ 
kmeans = KMeans(n_clusters=3, random_state=0).fit(happy_2023[['Ladder score']])
happy_2023['cluster'] = kmeans.labels_       # thêm cột cluster vào bảng happy_2023
happy_2023['cluster'] = happy_2023['cluster'].astype(int)

# tạo bảng mới gồm các cột: country, cluster, rank, Ladder score
happy_2023_new = happy_2023[['Country name', 'cluster', 'rank', 'Ladder score']]
happy_2023_new = happy_2023_new.sort_values(by=['rank'], ascending=True)
happy_2023_new = happy_2023_new.reset_index(drop=True)
# lưu bảng mới vào file csv
happy_2023_new.to_csv('happy_2023_new.csv', index=False)

# vẽ biểu đồ
fig = px.scatter(happy_2023_new, x="rank", y="Ladder score", color="cluster",
               hover_data=['Country name'])
fig.show()
