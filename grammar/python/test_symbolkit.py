import unittest
from symbolkit import render, SymbolKitError


class TestSymbolKit(unittest.TestCase):
    def test_status_dot(self):
        self.assertEqual(render('STATUS_DOT("live")'), "●")
        self.assertEqual(render('STATUS_DOT("idle")'), "◐")
        self.assertEqual(render('STATUS_DOT("offline")'), "○")

    def test_progress(self):
        self.assertEqual(render("PROGRESS(0.6)"), "▰▰▰▰▰▰▱▱▱▱")
        self.assertEqual(render("PROGRESS(0.23, 20)"), "▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱")

    def test_severity(self):
        self.assertEqual(render("SEVERITY(2)"), "●●○○")
        self.assertEqual(render("SEVERITY(3, 5)"), "●●●○○")

    def test_bar(self):
        self.assertEqual(render("BAR(12, 20, 10)"), "▓▓▓▓▓▓░░░░")
        self.assertEqual(render("BAR(0.6, 1.0, 8)"), "▓▓▓▓▓░░░")

    def test_spark(self):
        self.assertEqual(render("SPARK(0.1, 0.5, 0.9, 0.3)"), "▂▅▇▃")

    def test_tree(self):
        self.assertEqual(render("TREE(1, false)"), "├──")
        self.assertEqual(render("TREE(1, true)"), "└──")
        self.assertEqual(render("TREE(2, false)"), "│   ├──")

    def test_kashida(self):
        expected = "جيولينك" + "ـ" * 8
        self.assertEqual(render('KASHIDA_FILL("جيولينك", 15)'), expected)

    def test_rating(self):
        self.assertEqual(render("RATING(3)"), "●●●○○")
        self.assertEqual(render("RATING(4, 10)"), "●●●●○○○○○○")

    def test_retry(self):
        self.assertEqual(render("RETRY_NOTICE(30)"), "↻ 30s")

    def test_atom(self):
        self.assertEqual(render("@black-circle"), "●")
        self.assertEqual(render("@white-circle"), "○")

    def test_repetition(self):
        self.assertEqual(render("@black-circle × 3"), "●●●")

    def test_sequence(self):
        self.assertEqual(render('@black-circle + " " + @white-circle'), "● ○")

    def test_complex(self):
        self.assertEqual(
            render('STATUS_DOT("live") + " · " + PROGRESS(0.6)'),
            "● · ▰▰▰▰▰▰▱▱▱▱",
        )


if __name__ == "__main__":
    unittest.main()
