# app.py
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database.db import db
from pregnancy_data import WEEKS_DATA, NUTRITION_GUIDE, EXERCISE_GUIDE, HEALTH_TIPS, EMERGENCY_DATA
from chatbot_engine import chatbot_service
from meal_chat_engine import meal_chat_service

app = Flask(__name__)
app.config.from_object(Config)

def calculate_pregnancy_metrics(lmp_date_obj):
    if not lmp_date_obj:
        return None
    today = date.today()
    # Naegele's Rule: LMP + 280 days (40 weeks)
    due_date = lmp_date_obj + timedelta(days=280)
    conception_date = lmp_date_obj + timedelta(days=14)
    days_pregnant = max(0, (today - lmp_date_obj).days)
    days_remaining = max(0, (due_date - today).days)
    
    current_week = min(40, max(1, (days_pregnant // 7) + 1))
    current_day = days_pregnant % 7
    
    if current_week <= 12:
        trimester = 1
        trimester_name = "First Trimester"
    elif current_week <= 27:
        trimester = 2
        trimester_name = "Second Trimester"
    else:
        trimester = 3
        trimester_name = "Third Trimester"
        
    progress_pct = min(100, max(0, round((days_pregnant / 280) * 100, 1)))
    
    return {
        'lmp_date': lmp_date_obj.strftime('%Y-%m-%d'),
        'due_date': due_date.strftime('%Y-%m-%d'),
        'due_date_formatted': due_date.strftime('%B %d, %Y'),
        'conception_date': conception_date.strftime('%B %d, %Y'),
        'days_pregnant': days_pregnant,
        'days_remaining': days_remaining,
        'current_week': current_week,
        'current_day': current_day,
        'trimester': trimester,
        'trimester_name': trimester_name,
        'progress_pct': progress_pct,
        'week_data': WEEKS_DATA.get(current_week, WEEKS_DATA[20])
    }

def get_current_user():
    if 'user_id' in session:
        return db.query("SELECT * FROM users WHERE id = %s", (session['user_id'],), fetchone=True)
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this feature.", "warning")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_globals():
    user = get_current_user()
    user_metrics = None
    if user and user.get('lmp_date'):
        try:
            if isinstance(user['lmp_date'], str):
                lmp_obj = datetime.strptime(user['lmp_date'], '%Y-%m-%d').date()
            else:
                lmp_obj = user['lmp_date']
            user_metrics = calculate_pregnancy_metrics(lmp_obj)
        except Exception:
            user_metrics = None
    return {
        'current_user': user,
        'user_metrics': user_metrics,
        'current_year': date.today().year
    }

# ----------------- MAIN ROUTES ----------------- #

@app.route('/')
def index():
    user = get_current_user()
    recent_appointments = []
    active_medicines = []
    if user:
        recent_appointments = db.query(
            "SELECT * FROM appointments WHERE user_id = %s AND appointment_date >= %s ORDER BY appointment_date ASC LIMIT 2",
            (user['id'], date.today().strftime('%Y-%m-%d')),
            fetchall=True
        ) or []
        active_medicines = db.query(
            "SELECT * FROM medicine_reminders WHERE user_id = %s AND is_active = 1 LIMIT 3",
            (user['id'],),
            fetchall=True
        ) or []
    return render_template('index.html', recent_appointments=recent_appointments, active_medicines=active_medicines)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    input_lmp = None
    cycle_length = 28
    if request.method == 'POST':
        input_lmp = request.form.get('lmp_date')
        try:
            cycle_length = int(request.form.get('cycle_length', 28))
        except ValueError:
            cycle_length = 28
            
        if input_lmp:
            try:
                lmp_date_obj = datetime.strptime(input_lmp, '%Y-%m-%d').date()
                # Cycle length adjustment: Standard Naegele assumes 28-day cycle.
                # If cycle != 28, adjust LMP by (cycle - 28) days
                adjusted_lmp = lmp_date_obj + timedelta(days=(cycle_length - 28))
                result = calculate_pregnancy_metrics(adjusted_lmp)
                # Keep the user's entered LMP in result display
                result['input_lmp'] = input_lmp
                result['cycle_length'] = cycle_length
                
                # If user is logged in, optionally prompt to save LMP
                if 'user_id' in session and request.form.get('save_to_profile') == 'yes':
                    due_date_str = result['due_date']
                    db.query(
                        "UPDATE users SET lmp_date = %s, due_date = %s WHERE id = %s",
                        (input_lmp, due_date_str, session['user_id']),
                        commit=True
                    )
                    flash("Due date and LMP updated to your profile successfully!", "success")
            except ValueError:
                flash("Invalid date format entered. Please select a valid date.", "danger")
    return render_template('calculator.html', result=result, input_lmp=input_lmp, cycle_length=cycle_length)

@app.route('/tracker')
def tracker():
    user = get_current_user()
    default_week = 20
    if user and user.get('lmp_date'):
        try:
            if isinstance(user['lmp_date'], str):
                lmp_obj = datetime.strptime(user['lmp_date'], '%Y-%m-%d').date()
            else:
                lmp_obj = user['lmp_date']
            metrics = calculate_pregnancy_metrics(lmp_obj)
            if metrics:
                default_week = metrics['current_week']
        except Exception:
            pass
            
    selected_week = request.args.get('week', default=default_week, type=int)
    if selected_week < 1 or selected_week > 40:
        selected_week = 20
        
    week_info = WEEKS_DATA.get(selected_week, WEEKS_DATA[20])
    return render_template('tracker.html', selected_week=selected_week, week_info=week_info, all_weeks=WEEKS_DATA)

@app.route('/nutrition')
def nutrition():
    selected_trimester = request.args.get('trimester', default=1, type=int)
    if selected_trimester not in [1, 2, 3]:
        selected_trimester = 1
    return render_template('nutrition.html', nutrition_data=NUTRITION_GUIDE, selected_trimester=selected_trimester)

@app.route('/exercise')
def exercise():
    selected_trimester = request.args.get('trimester', default=1, type=int)
    if selected_trimester not in [1, 2, 3]:
        selected_trimester = 1
    return render_template('exercise.html', exercise_data=EXERCISE_GUIDE, selected_trimester=selected_trimester)

@app.route('/health-tips')
def health_tips():
    return render_template('health_tips.html', health_data=HEALTH_TIPS)

@app.route('/emergency')
def emergency():
    return render_template('emergency.html', emergency_data=EMERGENCY_DATA)

# ----------------- APPOINTMENT REMINDERS ----------------- #

@app.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    user_id = session['user_id']
    if request.method == 'POST':
        doctor_name = request.form.get('doctor_name', '').strip()
        clinic_hospital = request.form.get('clinic_hospital', '').strip()
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason', '').strip()
        notes = request.form.get('notes', '').strip()
        
        if not doctor_name or not appointment_date or not appointment_time or not reason:
            flash("Please fill in all required appointment fields.", "danger")
        else:
            db.query(
                """
                INSERT INTO appointments (user_id, doctor_name, clinic_hospital, appointment_date, appointment_time, reason, notes, is_completed)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
                """,
                (user_id, doctor_name, clinic_hospital, appointment_date, appointment_time, reason, notes),
                commit=True
            )
            flash("Doctor appointment scheduled successfully!", "success")
            return redirect(url_for('appointments'))

    # Retrieve all appointments for this user
    all_appointments = db.query(
        "SELECT * FROM appointments WHERE user_id = %s ORDER BY appointment_date ASC, appointment_time ASC",
        (user_id,),
        fetchall=True
    ) or []
    
    upcoming = []
    completed = []
    today_str = date.today().strftime('%Y-%m-%d')
    for appt in all_appointments:
        if appt.get('is_completed') or str(appt['appointment_date']) < today_str:
            completed.append(appt)
        else:
            upcoming.append(appt)
            
    return render_template('appointments.html', upcoming=upcoming, completed=completed, today=today_str)

@app.route('/appointments/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_appointment(id):
    user_id = session['user_id']
    appt = db.query("SELECT is_completed FROM appointments WHERE id = %s AND user_id = %s", (id, user_id), fetchone=True)
    if appt:
        new_status = 0 if appt['is_completed'] else 1
        db.query("UPDATE appointments SET is_completed = %s WHERE id = %s AND user_id = %s", (new_status, id, user_id), commit=True)
        flash("Appointment status updated.", "info")
    return redirect(url_for('appointments'))

@app.route('/appointments/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    user_id = session['user_id']
    db.query("DELETE FROM appointments WHERE id = %s AND user_id = %s", (id, user_id), commit=True)
    flash("Appointment removed successfully.", "info")
    return redirect(url_for('appointments'))

# ----------------- MEDICINE REMINDERS ----------------- #

@app.route('/medicines', methods=['GET', 'POST'])
@login_required
def medicines():
    user_id = session['user_id']
    if request.method == 'POST':
        medicine_name = request.form.get('medicine_name', '').strip()
        dosage = request.form.get('dosage', '').strip()
        frequency = request.form.get('frequency', 'Once daily')
        reminder_time = request.form.get('reminder_time')
        instructions = request.form.get('instructions', 'With food')
        
        if not medicine_name or not dosage or not reminder_time:
            flash("Please provide medicine name, dosage, and reminder time.", "danger")
        else:
            db.query(
                """
                INSERT INTO medicine_reminders (user_id, medicine_name, dosage, frequency, reminder_time, instructions, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, 1)
                """,
                (user_id, medicine_name, dosage, frequency, reminder_time, instructions),
                commit=True
            )
            flash("Medicine reminder added successfully!", "success")
            return redirect(url_for('medicines'))

    all_medicines = db.query(
        "SELECT * FROM medicine_reminders WHERE user_id = %s ORDER BY reminder_time ASC",
        (user_id,),
        fetchall=True
    ) or []
    
    today_str = date.today().strftime('%Y-%m-%d')
    return render_template('medicines.html', medicines=all_medicines, today_str=today_str)

@app.route('/medicines/toggle-active/<int:id>', methods=['POST'])
@login_required
def toggle_medicine_active(id):
    user_id = session['user_id']
    med = db.query("SELECT is_active FROM medicine_reminders WHERE id = %s AND user_id = %s", (id, user_id), fetchone=True)
    if med:
        new_active = 0 if med['is_active'] else 1
        db.query("UPDATE medicine_reminders SET is_active = %s WHERE id = %s AND user_id = %s", (new_active, id, user_id), commit=True)
        flash("Medicine reminder updated.", "info")
    return redirect(url_for('medicines'))

@app.route('/medicines/mark-taken/<int:id>', methods=['POST'])
@login_required
def mark_medicine_taken(id):
    user_id = session['user_id']
    today_str = date.today().strftime('%Y-%m-%d')
    db.query(
        "UPDATE medicine_reminders SET last_taken_date = %s WHERE id = %s AND user_id = %s",
        (today_str, id, user_id),
        commit=True
    )
    flash("Great job! Dose logged for today.", "success")
    return redirect(url_for('medicines'))

@app.route('/medicines/delete/<int:id>', methods=['POST'])
@login_required
def delete_medicine(id):
    user_id = session['user_id']
    db.query("DELETE FROM medicine_reminders WHERE id = %s AND user_id = %s", (id, user_id), commit=True)
    flash("Medicine reminder deleted.", "info")
    return redirect(url_for('medicines'))

# ----------------- CONTACT US ----------------- #

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        if not name or not email or not subject or not message:
            flash("Please fill in all required contact fields.", "danger")
        else:
            db.query(
                """
                INSERT INTO contact_messages (name, email, phone, subject, message, status)
                VALUES (%s, %s, %s, %s, %s, 'Unread')
                """,
                (name, email, phone, subject, message),
                commit=True
            )
            flash("Thank you for reaching out! Your message has been safely received. A MamaFollow care coordinator will reply soon.", "success")
            return redirect(url_for('contact'))
            
    return render_template('contact.html')

# ----------------- USER AUTH & PROFILE ----------------- #

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('profile'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        lmp_date = request.form.get('lmp_date')
        blood_group = request.form.get('blood_group', '').strip()
        emergency_name = request.form.get('emergency_contact_name', '').strip()
        emergency_phone = request.form.get('emergency_contact_phone', '').strip()
        
        if not name or not email or not password:
            flash("Name, Email, and Password are required.", "danger")
        elif password != confirm_password:
            flash("Passwords do not match.", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
        else:
            existing = db.query("SELECT id FROM users WHERE email = %s", (email,), fetchone=True)
            if existing:
                flash("An account with this email already exists. Please log in.", "warning")
            else:
                due_date_str = None
                if lmp_date:
                    try:
                        lmp_obj = datetime.strptime(lmp_date, '%Y-%m-%d').date()
                        due_date_str = (lmp_obj + timedelta(days=280)).strftime('%Y-%m-%d')
                    except ValueError:
                        lmp_date = None
                        
                pass_hash = generate_password_hash(password)
                new_id = db.query(
                    """
                    INSERT INTO users (name, email, password_hash, lmp_date, due_date, blood_group, emergency_contact_name, emergency_contact_phone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (name, email, pass_hash, lmp_date or None, due_date_str, blood_group, emergency_name, emergency_phone),
                    commit=True,
                    return_lastrowid=True
                )
                session['user_id'] = new_id
                session['user_name'] = name
                flash(f"Welcome to MamaFollow, {name}! Your maternal wellness journey begins now.", "success")
                return redirect(url_for('profile'))
                
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('profile'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        
        user = db.query("SELECT * FROM users WHERE email = %s", (email,), fetchone=True)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back, {user['name']}!", "success")
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile'))
        else:
            flash("Invalid email or password. Please try again.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out safely. Take care!", "info")
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    user = db.query("SELECT * FROM users WHERE id = %s", (user_id,), fetchone=True)
    
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_profile':
            name = request.form.get('name', '').strip()
            lmp_date = request.form.get('lmp_date')
            blood_group = request.form.get('blood_group', '').strip()
            emergency_name = request.form.get('emergency_contact_name', '').strip()
            emergency_phone = request.form.get('emergency_contact_phone', '').strip()
            
            due_date_str = None
            if lmp_date:
                try:
                    lmp_obj = datetime.strptime(lmp_date, '%Y-%m-%d').date()
                    due_date_str = (lmp_obj + timedelta(days=280)).strftime('%Y-%m-%d')
                except ValueError:
                    lmp_date = None
                    
            db.query(
                """
                UPDATE users 
                SET name = %s, lmp_date = %s, due_date = %s, blood_group = %s, 
                    emergency_contact_name = %s, emergency_contact_phone = %s 
                WHERE id = %s
                """,
                (name, lmp_date or None, due_date_str, blood_group, emergency_name, emergency_phone, user_id),
                commit=True
            )
            session['user_name'] = name
            flash("Profile details updated successfully!", "success")
            return redirect(url_for('profile'))
            
        elif action == 'change_password':
            old_pass = request.form.get('old_password')
            new_pass = request.form.get('new_password')
            confirm_new = request.form.get('confirm_new_password')
            
            if not check_password_hash(user['password_hash'], old_pass):
                flash("Current password incorrect.", "danger")
            elif new_pass != confirm_new:
                flash("New passwords do not match.", "danger")
            elif len(new_pass) < 6:
                flash("New password must be at least 6 characters.", "danger")
            else:
                new_hash = generate_password_hash(new_pass)
                db.query("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, user_id), commit=True)
                flash("Password changed successfully!", "success")
                return redirect(url_for('profile'))

    appointments = db.query(
        "SELECT * FROM appointments WHERE user_id = %s ORDER BY appointment_date ASC LIMIT 3",
        (user_id,),
        fetchall=True
    ) or []
    
    medicines = db.query(
        "SELECT * FROM medicine_reminders WHERE user_id = %s AND is_active = 1",
        (user_id,),
        fetchall=True
    ) or []
    
    return render_template('profile.html', user=user, appointments=appointments, medicines=medicines)

# ----------------- JSON API ENDPOINTS ----------------- #

@app.route('/api/calculate-due-date', methods=['POST'])
def api_calculate():
    data = request.get_json() or {}
    lmp_str = data.get('lmp_date')
    cycle = data.get('cycle_length', 28)
    if not lmp_str:
        return jsonify({'error': 'LMP date is required'}), 400
    try:
        lmp_date_obj = datetime.strptime(lmp_str, '%Y-%m-%d').date()
        adjusted_lmp = lmp_date_obj + timedelta(days=(int(cycle) - 28))
        metrics = calculate_pregnancy_metrics(adjusted_lmp)
        return jsonify({'success': True, 'metrics': metrics})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/week/<int:week_num>')
def api_week(week_num):
    if week_num in WEEKS_DATA:
        return jsonify({'success': True, 'data': WEEKS_DATA[week_num]})
    return jsonify({'error': 'Invalid week'}), 404

# ----------------- CHATBOT API ENDPOINTS ----------------- #

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    user_msg = data.get('message', '').strip()
    if not user_msg:
        return jsonify({'error': 'Message content is required'}), 400
    
    if 'chat_history' not in session:
        session['chat_history'] = []
        
    history = session['chat_history']
    bot_response = chatbot_service.generate_chat_response(user_msg, history)
    
    # Update session history
    history.append({'role': 'user', 'content': user_msg})
    history.append({'role': 'assistant', 'content': bot_response.get('reply', '')})
    session['chat_history'] = history[-10:]
    session.modified = True
    
    return jsonify({
        'success': True,
        'reply': bot_response.get('reply', ''),
        'emergency': bot_response.get('emergency', False),
        'links': bot_response.get('links', [])
    })

@app.route('/api/chat/clear', methods=['POST'])
def api_chat_clear():
    session['chat_history'] = []
    session.modified = True
    return jsonify({'success': True, 'message': 'Chat session history cleared.'})

@app.route('/api/chat/history', methods=['GET'])
def api_chat_history():
    history = session.get('chat_history', [])
    return jsonify({'success': True, 'history': history})

# ----------------- SMART MEAL CHAT & MEAL REMINDER ROUTES ----------------- #

@app.route('/meal-chat', methods=['GET', 'POST'])
def meal_chat():
    user = get_current_user()
    user_id = session.get('user_id')
    
    # Load or initialize dietary preferences
    prefs = None
    if user_id:
        prefs = db.query("SELECT * FROM user_diet_preferences WHERE user_id = %s", (user_id,), fetchone=True)
    
    if not prefs:
        prefs = session.get('diet_preferences', {
            'trimester': 2,
            'pregnancy_week': 20,
            'dietary_preference': 'Vegetarian',
            'allergies': 'None',
            'dietary_restrictions': 'Low Sodium',
            'foods_usually_eaten': 'Oatmeal, Lentil soup, Paneer, Spinach, Bananas, Apples, Yogurt, Brown Rice',
            'medical_conditions': 'None'
        })

    if request.method == 'POST':
        tri = int(request.form.get('trimester', 2))
        week = int(request.form.get('pregnancy_week', 20))
        pref = request.form.get('dietary_preference', 'Vegetarian').strip()
        allergies = request.form.get('allergies', 'None').strip()
        restrictions = request.form.get('dietary_restrictions', 'None').strip()
        usual_foods = request.form.get('foods_usually_eaten', '').strip()
        conditions = request.form.get('medical_conditions', 'None').strip()

        updated_prefs = {
            'trimester': tri,
            'pregnancy_week': week,
            'dietary_preference': pref,
            'allergies': allergies,
            'dietary_restrictions': restrictions,
            'foods_usually_eaten': usual_foods,
            'medical_conditions': conditions
        }
        session['diet_preferences'] = updated_prefs

        if user_id:
            existing = db.query("SELECT id FROM user_diet_preferences WHERE user_id = %s", (user_id,), fetchone=True)
            if existing:
                db.query("""
                    UPDATE user_diet_preferences 
                    SET trimester = %s, pregnancy_week = %s, dietary_preference = %s, allergies = %s, dietary_restrictions = %s, foods_usually_eaten = %s, medical_conditions = %s
                    WHERE user_id = %s
                """, (tri, week, pref, allergies, restrictions, usual_foods, conditions, user_id), commit=True)
            else:
                db.query("""
                    INSERT INTO user_diet_preferences (user_id, trimester, pregnancy_week, dietary_preference, allergies, dietary_restrictions, foods_usually_eaten, medical_conditions)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, tri, week, pref, allergies, restrictions, usual_foods, conditions), commit=True)

        flash("Dietary and nutrition preferences updated successfully! 🥗", "success")
        return redirect(url_for('meal_chat'))

    return render_template('meal_chat.html', user=user, prefs=prefs)

@app.route('/api/meal-chat', methods=['POST'])
def api_meal_chat():
    data = request.get_json() or {}
    user_msg = data.get('message', '').strip()
    custom_prefs = data.get('preferences')

    user_id = session.get('user_id')
    prefs = None
    if user_id and not custom_prefs:
        prefs = db.query("SELECT * FROM user_diet_preferences WHERE user_id = %s", (user_id,), fetchone=True)

    if not prefs:
        prefs = custom_prefs or session.get('diet_preferences', {
            'trimester': 2,
            'pregnancy_week': 20,
            'dietary_preference': 'Vegetarian',
            'allergies': 'None',
            'dietary_restrictions': 'Low Sodium',
            'foods_usually_eaten': 'Oatmeal, Lentil soup, Paneer, Spinach, Bananas, Apples, Yogurt, Brown Rice',
            'medical_conditions': 'None'
        })

    if 'meal_chat_history' not in session:
        session['meal_chat_history'] = []

    history = session['meal_chat_history']
    bot_res = meal_chat_service.generate_meal_response(user_msg, prefs, history)

    history.append({'role': 'user', 'content': user_msg})
    history.append({'role': 'assistant', 'content': bot_res.get('reply', '')})
    session['meal_chat_history'] = history[-8:]
    session.modified = True

    return jsonify({
        'success': True,
        'reply': bot_res.get('reply', ''),
        'meal_items': bot_res.get('meal_items', []),
        'has_condition_alert': bot_res.get('has_condition_alert', False),
        'links': bot_res.get('links', [])
    })

@app.route('/reminders')
def reminders():
    user = get_current_user()
    user_id = session.get('user_id')
    
    if user_id:
        meal_reminders = db.query(
            "SELECT * FROM meal_reminders WHERE user_id = %s ORDER BY reminder_time ASC",
            (user_id,),
            fetchall=True
        ) or []
    else:
        meal_reminders = session.get('guest_meal_reminders', [
            {'id': 1, 'meal_name': 'Millet Porridge with Groundnuts and a Boiled Egg', 'meal_type': 'Breakfast', 'reminder_time': '08:00', 'notes': 'Rich in iron, folate and slow-release carbs', 'is_active': 1},
            {'id': 2, 'meal_name': 'Ripe Banana, Orange and Pasteurised Milk', 'meal_type': 'Morning Snack', 'reminder_time': '11:00', 'notes': 'High calcium and protein boost', 'is_active': 1},
            {'id': 3, 'meal_name': 'Matooke with Beans, Dodo and Avocado', 'meal_type': 'Lunch', 'reminder_time': '13:00', 'notes': 'Plant iron paired with healthy fats for DHA absorption', 'is_active': 1},
            {'id': 4, 'meal_name': 'Boiled Sweet Potatoes with Groundnuts/Cowpeas & 1 Glass Lemon Water', 'meal_type': 'Evening Snack', 'reminder_time': '17:00', 'notes': 'High fiber and hydration replenisher', 'is_active': 1},
            {'id': 5, 'meal_name': 'Posho with Well-Cooked Fish and Steamed Sukuma Wiki', 'meal_type': 'Dinner', 'reminder_time': '20:00', 'notes': 'Light, easily digestible to avoid nighttime heartburn', 'is_active': 1}
        ])
    
    return render_template('reminders.html', user=user, reminders=meal_reminders)

@app.route('/add-reminder', methods=['POST'])
def add_reminder():
    user_id = session.get('user_id')
    meal_name = request.form.get('meal_name', '').strip()
    meal_type = request.form.get('meal_type', 'Breakfast').strip()
    reminder_time = request.form.get('reminder_time', '08:00').strip()
    notes = request.form.get('notes', '').strip()
    is_active = 1 if request.form.get('is_active') == 'on' else 1

    if not meal_name:
        flash("Meal name is required.", "danger")
        return redirect(url_for('reminders'))

    if user_id:
        db.query("""
            INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, meal_name, meal_type, reminder_time, notes, is_active), commit=True)
    else:
        reminders_list = session.get('guest_meal_reminders', [])
        new_id = max([r.get('id', 0) for r in reminders_list] or [0]) + 1
        reminders_list.append({
            'id': new_id,
            'meal_name': meal_name,
            'meal_type': meal_type,
            'reminder_time': reminder_time,
            'notes': notes,
            'is_active': is_active
        })
        session['guest_meal_reminders'] = reminders_list
        session.modified = True

    flash(f"Meal reminder for '{meal_name}' added successfully! ⏰", "success")
    return redirect(url_for('reminders'))

@app.route('/edit-reminder/<int:reminder_id>', methods=['POST'])
def edit_reminder(reminder_id):
    user_id = session.get('user_id')
    meal_name = request.form.get('meal_name', '').strip()
    meal_type = request.form.get('meal_type', 'Breakfast').strip()
    reminder_time = request.form.get('reminder_time', '08:00').strip()
    notes = request.form.get('notes', '').strip()
    is_active = 1 if request.form.get('is_active') == 'on' else 0

    if user_id:
        db.query("""
            UPDATE meal_reminders 
            SET meal_name = %s, meal_type = %s, reminder_time = %s, notes = %s, is_active = %s
            WHERE id = %s AND user_id = %s
        """, (meal_name, meal_type, reminder_time, notes, is_active, reminder_id, user_id), commit=True)
    else:
        reminders_list = session.get('guest_meal_reminders', [])
        for r in reminders_list:
            if r.get('id') == reminder_id:
                r['meal_name'] = meal_name
                r['meal_type'] = meal_type
                r['reminder_time'] = reminder_time
                r['notes'] = notes
                r['is_active'] = is_active
                break
        session['guest_meal_reminders'] = reminders_list
        session.modified = True

    flash("Meal reminder updated successfully!", "success")
    return redirect(url_for('reminders'))

@app.route('/delete-reminder/<int:reminder_id>', methods=['POST', 'GET'])
def delete_reminder(reminder_id):
    user_id = session.get('user_id')
    if user_id:
        db.query("DELETE FROM meal_reminders WHERE id = %s AND user_id = %s", (reminder_id, user_id), commit=True)
    else:
        reminders_list = session.get('guest_meal_reminders', [])
        session['guest_meal_reminders'] = [r for r in reminders_list if r.get('id') != reminder_id]
        session.modified = True

    flash("Meal reminder removed.", "info")
    return redirect(url_for('reminders'))

@app.route('/api/reminders', methods=['GET'])
def api_get_reminders():
    user_id = session.get('user_id')
    if user_id:
        raw = db.query(
            "SELECT id, meal_name, meal_type, reminder_time, notes, is_active FROM meal_reminders WHERE user_id = %s AND is_active = 1 ORDER BY reminder_time ASC",
            (user_id,),
            fetchall=True
        ) or []
        items = []
        for r in raw:
            t = str(r['reminder_time'])[:5]
            items.append({
                'id': r['id'],
                'meal_name': r['meal_name'],
                'meal_type': r['meal_type'],
                'reminder_time': t,
                'notes': r['notes']
            })
        return jsonify({'success': True, 'reminders': items})
    else:
        items = [r for r in session.get('guest_meal_reminders', []) if r.get('is_active') == 1]
        return jsonify({'success': True, 'reminders': items})

@app.route('/api/reminders/toggle/<int:reminder_id>', methods=['POST'])
def api_toggle_reminder(reminder_id):
    user_id = session.get('user_id')
    new_state = 1
    if user_id:
        curr = db.query("SELECT is_active FROM meal_reminders WHERE id = %s AND user_id = %s", (reminder_id, user_id), fetchone=True)
        if curr:
            new_state = 0 if curr['is_active'] else 1
            db.query("UPDATE meal_reminders SET is_active = %s WHERE id = %s AND user_id = %s", (new_state, reminder_id, user_id), commit=True)
    else:
        reminders_list = session.get('guest_meal_reminders', [])
        for r in reminders_list:
            if r.get('id') == reminder_id:
                r['is_active'] = 0 if r.get('is_active', 1) else 1
                new_state = r['is_active']
                break
        session['guest_meal_reminders'] = reminders_list
        session.modified = True

    return jsonify({'success': True, 'is_active': bool(new_state)})

@app.route('/api/reminders/load-presets', methods=['POST'])
def api_load_presets():
    user_id = session.get('user_id')
    presets = [
        ('Millet Porridge with Groundnuts and a Boiled Egg', 'Breakfast', '08:00', 'Rich in iron, folate and slow-release carbs'),
        ('Ripe Banana, Orange and Pasteurised Milk', 'Morning Snack', '11:00', 'High calcium and protein boost'),
        ('Matooke with Beans, Dodo and Avocado', 'Lunch', '13:00', 'Plant iron paired with healthy fats for DHA absorption'),
        ('Boiled Sweet Potatoes with Groundnuts/Cowpeas & 1 Glass Lemon Water', 'Evening Snack', '17:00', 'High fiber and hydration replenisher'),
        ('Posho with Well-Cooked Fish and Steamed Sukuma Wiki', 'Dinner', '20:00', 'Light, easily digestible to avoid nighttime heartburn')
    ]
    if user_id:
        db.query("DELETE FROM meal_reminders WHERE user_id = %s", (user_id,), commit=True)
        for name, mtype, rtime, notes in presets:
            db.query("""
                INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
                VALUES (%s, %s, %s, %s, %s, 1)
            """, (user_id, name, mtype, rtime, notes), commit=True)
    else:
        guest_list = []
        for idx, (name, mtype, rtime, notes) in enumerate(presets, 1):
            guest_list.append({
                'id': idx,
                'meal_name': name,
                'meal_type': mtype,
                'reminder_time': rtime,
                'notes': notes,
                'is_active': 1
            })
        session['guest_meal_reminders'] = guest_list
        session.modified = True

    flash("Recommended 5-meal pregnancy schedule loaded successfully! 🌟", "success")
    return redirect(url_for('reminders'))

@app.route('/api/reminders/add-from-chat', methods=['POST'])
def api_add_from_chat():
    data = request.get_json() or {}
    meal_name = data.get('meal_name', '').strip()
    meal_type = data.get('meal_type', 'Breakfast').strip()
    reminder_time = data.get('reminder_time', '08:00').strip()
    notes = data.get('notes', '').strip()

    if not meal_name:
        return jsonify({'error': 'Meal name is required'}), 400

    user_id = session.get('user_id')
    if user_id:
        db.query("""
            INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
            VALUES (%s, %s, %s, %s, %s, 1)
        """, (user_id, meal_name, meal_type, reminder_time, notes), commit=True)
    else:
        reminders_list = session.get('guest_meal_reminders', [])
        new_id = max([r.get('id', 0) for r in reminders_list] or [0]) + 1
        reminders_list.append({
            'id': new_id,
            'meal_name': meal_name,
            'meal_type': meal_type,
            'reminder_time': reminder_time,
            'notes': notes,
            'is_active': 1
        })
        session['guest_meal_reminders'] = reminders_list
        session.modified = True

    return jsonify({'success': True, 'message': f"'{meal_name}' scheduled in your Meal Reminders!"})

if __name__ == '__main__':
    # Initialize app
    print("[MamaFollow] Starting Pregnancy Care and Monitoring Portal on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
