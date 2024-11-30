import pandas as pd
import streamlit as st

# อัปโหลดไฟล์ Excel ที่ 1
st.title("แปลงและแบ่งข้อมูล Excel")

uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel ที่ 1", type=["xlsx"])
if uploaded_file is not None:
    # อ่านไฟล์ Excel
    df1 = pd.read_excel(uploaded_file)

    # แปลงคอลัมน์ให้ตรงตามที่ต้องการ
    df2 = pd.DataFrame({
        "ลำดับที่": range(1, len(df1) + 1),
        "คำนำหน้า": df1["คำนำหน้า"],
        "ชื่อ": df1["ชื่อ"],
        "นามสกุล": df1["นามสกุล"],
        "หมายเลขบัตรประชาชน": df1["เลขบัตรประชาชน"],
        "กรุ๊ปเลือด": df1["กรุ๊ปเลือด"],
        "หมายเลขติดต่อ": df1["เบอร์โทรศัพท์"],
        "อาชีพ": df1["อาชีพ"],
        "ทักษะ": df1["ทักษะ(ตัวอย่าง,ไกด์นำเที่ยว,พ่อครัว,ช่างตัดผม)"],
    })

    # แสดงตัวอย่างข้อมูลทั้งหมด
    st.write("ข้อมูลทั้งหมดที่แปลงแล้ว (Excel แบบที่ 2):")
    st.dataframe(df2)

    # แบ่งข้อมูลเป็นไฟล์ย่อย ไฟล์ละ 1000 แถว
    chunk_size = 1000
    chunks = [df2.iloc[i:i + chunk_size] for i in range(0, len(df2), chunk_size)]

    # ดาวน์โหลดไฟล์ย่อย
    for idx, chunk in enumerate(chunks, start=1):
        output_file = f"Excel_2_Output_Part_{idx}.xlsx"
        chunk.to_excel(output_file, index=False, engine="openpyxl")

        with open(output_file, "rb") as file:
            st.download_button(
                label=f"ดาวน์โหลดไฟล์ย่อยที่ {idx}",
                data=file,
                file_name=f"Excel_2_Output_Part_{idx}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.success("แบ่งไฟล์เสร็จสิ้น! ดาวน์โหลดไฟล์ทั้งหมดได้ด้านบน")
