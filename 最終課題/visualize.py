import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 日本語化設定
plt.rcParams['font.family'] = 'Hiragino Sans' 

def visualize_data():
    conn = sqlite3.connect('travel_data.db')
    df = pd.read_sql_query("SELECT * FROM hotels", conn)
    conn.close()

    # 異常値の除外（1000円以下やレビュー0をカット）
    df = df[(df['price'] > 1000) & (df['review'] > 0)]

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # 1. 棒グラフ（平均価格）
    sns.barplot(x='area', y='price', data=df, ax=ax[0], palette='coolwarm', ci=None)
    ax[0].set_title('東京 vs 福岡：平均宿泊価格の比較')
    ax[0].set_ylabel('平均価格 (円)')

    # 2. 散布図 + 相関関係の線（回帰線）
    # 東京と福岡で色を分けて線を引きます
    sns.regplot(x='price', y='review', data=df[df['area']=='東京'], ax=ax[1], 
                scatter_kws={'alpha':0.5}, line_kws={'color':'blue'}, label='東京の傾向')
    sns.regplot(x='price', y='review', data=df[df['area']=='福岡'], ax=ax[1], 
                scatter_kws={'alpha':0.5}, line_kws={'color':'red'}, label='福岡の傾向')

    ax[1].set_title('価格とレビュー評価の相関関係')
    ax[1].set_xlabel('宿泊価格 (円)')
    ax[1].set_ylabel('レビュー点数')
    ax[1].legend() 
    ax[1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('analysis_result_with_line.png')
    print("相関線入りのグラフを 'analysis_result_with_line.png' として保存しました！")
    plt.show()

if __name__ == "__main__":
    visualize_data()