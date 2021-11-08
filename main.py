from datetime import datetime
from classes.crawler import SysCrawler
from classes.filehandler import FileHandler

def allow_continuity():
    input('Pressione ENTER para continuar.\n');

def get_today_date():
    year = datetime.today().year;
    month = f'0{datetime.today().month }' if datetime.today().month < 10 else datetime.today().month;
    day = f'0{datetime.today().day }' if datetime.today().day < 10  else datetime.today().day;
    return f'{day}/{month}/{year}';

file_handler = FileHandler(get_today_date());
file_handler.rename_file();
students_data = file_handler.return_freq_dataset();

browser = SysCrawler();
browser.sign_in();
browser.redirect_to_class_notes();

allow_continuity();
browser.redirect_to_attendance_or_content(get_today_date(), 'f');

allow_continuity();
browser.handle_attendance(students_data);
browser.redirect_to_class_notes();

allow_continuity();
browser.redirect_to_attendance_or_content(get_today_date(), 'c');

allow_continuity();
browser.handle_content();
browser.redirect_to_class_notes();

allow_continuity();
browser.close_browser();
file_handler.move_file();