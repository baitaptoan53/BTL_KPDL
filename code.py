import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import webbrowser
from sklearn.linear_model import LinearRegression


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
#kiểm tra có cột nào bị trùng trong bảng country_mapping không
country_mapping.columns.duplicated()
# kiểm tra các giá trị null trong bảng happy_2023
happy_2023.isnull().sum()
# print(happy_2023.isnull().sum())
# Remove all columns between column name 'Ladder score in Dystopia' to 'Dystopia + residual'
happy_2023 = happy_2023.drop(
    happy_2023.loc[:, 'Ladder score in Dystopia':'Dystopia + residual'].columns, axis=1)
# Remove all columns between column name 'Standard error of ladder score' to 'lowerwhisker'
happy_2023 = happy_2023.drop(
    happy_2023.loc[:, 'Standard error of ladder score':'lowerwhisker'].columns, axis=1)

happy_2023['thứ hạng'] = happy_2023['Ladder score'].rank(ascending=False)
happy_2023['thứ hạng'] = happy_2023['thứ hạng'].astype(int)

# Rename the columns for consistency
happy_df_2023 = happy_2023.rename({'Country name': 'quốc gia',  'Ladder score': 'điểm hạnh phúc', 'Logged GDP per capita': 'GDP bình quân đầu người', 'Social support': 'Hỗ trợ xã hội', 'Healthy life expectancy': 'tuổi thọ',
                                   'Freedom to make life choices': 'tự do lựa chọn cuộc sống', 'Generosity': 'Tính hào phóng', 'Perceptions of corruption': 'Nhận thức về tham nhũng'}, axis=1)
happy_df_2023.head()
# print(happy_df_2023.head())



# happy_df_2023['top_bottom_identifier'] = happy_df_2023['rank'].map(
#     top_bottom_identifier)

# print(happy_df_2023.head())

# Dropping irrelevant columns
country_mapping.drop('alpha-2', inplace=True, axis=1)
# Remove all columns between column name 'country-code' to 'iso_3166-2'
country_mapping = country_mapping.drop(
    country_mapping.loc[:, 'country-code':'iso_3166-2'].columns, axis=1)
# Remove all columns between column name 'intermediate-region' to 'intermediate-region-code'
country_mapping = country_mapping.drop(
    country_mapping.loc[:, 'intermediate-region':'intermediate-region-code'].columns, axis=1)
# print(country_mapping.head())

# đổi tên cột trong bảng country_mapping
country_mapping = country_mapping.rename(
    {'name': 'quốc gia', 'alpha-3': 'iso alpha', 'sub-region': 'vùng quốc gia', 'region': 'châu lục'}, axis=1)
# print(country_mapping.head())

# Hợp nhất hai bảng happy_df_2023 và country_mapping thành một bảng mới có tên là happy_region_df
happy_region_df = happy_df_2023.merge(
    country_mapping, on='quốc gia', how='left')
# print(happy_region_df.head())

# kiểm tra các giá trị null trong bảng happy_region_df
# print(happy_region_df.isnull().sum())


# kiểm tra các giá trị null trong cột 'châu lục' sau khi merge 2 bảng
nan_region_rows = happy_region_df[happy_region_df['châu lục'].isnull()]
# print(nan_region_rows)

# sửa tên quốc gia trong bảng happy_region_df để khớp với bảng country_mapping và bảng happy_2023

# turkey -> turkiye
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    'Turkey', 'Turkiye', regex=True)

# Palestine, State of ----> State of Palestine
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    'Palestine, State of', 'State of Palestine', regex=True)

# Côte D'Ivoire ----> Ivory Coast
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    "Côte D'Ivoire", 'Ivory Coast', regex=True)

# Macedonia ----> North Macedonia
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    'Macedonia', 'North Macedonia', regex=True)

# Hong Kong ----> Hong Kong S.A.R. of China
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    'Hong Kong', 'Hong Kong S.A.R. of China', regex=True)

# Taiwan ----> Taiwan Province of China
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    'Taiwan', 'Taiwan Province of China', regex=True)

# Czech Republic ----> Czechia
country_mapping['quốc gia'] = country_mapping['quốc gia'].str.replace(
    'Czech Republic', 'Czechia', regex=True)

# Merge lại hai bảng happy_df_2023 và country_mapping thành một bảng mới có tên là happy_region_df
happy_region_df = happy_df_2023.merge(
    country_mapping, on='quốc gia', how='left')

# print(happy_region_df.head())

# kiểm tra các giá trị null trong cột 'tuổi thọ'sau khi merge 2 bảng
nan_hlf_rows = happy_region_df[happy_region_df['tuổi thọ'].isnull(
)]
# print(nan_hlf_rows)
happy_region_df.loc[98, 'tuổi thọ'] = '74.5'

# print(nan_hlf_rows)
# kiểm tra các giá trị null trong bảng happy_region_df
nan_region_rows = happy_region_df[happy_region_df['châu lục'].isnull()]
# print(nan_region_rows)

happy_region_df.loc[33, 'châu lục'] = 'Europe'
happy_region_df.loc[33, 'vùng quốc gia'] = 'Southern Europe'
happy_region_df.loc[33, 'iso alpha'] = 'XXK'

