from __future__ import annotations

from pathlib import Path

from PIL import Image

from libreprimus.image_transforms.review_index import write_review_pages


def test_review_index_generated_without_raw_source_embedding(tmp_path: Path) -> None:
    contact = tmp_path / "contact_sheets" / "synthetic.jpg"
    contact.parent.mkdir()
    Image.new("RGB", (8, 8), "white").save(contact)

    index_path, page_count = write_review_pages(
        out_dir=tmp_path,
        image_summaries=[
            {
                "image_id": "synthetic",
                "file_name": "synthetic.png",
                "contact_sheet": "experiments/results/image-transforms/stage3p/contact_sheets/synthetic.jpg",
                "candidate_types": ["sparse_dot_like_candidate"],
            }
        ],
        global_contact_sheet="experiments/results/image-transforms/stage3p/contact_sheets/global.jpg",
    )

    index_text = (tmp_path / "review_index.html").read_text(encoding="utf-8")
    assert page_count == 1
    assert index_path.endswith("review_index.html")
    assert "Flags are review aids" not in index_text
    assert "third_party/LiberPrimusPages" not in index_text
    assert (tmp_path / "review_pages/synthetic.html").is_file()
