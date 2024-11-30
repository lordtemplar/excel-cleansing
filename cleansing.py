import pandas as pd
import random

def clean_data(df):
    report = []

    # Step 0: Remove hidden spaces in "เลขบัตรประชาชน"
    initial_count = len(df)
    if "เลขบัตรประชาชน" in df.columns:
        df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.replace(" ", "").str.strip()
        report.append({
            "ฟังก์ชันที่ใช้": "ลบช่องว่างที่ซ่อนอยู่ในคอลัมน์ เลขบัตรประชาชน",
            "จำนวนข้อมูลก่อน": initial_count,
            "จำนวนข้อมูลที่ถูกลบ": 0,
            "จำนวนข้อมูลหลัง": len(df)
        })

    # Step 1: Convert all data to string
    df = df.astype(str)  # แปลงข้อมูลทั้งหมดใน DataFrame เป็น String
    report.append({
        "ฟังก์ชันที่ใช้": "แปลงข้อมูลทุกคอลัมน์เป็น String",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 2: Remove rows where "เลขบัตรประชาชน" does not have 13 digits
    initial_count = len(df)
    df = df[df["เลขบัตรประชาชน"].str.len() == 13]
    report.append({
        "ฟังก์ชันที่ใช้": "ลบข้อมูลที่เลขบัตรประชาชนไม่ครบ 13 หลัก",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": initial_count - len(df),
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 3: Remove duplicate rows based on "เลขบัตรประชาชน"
    initial_count = len(df)
    df = df.drop_duplicates(subset="เลขบัตรประชาชน", keep='first')
    report.append({
        "ฟังก์ชันที่ใช้": "ลบข้อมูลที่ซ้ำในเลขบัตรประชาชน",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": initial_count - len(df),
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 4: Fill missing values in "ทักษะ"
    initial_count = len(df)
    df["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"] = df["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"].fillna("ไม่มี")
    report.append({
        "ฟังก์ชันที่ใช้": "เติมค่า 'ไม่มี' ในคอลัมน์ทักษะ",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 5: Validate blood types and replace invalid or missing values
    valid_blood_types = ["เอ", "บี", "โอ", "เอบี"]
    initial_count = len(df)
    df["กรุ๊ปเลือด"] = df["กรุ๊ปเลือด"].apply(
        lambda x: x if x in valid_blood_types else random.choice(valid_blood_types)
    )
    report.append({
        "ฟังก์ชันที่ใช้": "ตรวจสอบและเติมกรุ๊ปเลือดที่ไม่ถูกต้อง",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 6: Replace all values in "คำนำหน้า" with "พลทหาร"
    df["คำนำหน้า"] = "พลทหาร"

    # Step 7: Clean "เบอร์โทรศัพท์"
    def clean_phone_number(phone):
        phone = str(phone).strip()
        if len(phone) < 10:  # If less than 10 digits
            return phone.zfill(10)  # Pad with leading zeros
        elif len(phone) > 10:  # If more than 10 digits
            return phone[:10]  # Trim to 10 digits
        return phone  # Return as-is if exactly 10 digits

    df["เบอร์โทรศัพท์"] = df["เบอร์โทรศัพท์"].apply(clean_phone_number)

    # Fill missing "เบอร์โทรศัพท์" by copying from the row above
    initial_count = len(df)
    df["เบอร์โทรศัพท์"] = df["เบอร์โทรศัพท์"].fillna(method='ffill')
    report.append({
        "ฟังก์ชันที่ใช้": "แก้ไขเบอร์โทรศัพท์ให้ครบ 10 หลัก",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 8: Remove duplicate rows across all columns
    initial_count = len(df)
    df = df.drop_duplicates()
    report.append({
        "ฟังก์ชันที่ใช้": "ลบข้อมูลที่ซ้ำในทุกคอลัมน์",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": initial_count - len(df),
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Convert report to DataFrame
    clean_report = pd.DataFrame(report)

    return df, clean_report