happy_region_df.loc[70, 'châu lục'] = 'Europe'
happy_region_df.loc[70, 'vùng quốc gia'] = 'Southern Europe'
happy_region_df.loc[70, 'iso alpha'] = 'BIH'

happy_region_df.loc[85, 'châu lục'] = 'Africa'
happy_region_df.loc[85, 'vùng quốc gia'] = 'Sub-Saharan Africa'
happy_region_df.loc[85, 'iso alpha'] = 'COG'

happy_region_df.loc[132, 'châu lục'] = 'Africa'
happy_region_df.loc[132, 'vùng quốc gia'] = 'Sub-Saharan Africa'
happy_region_df.loc[132, 'iso alpha'] = 'COD'

# print(happy_region_df)

# happy_region_df.tail(10)
# print(happy_region_df.isnull().sum())

happy_region_df_3cluster = happy_region_df[['điểm hạnh phúc', 'GDP bình quân đầu người',
                                            'Hỗ trợ xã hội', 'tự do lựa chọn cuộc sống', 'Tính hào phóng', 'Nhận thức về tham nhũng','tuổi thọ']]
# phân cụm dữ liệu trên bằng phương pháp KMeans với số cụm là 3 cụm
# lưu file happy_region_df_3cluster thành file csv
happy_region_df_3cluster.to_csv('happy_region_df_3cluster.csv', index=False)


# hiển thị các điểm dữ liệu trên đồ thị với màu sắc tương ứng với cụm mà nó thuộc về

def show_cluster():
    # phân cụm dùng thuật toán kmeans với số cụm là 3 cụm
    kmeans = KMeans(n_clusters=3, random_state=0).fit(happy_region_df_3cluster)
    # thêm cột nhãn cụm vào bảng happy_region_df_3cluster để phân biệt các cụm
    happy_region_df_3cluster['nhãn'] = kmeans.labels_
    #hiển thị thông tin quốc gia và nhãn cụm tương ứng của nó ra terminal 
    print(happy_region_df_3cluster[['điểm hạnh phúc', 'nhãn']])
    #lưu ra 1 file csv mới mappping nhãn cụm với các quốc gia tương ứng của bảng happy_df_2023 với cột điểm hạnh phúc phải trùng với cột điểm hạnh phúc của bảng happy_region_df_3cluster
    happy_df_2023['nhãn'] = happy_region_df_3cluster['nhãn']
    happy_df_2023.to_csv('happy_df_2023_cluster.csv', index=False)
    
    # hiển thị các điểm dữ liệu trên đồ thị với màu sắc tương ứng với cụm mà nó thuộc về và khoanh vùng các cụm bằng đường viền màu đen
    sns.scatterplot(x='GDP bình quân đầu người', y='điểm hạnh phúc', hue='nhãn', data=happy_region_df_3cluster, palette=['green', 'orange', 'blue'], legend='full', alpha=0.3)
    plt.title('Phân cụm dữ liệu')
    plt.xlabel('GDP bình quân đầu người')
    plt.ylabel('điểm hạnh phúc')
    plt.show()
    
# xây dựng form nhập liệu để người dùng nhập vào các thông tin cần thiết để dự đoán điểm hạnh phúc của một quốc gia

# khoi tao bien de luu gia tri cua cac bien
gdp_binh_quan_dau_nguoi = 0
Ho_tro_xa_hoi = 0
Tu_do_lua_chon_cuoc_song = 0
Tinh_hao_phong = 0
Nhan_thuc_ve_tham_nhuc = 0
tuoi_tho = 0

