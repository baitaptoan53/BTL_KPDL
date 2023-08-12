import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
happy_2023 = pd.read_csv("./WHR2023.csv")
country_mapping = pd.read_csv("./continents2.csv")
# hiển thị số cột và số dòng của bảng happy_2023  và continent_mapping
happy_2023.shape
country_mapping.shape

# tên cột của bảng happy_2023
happy_2023.columns
# tên cột của bảng country_mapping
country_mapping.columns
# kiểu dữ liệu của các cột trong bảng happy_2023
happy_2023.dtypes
# kiểu dữ liệu của các cột trong bảng country_mapping
country_mapping.dtypes

# kiểm có cột nào bị trùng trong bảng happy_2023 không
happy_2023.columns.duplicated()
# kiểm tra các giá trị null trong bảng happy_2023
happy_2023.isnull().sum()
# Remove all columns between column name 'Ladder score in Dystopia' to 'Dystopia + residual'
happy_2023 = happy_2023.drop(
    happy_2023.loc[:, 'Ladder score in Dystopia':'Dystopia + residual'].columns, axis=1)
# Remove all columns between column name 'Standard error of ladder score' to 'lowerwhisker'
happy_2023 = happy_2023.drop(
    happy_2023.loc[:, 'Standard error of ladder score':'lowerwhisker'].columns, axis=1)

happy_2023['rank'] = happy_2023['Ladder score'].rank(ascending=False)
happy_2023['rank'] = happy_2023['rank'].astype(int)

# Rename the columns for consistency
happy_df_2023 = happy_2023.rename({'Country name': 'quốc gia', 'Standard error of ladder score': 'Sai số chuẩn của điểm hạnh phúc', 'Ladder score': 'điểm hạnh phúc', 'Happiness score': 'điểm hạnh phúc', 'Logged GDP per capita': 'GDP bình quân đầu người', 'Social support': 'Hỗ trợ xã hội', 'Healthy life expectancy': 'tuổi thọ',
                                   'Freedom to make life choices': 'tự do lựa chọn cuộc sống', 'Generosity': 'Tính hào phóng', 'Perceptions of corruption': 'Nhận thức về tham nhũng', 'Explained by: Freedom to make life choices': 'tự do lựa chọn cuộc sống', 'Explained by: Generosity': 'tính hào phóng', 'Explained by: Perceptions of corruption': 'Nhận thức về tham nhũng'}, axis=1)
happy_df_2023.head()
# print(happy_df_2023.head())


def top_bottom_identifier(value):
    if value < 11:
        return "top 10 happiest"
    if value > 127:
        return "bottom 10 happiest"
    elif 11 <= value < 128:
        return "not top/bottom 10"


happy_df_2023['top_bottom_identifier'] = happy_df_2023['rank'].map(
    top_bottom_identifier)

# print(happy_df_2023.head())

# Dropping irrelevant columns
country_mapping.drop('alpha-2', inplace=True, axis=1)
# Remove all columns between column name 'country-code' to 'iso_3166-2'
country_mapping = country_mapping.drop(
    country_mapping.loc[:, 'country-code':'iso_3166-2'].columns, axis=1)
# Remove all columns between column name 'intermediate-region' to 'intermediate-region-code'
country_mapping = country_mapping.drop(
    country_mapping.loc[:, 'intermediate-region':'intermediate-region-code'].columns, axis=1)
country_mapping.head()

# print(country_mapping.head())

# Rename the columns for consistency
country_mapping = country_mapping.rename(
    {'name': 'quốc gia', 'alpha-3': 'iso alpha', 'sub-region': 'vùng quốc gia'}, axis=1)

# Merge the happiness data and country mapping dataframes
happy_region_df = happy_df_2023.merge(
    country_mapping, on='quốc gia', how='left')
# print(happy_region_df.head())

# kiểm tra các giá trị null trong bảng happy_region_df
# print(happy_region_df.isnull().sum())

# kiểm tra các giá trị null trong cột 'vùng quốc gia'
nan_hlf_rows = happy_region_df[happy_region_df['tuổi thọ'].isnull(
)]
# print(nan_hlf_rows)

# Check for rows with null region that did not match correctly when merging
# kiểm tra các giá trị null trong cột 'vùng quốc gia' sau khi merge 2 bảng
nan_region_rows = happy_region_df[happy_region_df['vùng quốc gia'].isnull()]
print(nan_region_rows)

# happy_2023['rank'] = happy_2023['Ladder score'].rank(ascending=False)
# happy_2023['rank'] = happy_2023['rank'].astype(int)

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
# kmeans = KMeans(n_clusters=3, random_state=0).fit(happy_2023[['Ladder score']])
# happy_2023['cluster'] = kmeans.labels_       # thêm cột cluster vào bảng happy_2023
# happy_2023['cluster'] = happy_2023['cluster'].astype(int)

# tạo bảng mới gồm các cột: country, cluster, rank, Ladder score
# happy_2023_new = happy_2023[['Country name', 'cluster', 'rank', 'Ladder score']]
# happy_2023_new = happy_2023_new.sort_values(by=['rank'], ascending=True)
# happy_2023_new = happy_2023_new.reset_index(drop=True)
# lưu bảng mới vào file csv
# happy_2023_new.to_csv('happy_2023_new.csv', index=False)

# vẽ biểu đồ
# fig = px.scatter(happy_2023_new, x="rank", y="Ladder score", color="cluster",
#                hover_data=['Country name'])
# fig.show()

# xây dựng file csv mapping giữa country và continent
