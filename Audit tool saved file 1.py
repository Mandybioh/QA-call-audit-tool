~score = st.slider(f"Quality Score for {row['File_Name']}", 1, 5, key=f"score_{i}")
comments = st.text_area(f"Comments for {row['File_Name']}", key=f"comments_{i}")
selected.at[i, 'QA_Score'] = score
selected.at[i, 'QA_Comments'] = comments