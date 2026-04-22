import seaborn as sns
import matplotlib.pyplot as plt

# Load Titanic dataset
titanic = sns.load_dataset('titanic')
sns.set(style='darkgrid')


# ------------------------------
# HISTOGRAMS & KDE
# ------------------------------
def plot_histograms(data):
    # 1. Basic Histogram
    plt.figure()
    sns.histplot(data=data, x='age', bins=20)
    plt.title("1. Basic Histogram of Age")
    plt.savefig("hist_basic_age.png")

    # 2. Histogram with KDE
    plt.figure()
    sns.histplot(data=data, x='age', bins=20, kde=True)
    plt.title("2. Histogram with KDE")
    plt.savefig("hist_with_kde.png")

    # 3. Histogram with Hue (Overlay)
    plt.figure()
    sns.histplot(data=data, x='age', bins=20, kde=True, hue='sex', palette='coolwarm')
    plt.title("3. Histogram with Hue (Overlay)")
    plt.savefig("hist_kde_hue_overlay.png")

    # 4. Histogram with Hue (Stacked)
    plt.figure()
    sns.histplot(data=data, x='age', bins=20, kde=True, hue='sex', palette='coolwarm', multiple='stack')
    plt.title("4. Histogram with Stacked Bars")
    plt.savefig("hist_kde_hue_stack.png")

    # 5. Histogram with Hue (Fill)
    plt.figure()
    sns.histplot(data=data, x='age', bins=20, kde=True, hue='sex', palette='coolwarm', multiple='fill')
    plt.title("5. Histogram with Filled Proportions")
    plt.savefig("hist_fill.png")

    # 6. KDE Only
    plt.figure()
    sns.kdeplot(data=data, x='age', hue='sex', palette='coolwarm', fill=True)
    plt.title("6. KDE Plot Only")
    plt.savefig("kde_only.png")

    # 7. Step Histogram
    plt.figure()
    sns.histplot(data=data, x='age', hue='sex', palette='coolwarm', fill=True, element='step', kde=True)
    plt.title("7. Step Histogram")
    plt.savefig("step_plot.png")

    # 8. Poly Histogram
    plt.figure()
    sns.histplot(data=data, x='age', hue='sex', palette='coolwarm', fill=True, element='poly', kde=True)
    plt.title("8. Poly Histogram")
    plt.savefig("poly_plot.png")


# ------------------------------
# BAR PLOTS
# ------------------------------
def plot_barplots(data):
    # 9. Countplot by Class
    plt.figure()
    sns.countplot(data=data, x='class', palette='viridis')
    plt.title("9. Countplot of Passenger Class")
    plt.savefig("countplot_class.png")

    # 10. Barplot - Average Fare by Class
    plt.figure()
    sns.barplot(data=data, x='class', y='fare', palette='cool')
    plt.title("10. Barplot: Average Fare by Class")
    plt.savefig("barplot_fare_by_class.png")


# ------------------------------
# BOX & VIOLIN PLOTS
# ------------------------------
def plot_box_violin(data):
    # 11. Boxplot - Age by Sex
    plt.figure()
    sns.boxplot(data=data, x='sex', y='age', palette='Set2')
    plt.title("11. Boxplot: Age by Sex")
    plt.savefig("boxplot_age_by_sex.png")

    # 12. Violinplot - Age by Sex
    plt.figure()
    sns.violinplot(data=data, x='sex', y='age', palette='Set2')
    plt.title("12. Violinplot: Age by Sex")
    plt.savefig("violinplot_age_by_sex.png")


# ------------------------------
# SCATTER & LINE PLOTS
# ------------------------------
def plot_scatter_line(data):
    # 13. Scatterplot - Age vs Fare
    plt.figure()
    sns.scatterplot(data=data, x='age', y='fare', hue='sex', palette='Set1')
    plt.title("13. Scatterplot: Age vs Fare")
    plt.savefig("scatter_age_fare.png")

    # 14. Lineplot - Average Fare by Age (with smoothing)
    plt.figure()
    sns.lineplot(data=data, x='age', y='fare', ci='sd')
    plt.title("14. Lineplot: Fare by Age")
    plt.savefig("lineplot_fare_by_age.png")


# ------------------------------
# HEATMAP / CORRELATION
# ------------------------------
def plot_heatmap(data):
    plt.figure()
    numeric_data = data[['age', 'fare', 'pclass']].dropna()
    corr = numeric_data.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title("15. Correlation Heatmap")
    plt.savefig("correlation_heatmap.png")


# Run all
# Uncomment to execute each different plot
if __name__ == "__main__":
    plot_histograms(titanic)
    plot_barplots(titanic)
    plot_box_violin(titanic)
    plot_scatter_line(titanic)
    plot_heatmap(titanic)

    # Show the last figure
    plt.show()