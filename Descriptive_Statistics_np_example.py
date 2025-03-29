import numpy as np
import matplotlib.pyplot as plt

def analyze_salaries(salaries):
    """
    Analyzes salary distribution using mean, median, standard deviation, quartiles, and IQR.
    Also detects outliers using the IQR method and plots a box plot.
    """

    # Compute statistics
    mean_salary = np.mean(salaries)
    median_salary = np.median(salaries)
    std_dev_salary = np.std(salaries)

    # Compute Coefficient of variation
    CV_salary = std_dev_salary/mean_salary

    # Compute quartiles and IQR
    q1 = np.percentile(salaries, 25)
    q2 = np.percentile(salaries, 50)  # Same as median
    q3 = np.percentile(salaries, 75)
    iqr = q3 - q1

    # Compute SD/IQR ratio
    sd_iqr_ratio = std_dev_salary / iqr

    # Detect outliers using the IQR method
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in salaries if x < lower_bound or x > upper_bound]

    # Print results with interpretation
    print("📊 Salary Analysis Results\n" + "-" * 30)
    print(f"Mean Salary: ${mean_salary:.2f}K → (Might be skewed by high salaries)")
    print(f"Median Salary (Q2): ${median_salary:.2f}K → (Better for skewed data)")
    print(f"Standard Deviation (SD): ${std_dev_salary:.2f}K → (Measures overall spread)")
    # If mean > median, it suggests the presence of high outliers.
    # If SD is high, salaries are widely spread.
    print(f'Coefficient of variation: {CV_salary:.2f}')
    # A low CV (e.g., <10%) means less variation.
    # A high CV (>50%) means high variability.
    print(f"Q1 (25th Percentile): ${q1:.2f}K")
    print(f"Q2 (Median, 50th Percentile): ${q2:.2f}K")
    print(f"Q3 (75th Percentile): ${q3:.2f}K")
    print(f"IQR (Middle 50% Range): ${iqr:.2f}K → (Better than SD for outliers)")
    # IQR tells us how spread out the middle 50% of salaries are.
    # If SD is much larger than IQR, there are likely extreme values.
    print(f"SD/IQR Ratio: {sd_iqr_ratio:.2f} → (Higher values suggest more variation)")
    # If SD/IQR > 1, data has high variability (possibly due to outliers).
    # If SD is close to IQR, data is evenly spread.
    
    if outliers:
        print(f"Outliers (Using IQR Method): {outliers} 🚨")
    else:
        print("No extreme outliers detected ✅")
    # This method identifies salaries that are too high or too low compared to the main group.
    # This is more robust than standard deviation, especially for skewed data.

    # Plot the box plot
    plt.figure(figsize=(8, 5))
    plt.boxplot(salaries, vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))

    # Add labels and title
    plt.xlabel("Salary (in $1,000s)")
    plt.title("Salary Distribution Box Plot")

    # Show quartiles
    plt.axvline(q1, color='r', linestyle='dashed', label="Q1 (25%)")
    plt.axvline(median_salary, color='g', linestyle='dashed', label="Median (50%)")
    plt.axvline(q3, color='b', linestyle='dashed', label="Q3 (75%)")

    # Show legend
    plt.legend()

    # Display the plot
    plt.show()

# Example dataset (in $1,000s)
salaries = [35, 38, 40, 45, 50, 52, 55, 60, 62, 65, 68, 70, 75, 80, 85, 90, 95, 120]

# Run analysis
analyze_salaries(salaries)
