"""Load the original study CSVs from the configured research directory."""

from pathlib import Path

import streamlit as st

from modules.data_loader import load_gait_csv

CONDITIONS = ("Baseline", "Verbal", "VR")


@st.cache_data(show_spinner=False)
def _read_research_csv(path, modified_ns):
    with Path(path).open("rb") as source:
        return load_gait_csv(source)


def load_research_data(directory):
    research = {"waveforms": {}, "discrete": {}}
    for group, prefix in (
        ("waveforms", "Kinematics_Kinetics"),
        ("discrete", "Discrete_Parameters"),
    ):
        for condition in CONDITIONS:
            path = Path(directory) / f"{prefix}_{condition}.csv"
            if path.is_file():
                frame = _read_research_csv(str(path), path.stat().st_mtime_ns)
                if not frame.empty and "Participant_ID" in frame:
                    research[group][condition] = frame
    return research
