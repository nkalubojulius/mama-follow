# meal_chat_engine.py
import os
import re
from datetime import datetime
from pregnancy_data import NUTRITION_GUIDE, WEEKS_DATA

MEAL_SYSTEM_PROMPT = """You are MamaCare Smart Nutrition AI, a friendly, encouraging, and clinically informed pregnancy meal planning assistant.
Your goal is to provide expectant mothers with wholesome, balanced, trimester-appropriate meal ideas and general educational nutrition support.

CRITICAL SAFETY & MEDICAL RULES:
1. GENERAL EDUCATIONAL INFORMATION ONLY: Frame all suggestions as general educational nutrition ideas.
2. NO MEDICAL DIAGNOSIS OR PRESCRIPTIONS: Never diagnose medical conditions, prescribe clinical diets, or advise altering medications.
3. NO CLAIMS THAT FOOD CURES DISEASE: Never claim that specific foods or nutrients can cure, treat, or reverse any medical illness.
4. CLINICAL REFERRAL: If the user mentions medical conditions (e.g. Gestational Diabetes, Preeclampsia, severe nausea/Hyperemesis, Hypertension, Anemia, severe food allergies), gently emphasize that they should consult their obstetrician or a Registered Dietitian (RD) for customized medical nutrition therapy.
5. PREGNANCY FOOD SAFETY RULES:
   - NO raw/undercooked meats, sushi, or runny eggs (Salmonella & Toxoplasmosis risks).
   - NO unpasteurized milk, soft cheeses (Brie, Feta, Camembert - Listeria risk).
   - NO high-mercury fish (Shark, Swordfish, King Mackerel).
   - Keep caffeine under 200 mg/day (~1 cup coffee).
   - ZERO alcohol.
6. STRUCTURED OUTPUT FORMAT: When suggesting a full meal plan, organize recommendations clearly into:
   - 🌅 Breakfast
   - 🍎 Mid-Morning Snack
   - 🥗 Lunch
   - 🥑 Evening Snack
   - 🍲 Dinner
   - 💧 Hydration & Key Nutrient Highlights
7. TONE: Warm, caring, practical, easy-to-cook, and encouraging.
"""

