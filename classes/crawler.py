from time import sleep
from os import getcwd, path, system
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC


class SysCrawler():

    def __init__(self):
        geckodriver = path.join(getcwd(), 'geckodriver.exe');
        env_vars = dotenv_values('.env');
        self.__page = 0;
        self.__sys_region = env_vars['SYS_REGION'];
        self.__login_email = env_vars['LOGIN_EMAIL'];
        self.__login_password = env_vars['LOGIN_PASSWORD'];
        self.__class_notes_link = env_vars['CLASS_NOTES_LINK'];
        self.__browser = webdriver.Firefox(executable_path=geckodriver);
        self.__display_message('Abrindo navegador...');
        self.__browser.get(env_vars['SYS_URL']);

    def __wait_for_loading(self, x):
        sleep(x);

    def __display_message(self, msg):
        lines = lambda x, y:print('=' * x, end=y);
        x = 60;
        placeholder = ' ' * (x - len(msg) - 3)

        lines(x, None);
        print('| ' + msg + placeholder + '|');
        lines(x, '\n\n');

    def __handle_region_selection(self):
        regional_select = Select(self.__browser.find_element_by_xpath("//select[@id='regional']"));
        regional_select.select_by_value(self.__sys_region);
        self.__browser.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click();

    def __handle_login(self):
        email_input_login = WebDriverWait(self.__browser, 10).until(
            EC.presence_of_element_located((By.ID, 'email'))
        );
        email_input_login.send_keys(self.__login_email);
        self.__browser.find_element_by_xpath("//input[@id='senha']").send_keys(self.__login_password);
        self.__browser.find_element_by_xpath("//button[@class='btn btn-primary btn-block']").click();
    
    def __display_std_info(self, data, std):
        print(f'Student: {std}')
        for i in range(len(data[std]['Data e hora'])):
            print(
                list(data[std]['Atividade'])[i],
                list(data[std]['Data e hora'])[i].split()[1]
            );

    def __format_std_name(self, div):
        name = div.find_element_by_xpath(".//label[@class='ds-alunos']").get_attribute('innerText');
        name = name.split('2021')[0].split();
        return f'{name[0]} {name[-1]}';

    def __change_page(self, pages):
        self.__page+=1;
        if self.__page < len(pages):
            pages[self.__page].click();
        else:
            print('N??o h?? mais p??ginas. Configure para a pr??xima UC.');
            input('Pressione ENTER para finalizar.');
            self.close_browser();
            exit();

    def __get_markings_from_user(self):
        while True:
            markings = input('Ordem de Marca????o: ');
            if len(markings) == 0 or len(markings) == 3:
                return 'fff' if len(markings) == 0 else markings;
            else:
                print('Por favor, forne??a uma marca????o v??lida'); 

    def __handle_freq_buttons_click(self, markings, btns):
        for i in range(3):
            if markings[i] == 'v':
                btns[i].click();
                btns[i].click();

    def __save_changes(self, btn):
        input('Pressione ENTER para confirmar as altera????es.');
        btn.click();

    def sign_in(self):
        self.__wait_for_loading(3);
        self.__display_message('Realizando login...');
        self.__handle_region_selection();
        self.__handle_login();

    def redirect_to_class_notes(self):
        self.__wait_for_loading(5);
        self.__display_message('Redirecionando para caderneta...');
        self.__browser.get(self.__class_notes_link);

    def redirect_to_attendance_or_content(self, date, destination):
        self.__display_message('Redirecionando para di??rio de classe...');
        pages = self.__browser.find_elements_by_xpath(
                "//ngb-pagination[@class='ng-star-inserted']//ul[@class='pagination']//li"
        )[2:-2];

        while True:
            divs = self.__browser.find_elements_by_xpath("//div[@class='list-body']");
            self.__display_message(f'Buscando aula na p??gina 0{self.__page+1}...');
            for d in divs:
                try:
                    elem = d.find_element_by_xpath(f".//span[@class='badge badge-pill badge-light']");
                    if date in elem.text:
                        self.__display_message('Aula encontrada. Redirecionando...');
                        dropdown = d.find_element_by_css_selector(".font-085.dropdown-menu");
                        self.__browser.execute_script(
                            "arguments[0].setAttribute('class', 'font-085 dropdown-menu show')", 
                            dropdown
                        );
                        link = dropdown.find_elements_by_xpath(
                            ".//a[@class='dropdown-item acao-editar text-primary ng-star-inserted']"
                        );
                        if destination in 'fF':
                            link[1].click();
                        else:
                            link[0].click();
                        return
                except:
                    pass;
            self.__change_page(pages);
            input('Pressione ENTER para continuar.\n');

    def handle_attendance(self, data):
        buttons = self.__browser.find_elements_by_xpath("//button[@class='btn btn-outline-primary m-2']");
        buttons[1].click();
        divs = self.__browser.find_elements_by_xpath("//div[@class='ng-star-inserted']");
        std_names = sorted(list(data.keys()));

        for std in std_names:
            for d in divs:
                name = self.__format_std_name(d);
                if std == name:
                    system('cls');
                    self.__display_std_info(data, std);
                    freq_buttons = d.find_elements_by_xpath(
                        ".//sig-botoes-frequencia[@class='ng-star-inserted']"
                    );
                    markings = self.__get_markings_from_user();
                    self.__handle_freq_buttons_click(markings, freq_buttons);     
        self.__save_changes(
            self.__browser.find_element_by_xpath("//button[@class='btn btn-success m-2']")
        );
    
    def handle_content(self):
        self.__save_changes(
            self.__browser.find_element_by_xpath("//button[@id='btn-salvar']")
        )

    def close_browser(self):
        self.__browser.close();

