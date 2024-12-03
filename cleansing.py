import pandas as pd
import random

def clean_data(df):
    report = []

    # Step 0: ลบช่องว่างและอักขระพิเศษใน "เลขบัตรประชาชน"
    initial_count = len(df)
    if "เลขบัตรประชาชน" in df.columns:
        df["เลขบัตรประชาชน"] = df["เลขบัตรประชาชน"].astype(str).str.replace(r"\s+", "", regex=True).str.strip()
        report.append({
            "ฟังก์ชันที่ใช้": "ลบช่องว่างและอักขระพิเศษในคอลัมน์ เลขบัตรประชาชน",
            "จำนวนข้อมูลก่อน": initial_count,
            "จำนวนข้อมูลที่ถูกลบ": 0,
            "จำนวนข้อมูลหลัง": len(df)
        })

    # Step 1: แปลงข้อมูลทุกคอลัมน์เป็น String
    initial_count = len(df)
    df = df.astype(str)
    report.append({
        "ฟังก์ชันที่ใช้": "แปลงข้อมูลทุกคอลัมน์เป็น String",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 2: ตรวจสอบ "เลขบัตรประชาชน" ให้ครบ 13 หลัก
    initial_count = len(df)
    invalid_rows = df[df["เลขบัตรประชาชน"].str.len() != 13]
    df = df[df["เลขบัตรประชาชน"].str.len() == 13]
    report.append({
        "ฟังก์ชันที่ใช้": "ลบข้อมูลที่เลขบัตรประชาชนไม่ครบ 13 หลัก",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": len(invalid_rows),
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 3: ลบข้อมูลที่ซ้ำในคอลัมน์ "เลขบัตรประชาชน"
    initial_count = len(df)
    df = df.drop_duplicates(subset="เลขบัตรประชาชน", keep='first')
    report.append({
        "ฟังก์ชันที่ใช้": "ลบข้อมูลที่ซ้ำในเลขบัตรประชาชน",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": initial_count - len(df),
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 4: เติมค่า "ไม่มี" ในคอลัมน์ "ทักษะ"
    initial_count = len(df)
    df["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"] = df["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"].fillna("ไม่มี")
    report.append({
        "ฟังก์ชันที่ใช้": "เติมค่า 'ไม่มี' ในคอลัมน์ทักษะ",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 5: ตรวจสอบกรุ๊ปเลือด
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

    # Step 6: แก้ไขคำนำหน้า
    df["คำนำหน้า"] = "พลทหาร"

    # Step 7: แก้ไขเบอร์โทรศัพท์
    def clean_phone_number(phone):
        phone = str(phone).strip()
        if len(phone) < 10:
            return phone.zfill(10)
        elif len(phone) > 10:
            return phone[:10]
        return phone

    df["เบอร์โทรศัพท์"] = df["เบอร์โทรศัพท์"].apply(clean_phone_number)
    df["เบอร์โทรศัพท์"] = df["เบอร์โทรศัพท์"].fillna(method='ffill')
    report.append({
        "ฟังก์ชันที่ใช้": "แก้ไขเบอร์โทรศัพท์ให้ครบ 10 หลัก",
        "จำนวนข้อมูลก่อน": initial_count,
        "จำนวนข้อมูลที่ถูกลบ": 0,
        "จำนวนข้อมูลหลัง": len(df)
    })

    # Step 8: ลบข้อมูลที่ซ้ำในทุกคอลัมน์
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
