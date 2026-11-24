import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CalcUsabilityTest(unittest.TestCase):
  def test_unknown_is_not_zero_and_examples_are_labeled(self):
    app=(ROOT/'assets/app.js').read_text(encoding='utf-8')
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    css=(ROOT/'assets/style.css').read_text(encoding='utf-8')
    self.assertIn('if(!raw)return NaN',app)
    self.assertIn('Number.isSafeInteger(cents)',app)
    self.assertIn('clear-example',app)
    self.assertIn('restore-example',app)
    self.assertIn('虚构教学演示值',html)
    self.assertIn('prefers-reduced-motion: reduce',css)
    self.assertIn('aria-live="polite"',html)
if __name__=='__main__':unittest.main()
