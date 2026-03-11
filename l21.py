import pandas as pd
import numpy as np
num_rows = 5
data = []
for i in range(num_rows):
    data.append({
        "Preview": f"https://picsum.photos/400/200?lock={i}",
        "Views": np.random.randint(0, 1000),
        "Active": np.random.choice([True, False]),
        "Category": np.random.choice(["🔥 LLM", "📊 Data", "⚙️ Tool"]),
        "Progress": np.random.randint(1, 100),
    })
print("--- Raw Data List ---")
print(data)
df = pd.DataFrame(data)
print("\n--- Pandas DataFrame ---")
print(df)