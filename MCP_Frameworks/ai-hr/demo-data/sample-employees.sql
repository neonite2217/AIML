-- Sample Employee Data for AI-HR Assistant Demo
-- 50 employees across different departments

INSERT INTO employees (name, email, department) VALUES
-- HR Department
('Alice Johnson', 'alice.johnson@neo.corp', 'HR'),
('Hannah Li', 'hannah.li@neo.corp', 'HR'),
('Samir Kapoor', 'samir.kapoor@neo.corp', 'HR'),
('Anita Kumar', 'anita.kumar@neo.corp', 'HR'),
('Grace Turner', 'grace.turner@neo.corp', 'HR'),
('Olivia Moore', 'olivia.moore@neo.corp', 'HR'),
('Vikram Rao', 'vikram.rao@neo.corp', 'HR'),

-- Finance Department
('Bob Smith', 'bob.smith@neo.corp', 'Finance'),
('Farah Khan', 'farah.khan@neo.corp', 'Finance'),
('Kevin Lee', 'kevin.lee@neo.corp', 'Finance'),
('Priya Nair', 'priya.nair@neo.corp', 'Finance'),
('Tina Roy', 'tina.roy@neo.corp', 'Finance'),
('Xavier Brooks', 'xavier.brooks@neo.corp', 'Finance'),
('Brian Carter', 'brian.carter@neo.corp', 'Finance'),
('Henry Lopez', 'henry.lopez@neo.corp', 'Finance'),
('Maya Singh', 'maya.singh@neo.corp', 'Finance'),
('Qadir Malik', 'qadir.malik@neo.corp', 'Finance'),
('Usha Menon', 'usha.menon@neo.corp', 'Finance'),

-- IT Department
('Charlie Patel', 'charlie.patel@neo.corp', 'IT'),
('George Davis', 'george.davis@neo.corp', 'IT'),
('Jasmine Mehta', 'jasmine.mehta@neo.corp', 'IT'),
('Omar Ali', 'omar.ali@neo.corp', 'IT'),
('Uma Verma', 'uma.verma@neo.corp', 'IT'),
('Zane Parker', 'zane.parker@neo.corp', 'IT'),
('Chloe Wright', 'chloe.wright@neo.corp', 'IT'),
('Isla Fernandez', 'isla.fernandez@neo.corp', 'IT'),
('Noah Kim', 'noah.kim@neo.corp', 'IT'),
('Thomas Hall', 'thomas.hall@neo.corp', 'IT'),

-- Sales Department
('Diana Gupta', 'diana.gupta@neo.corp', 'Sales'),
('Laura Miller', 'laura.miller@neo.corp', 'Sales'),
('Quentin White', 'quentin.white@neo.corp', 'Sales'),
('Victor Chen', 'victor.chen@neo.corp', 'Sales'),
('Dev Patel', 'dev.patel@neo.corp', 'Sales'),
('Jack Murphy', 'jack.murphy@neo.corp', 'Sales'),
('Peter Zhang', 'peter.zhang@neo.corp', 'Sales'),
('William Adams', 'william.adams@neo.corp', 'Sales'),

-- Marketing Department
('Ethan Brown', 'ethan.brown@neo.corp', 'Marketing'),
('Michael Thomas', 'michael.thomas@neo.corp', 'Marketing'),
('Riya Desai', 'riya.desai@neo.corp', 'Marketing'),
('Wendy Zhao', 'wendy.zhao@neo.corp', 'Marketing'),
('Elena Rossi', 'elena.rossi@neo.corp', 'Marketing'),
('Kiran Das', 'kiran.das@neo.corp', 'Marketing'),
('Rachel Green', 'rachel.green@neo.corp', 'Marketing'),

-- Operations Department
('Ian Wong', 'ian.wong@neo.corp', 'Operations'),
('Nina Shah', 'nina.shah@neo.corp', 'Operations'),
('Yara Ibrahim', 'yara.ibrahim@neo.corp', 'Operations'),
('Faisal Ahmed', 'faisal.ahmed@neo.corp', 'Operations'),
('Liam Scott', 'liam.scott@neo.corp', 'Operations'),
('Sofia Torres', 'sofia.torres@neo.corp', 'Operations');

-- Verify the data
SELECT 
    department, 
    COUNT(*) as employee_count 
FROM employees 
GROUP BY department 
ORDER BY employee_count DESC;