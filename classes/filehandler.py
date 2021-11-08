import shutil
import pandas as pd
from os import path, rename
from dotenv import dotenv_values


class FileAnalyser():

    @staticmethod
    def get_students_dataset(path, teacher_name):
        df = pd.read_csv(path, sep='\t', encoding='utf-16');
        df = df[df['Nome Completo'] != teacher_name];
        return { 
            name:df[df['Nome Completo'] == name][['Atividade', 'Data e hora']] 
            for name in df['Nome Completo'].unique()
        }

class FileHandler():

    def __init__(self, date):
        env_vars = dotenv_values('.env');
        self.__teacher_name = env_vars['TEACHER_NAME'];
        self.__file = f'{date.replace("/","_")}.csv';
        self.__file_downloads_path = path.join('C:\\', 'Users', env_vars['USER'], 'Downloads');
        self.__file_destination_path = path.join(
            'C:\\', 'Users', env_vars['USER'], 'Documents', env_vars['FOLDER_DESTINATION'], 'Listas de presença'
        );

    def __display_message(self, msg):
        lines = lambda x, y:print('=' * x, end=y);
        x = 60;
        placeholder = ' ' * (x - len(msg) - 3)

        lines(x, None);
        print('| ' + msg + placeholder + '|');
        lines(x, '\n\n');

    def rename_file(self):
        self.__display_message('Renomeando arquivo...');
        attendance_file = path.join(self.__file_downloads_path, 'meetingAttendanceList.csv');
        new_file = path.join(self.__file_downloads_path, self.__file);
        rename(attendance_file, new_file);

    def move_file(self):
        self.__display_message('Movendo arquivo...');
        shutil.move(
            path.join(self.__file_downloads_path, self.__file), 
            path.join(self.__file_destination_path, self.__file)
        );

    def return_freq_dataset(self):
        self.__display_message('Buscando dados dos alunos...');
        return FileAnalyser.get_students_dataset(
            path.join(self.__file_downloads_path, self.__file),
            self.__teacher_name
        );

if __name__ == '__main__':
    freq_handler = FileHandler('24/08/2021', 'caio_', 'SENAC', 'Caio.Couto');
    freq_handler.rename_file();
    students_data = freq_handler.return_freq_dataset();
    freq_handler.move_file();
    print(students_data);