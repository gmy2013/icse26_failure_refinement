import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data for the table
data = {
    'Model': ['CodeT5', 'CodeT5-distill-CodeLLama-7B', 'CodeT5-distill-CodeQwen-7B',
              'CodeT5-distill-DeepSeek', 'CodeT5-distill-GPT4'],
    'Correctness': [2.8, 3.1, 3.4, 4.1, 4.3],
    'Completeness': [2.9, 3.3, 3.4, 3.9, 4.2],
    'Fluency': [3.2, 3.5, 3.6, 4.3, 4.3]
}

# Convert the data into a pandas dataframe
df = pd.DataFrame(data)

# Reshape the data for the violin plot
df_melted = df.melt(id_vars=["Model"], value_vars=["Correctness", "Completeness", "Fluency"],
                    var_name="Evaluation Metric", value_name="Score")

plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# Create the violin plot with proper color differentiation for each model
sns.violinplot(x="Evaluation Metric", y="Score", hue="Model", data=df_melted,
               inner="quart", palette="Set2", dodge=True)

# Add color bar for better visualization
plt.title("Human Evaluation Results", fontsize=16)
plt.xlabel("Evaluation Metric", fontsize=12)
plt.ylabel("Score", fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()


def is_valid_bracket_sequence(seq):
    balance = 0
    for ch in seq:
        balance += 1 if ch == '(' else -1
        if balance < 0:
            return False
    return balance == 0

def count_valid_reversals(s):
    n = len(s)
    valid_count = 0

    # Convert to +/-1 array for easier prefix sum manipulation
    a = [1 if c == '(' else -1 for c in s]
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + a[i]

    # Iterate all possible intervals to reverse
    for l in range(n):
        for r in range(l, n):
            # Reverse subarray [l, r] in transformed bracket representation
            b = a[:l] + [-x for x in a[l:r+1][::-1]] + a[r+1:]
            # Check validity via prefix sum
            balance = 0
            is_valid = True
            for x in b:
                balance += x
                if balance < 0:
                    is_valid = False
                    break
            if is_valid and balance == 0:
                valid_count += 1

    return valid_count
