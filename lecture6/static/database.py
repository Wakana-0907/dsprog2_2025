import sqlite3
from typing import List
from models import Area, Forecast
from datetime import date


class WeatherDatabase:
    def __init__(self, db_path: str = "weather.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """データベースの初期化とテーブル作成"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # エリアテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS areas (
                    area_code TEXT PRIMARY KEY,
                    area_name TEXT NOT NULL
                )
            """)
            
            # 予報テーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS forecasts (
                    area_code TEXT,
                    forecast_date TEXT,
                    weather_code TEXT,
                    temp_max INTEGER,
                    temp_min INTEGER,
                    pop INTEGER,
                    wind TEXT,
                    fetched_at TEXT,
                    PRIMARY KEY (area_code, forecast_date)
                )
            """)
            
            conn.commit()
    
    def get_all_areas(self) -> List[Area]:
        """すべてのエリアを取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT area_code, area_name FROM areas")
            rows = cursor.fetchall()
            return [Area(area_code=row[0], area_name=row[1]) for row in rows]
    
    def save_areas(self, areas: List[Area]):
        """エリアを保存"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for area in areas:
                cursor.execute(
                    "INSERT OR REPLACE INTO areas (area_code, area_name) VALUES (?, ?)",
                    (area.area_code, area.area_name)
                )
            conn.commit()
    
    def save_forecasts(self, forecasts: List[Forecast]):
        """予報を保存"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for f in forecasts:
                cursor.execute(
                    """INSERT OR REPLACE INTO forecasts 
                       (area_code, forecast_date, weather_code, temp_max, temp_min, pop, wind, fetched_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        f.area_code,
                        f.forecast_date.isoformat(),
                        f.weather_code,
                        f.temp_max,
                        f.temp_min,
                        f.pop,
                        f.wind,
                        f.fetched_at.isoformat() if f.fetched_at else None
                    )
                )
            conn.commit()
    
    def get_forecasts(self, area_code: str) -> List[Forecast]:
        """特定エリアの予報を取得"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT area_code, forecast_date, weather_code, temp_max, temp_min, pop, wind, fetched_at
                   FROM forecasts WHERE area_code = ? ORDER BY forecast_date""",
                (area_code,)
            )
            rows = cursor.fetchall()
            return [
                Forecast(
                    area_code=row[0],
                    forecast_date=date.fromisoformat(row[1]),
                    weather_code=row[2],
                    temp_max=row[3],
                    temp_min=row[4],
                    pop=row[5],
                    wind=row[6],
                    fetched_at=row[7]
                )
                for row in rows
            ]