def input_data():
    lbl1 = Label(window, text="GDP bình quân đầu người",
                 font=("Arial Bold", 10))
    lbl1.grid(column=0, row=6)
    txt1 = Entry(window, width=20)
    txt1.grid(column=1, row=6)
    lbl2 = Label(window, text="Hỗ trợ xã hội", font=("Arial Bold", 10))
    lbl2.grid(column=0, row=7)
    txt2 = Entry(window, width=20)
    txt2.grid(column=1, row=7)
    lbl3 = Label(window, text="tự do lựa chọn cuộc sống",
                 font=("Arial Bold", 10))
    lbl3.grid(column=0, row=8)
    txt3 = Entry(window, width=20)
    txt3.grid(column=1, row=8)
    lbl4 = Label(window, text="Tính hào phóng", font=("Arial Bold", 10))
    lbl4.grid(column=0, row=9)
    txt4 = Entry(window, width=20)
    txt4.grid(column=1, row=9)
    lbl5 = Label(window, text="Nhận thức về tham nhũng",
                 font=("Arial Bold", 10))
    lbl5.grid(column=0, row=10)
    txt5 = Entry(window, width=20)
    txt5.grid(column=1, row=10)
    lbl6 = Label(window, text="tuổi thọ", font=("Arial Bold", 10))
    lbl6.grid(column=0, row=11)
    txt6 = Entry(window, width=20)
    txt6.grid(column=1, row=11)
    def ket_qua():
        if (txt1.get() != "" or txt2.get() != "" or txt3.get() != "" or txt4.get() != "" or txt5.get() != "" or txt6.get() != ""):
            gdp_binh_quan_dau_nguoi = float(txt1.get())
            Ho_tro_xa_hoi = float(txt2.get())
            Tu_do_lua_chon_cuoc_song = float(txt3.get())
            Tinh_hao_phong = float(txt4.get())
            Nhan_thuc_ve_tham_nhuc = float(txt5.get())
            tuoi_tho = float(txt6.get())
            # áp dụng mô hình hồi quy tuyến tính để dự đoán điểm hạnh phúc của một quốc gia
            # đầu vào của mô hình là các thông tin về GDP bình quân đầu người, Hỗ trợ xã hội, tự do lựa chọn cuộc sống, Tính hào phóng, Nhận thức về tham nhũng, tuổi thọ
            # đầu ra của mô hình là điểm hạnh phúc của một quốc gia
            # đọc file csv chứa dữ liệu đã được xử lý trước đó
            df = pd.read_csv('happy_region_df_3cluster.csv')
            # print(df)
            # tạo một mảng chứa các giá trị của các biến đầu vào
            X = df[['GDP bình quân đầu người', 'Hỗ trợ xã hội', 'tự do lựa chọn cuộc sống',
                    'Tính hào phóng', 'Nhận thức về tham nhũng', 'tuổi thọ']]
            # tạo một mảng chứa các giá trị của biến đầu ra
            y = df['điểm hạnh phúc']
            # tạo một mô hình hồi quy tuyến tính
            model = LinearRegression()
            # đưa dữ liệu vào mô hình để huấn luyện
            model.fit(X, y)
            # dự đoán điểm hạnh phúc của một quốc gia
            y_pred = model.predict([[gdp_binh_quan_dau_nguoi, Ho_tro_xa_hoi,
                Tu_do_lua_chon_cuoc_song, Tinh_hao_phong, Nhan_thuc_ve_tham_nhuc, tuoi_tho]])
            lbl7 = Label(window, text="Dự đoán điểm hạnh phúc của một quốc gia là: " +
                str(y_pred), font=("Arial Bold", 10))
            lbl7.grid(column=0, row=12)
        else:
            lbl7 = Label(window, text="Bạn chưa nhập đủ thông tin",
                font=("Arial Bold", 10))
            lbl7.grid(column=0, row=12)
    btn5 = Button(window, text="Kết quả", command=ket_qua)
    btn5.grid(column=1, row=12)
def diem_tb_tung_chau_luc():
    mean_happiness = happy_region_df.groupby(
        'vùng quốc gia')[['điểm hạnh phúc']].mean()
    mean_happiness = mean_happiness.sort_values(
    by=['điểm hạnh phúc'], ascending=False)
    # hiển thị trên form 
    lbl8 = Label(window, text="Điểm trung bình của từng châu lục", font=("Arial Bold", 10))
    lbl8.grid(column=0, row=13)
    lbl9 = Label(window, text=mean_happiness, font=("Arial Bold", 10))
    lbl9.grid(column=0, row=14)
    # hiển thị trên đồ thị
    mean_happiness.plot(kind='bar', figsize=(10, 6))
    plt.xlabel('vùng quốc gia') # add to x-label to the plot
    plt.ylabel('điểm hạnh phúc') # add y-label to the plot
    plt.title('Điểm trung bình của từng châu lục') # add title to the plot
    plt.show()

def do_thi_hinh_tron():
    fig = px.sunburst(data_frame=happy_region_df,
    path=["châu lục", "vùng quốc gia", "quốc gia"],
    values="điểm hạnh phúc",
    color="điểm hạnh phúc",
    color_continuous_scale='RdYlGn',
    width=1000,
    height=1000,
    title='Happiness score sunburst - region / sub region / country')
    fig.show()

def ban_do_the_gioi():
    happy_world_map = px.choropleth(happy_region_df, locations="iso alpha",
    color="thứ hạng", scope='world', title="Thứ hạng hạnh phúc của các quốc gia trên thế giới",
    color_continuous_scale="rdylgn_r", hover_name="quốc gia")
    happy_world_map.show()

# tạo form nhập liệu
window = Tk()
window.title("Dự đoán điểm hạnh phúc của một quốc gia")
window.geometry('500x300')
# hiển thị các nút btn theo dạng cột và cách nhau 10 đơn vị
btn4 = Button(window, text="Dự đoán điểm hạnh phúc", command=input_data)
btn4.grid(column=0, row=5)

btn6 = Button(window, text="Kết quả phân cụm", command=show_cluster)
btn6.grid(column=0, row=15)

btn7= Button(window, text="Điểm trung bình của từng châu lục", command=diem_tb_tung_chau_luc)
btn7.grid(column=0, row=25)

btn8= Button(window, text="Đồ thị hình tròn", command=do_thi_hinh_tron)
btn8.grid(column=0, row=35)

btn9 = Button(window, text="Bản đồ thế giới", command=ban_do_the_gioi)
btn9.grid(column=0, row=45)
window.mainloop()