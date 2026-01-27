import sqlite3

class HotelSearchTool:
    def __init__(self, db_name="travel_data.db"):
        self.db_name = db_name

    def search_best_hotels(self, area, max_price):
        """
        指定されたエリアと予算内で、レビュー評価の高い順にホテルを検索する
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # SQLクエリ：プレースホルダを使って安全に検索
        query = """
        SELECT name, price, review 
        FROM hotels 
        WHERE area = ? AND price <= ? 
        ORDER BY review DESC 
        LIMIT 5
        """
        
        cursor.execute(query, (area, max_price))
        results = cursor.fetchall()
        conn.close()
        return results

def main():
    searcher = HotelSearchTool()
    
    print("=== ホテル検索ツール ===")
    print("東京 か 福岡 を入力してください。")
    area_input = input("エリアを選択: ")
    
    try:
        price_input = int(input("最大予算（円）を入力: "))
        
        print(f"\n--- {area_input}で予算 {price_input}円以内のおすすめホテル ---")
        recommendations = searcher.search_best_hotels(area_input, price_input)
        
        if recommendations:
            for i, (name, price, review) in enumerate(recommendations, 1):
                print(f"{i}. {name}")
                print(f"   価格: {price}円 / レビュー: ⭐{review}")
        else:
            print("該当するホテルが見つかりませんでした。条件を変えてみてください。")
            
    except ValueError:
        print("予算は数字で入力してください。")

if __name__ == "__main__":
    main()