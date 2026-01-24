import sqlite3

class JobDatabase:
    def __init__(self, db_name="job_analysis.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """分析に必要なカラムを持つテーブルを作成"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS job_openings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    pref TEXT,
                    salary_min INTEGER,
                    salary_max INTEGER,
                    job_category TEXT,
                    source_url TEXT UNIQUE
                )
            ''')
            conn.commit()

    def insert_job(self, job_data):
        """データを保存（source_urlが同じなら無視する設定）"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                query = '''
                    INSERT OR IGNORE INTO job_openings 
                    (title, company, location, pref, salary_min, salary_max, job_category, source_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                cursor.execute(query, job_data)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

# --- ここからテスト実行 ---
if __name__ == "__main__":
    db = JobDatabase()
    
    # テスト用のダミーデータ（東京と秋田）
    test_data = [
        ('カフェ店員', 'Indeed喫茶', '東京都新宿区', '東京都', 1163, 1300, '飲食', 'http://test1.com'),
        ('コンビニスタッフ', 'Indeed商店', '秋田県秋田市', '秋田県', 951, 1000, '小売', 'http://test2.com')
    ]

    for data in test_data:
        success = db.insert_job(data)
        if success:
            print(f"Saved: {data[0]} in {data[3]}")

    print("\nDBの準備が完了しました！")