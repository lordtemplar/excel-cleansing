import streamlit as st
import pandas as pd
from cleansing import clean_data
from unit_groups import unit_groups, count_by_group, count_by_unit

st.title("โปรแกรมทำความสะอาดข้อมูล Excel พร้อมแก้ไขชื่อหน่วย")

# Upload Excel file
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Load the uploaded file into a DataFrame
        df = pd.read_excel(uploaded_file)

        # Display original data
        st.subheader("ข้อมูลดิบ (ก่อนทำความสะอาด):")
        st.dataframe(df)

        # Clean the data
        cleaned_df = clean_data(df)

        # Display cleaned data
        st.subheader("ข้อมูลที่ทำความสะอาดแล้ว:")
        st.dataframe(cleaned_df)

        # Edit unit names
        st.subheader("แก้ไขชื่อหน่วย:")
        unique_units = cleaned_df["สังกัด(หน่วยฝึกทหารใหม่)"].unique()

        edited_units = {}
        for unit in unique_units:
            new_name = st.text_input(f"แก้ไขชื่อหน่วย: {unit}", value=unit)
            edited_units[unit] = new_name

        if st.button("บันทึกการแก้ไข"):
            # Apply changes to the DataFrame
            cleaned_df["สังกัด(หน่วยฝึกทหารใหม่)"] = cleaned_df["สังกัด(หน่วยฝึกทหารใหม่)"].replace(edited_units)
            st.success("บันทึกการแก้ไขเรียบร้อย!")

            # Display updated data
            st.subheader("ข้อมูลหลังแก้ไขชื่อหน่วย:")
            st.dataframe(cleaned_df)

        # Count people by group
        st.subheader("จำนวนคนในแต่ละกลุ่ม:")
        group_counts = count_by_group(cleaned_df, unit_groups)
        st.dataframe(group_counts)

        # Count people by unit
        st.subheader("จำนวนคนในแต่ละหน่วย:")
        unit_counts = count_by_unit(cleaned_df)
        st.dataframe(unit_counts)

        # Provide download link for the cleaned and updated data
        st.subheader("ดาวน์โหลดข้อมูลที่แก้ไขแล้ว:")
        @st.cache_data
        def convert_df_to_excel(dataframe):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Cleaned Data')
            processed_data = output.getvalue()
            return processed_data

        cleaned_file = convert_df_to_excel(cleaned_df)
        st.download_button(
            label="📥 ดาวน์โหลดไฟล์ Excel",
            data=cleaned_file,
            file_name="Updated_Cleaned_Data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("กรุณาอัปโหลดไฟล์ Excel เพื่อเริ่มต้น")
