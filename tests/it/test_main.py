"""
Integration Tests
"""

import subprocess
import sys


class MainIT:
    """
    Runs the program as some kind of blackbox test
    """

    _CMD = ['python', 'src/main.py']

    _TEST_DB_PASSWORD = 'test1234'
    _TEST_DB_PASSWORD_OTHER = 'test4321'

    def test_import_kdbx31_pwonly(self):
        """
        Tests an import with two simple password databases
        """
        source = './tests/data/source_kdbx_3_1.kdbx'
        target = './tests/data/target_kdbx_3_1.kdbx'

        additional_args = [
            source,
            target
        ]

        return self._run_with_success(
            additional_args,
            self._TEST_DB_PASSWORD,
            self._TEST_DB_PASSWORD
        )

    def test_import_kdbx31_other_pwonly(self):
        """
        Tests an import with two simple password databases
        """
        source = './tests/data/source_kdbx_3_1.kdbx'
        target = './tests/data/target_kdbx_3_1_other_pw.kdbx'

        args = [
            source,
            target
        ]

        return self._run_with_success(
            args,
            self._TEST_DB_PASSWORD,
            self._TEST_DB_PASSWORD_OTHER
        )

    def test_import_kdbx31_keyfiles(self):
        """
        Tests an import with two password databases each
        protected by an additional keyfile
        """
        source = './tests/data/source_kdbx_3_1_w_key.kdbx'
        target = './tests/data/target_kdbx_3_1_w_key.kdbx'
        source_key = './tests/data/source_kdbx_3_1.key'
        target_key = './tests/data/target_kdbx_3_1.key'

        args = [
            '-k', source_key,
            '-l', target_key,
            source,
            target
        ]

        return self._run_with_success(
            args,
            self._TEST_DB_PASSWORD,
            self._TEST_DB_PASSWORD
        )

    def test_import_kdbx31_other_pw_keyfiles(self):
        """
        Tests an import with two password databases each
        protected by an additional keyfile
        """
        source = './tests/data/source_kdbx_3_1_w_key.kdbx'
        target = './tests/data/target_kdbx_3_1_w_key_other_pw.kdbx'
        source_key = './tests/data/source_kdbx_3_1.key'
        target_key = './tests/data/target_kdbx_3_1.key'

        args = [
            '-k', source_key,
            '-l', target_key,
            source,
            target
        ]

        return self._run_with_success(
            args,
            self._TEST_DB_PASSWORD,
            self._TEST_DB_PASSWORD_OTHER
        )

    def _run_with_success(self,
                          args: list,
                          srcpw,
                          dstpw):
        """
        Runs a command in a shell. Assumes a successful execution

        :param args:  Additional args provided for
                      the command
        :param srcpw: The password for the source keystore
        :param dstpw: The password for the target keystore
        :raises:    Some exception if the underlying process returns
                    with exit <> 0
        """
        cmd: list = self._CMD + args
        with subprocess.Popen(cmd,
                              shell=False,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT) as process:
            output = process.communicate(
                input=f'{srcpw}\n{dstpw}\n'.encode('UTF-8')
            )
            ret = process.returncode
            if ret:
                print(f'FAILURE %{ret}')
                print('\t', output)
            return ret


if __name__ == '__main__':
    FAILURES = 0
    it = MainIT()
    for key, value in MainIT.__dict__.items():
        if key.startswith('test_'):
            print(f'Running test: {key}')
            test_func = getattr(it, key)
            try:
                FAILURES += test_func()
            except Exception:
                pass
    if FAILURES > 0:
        print('TEST FAILURES ', FAILURES)
        sys.exit(-1)
    print('ALL TESTS PASSED')
