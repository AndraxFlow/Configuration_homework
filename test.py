#!/usr/bin/python3
import os
import shutil
import tarfile
import unittest
from unittest.mock import patch, MagicMock
from main import ShellEmulator




class EmulatorTestCase(unittest.TestCase):
    def setUp(self):
        self.executor = ShellEmulator('test_user', 'arch.tar','start_script.txt')
        self.executor.temp_dir = '/tmp/emulator'  # Ensure this matches the actual path used

    @patch('os.chdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_cd_command(self, mock_join, mock_chdir):
        command = 'cd new_folder'
        self.executor.execute_command(command)
        mock_chdir.assert_called_once_with('/tmp/emulator/new_folder')
        self.assertEqual(self.executor.temp_dir, '/tmp/emulator/new_folder')

    @patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
    def test_ls_command(self, mock_listdir):
        with patch('builtins.print') as mock_print:
            command = 'ls'
            self.executor.execute_command(command)
            mock_print.assert_any_call('file1.txt\nfile2.txt')
            mock_print.assert_any_call('\n')

    @patch('os.mkdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_mkdir_command(self, mock_join, mock_mkdir):
        command = 'mkdir new_folder'
        with patch('builtins.print') as mock_print:
            self.executor.execute_command(command)
            mock_mkdir.assert_called_once_with('/tmp/emulator/new_folder')
            mock_print.assert_called_once_with('\n')

    @patch('os.rmdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_rmdir_command(self, mock_join, mock_rmdir):
        command = 'rmdir old_folder'
        with patch('builtins.print') as mock_print:
            self.executor.execute_command(command)
            mock_rmdir.assert_called_once_with('/tmp/emulator/old_folder')
            mock_print.assert_called_once_with('\n')

    def test_whoami_command(self):
        with patch('builtins.print') as mock_print:
            command = 'whoami'
            self.executor.execute_command(command)
            mock_print.assert_called_once_with('test_user','\n')

    @patch('builtins.open', new_callable=MagicMock)
    def test_wc_command(self, mock_open):
        command = 'wc mock_file.txt'
        with patch('builtins.print') as mock_print:
            self.executor.execute_command(command)
            mock_print.assert_called_once_with({'mock_file.txt': {'lines': 0, 'words': 0, 'chars': 0}})

    def test_unknown_command(self):
        with patch('builtins.print') as mock_print:
            command = 'unknown_command'
            self.executor.execute_command(command)
            mock_print.assert_called_once_with("Команда 'unknown_command' не распознана.\n")

if __name__ == '__main__':
    unittest.main()