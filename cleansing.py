import pandas as pd
import random

def clean_data(df):
    # Rename columns for better readability
    df.columns = [
        "สังกัด(หน่วยฝึกทหารใหม่)", "คำนำหน้า", "ชื่อ", "นามสกุล", 
        "เลขบัตรประชาชน", "กรุ๊ปเลือด", "เบอร์โทรศัพท์", "อาชีพ", 
        "ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"
    ]

    # Step 1: Remove rows where "เลขบัตรประชาชน" does not have 13 digits
    df = df[df["เลขบัตรประชาชน"].astype(str).str.len() == 13]

    # Step 2: Remove duplicate rows based on "เลขบัตรประชาชน"
    df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.strip()
    df = df.drop_duplicates(subset="เลขบัตรประชาชน", keep='first')

    # Step 3: Fill missing values
    df["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"] = df["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"].fillna("ไม่มี")

    # Step 4: Validate blood types in "กรุ๊ปเลือด" and replace invalid or missing values
    valid_blood_types = ["เอ", "บี", "โอ", "เอบี"]
    df["กรุ๊ปเลือด"] = df["กรุ๊ปเลือด"].apply(
        lambda x: x if x in valid_blood_types else random.choice(valid_blood_types)
    )

    # Step 5: Replace all values in "คำนำหน้า" with "พลทหาร"
    df["คำนำหน้า"] = "พลทหาร"

    # Step 6: Clean "เบอร์โทรศัพท์"
    def clean_phone_number(phone):
        if pd.isna(phone):  # If the value is missing
            return None  # Temporary placeholder to be filled later
        phone = str(phone).strip()
        if len(phone) < 10:  # If less than 10 digits
            return phone.zfill(10)  # Pad with leading zeros
        elif len(phone) > 10:  # If more than 10 digits
            return phone[:10]  # Trim to 10 digits
        return phone  # Return as-is if exactly 10 digits

    df["เบอร์โทรศัพท์"] = df["เบอร์โทรศัพท์"].apply(clean_phone_number)

    # Fill missing "เบอร์โทรศัพท์" by copying from the row above
    df["เบอร์โทรศัพท์"] = df["เบอร์โทรศัพท์"].fillna(method='ffill')

    # Step 7: Remove duplicate rows across all columns
    df = df.drop_duplicates()

    # Step 8: Ensure "เลขบัตรประชาชน" is a string
    df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str)

    return df
