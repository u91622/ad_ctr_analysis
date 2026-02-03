import csv
import random
from datetime import datetime, timedelta
import math

def generate_data(num_rows=50000):
    print(f"Generating {num_rows} rows of synthetic ad data (Funnel: Click -> Reg -> Conv)...")
    
    random.seed(42)
    
    # ID Settings
    ad_ids = [f"ad_{str(i).zfill(5)}" for i in range(1, 101)]
    user_ids = [f"u_{str(i).zfill(6)}" for i in range(1, int(num_rows/5))]
    
    # Configuration Options
    device_types = ['mobile', 'desktop', 'tablet']
    device_weights = [60, 35, 5]
    
    browsers = ['Chrome', 'Safari', 'Edge', 'Firefox']
    browser_weights = [50, 30, 10, 10]
    
    regions = ['TW-Taipei', 'TW-NewTaipei', 'TW-Taichung', 'TW-Kaohsiung', 'US-CA', 'US-NY']
    
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
    age_weights = [15, 35, 25, 15, 10]
    
    exp_groups = ['control', 'test_creative_A']
    
    # Time Settings
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    total_seconds = int((end_date - start_date).total_seconds())
    
    data_rows = []
    
    for i in range(num_rows):
        # Base Fields
        imp_id = f"imp_{str(i).zfill(8)}"
        u_id = random.choice(user_ids)
        a_id = random.choice(ad_ids)
        
        # Datetime
        rand_sec = random.randint(0, total_seconds)
        ts = start_date + timedelta(seconds=rand_sec)
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")
        weekday = ts.weekday() # 0 = Monday
        
        # Dimensions
        dev = random.choices(device_types, weights=device_weights)[0]
        browser = random.choices(browsers, weights=browser_weights)[0]
        geo = random.choice(regions)
        age = random.choices(age_groups, weights=age_weights)[0]
        grp = random.choice(exp_groups)
        
        # CPC Bid
        cpc = round(random.uniform(0.5, 5.0), 2)
        
        # --- Click Logic ---
        base_ctr = 0.02
        prob_click = base_ctr
        
        if dev == 'mobile': prob_click *= 1.5           # Higher CTR on mobile
        if grp == 'test_creative_A': prob_click *= 1.15  # Higher CTR for experimental group
        if age == '25-34': prob_click *= 1.2             # Age group weighted
        
        # Noise
        prob_click += random.gauss(0, 0.005)
        if prob_click < 0: prob_click = 0
        
        is_click = 1 if random.random() < prob_click else 0
        
        # --- Funnel Logic: Click -> Registration -> Conversion ---
        is_reg = 0
        is_conv = 0
        
        if is_click == 1:
            # 30% chance of registration after click
            prob_reg = 0.30
            
            # Desktop preferred for registration (ease of typing)
            if dev == 'desktop': prob_reg *= 1.2
            
            if random.random() < prob_reg:
                is_reg = 1
                
                # 20% chance of conversion after registration
                prob_conv = 0.20
                
                # Higher conversion on weekends
                if weekday >= 5: prob_conv *= 1.3
                
                if random.random() < prob_conv:
                    is_conv = 1
                
        row = [imp_id, u_id, a_id, ts_str, dev, browser, geo, age, cpc, grp, is_click, is_reg, is_conv]
        data_rows.append(row)
        
    # Save to CSV
    headers = ['impression_id', 'user_id', 'ad_id', 'timestamp', 'device_type', 'browser', 'geo', 'age_group', 'cpc_bid', 'experiment_group', 'is_click', 'is_registration', 'is_conversion']
    
    csv_file = 'ad_data.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_rows)
        
    print(f"Saved {num_rows} rows to {csv_file}")

if __name__ == "__main__":
    generate_data()
