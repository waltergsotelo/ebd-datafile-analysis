import unittest

from analyze_ebird_datafile import analyze_rows, first_non_empty, parse_count


class AnalyzeEbirdDatafileTests(unittest.TestCase):
    def test_parse_count(self):
        self.assertEqual(parse_count("12"), 12)
        self.assertEqual(parse_count("1,200"), 1200)
        self.assertIsNone(parse_count("X"))
        self.assertIsNone(parse_count(""))
        self.assertIsNone(parse_count(None))

    def test_first_non_empty(self):
        row = {"A": " ", "B": "valor", "C": "otro"}
        self.assertEqual(first_non_empty(row, ["A", "B", "C"]), "valor")
        self.assertEqual(first_non_empty(row, ["X", "Y"]), "")

    def test_analyze_rows_summary(self):
        rows = [
            {
                "Common Name": "House Sparrow",
                "Count": "5",
                "Submission ID": "S1",
            },
            {
                "Common Name": "House Sparrow",
                "Count": "X",
                "Submission ID": "S1",
            },
            {
                "Common Name": "Great Egret",
                "Count": "2",
                "Submission ID": "S2",
            },
        ]
        summary = analyze_rows(rows)
        self.assertEqual(summary["observations"], 3)
        self.assertEqual(summary["unique_species"], 2)
        self.assertEqual(summary["known_individuals"], 7)
        self.assertEqual(summary["unknown_count_rows"], 1)
        self.assertEqual(summary["checklists"], 2)
        self.assertEqual(
            summary["top_species"],
            [("House Sparrow", 2), ("Great Egret", 1)],
        )

    def test_analyze_rows_with_spanish_headers(self):
        rows = [
            {"Nombre común": "Gorrión común", "Conteo": "3", "ID de envío": "E1"},
            {"Nombre común": "Garza blanca", "Conteo": "X", "ID de envío": "E2"},
        ]
        summary = analyze_rows(rows)
        self.assertEqual(summary["observations"], 2)
        self.assertEqual(summary["unique_species"], 2)
        self.assertEqual(summary["known_individuals"], 3)
        self.assertEqual(summary["unknown_count_rows"], 1)
        self.assertEqual(summary["checklists"], 2)
        self.assertEqual(
            summary["top_species"],
            [("Gorrión común", 1), ("Garza blanca", 1)],
        )


if __name__ == "__main__":
    unittest.main()