class MealKnowledgeEngine:
    @staticmethod
    def detect_medical_conditions(text, profile_conditions=""):
        combined = f"{text} {profile_conditions}".lower()
        conditions = []
        if re.search(r'gestational diabetes|diabetes|high blood sugar|glucose', combined):
            conditions.append("Gestational Diabetes / Blood Sugar Management")
        if re.search(r'hypertension|high blood pressure|preeclampsia', combined):
            conditions.append("Hypertension / Blood Pressure Management")
        if re.search(r'anemia|low iron|low hemoglobin|fatigue', combined):
            conditions.append("Iron-Deficiency Anemia Support")
        if re.search(r'morning sickness|nausea|vomiting|hyperemesis', combined):
            conditions.append("Morning Sickness / Nausea Soothing")
        if re.search(r'heartburn|acid reflux|gerd|indigestion', combined):
            conditions.append("Heartburn & Acid Reflux Relief")
        if re.search(r'constipation|bloating', combined):
            conditions.append("High Fiber / Constipation Relief")
        return conditions

    @staticmethod
    def generate_expert_meal_plan(user_msg, preferences=None):
        prefs = preferences or {}
        trimester = int(prefs.get('trimester', 2))
        week = int(prefs.get('pregnancy_week', 20))
        diet_type = (prefs.get('dietary_preference') or 'Vegetarian').strip()
        allergies = (prefs.get('allergies') or 'None').strip()
        restrictions = (prefs.get('dietary_restrictions') or 'None').strip()
        usual_foods = (prefs.get('foods_usually_eaten') or '').strip()
        med_conditions = (prefs.get('medical_conditions') or 'None').strip()
        
        detected_conditions = MealKnowledgeEngine.detect_medical_conditions(user_msg, med_conditions)
        is_veg = 'veg' in diet_type.lower() and 'non' not in diet_type.lower()
        is_vegan = 'vegan' in diet_type.lower()
        is_nonveg = 'non' in diet_type.lower() or 'meat' in diet_type.lower() or 'chicken' in user_msg.lower() or 'fish' in user_msg.lower()

        # Build Trimester Nutrient Blueprint
        if trimester == 1:
            tri_title = "Trimester 1 (Weeks 1-12) Focus: Folic Acid, Vitamin B6, Gentle Digestibility"
            tri_nutrients = "Folate 600mcg, Vitamin B6 for nausea, Iron 27mg, Hydration 2.5L"
        elif trimester == 3:
            tri_title = "Trimester 3 (Weeks 28-40+) Focus: High Fiber, Iron Stores, Calcium & Light Dinners"
            tri_nutrients = "Iron + Vit C pairing, Fiber 30g+, Calcium 1200mg, Electrolytes for leg cramps"
        else:
            tri_title = "Trimester 2 (Weeks 13-27) Focus: Calcium, Protein, Vitamin D & Omega-3 DHA"
            tri_nutrients = "Calcium 1000-1200mg, Protein 75-100g, Omega-3 DHA 300mg, Vit D 800IU"

        # Meal Components tailored by dietary preference
        if is_vegan:
            breakfast = "Warm Steel-Cut Oats cooked in Fortified Soy Milk, topped with Chia Seeds, Crushed Walnuts, and Blueberries."
            b_notes = "Rich in plant-based Omega-3 ALA, Folate, and slow-release complex carbs."
            m_snack = "Sliced Apple or Pear with 2 tablespoons of Creamy Almond Butter and Pumpkin Seeds."
            m_notes = "Healthy fats, Zinc, and steady energy."
            lunch = "Warm Quinoa & Spinach Bowl with Chickpeas, Diced Avocados, Cherry Tomatoes, and a Lemon-Tahini Dressing."
            l_notes = "Complete plant protein, non-heme Iron paired with Vitamin C for optimal absorption."
            e_snack = "Roasted Edamame / Spiced Roasted Makhana with a cup of Iced Mint Water."
            e_notes = "High plant protein and mineral replenishment."
            dinner = "Red Lentil Dahl with Steamed Broccoli, Carrots, and Brown Rice."
            d_notes = "Gentle on the digestive system; high dietary fiber."
        elif is_nonveg:
            breakfast = "2 Fully Cooked Hard-Boiled or Scrambled Eggs with Sautéed Spinach, Avocado slices, and 100% Whole Grain Toast."
            b_notes = "High Choline for baby brain development, high protein, and dietary folate."
            m_snack = "Pasteurized Greek Yogurt with Chia Seeds, Sliced Strawberries, and a drizzle of Pure Honey."
            m_notes = "High Calcium (300mg) and Probiotics for gut flora."
            lunch = "Grilled Lemon-Herb Salmon (low mercury) or Chicken Breast with Sweet Potato Mash and Steamed Asparagus."
            l_notes = "High Omega-3 DHA, Heme Iron, Vitamin A, and Lean Muscle Protein."
            e_snack = "Handful of Raw Walnuts & Dried Apricots with a cup of tender Coconut Water."
            e_notes = "Potassium, Magnesium, and plant Iron boost."
            dinner = "Tender Turkey or Chicken Stir-Fry with Bell Peppers, Snap Peas, and Quinoa or Brown Rice."
            d_notes = "Easily digestible, preventing evening acid reflux while fueling overnight fetal growth."
        else:
            # Vegetarian (Default)
            breakfast = "Warm Oatmeal Bowl made with Pasteurized Milk, topped with Sliced Bananas, Chia Seeds, and Crushed Walnuts (or Paneer Paratha with mint yogurt)."
            b_notes = "High Calcium, Vitamin B6, and Folate for steady morning energy."
            m_snack = "Plain Greek Yogurt or Fruit Chaat with Roasted Pumpkin & Sunflower Seeds."
            m_notes = "Probiotics, Protein, and bone-building Calcium."
            lunch = "Lentil / Moong Dal Soup with Steamed Spinach (Palak), Warm Brown Rice or Whole Wheat Roti, and a side of Cucumber Salad with Lemon."
            l_notes = "High Iron, Protein, and Vitamin C pairing for iron bioavailability."
            e_snack = "Handful of Roasted Spiced Chickpeas (Chana) with 1 glass of Fresh Tender Coconut Water."
            e_notes = "Electrolytes to prevent evening leg cramps and high dietary fiber."
            dinner = "Grilled Paneer or Tofu Cubes with Steamed Mixed Vegetables (Zucchini, Carrots, Green Beans) and Quinoa or Soft Roti."
            d_notes = "Lean protein, light on the stomach to prevent nighttime heartburn."

        # Medical Condition Notice (if applicable)
        condition_alert = ""
        if detected_conditions:
            cond_list = ", ".join(detected_conditions)
            condition_alert = (
                f"\n\n> ⚠️ **Clinical Nutrition Note ({cond_list})**:\n"
                f"> Because your profile mentions **{cond_list}**, please work closely with your OB-GYN or a Registered Dietitian. "
                f"They will provide personalized carbohydrate distribution, glycemic targets, or sodium parameters tailored to your lab results."
            )

        reply = (
            f"🥗 **Personalized MamaCare Daily Meal Plan**\n\n"
            f"**Diet Profile**: {diet_type} • **Stage**: {tri_title}\n"
            f"**Daily Nutrient Priority**: {tri_nutrients}\n\n"
            f"---\n\n"
            f"### 🌅 1. Breakfast (Approx. 8:00 AM)\n"
            f"**Menu**: {breakfast}\n"
            f"💡 *Nutrition Focus*: {b_notes}\n\n"
            f"### 🍎 2. Mid-Morning Snack (Approx. 11:00 AM)\n"
            f"**Menu**: {m_snack}\n"
            f"💡 *Nutrition Focus*: {m_notes}\n\n"
            f"### 🥗 3. Lunch (Approx. 1:00 PM)\n"
            f"**Menu**: {lunch}\n"
            f"💡 *Nutrition Focus*: {l_notes}\n\n"
            f"### 🥑 4. Evening Snack (Approx. 5:00 PM)\n"
            f"**Menu**: {e_snack}\n"
            f"💡 *Nutrition Focus*: {e_notes}\n\n"
            f"### 🍲 5. Dinner (Approx. 8:00 PM)\n"
            f"**Menu**: {dinner}\n"
            f"💡 *Nutrition Focus*: {d_notes}\n\n"
            f"---\n\n"
            f"### 💧 Hydration & Lifestyle Routine\n"
            f"- **Hydration Target**: 8 to 10 glasses (2.0 to 2.5 Liters) of filtered water throughout the day.\n"
            f"- **Digestion Tip**: Sit upright for at least 60-90 minutes after dinner before lying down to prevent acid reflux.{condition_alert}\n\n"
            f"*(You can add these scheduled meals directly to your **Meal Reminders** page with one click below!)*"
        )

        meal_items = [
            {'meal_name': breakfast.split(' topped with')[0].split(',')[0], 'meal_type': 'Breakfast', 'time': '08:00', 'notes': b_notes},
            {'meal_name': m_snack.split(' with')[0], 'meal_type': 'Morning Snack', 'time': '11:00', 'notes': m_notes},
            {'meal_name': lunch.split(' with')[0], 'meal_type': 'Lunch', 'time': '13:00', 'notes': l_notes},
            {'meal_name': e_snack.split(' with')[0], 'meal_type': 'Evening Snack', 'time': '17:00', 'notes': e_notes},
            {'meal_name': dinner.split(' with')[0], 'meal_type': 'Dinner', 'time': '20:00', 'notes': d_notes}
        ]

        return {
            'reply': reply,
            'meal_items': meal_items,
            'has_condition_alert': len(detected_conditions) > 0,
            'links': [
                {'title': 'Schedule in Meal Reminders', 'url': '/reminders'},
                {'title': 'View Trimester Nutrition Guide', 'url': f'/nutrition?trimester={trimester}'}
            ]
        }

