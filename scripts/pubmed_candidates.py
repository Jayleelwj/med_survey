#!/usr/bin/env python3
"""Build a deduplicated PubMed candidate corpus for the MS MRI AI survey."""

from __future__ import annotations

import json
import subprocess
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path


BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
QUERIES = {
    "broad_ai": '"multiple sclerosis"[Title/Abstract] AND (MRI[Title/Abstract] OR "magnetic resonance"[Title/Abstract]) AND ("deep learning"[Title/Abstract] OR "machine learning"[Title/Abstract] OR "artificial intelligence"[Title/Abstract]) AND 2015:2026[dp]',
    "lesion_segmentation": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND (lesion[Title/Abstract] AND segmentation[Title/Abstract]) AND 2015:2026[dp]',
    "diagnosis": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND (diagnosis[Title/Abstract] OR classification[Title/Abstract]) AND ("machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract]) AND 2015:2026[dp]',
    "prognosis": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND (prognosis[Title/Abstract] OR progression[Title/Abstract] OR EDSS[Title/Abstract]) AND ("machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract]) AND 2015:2026[dp]',
    "longitudinal": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND (longitudinal[Title/Abstract] OR "new lesion"[Title/Abstract] OR "enlarging lesion"[Title/Abstract]) AND (automatic[Title/Abstract] OR automated[Title/Abstract] OR "deep learning"[Title/Abstract]) AND 2015:2026[dp]',
    "advanced_biomarkers": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND ("central vein sign"[Title/Abstract] OR "paramagnetic rim"[Title/Abstract] OR "cortical lesion"[Title/Abstract]) AND (automatic[Title/Abstract] OR automated[Title/Abstract] OR "machine learning"[Title/Abstract] OR "deep learning"[Title/Abstract]) AND 2015:2026[dp]',
    "spinal_cord": '"multiple sclerosis"[Title/Abstract] AND "spinal cord"[Title/Abstract] AND MRI[Title/Abstract] AND (segmentation[Title/Abstract] OR "deep learning"[Title/Abstract] OR automated[Title/Abstract]) AND 2015:2026[dp]',
    "atrophy_quantification": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND (atrophy[Title/Abstract] OR volumetry[Title/Abstract] OR quantification[Title/Abstract]) AND (automatic[Title/Abstract] OR automated[Title/Abstract] OR "deep learning"[Title/Abstract]) AND 2015:2026[dp]',
    "radiomics": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND radiomics[Title/Abstract] AND 2015:2026[dp]',
    "real_world": '"multiple sclerosis"[Title/Abstract] AND MRI[Title/Abstract] AND ("real-world"[Title/Abstract] OR workflow[Title/Abstract] OR deployed[Title/Abstract]) AND (AI[Title/Abstract] OR automated[Title/Abstract] OR computational[Title/Abstract]) AND 2015:2026[dp]',
}


def get(url: str) -> bytes:
    last_error: subprocess.CalledProcessError | None = None
    for attempt in range(5):
        try:
            result = subprocess.run(
                [
                    "curl",
                    "-sS",
                    "-L",
                    "--http1.1",
                    "--retry",
                    "4",
                    "--retry-all-errors",
                    "--max-time",
                    "90",
                    url,
                ],
                check=True,
                capture_output=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    assert last_error is not None
    raise last_error


def esearch(term: str, retmax: int = 40) -> list[str]:
    params = urllib.parse.urlencode(
        {"db": "pubmed", "retmode": "json", "retmax": retmax, "sort": "relevance", "term": term}
    )
    payload = json.loads(get(f"{BASE}/esearch.fcgi?{params}"))
    return payload["esearchresult"]["idlist"]


def text_of(node: ET.Element | None) -> str:
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def article_year(article: ET.Element) -> str:
    for path in (
        ".//ArticleDate/Year",
        ".//JournalIssue/PubDate/Year",
        ".//JournalIssue/PubDate/MedlineDate",
        ".//PubMedPubDate[@PubStatus='pubmed']/Year",
    ):
        value = text_of(article.find(path))
        if value:
            return value[:4]
    return ""


def parse_articles(xml_bytes: bytes, tags: dict[str, list[str]]) -> list[dict[str, object]]:
    root = ET.fromstring(xml_bytes)
    records: list[dict[str, object]] = []
    for item in root.findall(".//PubmedArticle"):
        citation = item.find("MedlineCitation")
        article = item.find(".//Article")
        if citation is None or article is None:
            continue
        pmid = text_of(citation.find("PMID"))
        title = text_of(article.find("ArticleTitle"))
        journal = text_of(article.find("Journal/Title"))
        abstract = " ".join(text_of(x) for x in article.findall("Abstract/AbstractText"))
        authors = []
        for author in article.findall("AuthorList/Author"):
            collective = text_of(author.find("CollectiveName"))
            if collective:
                authors.append(collective)
                continue
            family = text_of(author.find("LastName"))
            initials = text_of(author.find("Initials"))
            if family:
                authors.append(f"{family} {initials}".strip())
        doi = ""
        for article_id in item.findall(".//ArticleId"):
            if article_id.attrib.get("IdType") == "doi":
                doi = text_of(article_id)
                break
        pub_types = [text_of(x) for x in article.findall("PublicationTypeList/PublicationType")]
        records.append(
            {
                "pmid": pmid,
                "doi": doi,
                "year": article_year(item),
                "title": title,
                "journal": journal,
                "authors": authors,
                "publication_types": pub_types,
                "query_tags": sorted(tags.get(pmid, [])),
                "abstract": abstract,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            }
        )
    return records


def main() -> None:
    out_dir = Path("tmp/research")
    out_dir.mkdir(parents=True, exist_ok=True)
    tags: dict[str, list[str]] = {}
    for name, query in QUERIES.items():
        for pmid in esearch(query):
            tags.setdefault(pmid, []).append(name)
        time.sleep(0.4)

    pmids = sorted(tags)
    records: list[dict[str, object]] = []
    for start in range(0, len(pmids), 100):
        batch = pmids[start : start + 100]
        params = urllib.parse.urlencode({"db": "pubmed", "retmode": "xml", "id": ",".join(batch)})
        records.extend(parse_articles(get(f"{BASE}/efetch.fcgi?{params}"), tags))
        time.sleep(0.4)

    records.sort(key=lambda x: (str(x["year"]), str(x["title"])), reverse=True)
    (out_dir / "pubmed_candidates.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = ["year\tpmid\tdoi\tquery_tags\ttitle"]
    for record in records:
        lines.append(
            "\t".join(
                [
                    str(record["year"]),
                    str(record["pmid"]),
                    str(record["doi"]),
                    ",".join(record["query_tags"]),
                    str(record["title"]).replace("\t", " "),
                ]
            )
        )
    (out_dir / "pubmed_candidates.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} deduplicated PubMed records to {out_dir}")


if __name__ == "__main__":
    main()
