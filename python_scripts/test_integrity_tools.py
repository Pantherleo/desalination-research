"""Test valid, missing and unsafe XMF companion references on synthetic data."""
from pathlib import Path
import tempfile
import unittest
from audit_project import hdf_references


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / 'RO_data'
        self.root.mkdir()
        self.xmf = self.root / 'case.xmf'

    def tearDown(self):
        self.temp.cleanup()

    def xml(self, text):
        self.xmf.write_text('<Xdmf><DataItem Format="HDF">'+text+'</DataItem></Xdmf>', encoding='utf-8')

    def test_existing_relative_companion(self):
        h5 = self.root / 'case.h5'
        h5.write_bytes(b'fixture')
        self.xml('case.h5:Data0')
        self.assertEqual(hdf_references(self.xmf, self.root), [h5.resolve()])

    def test_missing_companion(self):
        self.xml('missing.h5:Data0')
        with self.assertRaisesRegex(ValueError, 'missing'):
            hdf_references(self.xmf, self.root)

    def test_directory_traversal(self):
        (self.base / 'outside.h5').write_bytes(b'fixture')
        self.xml('../outside.h5:Data0')
        with self.assertRaisesRegex(ValueError, 'escapes'):
            hdf_references(self.xmf, self.root)

    def test_incomplete_reference(self):
        self.xml('case.h5:')
        with self.assertRaisesRegex(ValueError, 'file and dataset'):
            hdf_references(self.xmf, self.root)


if __name__ == '__main__':
    unittest.main()
