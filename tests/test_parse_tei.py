from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from make_parse_tei import parse_tei_file


def test_parse_paper2():
    xml_path = Path("data/tei/paper2.tei.xml")
    result = parse_tei_file(xml_path)

    assert result["paper_id"] == "paper2"
    assert isinstance(result["title"], str)
    assert isinstance(result["abstract"], str)
    assert isinstance(result["num_figures"], int)
    assert isinstance(result["links"], list)

    assert result["title"] != ""
    assert result["abstract"] != ""
    assert result["num_figures"] >= 0