class MealChatService:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', '').strip()
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("[MamaCare Meal AI] Google GenAI client initialized for Smart Meal Chat.")
            except Exception as e:
                print(f"[MamaCare Meal AI] Notice: Google GenAI initialization failed ({e}). Operating in Expert Knowledge Engine mode.")
                self.client = None
        else:
            print("[MamaCare Meal AI] GEMINI_API_KEY not provided. Operating seamlessly in Expert Knowledge Engine mode.")

    def generate_meal_response(self, user_message, user_preferences=None, chat_history=None):
        user_msg = (user_message or '').strip()
        prefs = user_preferences or {}
        
        # Check for medical conditions or severe symptoms in message
        detected_conditions = MealKnowledgeEngine.detect_medical_conditions(user_msg, prefs.get('medical_conditions', ''))
        
        if not user_msg:
            user_msg = "Please suggest a healthy pregnancy meal plan tailored to my profile."

        # If Gemini API client is available and online, use Gemini 2.5 Flash
        if self.client:
            try:
                pref_context = (
                    f"USER PREGNANCY & NUTRITION PROFILE:\n"
                    f"- Gestational Stage: Trimester {prefs.get('trimester', 2)}, Week {prefs.get('pregnancy_week', 20)}\n"
                    f"- Diet Preference: {prefs.get('dietary_preference', 'Vegetarian')}\n"
                    f"- Food Allergies: {prefs.get('allergies', 'None')}\n"
                    f"- Dietary Restrictions: {prefs.get('dietary_restrictions', 'None')}\n"
                    f"- Staple / Usual Foods: {prefs.get('foods_usually_eaten', 'Not specified')}\n"
                    f"- Relevant Medical Conditions: {prefs.get('medical_conditions', 'None')}\n\n"
                )

                formatted_prompt = f"{MEAL_SYSTEM_PROMPT}\n\n{pref_context}"
                if chat_history:
                    formatted_prompt += "RECENT CHAT HISTORY:\n"
                    for msg in chat_history[-4:]:
                        role = "User" if msg.get('role') == 'user' else "Assistant"
                        formatted_prompt += f"{role}: {msg.get('content', '')}\n"
                    formatted_prompt += "\n"

                formatted_prompt += f"User's Question: {user_msg}\nAssistant Response:"

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=formatted_prompt
                )
                if response and response.text:
                    expert_data = MealKnowledgeEngine.generate_expert_meal_plan(user_msg, prefs)
                    return {
                        'reply': response.text.strip(),
                        'meal_items': expert_data.get('meal_items', []),
                        'has_condition_alert': len(detected_conditions) > 0,
                        'links': expert_data.get('links', [])
                    }
            except Exception as e:
                print(f"[MamaCare Meal AI] Gemini call exception ({e}), falling back to Expert Knowledge Engine.")

        # Fallback to Expert Clinical Nutrition Engine
        return MealKnowledgeEngine.generate_expert_meal_plan(user_msg, prefs)

meal_chat_service = MealChatService()