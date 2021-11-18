# Attendance Handler

## What is this project and what does it do?
I started working for and education company and they asked all the instructor to register attendance and content to their system. Since it envolved a lot of repetitive clicking, I decided to create a semi-autonomous bot to help me in this task.

Using Selenium and Pandas, the bot is reponsible for:
    a. Father Sudents' data (name, activity and time) provided by the platform via and CSV file, and organize it in and dictionary and rename the file to current date;
    b. Open Firefox and navigate to the current class notes page;
    c. Open the class' Attedance page and, by my command, mark each student as "Present" or "Not Present";
    d. Navigate to the Content page so I can fill the form;
    e. Close the browser and move the CSV file to a specified directory after I finished. 
