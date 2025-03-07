import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="Data sweeper", layout='wide')

#custom CSS
st.markdown(
"""
<style>
.stApp{
  background-color: black;
  color: white;
}
.stButton>button {
    margin: 10px 0;
}
</style>
""",
unsafe_allow_html=True
)

#title and description 
st.title("Datasweeper Sterling Integrator by Furqan Ali Khan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for quarter 3!") 

# Maximum file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# file uploader
uploaded_files = st.file_uploader("Upload your file (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
   for file in uploaded_files:
        # Check file size
        if file.size > MAX_FILE_SIZE:
            st.error(f"File {file.name} is too large. Maximum size is 10 MB")
            continue

        file_ext = os.path.splitext(file.name)[-1].lower()

        with st.spinner(f"Processing {file.name}..."):
            try:
                if file_ext == ".csv":
                    df = pd.read_csv(file)
                elif file_ext == ".xlsx":
                    df = pd.read_excel(file)
                else:
                    st.error(f"Unsupported file type: {file_ext}")       
                    continue

                if df.empty:
                    st.error(f"File {file.name} is empty!")
                    continue

                #file details
                st.write("File Information:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"Total Rows: {len(df)}")
                with col2:
                    st.write(f"Total Columns: {len(df.columns)}")
                with col3:
                    st.write(f"Memory Usage: {df.memory_usage().sum() / 1024:.2f} KB")

                st.write("Preview the head of the Dataframe")
                st.dataframe(df.head())

                # data cleaning options
                st.subheader("Data Cleaning Options")
                if st.checkbox(f"Clean data for {file.name}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(f"Remove duplicates from {file.name}"):
                            initial_rows = len(df)
                            df.drop_duplicates(inplace=True)
                            removed_rows = initial_rows - len(df)
                            st.write(f"Removed {removed_rows} duplicate rows!")

                    with col2:
                        if st.button(f"Fill missing values for {file.name}"):
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            missing_before = df[numeric_cols].isnull().sum().sum()
                            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write(f"Filled {missing_before} missing values in numeric columns")

                    st.subheader("Select Columns to Keep")        
                    columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
                    df = df[columns]

                #data visualization
                st.subheader("Data Visualization")
                if st.checkbox(f"Show Visualization for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        viz_type = st.selectbox(
                            "Select visualization type",
                            ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot"],
                            key=f"viz_{file.name}"
                        )
                        
                        x_col = st.selectbox("Select X-axis column", df.columns, key=f"x_{file.name}")
                        if viz_type != "Box Plot":
                            y_col = st.selectbox("Select Y-axis column", numeric_cols, key=f"y_{file.name}")
                            
                        if viz_type == "Bar Chart":
                            st.bar_chart(data=df, x=x_col, y=y_col)
                        elif viz_type == "Line Chart":
                            st.line_chart(data=df, x=x_col, y=y_col)
                        elif viz_type == "Scatter Plot":
                            fig = px.scatter(df, x=x_col, y=y_col)
                            st.plotly_chart(fig)
                        elif viz_type == "Box Plot":
                            fig = px.box(df, x=x_col, y=numeric_cols)
                            st.plotly_chart(fig)
                    else:
                        st.warning("No numeric columns available for visualization")

                # Conversion Options
                st.subheader("Conversion Options")    
                conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)  
                if st.button(f"Convert {file.name}"):
                   buffer = BytesIO()
                   if conversion_type == "CSV":
                       df.to_csv(buffer, index=False)
                       file_name = file.name.replace(file_ext, ".csv")
                       mime_type = "text/csv"

                   elif conversion_type == "Excel":
                       df.to_excel(buffer, index=False)
                       file_name = file.name.replace(file_ext, ".xlsx")
                       mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                   buffer.seek(0)

                   st.download_button(
                       label=f"Download {file.name} as {conversion_type}",
                       data=buffer,
                       file_name=file_name,
                       mime=mime_type
                   )  
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                continue
                
   st.success("All files processed successfully!")           

