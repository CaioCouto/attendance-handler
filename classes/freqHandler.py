import shutil
import pandas as pd
from os import path, system, rename, remove
from datetime import datetime


class FreqAnalyser():

    @staticmethod
    def get_students_dataset(path):
        df = pd.read_csv(path, sep='\t', encoding='utf-16');
        df = df[df['Nome Completo'] != 'Caio.Couto'];
        std_names = sorted(list({ 
            name:df[df['Nome Completo'] == name][['Atividade', 'Data e hora']] 
            for name in df['Nome Completo'].unique()
        }.keys()));
        print(std_names);
        return { 
            name:df[df['Nome Completo'] == name][['Atividade', 'Data e hora']] 
            for name in df['Nome Completo'].unique()
        }

class FreqHandler():

    def __init__(self, date, user, destination):
        self.__file = f'{date.replace("/","_")}.csv';
        self.__file_original_path = path.join(
            'C:\\', 'Users', user, 'Downloads'
        );
        self.__file_destination_path = path.join(
            'C:\\', 'Users', user, 'Documents', destination, 'Listas de presença'
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
        original_file = path.join(self.__file_original_path, 'meetingAttendanceList.csv');
        new_file = path.join(self.__file_original_path, self.__file);
        rename(original_file,new_file);

    def move_file(self):
        self.__display_message('Movendo arquivo...');
        shutil.move(
            path.join(self.__file_original_path, self.__file), 
            path.join(self.__file_destination_path, self.__file)
        );

    def return_freq_dataset(self):
        self.__display_message('Buscando dados dos alunos...');
        return FreqAnalyser.get_students_dataset(
            path.join(self.__file_original_path, self.__file)
        );

if __name__ == '__main__':
    freq_handler = FreqHandler('17/09/2021');
    freq_handler.rename_file();
    students_data = freq_handler.return_freq_dataset();
    freq_handler.move_file();
    print(students_data);