-- MamaCare Seed Data for Evaluation & Viva Voce
USE mamacare_db;

-- Insert a demo test user (password is 'password123')
INSERT IGNORE INTO users (id, name, email, password_hash, lmp_date, due_date, blood_group, emergency_contact_name, emergency_contact_phone)
VALUES (
    1,
    'Sarah Johnson',
    'sarah@example.com',
    'scrypt:32768:8:1$uH2tqE6u5f0x1q2w$98e1f0e4fb90172e2cfbc3fbc19c01bc89a74c74032d8471bc60731fa63bc872cb039bb871a28a3f81e37f61c6b659c2593d6e5ef8cb5c102a0a2df339c94b79',
    DATE_SUB(CURDATE(), INTERVAL 140 DAY),
    DATE_ADD(DATE_SUB(CURDATE(), INTERVAL 140 DAY), INTERVAL 280 DAY),
    'O+',
    'Michael Johnson (Husband)',
    '+1 (555) 234-5678'
);

-- Sample Doctor Appointments
INSERT INTO appointments (user_id, doctor_name, clinic_hospital, appointment_date, appointment_time, reason, notes, is_completed)
VALUES 
(1, 'Dr. Emily Carter, OB-GYN', 'City Maternity Hospital, Suite 302', DATE_ADD(CURDATE(), INTERVAL 5 DAY), '10:30:00', '20-Week Anatomy Scan', 'Drink 2 glasses of water prior to ultrasound.', FALSE),
(1, 'Dr. Robert Davis', 'Wellness Family Clinic', DATE_ADD(CURDATE(), INTERVAL 20 DAY), '14:00:00', 'Routine Prenatal Checkup & Blood Pressure', 'Discuss iron supplement dosage.', FALSE);

-- Sample Medicine Reminders
INSERT INTO medicine_reminders (user_id, medicine_name, dosage, frequency, reminder_time, instructions, is_active)
VALUES
(1, 'Prenatal Multivitamin with DHA', '1 Tablet', 'Once daily', '08:30:00', 'After breakfast', TRUE),
(1, 'Ferrous Sulfate (Iron)', '65 mg', 'Once daily', '13:00:00', 'Take with orange juice for absorption', TRUE),
(1, 'Calcium Carbonate + Vit D3', '500 mg', 'Twice daily', '20:00:00', 'Take with dinner / bedtime', TRUE);

-- Sample Meal Reminders
INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
VALUES
(1, 'Warm Oatmeal with Walnuts & Chia Seeds', 'Breakfast', '08:00:00', 'Rich in iron, folate and slow-release carbs', TRUE),
(1, 'Greek Yogurt with Sliced Strawberries', 'Morning Snack', '11:00:00', 'High calcium and protein boost', TRUE),
(1, 'Spinach Lentil Bowl with Brown Rice & Avocado', 'Lunch', '13:00:00', 'Plant iron paired with healthy fats for DHA absorption', TRUE),
(1, 'Roasted Chickpeas & 1 Glass Lemon Water', 'Evening Snack', '17:00:00', 'High fiber and hydration replenisher', TRUE),
(1, 'Steamed Vegetables with Paneer/Tofu & Quinoa', 'Dinner', '20:00:00', 'Light, easily digestible to avoid nighttime heartburn', TRUE);

-- Sample User Diet Preferences
INSERT INTO user_diet_preferences (user_id, trimester, pregnancy_week, dietary_preference, allergies, dietary_restrictions, foods_usually_eaten, medical_conditions)
VALUES
(1, 2, 20, 'Vegetarian', 'None', 'Low Sodium', 'Oatmeal, Lentil soup, Paneer, Spinach, Bananas, Apples, Yogurt, Brown Rice', 'None');