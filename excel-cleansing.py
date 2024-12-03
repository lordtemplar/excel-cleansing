import streamlit as st
import pandas as pd
from cleansing import clean_data
from unit_groups import unit_groups, count_by_group_with_units, count_by_unit

st.set_page_config(layout="centered")  # ตั้งค่า layout เป็นแบบ "centered"

st.title("โปรแกรมทำความสะอาดข้อมูล Excel พร้อมแสดงรายงาน")

# Upload Excel file
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Load the uploaded file into a DataFrame
        original_df = pd.read_excel(uploaded_file)  # เก็บข้อมูลดิบเดิมใน original_df

        # Display original data
        st.subheader("ข้อมูลดิบ (ก่อนทำความสะอาด):")
        st.dataframe(original_df, use_container_width=True)  # แสดงข้อมูลดิบเดิม

        # Clean the data and generate a report
        cleaned_df, clean_report = clean_data(original_df)  # ส่ง original_df เข้าสู่ clean_data

        # Display cleaned data
        st.subheader("ข้อมูลที่ทำความสะอาดแล้ว:")
        st.dataframe(cleaned_df, use_container_width=True)  # แสดงข้อมูลหลังการ Clean

        # Display clean report
        st.subheader("รายงานการทำความสะอาดข้อมูล:")
        st.dataframe(clean_report, use_container_width=True)

        # Display counts by group with subunits (including units with no data)
        st.subheader("จำนวนคนในแต่ละกลุ่ม (พร้อมหน่วยย่อย):")
        group_counts_with_units = count_by_group_with_units(cleaned_df, unit_groups)

        for group in group_counts_with_units:
            st.write(f"**{group['กลุ่ม']}** (จำนวนรวม: {group['จำนวนรวมในกลุ่ม']} คน)")
            st.dataframe(group["หน่วยย่อย"], use_container_width=True)

        # Count people by unit
        st.subheader("จำนวนคนในแต่ละหน่วย:")
        unit_counts = count_by_unit(cleaned_df)

        # Add total row to unit counts
        total_row = pd.DataFrame([["รวม", unit_counts["จำนวนคน"].sum(), ""]], columns=unit_counts.columns)
        unit_counts = pd.concat([unit_counts, total_row], ignore_index=True)

        st.dataframe(unit_counts, use_container_width=True)

        # Function to create a summary report for all units in all groups
        def create_summary_report(cleaned_df, unit_groups):
            summary_report = []

            for group_name, units in unit_groups.items():
                for unit in units:
                    # Count the number of people in each unit
                    unit_count = cleaned_df[cleaned_df["สังกัด(หน่วยฝึกทหารใหม่)"] == unit].shape[0]
                    summary_report.append({
                        "กลุ่ม": group_name,
                        "หน่วย": unit,
                        "จำนวนคน": unit_count
                    })

            return pd.DataFrame(summary_report)

        # Generate the summary report
        summary_report = create_summary_report(cleaned_df, unit_groups)

        # Add a download button for the summary report
        st.subheader("ดาวน์โหลดรายงานรวมทุกหน่วย")
        @st.cache_data
        def convert_summary_to_excel(dataframe):
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                dataframe.to_excel(writer, index=False, sheet_name='Summary Report')
            processed_data = output.getvalue()
            return processed_data

        summary_file = convert_summary_to_excel(summary_report)
        st.download_button(
            label="📥 ดาวน์โหลดรายงานรวมทุกหน่วย (Excel)",
            data=summary_file,
            file_name="Summary_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("กรุณาอัปโหลดไฟล์ Excel เพื่อเริ่มต้น")
