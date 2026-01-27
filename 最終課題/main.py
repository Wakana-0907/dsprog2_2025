import requests
import sqlite3
import time

class HotelFetcher:
    def __init__(self, app_id):
        #「キーワード検索API」に変更
        self.api_url = "https://app.rakuten.co.jp/services/api/Travel/KeywordHotelSearch/20170426"
        self.app_id = app_id

    def fetch_by_keyword(self, keyword, area_name):
        all_hotels = []
        for page in range(1, 4):
            print(f"--- {area_name} ({keyword}) の {page}ページ目を収集中... ---")
            
            params = {
                "applicationId": self.app_id,
                "format": "json",
                "keyword": keyword,
                "page": page,
                "formatVersion": 2
            }
            
            try:
                res = requests.get(self.api_url, params=params, timeout=15)
                
                if res.status_code != 200:
                    print(f"停止：{res.status_code} エラー")
                    print(f"詳細: {res.text}")
                    break
                    
                data = res.json()
                if "hotels" not in data or not data["hotels"]:
                    print("これ以上のデータはありません。")
                    break
                
                for h in data["hotels"]:
                    info = h[0]["hotelBasicInfo"]
                    price = info.get("hotelMinCharge")
                    review = info.get("reviewAverage")
                    
                    if price and review:
                        all_hotels.append({
                            "area": area_name,
                            "name": info["hotelName"],
                            "price": price,
                            "review": review
                        })
                time.sleep(1) 
            except Exception as e:
                print(f"通信エラー: {e}")
                break
        return all_hotels

class HotelDatabase:
    def __init__(self, db_name="travel_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("DROP TABLE IF EXISTS hotels")
        self.conn.execute("""
            CREATE TABLE hotels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area TEXT,
                name TEXT,
                price INTEGER,
                review REAL
            )
        """)

    def save_hotels(self, hotels):
        query = "INSERT INTO hotels (area, name, price, review) VALUES (?, ?, ?, ?)"
        for h in hotels:
            self.conn.execute(query, (h["area"], h["name"], h["price"], h["review"]))
        self.conn.commit()

def main():
    MY_APP_ID = "1021822633563982352" 
    fetcher = HotelFetcher(MY_APP_ID)
    db = HotelDatabase()

    # 地域コードではなく、「駅名」で検索します
    search_list = [
        {"keyword": "東京駅", "label": "東京"},
        {"keyword": "博多駅", "label": "福岡"}
    ]
    
    total_count = 0
    for item in search_list:
        results = fetcher.fetch_by_keyword(item["keyword"], item["label"])
        if results:
            db.save_hotels(results)
            print(f"{item['label']} のデータを {len(results)}件 保存完了！")
            total_count += len(results)

    if total_count > 0:
        print(f"\n合計 {total_count} 件保存！")
    else:
        print("\nエラーです、確認してください！")

if __name__ == "__main__":
    main()