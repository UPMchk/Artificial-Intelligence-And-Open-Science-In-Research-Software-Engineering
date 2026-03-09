import csv
import re
from pathlib import Path

from wordcloud import WordCloud


STOPWORDS = {
    "the", "and", "of", "to", "in", "a", "for", "is", "that", "on", "with",
    "as", "are", "this", "we", "be", "by", "an", "or", "from", "at", "our",
    "can", "their", "these", "which", "have", "has", "was", "were", "it",
    "its", "also", "than", "such", "using", "used", "use", "into", "between",
    "paper", "study", "studies", "article", "research", "results", "result",
    "method", "methods", "approach", "work"
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    words = [w for w in text.split() if len(w) > 2 and w not in STOPWORDS]
    return " ".join(words)


def main():
    project_root = Path(__file__).resolve().parent.parent
    input_csv = project_root / "results" / "abstracts.csv"
    output_png = project_root / "results" / "keyword_cloud.png"

    abstracts = []

    with input_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            abstract = row["abstract"].strip()
            if abstract:
                abstracts.append(abstract)

    full_text = clean_text(" ".join(abstracts))

    wc = WordCloud(width=1600, height=900, background_color="white")
    wc.generate(full_text)
    wc.to_file(output_png)

    print(f"Keyword cloud guardada en: {output_png}")


if __name__ == "__main__":
    main()