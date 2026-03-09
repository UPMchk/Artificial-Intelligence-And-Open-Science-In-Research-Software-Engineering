import csv
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    project_root = Path(__file__).resolve().parent.parent
    input_csv = project_root / "results" / "figures_per_paper.csv"
    output_png = project_root / "results" / "figures_per_paper.png"

    paper_ids = []
    num_figures = []

    with input_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            paper_ids.append(row["paper_id"])
            num_figures.append(int(row["num_figures"]))

    plt.figure(figsize=(10, 6))
    plt.bar(paper_ids, num_figures)
    plt.xlabel("Paper")
    plt.ylabel("Number of figures")
    plt.title("Number of figures per article")
    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()

    print(f"Gráfico guardado en: {output_png}")


if __name__ == "__main__":
    main()