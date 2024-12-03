import pandas as pd
import streamlit as st
from io import BytesIO

def compare_excel(file1, file2):
    # โหลดข้อมูลจาก Excel ทั้งสองไฟล์
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # หาข้อมูลที่เหมือนกัน
    common_data = pd.merge(df1, df2, how='inner')
    
    # หาข้อมูลที่แตกต่างกัน
    diff_data = pd.concat([df1, df2]).drop_duplicates(keep=False)
    
    return common_data, diff_data

def download_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

# สร้าง Streamlit App
st.title("Excel File Comparison")

# อัพโหลดไฟล์ Excel 2 ไฟล์
file1 = st.file_uploader("Upload First Excel File", type=["xlsx"])
file2 = st.file_uploader("Upload Second Excel File", type=["xlsx"])

if file1 and file2:
    # เปรียบเทียบไฟล์
    common_data, diff_data = compare_excel(file1, file2)
    
    # แสดงผลข้อมูลที่เหมือนและแตกต่าง
    st.subheader("Common Data")
    st.write(common_data)
    
    st.subheader("Different Data")
    st.write(diff_data)
    
    # ปุ่มดาวน์โหลดไฟล์ที่แตกต่าง
    st.download_button(
        label="Download Different Data as Excel",
        data=download_excel(diff_data),
        file_name="different_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
