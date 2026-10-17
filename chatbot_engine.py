# chatbot_engine.py
import os
import re
from datetime import datetime
from pregnancy_data import WEEKS_DATA, NUTRITION_GUIDE, EXERCISE_GUIDE, HEALTH_TIPS, EMERGENCY_DATA

SYSTEM_PROMPT = """You are MamaFollow AI, a friendly, caring, empathetic, and professional pregnancy educational assistant.
Your purpose is to provide general educational information and supportive guidance for expectant mothers.

STRICT SAFETY AND MEDICAL GUIDELINES:
1. GENERAL EDUCATIONAL INFORMATION ONLY: Always provide clear, evidence-based educational support.
2. NO MEDICAL DIAGNOSIS: Never diagnose medical conditions, diseases, or obstetric complications.
3. NO PRESCRIPTIONS OR DOSAGE CHANGES: Never prescribe medications or advise changing prescribed pharmaceutical dosages.
4. DO NOT REPLACE HEALTHCARE PROVIDERS: Consistently emphasize that you cannot replace a licensed obstetrician, gynecologist, or midwife.
5. URGENT EMERGENCY SYMPTOMS: If the user mentions red-flag symptoms (heavy vaginal bleeding, sudden severe swelling of face/hands, severe pounding headache with vision changes, sharp constant abdominal pain, leaking amniotic fluid, or significantly decreased fetal movement in the 3rd trimester), immediately advise them in a calm, clear manner to contact emergency medical services (912/112) or go to their nearest maternity hospital emergency room.
6. NO GUARANTEES: Never make absolute medical guarantees regarding the health of the mother or baby.
7. TONE: Warm, encouraging, simple, supportive, and professional. Use maternal emojis (🌸, 👶, 💧, 🥑, ✨) appropriately.
"""

