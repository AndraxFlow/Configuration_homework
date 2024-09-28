#!/usr/bin/python3
import os
import tarfile
import argparse
import time



class ShellEmulator:
    def __init__(self, username, tar_file, start_script):
        self.username = username
        self.temp_dir = '/tmp/emulator'
        print('\nWELCOME, '+self.username+', to the greatest emulator EVER.\n')
            # Now I am trying to define your start script.\n\
            # For that time, you can read the RULES:\n\
            # You can do some basic commands like:\n\
            #     cd, ls, mkdir, rmdir, whoami, wc\n\
            #     to EXIT write EXIT')
        #time.sleep(4)
        self.load_filesystem(tar_file)
        self.execute_start_script(start_script)

    def wc(self, filename):
        results = {}
        
        chars = 0
        words = 0
        lines = 0
        try:
            with open(filename) as fh:
                for line in fh:
                    lines += 1
                    words += len(line.split())
                    chars += len(line)
            results[filename] = {
                'lines': lines,
                'words': words,
                'chars': chars,
            }
        except Exception as err:
            print(err)
        return results

    def load_filesystem(self, tar_file):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        with tarfile.open(tar_file, 'r') as tar:
            tar.extractall(path=self.temp_dir)

    def execute_start_script(self, start_script):
        script_path = os.path.join(self.temp_dir, start_script)
        if os.path.exists(script_path):
            with open(script_path, 'r') as file:
                for line in file:
                    print('execute', line)
                    self.execute_command(line)
        else:
            print(f"Стартовый скрипт '{start_script}' не найден.")

    def execute_command(self, command):
        command_parts = command.split()
        if command_parts[0] == 'cd':
            try:
                os.chdir(os.path.join(self.temp_dir, command_parts[1]))
                self.temp_dir = os.path.join(self.temp_dir, command_parts[1])
                print('\n')
            except Exception as e:
                print(f"Ошибка: {e}\n")
        elif command_parts[0] == 'ls':
            print("\n".join(os.listdir(self.temp_dir)))
            print('\n')
        elif command_parts[0] == 'mkdir':
            try:
                os.mkdir(os.path.join(self.temp_dir, command_parts[1]))
                print('\n')
            except Exception as e:
                print(f"Ошибка: {e}\n")
        elif command_parts[0] == 'rmdir':
            try:
                os.rmdir(os.path.join(self.temp_dir, command_parts[1]))
                print('\n')
            except Exception as e:
                print(f"Ошибка: {e}\n")
        elif command_parts[0] == 'whoami':
            print(self.username, '\n')
        elif command_parts[0] == 'wc':
            try:
                result = self.wc(command_parts[1])
                print(result)  
            except Exception as e:
                print(f"Ошибка: {e}\n")
        else:
            print(f"Команда '{command}' не распознана.\n")
            

    def start(self):
        while True:
            command = input(f"{os.getcwd()}$")
            if command.lower() in ['exit', 'quit']:
                break
            self.execute_command(command)

if __name__ == "__main__":
    #tar_file = input('Введите адрес файла tar: ')
    #emulator = ShellEmulator(tar_file)
    #emulator.start()

    parser = argparse.ArgumentParser(description='Эмулятор оболочки ОС ')
    parser.add_argument('username', type=str, help='Имя пользователя для приглашения')
    parser.add_argument('tar_file', type=str, help='Путь к архиву виртуальной файловой системы')
    parser.add_argument('start_script', type=str, help='Путь к стартовому скрипту')

    args = parser.parse_args()
    emulator = ShellEmulator(args.username, args.tar_file, args.start_script)
    emulator.start()
