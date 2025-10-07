-- Sample Attendance Data for AI-HR Assistant Demo
-- Creates realistic attendance patterns for the last 30 days

-- Today's attendance (with some late arrivals for demo)
INSERT INTO attendance (employee_id, date, status) VALUES
-- Late arrivals today (for demo workflow)
(2, CURRENT_DATE, 'late'),    -- Bob Smith (Finance)
(5, CURRENT_DATE, 'late'),    -- Ethan Brown (Marketing)
(11, CURRENT_DATE, 'late'),   -- Kevin Lee (Finance)
(19, CURRENT_DATE, 'late'),   -- Samir Kapoor (HR)
(27, CURRENT_DATE, 'late'),   -- Anita Kumar (HR)

-- Regular attendance today
(1, CURRENT_DATE, 'present'), -- Alice Johnson
(3, CURRENT_DATE, 'present'), -- Charlie Patel
(4, CURRENT_DATE, 'present'), -- Diana Gupta
(6, CURRENT_DATE, 'present'), -- Farah Khan
(7, CURRENT_DATE, 'present'), -- George Davis
(8, CURRENT_DATE, 'present'), -- Hannah Li
(9, CURRENT_DATE, 'present'), -- Ian Wong
(10, CURRENT_DATE, 'present'), -- Jasmine Mehta
(12, CURRENT_DATE, 'present'), -- Laura Miller
(13, CURRENT_DATE, 'present'), -- Michael Thomas
(14, CURRENT_DATE, 'present'), -- Nina Shah
(15, CURRENT_DATE, 'present'), -- Omar Ali
(16, CURRENT_DATE, 'present'), -- Priya Nair
(17, CURRENT_DATE, 'present'), -- Quentin White
(18, CURRENT_DATE, 'present'), -- Riya Desai
(20, CURRENT_DATE, 'present'), -- Tina Roy
(21, CURRENT_DATE, 'present'), -- Uma Verma
(22, CURRENT_DATE, 'present'), -- Victor Chen
(23, CURRENT_DATE, 'present'), -- Wendy Zhao
(24, CURRENT_DATE, 'present'), -- Xavier Brooks
(25, CURRENT_DATE, 'present'), -- Yara Ibrahim
(26, CURRENT_DATE, 'present'), -- Zane Parker
(28, CURRENT_DATE, 'present'), -- Brian Carter
(29, CURRENT_DATE, 'present'), -- Chloe Wright
(30, CURRENT_DATE, 'present'), -- Dev Patel

-- Absent today
(31, CURRENT_DATE, 'absent'),  -- Elena Rossi
(32, CURRENT_DATE, 'absent');  -- Faisal Ahmed

-- Yesterday's attendance
INSERT INTO attendance (employee_id, date, status) VALUES
-- Most present yesterday
(1, CURRENT_DATE - INTERVAL '1 day', 'present'),
(2, CURRENT_DATE - INTERVAL '1 day', 'present'), -- Bob was on time yesterday
(3, CURRENT_DATE - INTERVAL '1 day', 'present'),
(4, CURRENT_DATE - INTERVAL '1 day', 'present'),
(5, CURRENT_DATE - INTERVAL '1 day', 'present'), -- Ethan was on time yesterday
(6, CURRENT_DATE - INTERVAL '1 day', 'present'),
(7, CURRENT_DATE - INTERVAL '1 day', 'present'),
(8, CURRENT_DATE - INTERVAL '1 day', 'present'),
(9, CURRENT_DATE - INTERVAL '1 day', 'present'),
(10, CURRENT_DATE - INTERVAL '1 day', 'present'),
(11, CURRENT_DATE - INTERVAL '1 day', 'late'),    -- Kevin was late yesterday too
(12, CURRENT_DATE - INTERVAL '1 day', 'present'),
(13, CURRENT_DATE - INTERVAL '1 day', 'present'),
(14, CURRENT_DATE - INTERVAL '1 day', 'present'),
(15, CURRENT_DATE - INTERVAL '1 day', 'present'),
(16, CURRENT_DATE - INTERVAL '1 day', 'present'),
(17, CURRENT_DATE - INTERVAL '1 day', 'present'),
(18, CURRENT_DATE - INTERVAL '1 day', 'present'),
(19, CURRENT_DATE - INTERVAL '1 day', 'present'), -- Samir was on time yesterday
(20, CURRENT_DATE - INTERVAL '1 day', 'present'),
(21, CURRENT_DATE - INTERVAL '1 day', 'present'),
(22, CURRENT_DATE - INTERVAL '1 day', 'present'),
(23, CURRENT_DATE - INTERVAL '1 day', 'present'),
(24, CURRENT_DATE - INTERVAL '1 day', 'present'),
(25, CURRENT_DATE - INTERVAL '1 day', 'present'),
(26, CURRENT_DATE - INTERVAL '1 day', 'present'),
(27, CURRENT_DATE - INTERVAL '1 day', 'present'), -- Anita was on time yesterday
(28, CURRENT_DATE - INTERVAL '1 day', 'present'),
(29, CURRENT_DATE - INTERVAL '1 day', 'present'),
(30, CURRENT_DATE - INTERVAL '1 day', 'present'),
(31, CURRENT_DATE - INTERVAL '1 day', 'present'), -- Elena was present yesterday
(32, CURRENT_DATE - INTERVAL '1 day', 'present'); -- Faisal was present yesterday

-- Sample data for the past week (simplified)
-- Day -2
INSERT INTO attendance (employee_id, date, status) 
SELECT 
    id, 
    CURRENT_DATE - INTERVAL '2 days',
    CASE 
        WHEN id % 15 = 0 THEN 'late'
        WHEN id % 20 = 0 THEN 'absent'
        ELSE 'present'
    END
FROM employees;

-- Day -3
INSERT INTO attendance (employee_id, date, status) 
SELECT 
    id, 
    CURRENT_DATE - INTERVAL '3 days',
    CASE 
        WHEN id % 12 = 0 THEN 'late'
        WHEN id % 25 = 0 THEN 'absent'
        ELSE 'present'
    END
FROM employees;

-- Day -4
INSERT INTO attendance (employee_id, date, status) 
SELECT 
    id, 
    CURRENT_DATE - INTERVAL '4 days',
    CASE 
        WHEN id % 18 = 0 THEN 'late'
        WHEN id % 30 = 0 THEN 'absent'
        ELSE 'present'
    END
FROM employees;

-- Day -5 (Friday last week)
INSERT INTO attendance (employee_id, date, status) 
SELECT 
    id, 
    CURRENT_DATE - INTERVAL '5 days',
    CASE 
        WHEN id % 10 = 0 THEN 'late'
        WHEN id % 22 = 0 THEN 'absent'
        ELSE 'present'
    END
FROM employees;

-- Verification queries
SELECT 'Today''s Late Arrivals:' as summary;
SELECT e.name, e.email, e.department 
FROM employees e 
JOIN attendance a ON e.id = a.employee_id 
WHERE a.date = CURRENT_DATE AND a.status = 'late'
ORDER BY e.department, e.name;

SELECT 'Attendance Summary for Today:' as summary;
SELECT 
    status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employees), 1) as percentage
FROM attendance 
WHERE date = CURRENT_DATE 
GROUP BY status
ORDER BY count DESC;