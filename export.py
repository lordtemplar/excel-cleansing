import pandas as pd
import streamlit as st

# อัปโหลดไฟล์ Excel ที่ 1
st.title("แปลงข้อมูลจาก Excel ที่ 1 ไปยัง Excel ที่ 2")

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

    # แสดงตัวอย่างข้อมูล
    st.write("ข้อมูลที่แปลงแล้ว:")
    st.dataframe(df2)

    # ดาวน์โหลดไฟล์ Excel ที่ 2
    output_file = "Excel_2_Output.xlsx"
    df2.to_excel(output_file, index=False, engine="openpyxl")
    with open(output_file, "rb") as file:
        st.download_button(
            label="ดาวน์โหลดไฟล์ Excel ที่ 2",
            data=file,
            file_name="Excel_2_Output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
