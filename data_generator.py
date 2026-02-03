import csv
import random
from datetime import datetime, timedelta
import math

def generate_data(num_rows=50000):
    print(f"正在生成 {num_rows} 筆合成廣告資料 (含漏斗: 點擊 -> 註冊 -> 轉換)...")
    
    random.seed(42)
    
    # ID 設定
    ad_ids = [f"ad_{str(i).zfill(5)}" for i in range(1, 101)]
    user_ids = [f"u_{str(i).zfill(6)}" for i in range(1, int(num_rows/5))]
    
    # 選項配置
    device_types = ['mobile', 'desktop', 'tablet']
    device_weights = [60, 35, 5]
    
    browsers = ['Chrome', 'Safari', 'Edge', 'Firefox']
    browser_weights = [50, 30, 10, 10]
    
    regions = ['TW-Taipei', 'TW-NewTaipei', 'TW-Taichung', 'TW-Kaohsiung', 'US-CA', 'US-NY']
    
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    age_weights = [15, 35, 25, 15, 10]
    
    exp_groups = ['control', 'test_creative_A']
    
    # 時間設定
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    total_seconds = int((end_date - start_date).total_seconds())
    
    data_rows = []
    
    for i in range(num_rows):
        # 基礎欄位
        imp_id = f"imp_{str(i).zfill(8)}"
        u_id = random.choice(user_ids)
        a_id = random.choice(ad_ids)
        
        # 時間戳記
        rand_sec = random.randint(0, total_seconds)
        ts = start_date + timedelta(seconds=rand_sec)
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        weekday = ts.weekday() # 0=星期一
        
        # 維度
        dev = random.choices(device_types, weights=device_weights)[0]
        browser = random.choices(browsers, weights=browser_weights)[0]
        geo = random.choice(regions)
        age = random.choices(age_groups, weights=age_weights)[0]
        grp = random.choice(exp_groups)
        
        # CPC (每次點擊成本)
        cpc = round(random.uniform(0.5, 5.0), 2)
        
        # --- 點擊 (Click) 邏輯 ---
        base_ctr = 0.02
        prob_click = base_ctr
        
        if dev == 'mobile': prob_click *= 1.5      # 行動裝置點擊率較高
        if grp == 'test_creative_A': prob_click *= 1.15 # 實驗組點擊率較高
        if age == '25-34': prob_click *= 1.2       # 特定年齡層加權
        
        # 雜訊 (Noise)
        prob_click += random.gauss(0, 0.005)
        if prob_click < 0: prob_click = 0
        
        is_click = 1 if random.random() < prob_click else 0
        
        # --- 漏斗邏輯: 點擊 -> 註冊 (Registration) -> 轉換 (Conversion) ---
        is_reg = 0
        is_conv = 0
        
        if is_click == 1:
            # 點擊後，有 30% 機率註冊
            prob_reg = 0.30
            
            # 桌機註冊較容易 (打字方便)
            if dev == 'desktop': prob_reg *= 1.2
            
            if random.random() < prob_reg:
                is_reg = 1
                
                # 註冊後，有 20% 機率轉換 (購買)
                prob_conv = 0.20
                
                # 週末轉換率較高
                if weekday >= 5: prob_conv *= 1.3
                
                if random.random() < prob_conv:
                    is_conv = 1
                
        row = [imp_id, u_id, a_id, ts_str, dev, browser, geo, age, cpc, grp, is_click, is_reg, is_conv]
        data_rows.append(row)
        
    # 儲存為 CSV
    headers = ['impression_id', 'user_id', 'ad_id', 'timestamp', 'device_type', 'browser', 'geo', 'age_group', 'cpc_bid', 'experiment_group', 'is_click', 'is_registration', 'is_conversion']
    
    csv_file = 'ad_data.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_rows)
        
    print(f"已儲存 {num_rows} 筆資料至 {csv_file}")

if __name__ == "__main__":
    generate_data()
