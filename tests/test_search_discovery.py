import unittest
import json
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/google-ai-income-handbook/"
class SiteDiscoveryTest(unittest.TestCase):
    def test_sitemap_urls_resolve_to_real_repo_resources(self):
        root = ET.fromstring((ROOT/'sitemap.xml').read_text(encoding='utf-8'))
        ns = {"sm":"http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [e.text for e in root.findall(".//sm:loc", ns)]
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(len(urls), 3)
        self.assertIn(BASE, urls)
        for u in urls:
            self.assertTrue(u.startswith(BASE))
            rel=u.removeprefix(BASE).strip('/')
            if rel: self.assertTrue((ROOT/rel).is_file(), rel)
        for node in root.findall("sm:url", ns):
            self.assertEqual(node.find("sm:lastmod", ns).text, "2026-11-23")
    def test_authoritative_page_and_machine_navigation(self):
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        self.assertIn('rel="canonical" href="'+BASE+'"',html)
        self.assertIn('type="application/ld+json"',html)
        robot=(ROOT/'robots.txt').read_text(encoding='utf-8')
        self.assertIn("Sitemap: "+BASE+"sitemap.xml",robot)
        nav=(ROOT/'llms.txt').read_text(encoding='utf-8')
        for value in [BASE,"AIPMAndy","https://metaver.vip/","https://www.a6no1.cn/"]:
            self.assertIn(value,nav)
        self.assertIn("2026-11-23", nav)
        self.assertIn("教学样例", nav)
if __name__=="__main__":unittest.main()
