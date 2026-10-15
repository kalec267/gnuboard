"""포트 변경 시 기존 자격 증명 보존과 잘못된 설정의 거부를 확인한다."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from local_port import select_port


class LocalPortTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / '.env'
        self.original = 'DB_PASSWORD=preserved-placeholder\nSHOP_ADMIN_PASSWORD=preserved-admin\n'
        self.path.write_text(self.original, encoding='utf-8')
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_existing_installation_keeps_default_without_rewriting_credentials(self):
        self.assertEqual(select_port(self.path), 8080)
        self.assertEqual(self.path.read_text(), self.original)

    def test_port_change_survives_restart_and_preserves_credentials(self):
        self.assertEqual(select_port(self.path, 18080), 18080)
        self.assertEqual(self.path.read_text(), self.original + 'SHOP_PORT=18080\n')
        os.environ.pop('SHOP_PORT')
        self.assertEqual(select_port(self.path), 18080)
        self.assertEqual(select_port(self.path, 28080), 28080)
        self.assertEqual(self.path.read_text(), self.original + 'SHOP_PORT=28080\n')

    def test_explicit_argument_overrides_process_environment(self):
        os.environ['SHOP_PORT'] = '28080'
        self.assertEqual(select_port(self.path, 18080), 18080)
        self.assertEqual(os.environ['SHOP_PORT'], '18080')

    def test_invalid_values_cannot_modify_existing_settings(self):
        for value in ('0', '65536', '8080:80', '18080\nDB_PASSWORD=changed', ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                select_port(self.path, value)
        self.assertEqual(self.path.read_text(), self.original)

    def test_quoted_saved_port_and_comment_are_supported(self):
        self.path.write_text(self.original + 'SHOP_PORT="18080" # local\n')
        self.assertEqual(select_port(self.path), 18080)


if __name__ == '__main__':
    unittest.main()
