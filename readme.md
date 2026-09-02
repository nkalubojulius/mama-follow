# MamaCare – Pregnancy Care and Monitoring Website
**A Modern, Responsive, and User-Friendly Web Application for Maternal Health and Pregnancy Tracking**  
*College Final-Year Project*

---

## 1. Project Overview & Abstract

**MamaCare** is an evidence-based pregnancy care and monitoring web application created to assist expectant mothers throughout the 40 weeks of gestation. The platform combines clinical due date estimation algorithms (**Naegele's Rule**), developmental milestone tracking, personalized nutrition and safe exercise guidance, clinical appointment management, and daily medication reminders into an intuitive, maternal-themed web interface.

> **Crucial Medical Disclaimer:**  
> MamaCare is developed strictly for educational and informational support and is **not** a replacement for professional medical advice, clinical diagnosis, or emergency obstetric care.

---

## 2. Key Modules & Functional Features

1. **Home Page & Maternal Dashboard**:
   - Engaging welcome banner, quick due date estimator, feature highlights, and pregnancy progress tracking widget.
2. **Due Date Calculator (Naegele's Rule)**:
   - Accurately computes the Estimated Due Date (EDD), Estimated Conception Date, Trimester classification, and days remaining based on the user's Last Menstrual Period (LMP) and menstrual cycle length.
3. **40-Week Interactive Pregnancy Tracker**:
   - Week-by-week fetal development milestones (heartbeat, organogenesis, bone calcification, lung maturity).
   - Relatable fruit and vegetable size analogies (e.g. Avocado at Week 16, Banana at Week 20, Watermelon at Week 40).
   - Expected maternal physical symptoms, body changes, and weekly clinical action checklists.
4. **Nutrition & Hydration Guide**:
   - Trimester-specific nutrient breakdowns (Folic Acid, Iron, Calcium, Omega-3 DHA, Vitamin D).
   - Comprehensive food safety matrix highlighting high-risk foods to avoid (high-mercury fish, unpasteurized dairy, raw meats).
   - Interactive client-side 8-glass daily water tracker with local storage persistence.
5. **Exercise & Kegel Guide**:
   - Safe, low-impact exercise recommendations organized by trimester (walking, prenatal yoga, swimming, stationary cycling).
   - Exercise contraindications and warning stop signals.
   - Interactive animated **Kegel Pelvic Floor Trainer** with visual contraction/relaxation indicators and audio cues.
6. **Health Tips & Symptom Relief**:
   - Sleep guidance (the "SOS - Sleep On Side" position and pillow placement).
   - Natural remedies for morning sickness, heartburn, backache, and leg cramps.
   - Maternal mental health and mindfulness techniques.
7. **Doctor Appointment Reminders**:
   - Add, view, complete, and delete scheduled obstetrician visits and ultrasound scans.
   - Standard clinical prenatal visit timeline (monthly, bi-weekly, weekly).
8. **Medicine & Supplement Reminders**:
   - Daily medication manager for prenatal vitamins, iron, and calcium supplements.
   - One-tap "Mark Taken Today" tracking with timestamps.
9. **User Authentication & Personal Profile**:
   - Secure user registration, login, and session management using **Werkzeug password hashing**.
   - Profile management with dynamic gestational age progress and emergency contacts.
10. **Emergency Red-Flag Information**:
    - Danger sign checklist (preeclampsia symptoms, heavy bleeding, fluid leakage, decreased fetal movements).
    - 24/7 national emergency hotline directory.
    - Comprehensive hospital go-bag checklist for mom, baby, and birth partner.
11. **MamaCare AI Chatbot Assistant**:
    - Interactive floating assistant in bottom-right corner for 24/7 educational pregnancy guidance.
    - Powered by **Google GenAI (Gemini 2.5 Flash)** with an intelligent clinical Knowledge Engine fallback.
    - Answers questions on trimesters, 40-week milestones, nutrition, safe exercises, hydration, symptom relief, and due dates.
    - **Strict Medical Guardrails**: Immediate emergency red-flag triage detection, medication prescribing refusal, and prominent educational disclaimers.
12. **Smart Meal Chatbot (`/meal-chat`)**:
    - AI-powered nutrition planner accepting trimester, gestational week, food preferences (Veg/Non-Veg/Vegan/Pescatarian), allergies, dietary restrictions, and medical conditions (Gestational Diabetes, Anemia, Hypertension, Morning Sickness).
    - Crafts complete 5-meal daily plans (Breakfast 🌅, Morning Snack 🍎, Lunch 🥗, Evening Snack 🥑, Dinner 🍲, Hydration 💧).
    - Includes one-click **"Add to Meal Reminders"** buttons to schedule recommended meals instantly.
13. **Daily Meal Reminders & Alarm Engine (`/reminders`)**:
    - Comprehensive meal scheduling dashboard with CRUD management (add, edit, delete, toggle active).
    - Real-time client-side alarm engine with gentle Web Audio API melodic chimes (`playMealAlarmChime()`).
    - Dismissible on-screen toast banners with 10-minute snooze and "Mark Eaten" tracking.
    - Native HTML5 browser notifications.
    - 1-click **"Load Recommended Schedule"** preset generator.
14. **Contact Us & FAQ System**:
    - User inquiry form stored securely in the database.
    - Interactive accordion answering common pregnancy questions.

---

## 3. Technology Stack

- **Frontend**: HTML5, CSS3 (Custom responsive styling with soft maternal pastel theme), JavaScript (ES6+), Bootstrap 5.3, FontAwesome 6.
- **Backend**: Python 3, Flask framework, Werkzeug security.
- **Database**: MySQL (with seamless zero-configuration SQLite automatic fallback).
- **Algorithms**: Naegele's Rule, Date Difference Gestational Calculator, Trimester Rule-Based Guidance Logic.

---

## 4. Mathematical Algorithms & Clinical Formulas

### 1. Naegele's Rule for Due Date Calculation
$$\text{Estimated Due Date (EDD)} = \text{LMP} + 280\text{ days}$$
*(Or: $\text{LMP Year} + 1\text{ year} - 3\text{ months} + 7\text{ days} + (\text{Cycle Length} - 28\text{ days})$)*

### 2. Estimated Conception Date
$$\text{Conception Date} = \text{LMP} + 14\text{ days}$$

### 3. Current Gestational Age
$$\text{Days Pregnant} = \max(0, \text{Today} - \text{LMP})$$
$$\text{Current Week} = \lfloor\text{Days Pregnant} / 7\rfloor + 1$$
$$\text{Current Day} = \text{Days Pregnant} \pmod 7$$

### 4. Gestational Progress Percentage
$$\text{Progress \%} = \min\left(100, \max\left(0, \text{round}\left(\frac{\text{Days Pregnant}}{280} \times 100\right)\right)\right)$$

---

## 5. Database Schema

- **`users`**: `id`, `name`, `email`, `password_hash`, `lmp_date`, `due_date`, `blood_group`, `emergency_contact_name`, `emergency_contact_phone`, `created_at`
- **`appointments`**: `id`, `user_id`, `doctor_name`, `clinic_hospital`, `appointment_date`, `appointment_time`, `reason`, `notes`, `is_completed`, `created_at`
- **`medicine_reminders`**: `id`, `user_id`, `medicine_name`, `dosage`, `frequency`, `reminder_time`, `instructions`, `is_active`, `last_taken_date`, `created_at`
- **`meal_reminders`**: `id`, `user_id`, `meal_name`, `meal_type`, `reminder_time`, `notes`, `is_active`, `created_at`
- **`user_diet_preferences`**: `id`, `user_id`, `trimester`, `pregnancy_week`, `dietary_preference`, `allergies`, `dietary_restrictions`, `foods_usually_eaten`, `medical_conditions`, `updated_at`
- **`contact_messages`**: `id`, `name`, `email`, `phone`, `subject`, `message`, `status`, `created_at`
- **`pregnancy_logs`**: `id`, `user_id`, `week_number`, `weight_kg`, `blood_pressure`, `mood`, `symptoms`, `log_date`, `created_at`

---

## 6. How to Run the Project

### Step 1: Install Dependencies
```bash
cd pregnancy-care-website
pip install -r requirements.txt
```

### Step 2: Configure Database (Optional)
- **Option A (MySQL - Recommended for Production)**: Start your local MySQL server (XAMPP / WAMP / MySQL Server). The application automatically connects to database `mamacare_db` on `localhost:3306` with user `root`.
- **Option B (Zero-Configuration SQLite - Automatic Fallback)**: If MySQL is not running or credentials are not configured, MamaCare **automatically creates and initializes a local SQLite database** (`database/mamacare.db`) with full sample data so the application runs seamlessly out-of-the-box!

### Step 3: Start the Flask Application
```bash
python app.py
```
Open your web browser and navigate to: **`http://127.0.0.1:5000`**

### Preloaded Demo Account (for Viva/Testing):
- **Email:** `sarah@example.com`
- **Password:** `password123`

---

## 7. College Viva Voce Examination Q&A

**Q1: What is the main objective of the MamaCare project?**  
*Answer:* To provide expectant mothers with an accessible, clinically informed web platform to calculate due dates, monitor 40 weeks of fetal growth, access safe nutrition and exercise guidelines, and manage medical appointments and daily medications.

**Q2: How does Naegele's Rule calculate the pregnancy due date?**  
*Answer:* Naegele's Rule adds 280 days (40 weeks / 10 lunar months) to the first day of the mother's Last Menstrual Period (LMP). It also accounts for menstrual cycle length variations beyond 28 days.

**Q3: How are passwords stored securely in MamaCare?**  
*Answer:* Passwords are never stored in plain text. They are hashed using cryptographic salt-hash algorithms (`scrypt` or `pbkdf2:sha256`) via Python's `werkzeug.security` module.

**Q4: How does the application handle database portability?**  
*Answer:* MamaCare includes a unified Database Manager (`database/db.py`) that targets MySQL by default, but provides an intelligent automatic fallback to SQLite if MySQL is offline, ensuring zero startup failure during evaluation.
