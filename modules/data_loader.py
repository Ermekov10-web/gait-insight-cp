"""Read gait CSV files without storing uploaded data on disk."""

import csv

import pandas as pd


def load_gait_csv(source):
    """Read semicolon/decimal-comma and comma/decimal-point CSV files."""
    source.seek(0)
    header = source.readline().decode("utf-8-sig")
    source.seek(0)
    delimiter = csv.Sniffer().sniff(header, delimiters=";,").delimiter
    frame = pd.read_csv(
        source,
        sep=delimiter,
        decimal="," if delimiter == ";" else ".",
        encoding="utf-8-sig",
        dtype={"subject": "string", "Participant_ID": "string"},
    )
    frame.columns = frame.columns.str.strip()
    if "Participant_ID" not in frame and "subject" in frame:
        frame["Participant_ID"] = frame["subject"]
    return frame


def validate_gait_data(frame):
    if frame.empty:
        return False, "CSV contains no data rows."
    if "Participant_ID" not in frame or frame["Participant_ID"].dropna().empty:
        return False, "CSV must contain a subject or Participant_ID column."
    measurements = frame.filter(regex=r"_pct_GC_\d+$").select_dtypes("number")
    if measurements.empty or not measurements.notna().any().any():
        return False, "CSV must contain numeric gait-cycle measurements."
    return True, ""
