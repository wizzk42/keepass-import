import subprocess
import sys


class MainIT:
    _CMD = ['python', 'src/main.py']

    _TEST_DB_PASSWORD = 'test1234'.encode('UTF-8')

    def test_import_kdbx31_pwonly(self):
        """
        Tests an import with two simple password databases
        """
        _SOURCE_DATABASE_PATH = './tests/data/source_kdbx_3_1.kdbx'
        _TARGET_DATABASE_PATH = './tests/data/target_kdbx_3_1.kdbx'

        additional_args = [
            _SOURCE_DATABASE_PATH,
            _TARGET_DATABASE_PATH
        ]

        return self._run_with_success(additional_args)

    def test_import_kdbx31_keyfiles(self):
        """
        Tests an import with two password databases each
        protected by an additional keyfile
        """
        _SOURCE_DATABASE_W_KEY_PATH = './tests/data/source_kdbx_3_1_w_key.kdbx'
        _TARGET_DATABASE_W_KEY_PATH = './tests/data/target_kdbx_3_1_w_key.kdbx'
        _SOURCE_DATABASE_KEY = './tests/data/source_kdbx_3_1.key'
        _TARGET_DATABASE_KEY = './tests/data/target_kdbx_3_1.key'

        additional_args = [
            '-k', _SOURCE_DATABASE_KEY,
            '-l', _TARGET_DATABASE_KEY,
            _SOURCE_DATABASE_W_KEY_PATH,
            _TARGET_DATABASE_W_KEY_PATH
        ]

        return self._run_with_success(additional_args)

    def _run_with_success(self, additional_args: list):
        """
        Runs a command in a shell. Assumes a successful execution

        :param      additional_args: Additional args provided for
                    the command
        :raises:    Some exception if the underlying process returns
                    with exit <> 0
        """
        cmd: list = self._CMD + additional_args
        with subprocess.Popen(
            cmd,
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ) as p:
            output = p.communicate(
                input=self._TEST_DB_PASSWORD
                      + '\n'.encode('UTF-8')
                      + self._TEST_DB_PASSWORD
                      + '\n'.encode('UTF-8')
            )
            rc = p.returncode
            if rc:
                print(f'FAILURE %(rc)d')
                print('\t', output)
            return rc


if __name__ == '__main__':
    failures = 0
    it = MainIT()
    for key, value in MainIT.__dict__.items():
        if key.startswith('test_'):
            test_func = getattr(it, key)
            try:
                failures += test_func()
            except Exception:
                pass
    if failures > 0:
        print('TEST FAILURES ', failures)
        sys.exit(-1)
    print('ALL TESTS PASSED')
