import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path


TEI_NS = {"tei": "http://www.tei-c.org/ns/1.0"}
URL_PATTERN = re.compile(r"(https?://[^\s<>\"]+|www\.[^\s<>\"]+)", re.IGNORECASE)


def clean_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split()).strip()


def get_title(root: ET.Element) -> str:
    title_el = root.find(".//tei:titleStmt/tei:title", TEI_NS)
    if title_el is None:
        return ""
    return clean_text("".join(title_el.itertext()))


def get_abstract(root: ET.Element) -> str:
    abstract_el = root.find(".//tei:profileDesc/tei:abstract", TEI_NS)
    if abstract_el is None:
        return ""
    return clean_text(" ".join(abstract_el.itertext()))


def count_figures(root: ET.Element) -> int:
    figures = root.findall(".//tei:figure", TEI_NS)
    count = 0

    for fig in figures:
        fig_type = (fig.get("type") or "").lower()
        head_el = fig.find("tei:head", TEI_NS)
        head_text = clean_text("".join(head_el.itertext())) if head_el is not None else ""

        # Excluir tablas si vienen marcadas así
        if fig_type == "table":
            continue
        if head_text.lower().startswith("table"):
            continue

        count += 1

    return count


def extract_links(root: ET.Element) -> list[str]:
    links = []

    # 1) target=... en elementos XML
    for el in root.findall(".//*[@target]"):
        target = (el.get("target") or "").strip()
        if target.startswith("http://") or target.startswith("https://"):
            links.append(target)

    # 2) URLs escritas como texto
    all_text = " ".join(root.itertext())
    for match in URL_PATTERN.findall(all_text):
        url = match.strip().rstrip(".,);]")
        if url.startswith("www."):
            url = "http://" + url
        links.append(url)

    # quitar duplicados conservando orden
    seen = set()
    unique_links = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)

    return unique_links


def parse_tei_file(xml_path: Path) -> dict:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return {
        "paper_id": xml_path.stem.replace(".tei", ""),
        "filename": xml_path.name,
        "title": get_title(root),
        "abstract": get_abstract(root),
        "num_figures": count_figures(root),
        "links": extract_links(root),
    }


def write_abstracts_csv(records: list[dict], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "filename", "title", "abstract"])
        for r in records:
            writer.writerow([r["paper_id"], r["filename"], r["title"], r["abstract"]])


def write_figures_csv(records: list[dict], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "filename", "title", "num_figures"])
        for r in records:
            writer.writerow([r["paper_id"], r["filename"], r["title"], r["num_figures"]])


def write_links_csv(records: list[dict], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["paper_id", "filename", "title", "link"])
        for r in records:
            if not r["links"]:
                writer.writerow([r["paper_id"], r["filename"], r["title"], ""])
            else:
                for link in r["links"]:
                    writer.writerow([r["paper_id"], r["filename"], r["title"], link])


def main() -> None:
    tei_dir = Path("data/tei")
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)

    xml_files = sorted(tei_dir.glob("*.xml"))
    if not xml_files:
        print("No se encontraron archivos XML en data/tei/")
        return

    records = [parse_tei_file(xml_file) for xml_file in xml_files]

    write_abstracts_csv(records, results_dir / "abstracts.csv")
    write_figures_csv(records, results_dir / "figures_per_paper.csv")
    write_links_csv(records, results_dir / "links_per_paper.csv")

    print(f"Procesados {len(records)} archivos TEI/XML.")
    print("Generados:")
    print("- results/abstracts.csv")
    print("- results/figures_per_paper.csv")
    print("- results/links_per_paper.csv")


if __name__ == "__main__":
    main()