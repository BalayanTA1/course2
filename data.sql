CREATE TABLE Institute (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Study_Group (
    group_number SERIAL PRIMARY KEY,
    institute_id INT REFERENCES Institute(id) ON DELETE CASCADE
);

CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    education_form VARCHAR(20),
    group_number INT REFERENCES Study_Group(group_number) ON DELETE CASCADE,
    password VARCHAR(255) NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Subject (
    name VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Teacher (
    teacher_id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    academic_degree VARCHAR(50),
    title VARCHAR(50),
    position VARCHAR(50),
    institute_id INT REFERENCES Institute(id) ON DELETE CASCADE,
    password VARCHAR(255) NOT NULL,
    login VARCHAR(100) NOT NULL UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Teacher_Subject (
    teacher_id INT REFERENCES Teacher(teacher_id) ON DELETE CASCADE,
    subject_name VARCHAR(50) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (teacher_id, subject_name)
);

CREATE TABLE Work (
    work_number INT PRIMARY KEY,  
    name VARCHAR(50) NOT NULL,
    subject_name VARCHAR(50) REFERENCES Subject(name) ON DELETE CASCADE,
    is_lab BOOLEAN NOT NULL DEFAULT FALSE,  
    is_control BOOLEAN NOT NULL DEFAULT FALSE,  
    CHECK (is_lab <> is_control)  
);

CREATE TABLE Work_Groups (
    date DATE NOT NULL,
    deadline DATE NOT NULL,
    group_number INT REFERENCES Study_Group(group_number) ON DELETE CASCADE,
    work_number INT REFERENCES Work(work_number) ON DELETE CASCADE,  
    subject_name VARCHAR(50) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (group_number, work_number)
);

CREATE TABLE Work_Result (
    grade INT NOT NULL,
    submission_date DATE NOT NULL,
    student_id INT REFERENCES Student(student_id) ON DELETE CASCADE,
    work_number INT REFERENCES Work(work_number) ON DELETE CASCADE,  
    subject_name VARCHAR(50) REFERENCES Subject(name) ON DELETE CASCADE,
    PRIMARY KEY (student_id, work_number)
);

CREATE TABLE Uploaded_Files ( 
    file_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Student(student_id) ON DELETE CASCADE, 
    work_number INT REFERENCES Work(work_number) ON DELETE CASCADE, 
    file_path VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
 );