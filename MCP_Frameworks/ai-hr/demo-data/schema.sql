-- AI-HR Assistant Database Schema
-- PostgreSQL database schema for employee and attendance management

-- Create database (run as superuser)
-- CREATE DATABASE companydb;
-- CREATE USER hradmin WITH PASSWORD 'hrpass';
-- GRANT ALL PRIVILEGES ON DATABASE companydb TO hradmin;

-- Connect to companydb database
-- \c companydb

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT NOT NULL,
    hire_date DATE DEFAULT CURRENT_DATE,
    position TEXT,
    manager_id INTEGER REFERENCES employees(id),
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('present', 'late', 'absent', 'sick', 'vacation')),
    check_in_time TIME,
    check_out_time TIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(employee_id, date)
);

-- Create departments table (optional, for normalization)
CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    manager_id INTEGER REFERENCES employees(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create attendance_notifications table (for tracking email notifications)
CREATE TABLE IF NOT EXISTS attendance_notifications (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    attendance_id INTEGER NOT NULL REFERENCES attendance(id) ON DELETE CASCADE,
    notification_type TEXT NOT NULL CHECK (notification_type IN ('late_arrival', 'absence', 'follow_up')),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_subject TEXT,
    email_body TEXT,
    response_received BOOLEAN DEFAULT FALSE,
    response_content TEXT,
    response_received_at TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees(department);
CREATE INDEX IF NOT EXISTS idx_employees_email ON employees(email);
CREATE INDEX IF NOT EXISTS idx_attendance_employee_date ON attendance(employee_id, date);
CREATE INDEX IF NOT EXISTS idx_attendance_date ON attendance(date);
CREATE INDEX IF NOT EXISTS idx_attendance_status ON attendance(status);
CREATE INDEX IF NOT EXISTS idx_attendance_date_status ON attendance(date, status);
CREATE INDEX IF NOT EXISTS idx_notifications_employee ON attendance_notifications(employee_id);
CREATE INDEX IF NOT EXISTS idx_notifications_sent_at ON attendance_notifications(sent_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_employees_updated_at 
    BEFORE UPDATE ON employees 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_attendance_updated_at 
    BEFORE UPDATE ON attendance 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default departments
INSERT INTO departments (name, description) VALUES
('HR', 'Human Resources - Employee management and policies'),
('Finance', 'Financial operations and accounting'),
('IT', 'Information Technology and systems'),
('Sales', 'Sales and customer acquisition'),
('Marketing', 'Marketing and brand management'),
('Operations', 'Business operations and logistics')
ON CONFLICT (name) DO NOTHING;

-- Create useful views
CREATE OR REPLACE VIEW employee_attendance_summary AS
SELECT 
    e.id,
    e.name,
    e.email,
    e.department,
    COUNT(a.id) as total_days_recorded,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_days,
    COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_days,
    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_days,
    ROUND(
        COUNT(CASE WHEN a.status = 'present' THEN 1 END) * 100.0 / 
        NULLIF(COUNT(CASE WHEN a.status IN ('present', 'late', 'absent') THEN 1 END), 0), 
        2
    ) as attendance_percentage
FROM employees e
LEFT JOIN attendance a ON e.id = a.employee_id
GROUP BY e.id, e.name, e.email, e.department;

CREATE OR REPLACE VIEW daily_attendance_report AS
SELECT 
    a.date,
    COUNT(*) as total_employees,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present,
    COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late,
    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent,
    ROUND(COUNT(CASE WHEN a.status = 'present' THEN 1 END) * 100.0 / COUNT(*), 2) as present_percentage,
    ROUND(COUNT(CASE WHEN a.status = 'late' THEN 1 END) * 100.0 / COUNT(*), 2) as late_percentage
FROM attendance a
GROUP BY a.date
ORDER BY a.date DESC;

CREATE OR REPLACE VIEW recent_late_arrivals AS
SELECT 
    e.name,
    e.email,
    e.department,
    a.date,
    a.check_in_time,
    a.notes,
    CASE 
        WHEN an.id IS NOT NULL THEN 'Notified'
        ELSE 'Not Notified'
    END as notification_status
FROM employees e
JOIN attendance a ON e.id = a.employee_id
LEFT JOIN attendance_notifications an ON a.id = an.attendance_id
WHERE a.status = 'late' 
    AND a.date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY a.date DESC, e.name;

-- Grant permissions to hradmin user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hradmin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hradmin;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO hradmin;

-- Display schema information
SELECT 'Schema created successfully!' as status;
SELECT 'Tables created:' as info;
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
ORDER BY table_name;