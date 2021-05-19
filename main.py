import pandas as pd
import streamlit as st
import os

cwd = os.getcwd()
os.chdir("/Users/elliotkantor/Documents/python_personal/GoogleAPI/eli.kant03 Sheets")
import ezsheets

os.chdir(cwd)
st.set_page_config(layout="wide")

st.title("2021 Seniors College Data")


@st.cache
def get_sheet():
    spreadsheet = ezsheets.Spreadsheet(os.environ["URL"])
    sheet = spreadsheet.sheets[0]
    return sheet


@st.cache
def get_dataframe(sheet):
    n_rows, n_cols = 78, 3
    df = pd.DataFrame(sheet.getRows())
    df.columns = df.iloc[0]
    df = df[1:]
    df = df.iloc[:n_rows, :n_cols]
    return df


@st.cache
def unpack_names(df):
    new_df = pd.concat(
        [
            pd.Series(row["Name"], row["Students"].split("\n"))
            for _, row in df.iterrows()
        ]
    ).reset_index()
    new_df2 = pd.concat(
        [
            pd.Series(row["Address"], row["Students"].split("\n"))
            for _, row in df.iterrows()
        ]
    ).reset_index()
    new_df.columns = ["Student", "School"]
    new_df2.columns = ["Student", "Address"]

    new_df["School Address"] = new_df2["Address"]
    return new_df


sheet = get_sheet()
df = get_dataframe(sheet)
df = unpack_names(df)

st.dataframe(df)

"## Search for a student"
student_query = st.text_input("Enter student name")
results = df.loc[df.Student.str.contains(student_query.title())]
if student_query and results.shape[0] > 0:
    st.write(results)
else:
    "No results found"

"## Search by school"
chosen_schools = st.multiselect("Select one or more schools", list(df.School.unique()))
if chosen_schools:
    st.write(df.loc[df["School"].isin(chosen_schools)])
