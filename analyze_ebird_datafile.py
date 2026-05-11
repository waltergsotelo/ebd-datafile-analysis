import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


def parse_count(value):
    if value is None:
        return None
    normalized = value.strip().replace(",", "")
    if not normalized or normalized.upper() == "X":
        return None
    try:
        return int(normalized)
    except ValueError:
        return None


def first_non_empty(row, keys):
    for key in keys:
        value = row.get(key, "")
        if value and value.strip():
            return value.strip()
    return ""


def analyze_rows(rows):
    observation_count = len(rows)
    species_counter = Counter()
    known_individuals = 0
    unknown_count_rows = 0
    checklist_ids = set()

    for row in rows:
        species = first_non_empty(row, ["Common Name", "Nombre común"])
        if species:
            species_counter[species] += 1

        checklist = first_non_empty(
            row, ["Submission ID", "Checklist ID", "ID de envío", "ID de lista"]
        )
        if checklist:
            checklist_ids.add(checklist)

        count_value = parse_count(first_non_empty(row, ["Count", "Conteo"]))
        if count_value is None:
            unknown_count_rows += 1
        else:
            known_individuals += count_value

    return {
        "observations": observation_count,
        "unique_species": len(species_counter),
        "known_individuals": known_individuals,
        "unknown_count_rows": unknown_count_rows,
        "checklists": len(checklist_ids),
        "top_species": species_counter.most_common(10),
    }


def analyze_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    return analyze_rows(rows)


def format_summary(summary):
    lines = [
        "Resumen del data file de eBird",
        f"- Observaciones totales: {summary['observations']}",
        f"- Especies únicas: {summary['unique_species']}",
        f"- Individuos (conteos numéricos): {summary['known_individuals']}",
        f"- Registros con conteo no numérico: {summary['unknown_count_rows']}",
    ]

    lines.append(f"- Listas (Submission ID/Checklist ID): {summary['checklists']}")

    lines.append("- Top especies más reportadas:")
    if not summary["top_species"]:
        lines.append("  (sin datos)")
    else:
        for species, count in summary["top_species"]:
            lines.append(f"  - {species}: {count}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analiza un data file CSV exportado desde eBird."
    )
    parser.add_argument("csv_file", type=Path, help="Ruta al archivo CSV de eBird")
    args = parser.parse_args()

    try:
        summary = analyze_csv(args.csv_file)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo: {args.csv_file}", file=sys.stderr)
        sys.exit(2)
    except (OSError, csv.Error) as exc:
        print(f"Error al leer el archivo CSV: {exc}", file=sys.stderr)
        sys.exit(2)

    print(format_summary(summary))


if __name__ == "__main__":
    main()
