import streamlit as st
import pandas as pd
import numpy as np
# c. Add streamlit text at top
st.write("# Pokemon Dashboard") 
# d. Add a streamlit slider
num_rows = st.slider("Number of rows", 1, 10000, 5)
# e. Add a Numpy random seed (between 2-50)
np.random.seed(42) 
# Generate fictitious data
data = []
for i in range(num_rows):
    data.append({
        "Preview": f"https://picsum.photos/400/200?lock={i}",
        "Views": np.random.randint(0, 1000),
        "Active": np.random.choice([True, False]),
        "Category": np.random.choice(["🔥 LLM", "📊 Data", "⚙️ Tool"]),
        "Progress": np.random.randint(1, 100),
    })
# 3. Add line chart (Top 10 Views)
data = pd.DataFrame(data)
st.subheader("Top 10 Views")
st.line_chart(data["Views"].head(10))
# f. Configure streamlit image and progress column
config = {
    "Preview": st.column_config.ImageColumn(),
    "Progress": st.column_config.ProgressColumn(),
}
# g. Add toggle to enable editing
if st.toggle("Enable editing"):
    edited_data = st.data_editor(data, column_config=config, use_container_width=True)
else:
    st.dataframe(data, column_config=config, use_container_width=True)