class PregnancyKnowledgeEngine:
    @staticmethod
    def detect_emergency(text):
        text_lower = text.lower()
        emergency_triggers = [
            r'heavy (vaginal )?bleeding', r'bleeding heavily', r'soaking a pad',
            r'severe (abdominal|stomach|pelvic) pain', r'unbearable pain',
            r'fluid (leaking|gushing|broke)', r'water broke.*(green|brown)',
            r'no (baby )?(kicks|movement)', r'decreased (baby )?(movement|kicks)', r'baby not moving',
            r'severe headache.*vision', r'blurred vision.*headache', r'seeing spots.*swelling',
            r'sudden (facial |hand )?swelling', r'face swollen suddenly',
            r'high fever.*chills', r'fever (over|above) 101'
        ]
        for pattern in emergency_triggers:
            if re.search(pattern, text_lower):
                return True
        return False

    @staticmethod
    def get_expert_response(user_msg):
        text = user_msg.lower().strip()
        
        # 1. Emergency Red-Flag Triage
        if PregnancyKnowledgeEngine.detect_emergency(text):
            return {
                'reply': "🚨 **Important Safety Notice**: The symptoms you described may require prompt clinical evaluation.\n\n"
                         "If you are experiencing **heavy bleeding, severe abdominal pain, sudden severe swelling, vision disturbances, fluid leaking, or a noticeable reduction in baby movements**, please do not wait.\n\n"
                         "👉 **Immediate Next Steps**:\n"
                         "1. Contact your OB-GYN, midwife, or labor & delivery triage unit immediately.\n"
                         "2. If severe or unremitting, call emergency services (**912 in the Uganda**) or head to the nearest hospital emergency room.\n\n"
                         "*MamaFollow is an educational tool and cannot replace emergency medical care.*",
                'emergency': True,
                'links': [{'title': 'Emergency Red Flags Guide', 'url': '/emergency'}]
            }

        # 2. Medication / Prescription Guardrail
        if any(w in text for w in ['prescribe', 'which antibiotic', 'take ibuprofen', 'take aspirin', 'change my medicine', 'dosage of']):
            return {
                'reply': "💊 **Medication Safety Guidance**:\n\n"
                         "As MamaFollow AI, I cannot prescribe medications or advise changes to your pharmaceutical treatment.\n\n"
                         "- **Prenatal Vitamins & Minerals**: Standard prenatal multivitamins with 400-600 mcg Folic Acid, 27 mg Iron, and Calcium are generally recommended.\n"
                         "- **Over-the-Counter Drugs**: Always consult your obstetrician or pharmacist before taking medications (e.g., NSAIDs like Ibuprofen are generally avoided in pregnancy).\n\n"
                         "Please consult your healthcare provider for any medication decisions.",
                'emergency': False,
                'links': [{'title': 'Medicine Reminders', 'url': '/medicines'}]
            }

        # 3. Week Number Detection (e.g., "week 20", "week 12", "how big is week 24")
        week_match = re.search(r'week\s*(\d{1,2})', text)
        if week_match:
            wnum = int(week_match.group(1))
            if 1 <= wnum <= 40:
                wdata = WEEKS_DATA.get(wnum)
                if wdata:
                    return {
                        'reply': f"🌸 **Week {wnum} Fetal Development & Maternal Overview**:\n\n"
                                 f"- **Baby Size Analogy**: Size of a **{wdata['fruit']}** {wdata['emoji']}\n"
                                 f"- **Estimated Dimensions**: Length ~{wdata['length_cm']} cm • Weight ~{wdata['weight_g']} g\n"
                                 f"- **Fetal Milestones**: {wdata['milestones'][0]}\n"
                                 f"- **Maternal Body**: {wdata['mother_changes'][0]}\n"
                                 f"- **Helpful Tip**: {wdata['tips'][0]}\n\n"
                                 f"Would you like to explore more details for Week {wnum}?",
                        'emergency': False,
                        'links': [{'title': f'Explore Week {wnum} Tracker', 'url': f'/tracker?week={wnum}'}]
                    }

        # 4. Trimester Inquiries
        if 'trimester 1' in text or 'first trimester' in text or '1st trimester' in text:
            return {
                'reply': "🌱 **First Trimester (Weeks 1 to 12)**:\n\n"
                         "- **Major Milestones**: Fertilization, neural tube closure, baby's heart begins beating at week 5, and all vital organ structures form by week 12.\n"
                         "- **Common Symptoms**: Morning sickness, tender breasts, fatigue, and frequent urination.\n"
                         "- **Key Focus**: Take daily Folic Acid (400-600 mcg), stay hydrated, eat small frequent meals, and schedule your initial prenatal dating scan.",
                'emergency': False,
                'links': [{'title': 'Trimester 1 Nutrition', 'url': '/nutrition?trimester=1'}, {'title': 'Due Date Calculator', 'url': '/calculator'}]
            }
        if 'trimester 2' in text or 'second trimester' in text or '2nd trimester' in text:
            return {
                'reply': "✨ **Second Trimester (Weeks 13 to 27) – The 'Golden Trimester'**:\n\n"
                         "- **Major Milestones**: Baby begins hearing sounds, facial features define, fingerprints form, and mothers feel 'quickening' (first kicks around weeks 16-20).\n"
                         "- **Mother Changes**: Energy surge, appetite improves, baby bump emerges. Round ligament twinges are common.\n"
                         "- **Key Checks**: 20-week detailed Anatomy Ultrasound scan and gestational diabetes glucose screening (weeks 24-28).",
                'emergency': False,
                'links': [{'title': 'Trimester 2 Nutrition', 'url': '/nutrition?trimester=2'}, {'title': 'Prenatal Exercises', 'url': '/exercise?trimester=2'}]
            }
        if 'trimester 3' in text or 'third trimester' in text or '3rd trimester' in text:
            return {
                'reply': "👶 **Third Trimester (Weeks 28 to 40+) – The Final Stretch**:\n\n"
                         "- **Major Milestones**: Rapid fetal weight gain, lung surfactant production, eyes opening, and baby turning head-down into vertex position.\n"
                         "- **Mother Changes**: Braxton Hicks practice contractions, frequent urination, backaches, and pelvic heaviness.\n"
                         "- **Key Checklist**: Daily kick count tracking (10 kicks in 2 hours), Group B Strep screening (weeks 35-37), and packing your hospital bag!",
                'emergency': False,
                'links': [{'title': 'Trimester 3 Workouts', 'url': '/exercise?trimester=3'}, {'title': 'Hospital Bag Checklist', 'url': '/emergency'}]
            }

        # 5. Nutrition & Foods to Avoid
        if any(w in text for w in ['nutrition', 'diet', 'what to eat', 'food to avoid', 'safe food', 'folic acid', 'calcium', 'iron', 'coffee', 'caffeine', 'fish']):
            return {
                'reply': "🥗 **Pregnancy Nutrition & Food Safety Essentials**:\n\n"
                         "- **Essential Nutrients**: Folic acid (dark leafy greens), Iron (lentils, spinach, lean meats), Calcium (milk, yogurt), and Omega-3 DHA (salmon, walnuts).\n"
                         "- **Foods Strictly to Avoid**:\n"
                         "  ❌ High-mercury fish (shark, swordfish, king mackerel)\n"
                         "  ❌ Raw/undercooked meats, sushi, and runny eggs (Salmonella/Toxoplasmosis)\n"
                         "  ❌ Unpasteurized milk, juices, and soft cheeses like Brie/Feta (Listeria)\n"
                         "  ❌ Limit caffeine to under 200 mg/day (~1 cup coffee)\n"
                         "  ❌ Zero alcohol.",
                'emergency': False,
                'links': [{'title': 'Full Nutrition Guide', 'url': '/nutrition'}]
            }

        # 6. Safe Exercise & Kegel
        if any(w in text for w in ['exercise', 'workout', 'walking', 'yoga', 'gym', 'kegel', 'pelvic floor', 'squat']):
            return {
                'reply': "🧘‍♀️ **Safe Prenatal Exercise & Pelvic Floor Guidance**:\n\n"
                         "- **Safe Workouts**: Brisk walking, prenatal yoga, swimming, and stationary cycling (20-30 minutes, 4-5 days/week).\n"
                         "- **Kegel / Pelvic Floor Training**: Squeeze and lift your pelvic muscles for 5 seconds, then fully relax for 5 seconds. Repeat 10 times, 3 times daily to strengthen bladder control and assist labor.\n"
                         "- **What to Avoid**: Contact sports, hot yoga, and lying flat on your back after week 16.\n"
                         "- **Stop Immediately If**: You feel dizzy, short of breath, experience vaginal bleeding, or painful contractions.",
                'emergency': False,
                'links': [{'title': 'Interactive Kegel Trainer', 'url': '/exercise'}]
            }

        # 7. Hydration & Water
        if any(w in text for w in ['water', 'hydration', 'drink water', 'how much water', 'dehydration']):
            return {
                'reply': "💧 **Hydration Guidelines for Expectant Mothers**:\n\n"
                         "- **Recommended Target**: Aim for **8 to 10 glasses (2.0 to 2.5 Liters)** of filtered water daily.\n"
                         "- **Why It Matters**: Water maintains healthy amniotic fluid levels, prevents constipation, reduces urinary tract infection risks, and minimizes fatigue.\n"
                         "- **Tip**: Keep a refillable water bottle handy and use our interactive Daily Water Tracker!",
                'emergency': False,
                'links': [{'title': 'Daily Water Tracker', 'url': '/nutrition'}]
            }

        # 8. Morning Sickness & Nausea
        if any(w in text for w in ['morning sickness', 'nausea', 'vomit', 'throwing up', 'nauseous']):
            return {
                'reply': "🍋 **Soothing Morning Sickness & Nausea**:\n\n"
                         "- Keep plain crackers or dry toast near your bedside and eat a small bite before getting up.\n"
                         "- Eat small, frequent snacks every 1.5 to 2 hours instead of large heavy meals.\n"
                         "- Sip cold lemon water, ginger tea, or tender coconut water.\n"
                         "- Ask your doctor if Vitamin B6 supplements (pyridoxine) are appropriate for you.\n"
                         "- *Contact your doctor if you cannot keep any fluids down for over 24 hours (Hyperemesis Gravidarum).*",
                'emergency': False,
                'links': [{'title': 'Health & Symptom Tips', 'url': '/health-tips'}]
            }

        # 9. Sleep & Rest Positions
        if any(w in text for w in ['sleep', 'sleeping position', 'back sleeping', 'pillow', 'insomnia', 'tired', 'fatigue']):
            return {
                'reply': "🌙 **Sleep Positions & Rest Optimization**:\n\n"
                         "- **The Gold Standard (SOS - Sleep On Side)**: Sleeping on your **left side** is recommended because it avoids pressure on the Inferior Vena Cava and maximizes blood/oxygen flow to your baby and kidneys.\n"
                         "- **Pillow Strategy**: Place one pillow between your bent knees, a wedge pillow under your belly, and a support pillow behind your back.\n"
                         "- **Wind-Down**: Avoid screens 1 hour before bedtime and taper fluid intake 2 hours before sleep to reduce midnight bathroom visits.",
                'emergency': False,
                'links': [{'title': 'Sleep Guidance Guide', 'url': '/health-tips'}]
            }

        # 10. Due Date Calculation & Naegele's Rule
        if any(w in text for w in ['due date', 'calculate', 'edd', 'naegele', 'how many weeks', 'lmp']):
            return {
                'reply': "📅 **How Pregnancy Due Dates Are Calculated (Naegele's Rule)**:\n\n"
                         "Estimated Due Date (EDD) = First day of your Last Menstrual Period (LMP) + 280 days (40 weeks).\n\n"
                         "You can enter your exact LMP and menstrual cycle length into our Due Date Calculator to see your estimated delivery date, current gestational age, and countdown!",
                'emergency': False,
                'links': [{'title': 'Use Due Date Calculator', 'url': '/calculator'}]
            }

        # 11. General Greetings & Help
        if any(w in text for w in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'who are you', 'help']):
            return {
                'reply': "Hello! 👋 I'm MamaFollow AI, your pregnancy wellness assistant.\n\n"
                         "I can share evidence-based educational insights on:\n"
                         "- 🤰 Week-by-week baby growth (Weeks 1 to 40)\n"
                         "- 🥗 Trimester nutrition & food safety\n"
                         "- 🧘‍♀️ Safe workouts & Kegel pelvic exercises\n"
                         "- 🌙 Sleep positions & symptom relief\n"
                         "- 📅 Due date calculations & prenatal schedules\n\n"
                         "How can I support your pregnancy journey today?",
                'emergency': False,
                'links': []
            }

        # 12. Default Helpful Educational Guidance
        return {
            'reply': "Thank you for asking! 🌸\n\n"
                     "MamaFollow is here to provide general educational information about pregnancy stages, trimester nutrition, safe physical wellness, and symptom management.\n\n"
                     "Could you please clarify if you'd like information about a specific pregnancy week (1-40), nutrition guidelines, safe exercise, or symptom relief? Always feel free to consult your OB-GYN for personalized medical advice.",
            'emergency': False,
            'links': [{'title': 'Explore 40-Week Tracker', 'url': '/tracker'}, {'title': 'Care Guides', 'url': '/health-tips'}]
        }

