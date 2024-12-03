import pandas as pd

unit_groups = {
    "กลุ่มที่ 1 พล.1 รอ.": [
        "พล.1 รอ.", "ร.31 รอ.", "ร.31 พัน.1 รอ.", "ร.31 พัน.2 รอ.", "ร.31 พัน.3 รอ.",
        "ป.1 พัน.1 รอ.", "ป.1 พัน.11 รอ.", "ป.1 พัน.31 รอ.",
        "ม.พัน.4 พล.1 รอ.", "ช.พัน.1 พล.1 รอ.", "ส.พัน.1"
    ],
        "กลุ่มที่ 2 พล.ร.2 รอ.": [
        "พล.ร.2 รอ.", "ร.2 รอ.", "ร.2 พัน.1 รอ.", "ร.2 พัน.2 รอ.", "ร.2 พัน.3 รอ.",
        "ร.12 รอ.", "ร.12 พัน.1 รอ.", "ร.12 พัน.2 รอ.", "ร.12 พัน.3 รอ.",
        "ร.21 รอ.", "ร.21 พัน.1 รอ.", "ร.21 พัน.2 รอ.", "ร.21 พัน.3 รอ.",
        "ป.2 พัน.2 รอ.", "ป.2 พัน.12 รอ.", "ป.2 พัน.21 รอ.", "ป.2 พัน.102 รอ.",
        "ม.พัน.2 รอ. พล.ร.2 รอ.", "ม.พัน.30 รอ. พล.ร.2 รอ.", "ช.พัน.2 พล.ร.2 รอ.",
        "ส.พัน.2", "พัน.ซบร.กรม สน.2"
    ],
    "กลุ่มที่ 3 พล.ร.9": [
        "พล.ร.9", "ร.9 พัน.1", "ร.9 พัน.2", "ร.9 พัน.3",
        "ร.19 พัน.1", "ร.19 พัน.2", "ร.19 พัน.3",
        "ร.29 พัน.1", "ร.29 พัน.2", "ร.29 พัน.3",
        "ป.9 พัน.9", "ป.9 พัน.19", "ป.9 พัน.109",
        "พัน.ขส.กรม สน.พล.ร.9", "พัน.ซบร.กรม สน.พล.ร.9",
        "ม.พัน.19 พล.ร.9", "ช.พัน.9 พล.ร.9", "ส.พัน.9 พล.ร.9"
    ],
    "กลุ่มที่ 4 พล.ร.11": [
        "พล.ร.11", "พัน.ซบร.กรม สน.พล.ร.11",
        "ร.111 พัน.1", "ร.111 พัน.2", "ร.111 พัน.3",
        "ร.112 พัน.1", "ร.112 พัน.2", "ร.112 พัน.3"
    ],
    "กลุ่มที่ 5 พล.ม.2 รอ.": [
        "พล.ม.2 รอ.", "ม.1 พัน.1 รอ.", "ม.1 พัน.3 รอ.", "ม.1 พัน.17 รอ.",
        "ม.4 พัน.5 รอ.", "ม.4 พัน.11 รอ.", "ม.4 พัน.25 รอ.",
        "ม.5 พัน.20 รอ.", "ม.5 พัน.23 รอ.", "ม.5 พัน.24 รอ.",
        "ม.พัน.27 พล.ม.2 รอ.", "ม.พัน.29 รอ.", "ส.พัน.12", "พัน.ซบร.กรม สน.12"
    ],
    "กลุ่มที่ 6 พล.พัฒนา.1": [
        "พัน.พัฒนา.1", "ช.1 พัน.112 รอ.", "ช.1 พัน.52 รอ."
    ],
    "กลุ่มที่ 7 บชร.1": [
        "พัน.สพ.กระสุน 21 บชร.1", "พัน.สบร.21 บชร.1",
        "หน่วยฝึกที่ 1", "หน่วยฝึกที่ 2", "หน่วยฝึกที่ 3", "พัน.สห.11"
    ],
    "กลุ่มที่ 8 มทบ.": [
        "มทบ.12", "มทบ.13", "มทบ.14", "มทบ.15",
        "มทบ.16", "มทบ.17", "มทบ.18", "มทบ.19"
    ],
    "กลุ่มที่ 9 บก.ทภ.1": [
        "บก.ทภ.1 (ส.พัน.21 ทภ.1)"
    ],
    "กลุ่มที่ 10 ร้อย.ฝรพ.1": [
        "ร้อย.ฝรพ.1"
    ]
}

def count_by_group_with_units(df, unit_groups):
    group_counts = []

    for group_name, units in unit_groups.items():
        # Count total people in this group
        total_count = df["สังกัด(หน่วยฝึกทหารใหม่)"].isin(units).sum()

        # Count people in each unit within the group
        unit_details = (
            df[df["สังกัด(หน่วยฝึกทหารใหม่)"].isin(units)]
            .groupby("สังกัด(หน่วยฝึกทหารใหม่)")
            .size()
            .reset_index(name="จำนวนคน")
        )

        # Add units with no data and mark them as "ไม่มีข้อมูล"
        for unit in units:
            if unit not in unit_details["สังกัด(หน่วยฝึกทหารใหม่)"].values:
                unit_details = pd.concat(
                    [unit_details, pd.DataFrame({"สังกัด(หน่วยฝึกทหารใหม่)": [unit], "จำนวนคน": [0]})],
                    ignore_index=True
                )

        # Sort unit details alphabetically for clarity
        unit_details = unit_details.sort_values(by="สังกัด(หน่วยฝึกทหารใหม่)").reset_index(drop=True)

        group_counts.append({
            "กลุ่ม": group_name,
            "จำนวนรวมในกลุ่ม": total_count,
            "หน่วยย่อย": unit_details
        })

    return group_counts

def count_by_unit(df):
    unit_counts = df["สังกัด(หน่วยฝึกทหารใหม่)"].value_counts().reset_index()
    unit_counts.columns = ["หน่วย", "จำนวนคน"]

    # Map each unit to its group
    group_mapping = {}
    for group_name, units in unit_groups.items():
        for unit in units:
            group_mapping[unit] = group_name

    unit_counts["กลุ่ม"] = unit_counts["หน่วย"].map(group_mapping).fillna("ไม่ระบุ")

    return unit_counts

def generate_group_report(df, unit_groups):
    report = []

    for group_name, units in unit_groups.items():
        for unit in units:
            # Count the number of people in each unit
            count = df[df["สังกัด(หน่วยฝึกทหารใหม่)"] == unit].shape[0]
            report.append({"กลุ่ม": group_name, "หน่วย": unit, "จำนวนคน": count})

    # Convert report to DataFrame
    report_df = pd.DataFrame(report)
    return report_df
