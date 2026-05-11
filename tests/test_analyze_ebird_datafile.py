import unittest

from analyze_ebird_datafile import analyze_rows, parse_count


class AnalyzeEbirdDatafileTests(unittest.TestCase):
    def test_parse_count(self):
        self.assertEqual(parse_count("12"), 12)
        self.assertEqual(parse_count("1,200"), 1200)
        self.assertIsNone(parse_count("X"))
        self.assertIsNone(parse_count(""))
        self.assertIsNone(parse_count(None))

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
        self.assertEqual(summary["top_species"][0], ("House Sparrow", 2))


if __name__ == "__main__":
    unittest.main()
