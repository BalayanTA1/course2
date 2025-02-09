-- Создание таблицы Институт
CREATE TABLE Institute (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы Группа (переименована в Study_Group)
CREATE TABLE Study_Group (
    group_number SERIAL PRIMARY KEY,
    institute_id INT REFERENCES Institute(id) ON DELETE CASCADE
);

-- Создание таблицы Студент
CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    education_form VARCHAR(50),
    group_number INT REFERENCES Study_Group(group_number) ON DELETE CASCADE,
    password VARCHAR(255) NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE
);

-- Создание таблицы Предмет
CREATE TABLE Subject (
    name VARCHAR(255) PRIMARY KEY
);

-- Создание таблицы Лабораторная работа
CREATE TABLE Lab_Work (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE
);

-- Создание таблицы Контрольная работа
CREATE TABLE Control_Work (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE
);

-- Создание таблицы Лабораторные группы
CREATE TABLE Lab_Groups (
    deadline DATE NOT NULL,
    group_number INT REFERENCES Study_Group(group_number) ON DELETE CASCADE,
    lab_work_id INT REFERENCES Lab_Work(id) ON DELETE CASCADE,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (group_number, lab_work_id)
);

-- Создание таблицы Контрольные группы
CREATE TABLE Control_Groups (
    date DATE NOT NULL,
    group_number INT REFERENCES Study_Group(group_number) ON DELETE CASCADE,
    control_work_id INT REFERENCES Control_Work(id) ON DELETE CASCADE,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (group_number, control_work_id)
);

-- Создание таблицы Результат контрольной работы
CREATE TABLE Control_Work_Result (
    grade INT NOT NULL,
    student_id INT REFERENCES Student(student_id) ON DELETE CASCADE,
    control_work_id INT REFERENCES Control_Work(id) ON DELETE CASCADE,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (student_id, control_work_id)
);

-- Создание таблицы Сдача лабораторной работы
CREATE TABLE Lab_Work_Submission (
    submission_date DATE NOT NULL,
    student_id INT REFERENCES Student(student_id) ON DELETE CASCADE,
    lab_work_id INT REFERENCES Lab_Work(id) ON DELETE CASCADE,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (student_id, lab_work_id)
);

-- Создание таблицы Преподаватель
CREATE TABLE Teacher (
    teacher_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    academic_degree VARCHAR(100),
    title VARCHAR(100),
    position VARCHAR(100),
    institute_id INT REFERENCES Institute(id) ON DELETE CASCADE,
    password VARCHAR(255) NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Создание таблицы Преподаватель_предмет
CREATE TABLE Teacher_Subject (
    teacher_id INT REFERENCES Teacher(teacher_id) ON DELETE CASCADE,
    subject_name VARCHAR(255) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (teacher_id, subject_name)
);