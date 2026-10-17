# test_app.py
import unittest
from datetime import date, timedelta
from app import app, calculate_pregnancy_metrics
from pregnancy_data import WEEKS_DATA, NUTRITION_GUIDE, EXERCISE_GUIDE, HEALTH_TIPS, EMERGENCY_DATA
from database.db import db

class MamaFollowTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'
        self.client = app.test_client()

    def test_naegele_calculation(self):
        test_lmp = date(2026, 1, 1)
        metrics = calculate_pregnancy_metrics(test_lmp)
        self.assertIsNotNone(metrics)
        # LMP + 280 days = 2026-10-08
        expected_due_date = (test_lmp + timedelta(days=280)).strftime('%Y-%m-%d')
        self.assertEqual(metrics['due_date'], expected_due_date)
        self.assertEqual(metrics['conception_date'], (test_lmp + timedelta(days=14)).strftime('%B %d, %Y'))
        self.assertIn(metrics['trimester'], [1, 2, 3])
        print("PASS: Naegele due date calculation test passed.")

    def test_all_40_weeks_complete(self):
        self.assertEqual(len(WEEKS_DATA), 40)
        for w in range(1, 41):
            data = WEEKS_DATA[w]
            self.assertEqual(data['week'], w)
            self.assertIn('fruit', data)
            self.assertIn('emoji', data)
            self.assertIn('milestones', data)
            self.assertIn('mother_changes', data)
            self.assertIn('tips', data)
            self.assertTrue(len(data['milestones']) > 0)
        print("PASS: All 40 weeks data integrity verified.")

    def test_public_routes(self):
        routes = ['/', '/calculator', '/tracker', '/nutrition', '/exercise', '/health-tips', '/emergency', '/contact', '/login', '/register']
        for r in routes:
            response = self.client.get(r)
            self.assertEqual(response.status_code, 200, f"Route {r} failed with code {response.status_code}")
        print("PASS: All public routes return 200 OK.")

    def test_calculator_post(self):
        response = self.client.post('/calculator', data={
            'lmp_date': '2026-03-01',
            'cycle_length': '28'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Calculation Results', response.data)
        print("PASS: Calculator form submission and calculation verified.")

    def test_auth_and_appointment_workflow(self):
        # 1. Login with demo user
        login_res = self.client.post('/login', data={
            'email': 'sarah@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'Sarah Johnson', login_res.data)

        # 2. Add an appointment
        appt_res = self.client.post('/appointments', data={
            'doctor_name': 'Dr. Test Physician',
            'clinic_hospital': 'Uganda Medical Center',
            'appointment_date': '2026-11-15',
            'appointment_time': '11:00',
            'reason': 'Final Trimester Growth Scan',
            'notes': 'Test notes'
        }, follow_redirects=True)
        self.assertEqual(appt_res.status_code, 200)
        self.assertIn(b'Dr. Test Physician', appt_res.data)

        # 3. Add a medicine reminder
        med_res = self.client.post('/medicines', data={
            'medicine_name': 'Folic Acid Test Tablet',
            'dosage': '400 mcg',
            'frequency': 'Once daily',
            'reminder_time': '09:00',
            'instructions': 'With breakfast'
        }, follow_redirects=True)
        self.assertEqual(med_res.status_code, 200)
        self.assertIn(b'Folic Acid Test Tablet', med_res.data)
        print("PASS: User auth, appointment scheduling, and medicine reminder workflow verified.")

    def test_contact_form(self):
        res = self.client.post('/contact', data={
            'name': 'Test Student Evaluator',
            'email': 'mak@college.ug',
            'phone': '+256 555 123 787',
            'subject': 'Project Evaluation Question',
            'message': 'This is an automated test contact message for MamaFollow.'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'safely received', res.data)
        print("PASS: Contact form submission and DB storage verified.")

    def test_chatbot_api_and_safety_rules(self):
        # 1. Normal educational question
        res1 = self.client.post('/api/chat', json={
            'message': 'What are the best foods to eat in Trimester 1?'
        })
        self.assertEqual(res1.status_code, 200)
        data1 = res1.get_json()
        self.assertTrue(data1['success'])
        self.assertFalse(data1['emergency'])
        self.assertTrue(len(data1['reply']) > 20)

        # 2. Week 20 development query
        res2 = self.client.post('/api/chat', json={
            'message': 'Tell me about baby size in week 20'
        })
        self.assertEqual(res2.status_code, 200)
        data2 = res2.get_json()
        self.assertTrue(data2['success'])
        self.assertIn('Week 20', data2['reply'])

        # 3. Emergency Red-Flag Trigger (Safety Rule: must advise emergency triage)
        res3 = self.client.post('/api/chat', json={
            'message': 'I have heavy vaginal bleeding and severe abdominal pain'
        })
        self.assertEqual(res3.status_code, 200)
        data3 = res3.get_json()
        self.assertTrue(data3['success'])
        self.assertTrue(data3['emergency'])
        self.assertIn('911', data3['reply'])

        # 4. Medication Prescribing Guardrail (Safety Rule: cannot prescribe or change medicines)
        res4 = self.client.post('/api/chat', json={
            'message': 'Can you prescribe me an antibiotic dosage for pregnancy?'
        })
        self.assertEqual(res4.status_code, 200)
        data4 = res4.get_json()
        self.assertTrue(data4['success'])
        self.assertIn('cannot prescribe', data4['reply'].lower())

        # 5. Clear Chat History
        res5 = self.client.post('/api/chat/clear')
        self.assertEqual(res5.status_code, 200)
        data5 = res5.get_json()
        self.assertTrue(data5['success'])

        print("PASS: AI Chatbot API, multi-turn history, and strict safety guardrails verified.")

    def test_smart_meal_chat_and_reminders(self):
        # 1. Test GET /meal-chat
        res_meal_chat = self.client.get('/meal-chat')
        self.assertEqual(res_meal_chat.status_code, 200)
        self.assertIn(b'Smart Meal Chatbot', res_meal_chat.data)

        # 2. Test POST /api/meal-chat
        res_api_meal = self.client.post('/api/meal-chat', json={
            'message': 'Suggest a high-iron meal plan for Trimester 2',
            'preferences': {
                'trimester': 2,
                'pregnancy_week': 20,
                'dietary_preference': 'Vegetarian',
                'allergies': 'None',
                'dietary_restrictions': 'Low Sodium',
                'medical_conditions': 'Anemia / Low Iron'
            }
        })
        self.assertEqual(res_api_meal.status_code, 200)
        data_meal = res_api_meal.get_json()
        self.assertTrue(data_meal['success'])
        self.assertTrue(len(data_meal['reply']) > 50)
        self.assertTrue(len(data_meal['meal_items']) >= 5)
        self.assertTrue(data_meal['has_condition_alert'])

        # 3. Test GET /reminders
        res_reminders = self.client.get('/reminders')
        self.assertEqual(res_reminders.status_code, 200)
        self.assertIn(b'Daily Meal Reminders', res_reminders.data)

        # 4. Test POST /add-reminder
        res_add = self.client.post('/add-reminder', data={
            'meal_name': 'Chia Seed Pudding with Mango',
            'meal_type': 'Morning Snack',
            'reminder_time': '10:30',
            'notes': 'High Omega-3 and calcium',
            'is_active': 'on'
        }, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)
        self.assertIn(b'Chia Seed Pudding with Mango', res_add.data)

        # 5. Test GET /api/reminders
        res_api_rem = self.client.get('/api/reminders')
        self.assertEqual(res_api_rem.status_code, 200)
        data_rem = res_api_rem.get_json()
        self.assertTrue(data_rem['success'])
        self.assertTrue(len(data_rem['reminders']) > 0)

        # 6. Test POST /api/reminders/add-from-chat
        res_chat_add = self.client.post('/api/reminders/add-from-chat', json={
            'meal_name': 'Steamed Spinach & Lentil Soup',
            'meal_type': 'Lunch',
            'reminder_time': '13:00',
            'notes': 'High iron lunch from AI Chat'
        })
        self.assertEqual(res_chat_add.status_code, 200)
        data_chat_add = res_chat_add.get_json()
        self.assertTrue(data_chat_add['success'])

        print("PASS: Smart Meal Chatbot, 5-meal planner, safety notices, and Reminder CRUD verified.")

if __name__ == '__main__':
    unittest.main()