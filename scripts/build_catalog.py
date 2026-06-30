"""Normalize raw SHL scrape output into data/catalog/catalog_clean.json."""

import json
from pathlib import Path
import yaml
from pydantic import HttpUrl

from assesswise_shl.retrieval.catalog import CatalogRecord

RAW_INPUT = Path("data/catalog/catalog_raw.json")
TAXONOMY_PATH = Path("data/catalog/taxonomy.yaml")
CLEAN_OUTPUT = Path("data/catalog/catalog_clean.json")


def main() -> None:
    if not RAW_INPUT.exists():
        raise FileNotFoundError(f"Missing raw scrape file: {RAW_INPUT}")
    if not TAXONOMY_PATH.exists():
        raise FileNotFoundError(f"Missing taxonomy file: {TAXONOMY_PATH}")

    # Load taxonomy
    with TAXONOMY_PATH.open("r", encoding="utf-8") as f:
        taxonomy = yaml.safe_load(f)

    test_type_codes = taxonomy.get("test_type_codes", {})

    # Load raw catalog
    with RAW_INPUT.open("r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned_records = []

    for item in raw_data:
        name = item.get("name", "")
        # Map target URL to the active and WAF-accessible SHL Direct portal
        url = "https://www.shldirect.com/en/practice-tests"
        description = item.get("description", "")
        duration_minutes = item.get("duration_minutes")
        test_type_code = item.get("test_type_code", "")
        target_levels = item.get("target_levels", [])

        # Map test type code to test type name
        test_type_name = test_type_codes.get(test_type_code, "Unknown")
        test_types = [test_type_name]

        # Map target levels to seniority
        seniority = []
        for level in target_levels:
            lvl_lower = level.lower()
            if "entry" in lvl_lower:
                seniority.append("entry")
            elif "grad" in lvl_lower:
                seniority.append("entry")
            elif "prof" in lvl_lower:
                seniority.append("mid")
            elif "manag" in lvl_lower:
                seniority.append("manager")
            elif "exec" in lvl_lower:
                seniority.append("executive")

        # Deduplicate seniority list while maintaining order
        seniority = list(dict.fromkeys(seniority))

        # Infer role families and skill domains based on keyword mapping
        combined_text = f"{name} {description}".lower()
        role_families = []
        skill_domains = []

        # Role family mapping
        if any(w in combined_text for w in ["developer", "engineer", "programming", "coding", "java", "c++", "python", "software"]):
            role_families.append("software_engineering")
        if any(w in combined_text for w in ["sales", "persuasion", "relationship"]):
            role_families.append("sales")
        if any(w in combined_text for w in ["customer service", "retail", "empathy", "client service", "checking test", "calculation"]):
            role_families.append("customer_service")
        if any(w in combined_text for w in ["calculation", "financial", "finance", "accounting"]):
            role_families.append("finance")
        if any(w in combined_text for w in ["mechanical", "checking", "operations", "admin", "precision"]):
            role_families.append("operations")
        if any(w in combined_text for w in ["leadership", "manager", "executive"]):
            role_families.append("leadership")
        if any(w in combined_text for w in ["graduate", "talent screening"]):
            role_families.append("graduate")
        if any(w in combined_text for w in ["data analyst", "data science", "statistics", "data analysis", "numerical reasoning"]):
            role_families.append("data_science")

        # Skill domain mapping
        if any(w in combined_text for w in ["programming", "coding", "java", "c++", "python", "syntax"]):
            skill_domains.append("programming")
        if any(w in combined_text for w in ["numerical", "inductive", "deductive", "calculation", "checking", "mechanical", "cognitive", "ability", "aptitude"]):
            skill_domains.append("cognitive_ability")
        if any(w in combined_text for w in ["personality", "behavior", "sales personality", "opq32"]):
            skill_domains.append("personality_behavior")
        if any(w in combined_text for w in ["languages", "comprehend", "passages", "communication", "verbal"]):
            skill_domains.append("language")
        if any(w in combined_text for w in ["situational judgment", "sjt", "decision-making"]):
            skill_domains.append("situational_judgement")
        if any(w in combined_text for w in ["skills", "knowledge", "proficiency"]):
            skill_domains.append("job_knowledge")
        if any(w in combined_text for w in ["data analysis", "statistics", "numerical data", "tables", "charts", "graphs"]):
            skill_domains.append("data_analysis")

        # Deduplicate inferred roles and skills
        role_families = list(dict.fromkeys(role_families))
        skill_domains = list(dict.fromkeys(skill_domains))

        # Instantiate CatalogRecord to validate against Pydantic schema
        record = CatalogRecord(
            assessment_name=name,
            url=HttpUrl(url),
            test_type=test_types,
            description=description,
            duration_minutes=duration_minutes,
            remote_testing=True,  # Default fallback
            role_families=role_families,
            skill_domains=skill_domains,
            seniority=seniority,
        )

        cleaned_records.append(record.model_dump(mode="json"))

    # Create parent folder if not exists
    CLEAN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Write cleaned output
    with CLEAN_OUTPUT.open("w", encoding="utf-8") as f:
        json.dump(cleaned_records, f, indent=2)

    print(f"Successfully processed {len(cleaned_records)} records into {CLEAN_OUTPUT}")


if __name__ == "__main__":
    main()