class ChatbotService:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', '').strip()
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("[MamaFollow Chatbot] Google GenAI client initialized with API key.")
            except Exception as e:
                print(f"[MamaFollow Chatbot] Notice: Google GenAI initialization failed ({e}). Using expert knowledge engine fallback.")
                self.client = None
        else:
            print("[MamaFollow Chatbot] GEMINI_API_KEY not provided. Operating seamlessly in Expert Knowledge Engine mode.")

    def generate_chat_response(self, user_message, conversation_history=None):
        if not user_message or not user_message.strip():
            return {
                'reply': "Please type a question about your pregnancy or maternal wellness, and I'll be happy to help! 🌸",
                'emergency': False,
                'links': []
            }

        # First evaluate for critical red-flag emergency triggers
        if PregnancyKnowledgeEngine.detect_emergency(user_message):
            return PregnancyKnowledgeEngine.get_expert_response(user_message)

        # If Gemini API client is available and online, use Gemini 2.5 Flash
        if self.client:
            try:
                formatted_prompt = f"{SYSTEM_PROMPT}\n\n"
                if conversation_history:
                    formatted_prompt += "PREVIOUS CONVERSATION CONTEXT:\n"
                    for msg in conversation_history[-6:]:
                        role = "User" if msg.get('role') == 'user' else "Assistant"
                        formatted_prompt += f"{role}: {msg.get('content', '')}\n"
                    formatted_prompt += "\n"
                
                formatted_prompt += f"User's New Question: {user_message}\nAssistant Response:"

                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=formatted_prompt
                )
                if response and response.text:
                    return {
                        'reply': response.text.strip(),
                        'emergency': False,
                        'links': []
                    }
            except Exception as e:
                print(f"[MamaFollow Chatbot] Gemini API call exception ({e}), falling back to Expert Knowledge Engine.")

        # Fallback to rich rule-based clinical knowledge engine
        return PregnancyKnowledgeEngine.get_expert_response(user_message)

chatbot_service = ChatbotService()