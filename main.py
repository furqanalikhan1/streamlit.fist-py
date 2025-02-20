import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title== "Data sweeper", layout'wide' )

#custom CSS

st.markdwon(
"""
<style>
.stApp{
  background-color: black;
  color: white;
}
</style>
""",
unsafe_allow_html=True
)

#title and description 
st.title(" Datasweeper sterling integrator by furqan ali khan ")
st.write(" Transform your files between CSV and Excl formates with bulit-in data cleaning and visualization Creating the project for quarter 3!") 



# file uploder
uploaded_files =st.file_uploader("upload your file (accepts CSV or Excel):", type=["cvs" ,"xlsx"], accept_multiple_files=(True))

if uploaded_files:
   for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1] .lower()


        if file_ext ==".csv":
            df = pd.read_csv(file)
        elif file_ext =="xlsx":
            df ==pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")       
            continue


        #file detaills
        st.write ("  perview the head of the Dataframe")
        st.dataframe(df.head)


        # data cleaning options

        st.subheader (" Data Cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inpalce=True)
                    st.erite(" Duplicates removes!")


            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols =df.select_dtypes(includes=['number']). columns
                    df[numeric_cols] = df [numeric_cols].fillna(df [numeric_cols].mean())
                    st.write("Missing vallues have been filled")


            st.subheader(" Select Columns to keep")        
            columns = st.multiselect (f" Choose for  {file.name}", df.columns,default=df.columns)
            df =df [columns]


            #data visualizat
            st.subheader("Data Visualizattion")
            if st.checkbox(f"Show Visualizattion for {file.name}"):
                 st.ber_chart(df.select_dtypes(include='number').iloc[:, :2])


             # Conversion Options
            st.subheader ("Conversion Options")    
            conversion_type =st.radio(f"Convert {file.name} to:",["CVS" ,"Excel"], key=file.name)  
            if st.button(f"Convert {file.name}"):
               buffer = BytesIO()
               if conversion_type == "CSV":
                   df.tp.cvs(buffer, index=False)
                   file_name = file.name. replace(file_ext, ".csv")
                   mime_type = "text/csv"



            elif conversion_type  == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformate-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                date=buffer,
                file_name=file_name,
                mime=mime_type
              )  
   st.success(" All files processwd successfully!")           

