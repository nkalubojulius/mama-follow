# pregnancy_data.py
# Comprehensive clinical and educational pregnancy data for MamaCare

_RAW_WEEKS_DATA = {
    "1": {
        "week": 1,
        "trimester": 1,
        "fruit": "Microscopic Ovum",
        "emoji": "\u2728",
        "length_cm": 0.1,
        "weight_g": 0.01,
        "milestones": [
            "Ovulation and fertilization take place in the fallopian tube.",
            "Zygote begins rapid cellular division.",
            "Genetic code is completely established."
        ],
        "mother_changes": [
            "Menstrual period ending; uterine wall starts rebuilding."
        ],
        "tips": [
            "Take daily 400mcg Folic Acid prenatal vitamin; avoid alcohol and smoking."
        ]
    },
    "2": {
        "week": 2,
        "trimester": 1,
        "fruit": "Blastocyst",
        "emoji": "🔬",
        "length_cm": 0.2,
        "weight_g": 0.02,
        "milestones": [
            "Blastocyst travels down toward the uterine lining.",
            "Inner cells form embryo; outer cells prepare placenta.",
            "Amniotic cavity begins formation."
        ],
        "mother_changes": [
            "Possible mild ovulation or implantation spotting."
        ],
        "tips": [
            "Track exact LMP date; eat dark leafy greens and legumes."
        ]
    },
    "3": {
        "week": 3,
        "trimester": 1,
        "fruit": "Poppy Seed",
        "emoji": "🌱",
        "length_cm": 0.3,
        "weight_g": 0.04,
        "milestones": [
            "Implantation occurs in uterine endometrium.",
            "Placenta starts producing hCG pregnancy hormone.",
            "Primitive neural tube begins forming."
        ],
        "mother_changes": [
            "Positive home pregnancy test; tender swollen breasts."
        ],
        "tips": [
            "Confirm with morning pregnancy test; limit caffeine to <200mg/day."
        ]
    },
    "4": {
        "week": 4,
        "trimester": 1,
        "fruit": "Mustard Seed",
        "emoji": "🌿",
        "length_cm": 0.4,
        "weight_g": 0.1,
        "milestones": [
            "Embryo differentiates into ectoderm, mesoderm, and endoderm layers.",
            "Yolk sac provides essential early nutrients.",
            "Early vascular circulation begins."
        ],
        "mother_changes": [
            "Missed period; fatigue and frequent urination begin."
        ],
        "tips": [
            "Book first prenatal appointment with OB-GYN; avoid raw/undercooked meats."
        ]
    },
    "5": {
        "week": 5,
        "trimester": 1,
        "fruit": "Apple Seed",
        "emoji": "🍎",
        "length_cm": 0.5,
        "weight_g": 0.2,
        "milestones": [
            "Primitive heart starts rhythmic contractions (100-110 bpm).",
            "Neural tube closes forming brain and spinal cord.",
            "Limb buds emerge for arms and legs."
        ],
        "mother_changes": [
            "Morning sickness, nausea, food aversions, high fatigue."
        ],
        "tips": [
            "Keep crackers by bedside; eat small frequent meals to ease nausea."
        ]
    },
    "6": {
        "week": 6,
        "trimester": 1,
        "fruit": "Sweet Pea",
        "emoji": "🫛",
        "length_cm": 0.6,
        "weight_g": 0.5,
        "milestones": [
            "Facial features emerge with dark spots for eyes and nostrils.",
            "Blood circulation is fully operational.",
            "Digestive and respiratory systems begin development."
        ],
        "mother_changes": [
            "Frequent bathroom trips; heightened emotional sensitivity."
        ],
        "tips": [
            "Wear a supportive wire-free bra; drink 8-10 glasses of water daily."
        ]
    },
    "7": {
        "week": 7,
        "trimester": 1,
        "fruit": "Blueberry",
        "emoji": "🫐",
        "length_cm": 1.3,
        "weight_g": 1.0,
        "milestones": [
            "Rapid brain growth (~100,000 new neurons per minute).",
            "Paddle-shaped hands and feet develop.",
            "Tooth buds and eye lenses form."
        ],
        "mother_changes": [
            "Nausea peaks; possible heartburn and mild bloating."
        ],
        "tips": [
            "Eat Vitamin B6 foods (bananas, chickpeas); avoid lying flat after meals."
        ]
    },
    "8": {
        "week": 8,
        "trimester": 1,
        "fruit": "Raspberry",
        "emoji": "🍓",
        "length_cm": 1.6,
        "weight_g": 1.5,
        "milestones": [
            "Webbed fingers and toes start separating.",
            "Baby makes involuntary reflex movements.",
            "Ears, nose tip, and upper lip become visible."
        ],
        "mother_changes": [
            "Waistline feels tighter; vivid dreams and restless sleep."
        ],
        "tips": [
            "Write down questions for your doctor; eat calcium-rich yogurt."
        ]
    },
    "9": {
        "week": 9,
        "trimester": 1,
        "fruit": "Green Olive",
        "emoji": "🫒",
        "length_cm": 2.3,
        "weight_g": 2.0,
        "milestones": [
            "Embryonic tail completely disappears; now officially a fetus!",
            "Heart has 4 distinct pumping chambers.",
            "Baby can bend tiny elbows and wrists."
        ],
        "mother_changes": [
            "Morning sickness peak; mild pelvic fullness and lower backache."
        ],
        "tips": [
            "Stay hydrated to prevent dizziness; snack on almonds and walnuts."
        ]
    },
    "10": {
        "week": 10,
        "trimester": 1,
        "fruit": "Prune / Fig",
        "emoji": "🍇",
        "length_cm": 3.1,
        "weight_g": 4.0,
        "milestones": [
            "All vital organs are functioning.",
            "Tiny nails and hair follicles form.",
            "Bones and cartilage actively calcify."
        ],
        "mother_changes": [
            "Visible veins on breasts/belly; round ligament stretching twinges."
        ],
        "tips": [
            "Wear loose cotton clothes; do daily gentle stretching."
        ]
    },
    "11": {
        "week": 11,
        "trimester": 1,
        "fruit": "Lime",
        "emoji": "🍋",
        "length_cm": 4.1,
        "weight_g": 7.0,
        "milestones": [
            "Baby opens and closes hands into tiny fists.",
            "Diaphragm develops and baby practices hiccuping.",
            "Tooth buds harden inside gums."
        ],
        "mother_changes": [
            "Energy slowly returns; hair and nails grow faster."
        ],
        "tips": [
            "Pair iron foods (spinach, beans) with Vitamin C (citrus, peppers)."
        ]
    },
    "12": {
        "week": 12,
        "trimester": 1,
        "fruit": "Plum",
        "emoji": "🍑",
        "length_cm": 5.4,
        "weight_g": 14.0,
        "milestones": [
            "End of 1st Trimester! Major anatomical systems formed.",
            "Baby curls toes and practices thumb sucking.",
            "Kidneys produce amniotic fluid."
        ],
        "mother_changes": [
            "Uterus rises above pelvis; morning sickness begins decreasing."
        ],
        "tips": [
            "Celebrate finishing 1st Trimester! Schedule 2nd trimester routine checks."
        ]
    },
    "13": {
        "week": 13,
        "trimester": 2,
        "fruit": "Lemon",
        "emoji": "🍋",
        "length_cm": 7.4,
        "weight_g": 23.0,
        "milestones": [
            "Start of 2nd Trimester! Unique fingerprints are set.",
            "Vocal cords begin developing.",
            "Baby swallows amniotic fluid."
        ],
        "mother_changes": [
            "Second trimester energy boost; improved appetite."
        ],
        "tips": [
            "Sleep on your left side to maximize placental blood circulation."
        ]
    },
    "14": {
        "week": 14,
        "trimester": 2,
        "fruit": "Nectarine",
        "emoji": "🍑",
        "length_cm": 8.7,
        "weight_g": 43.0,
        "milestones": [
            "Thyroid gland begins producing hormones.",
            "Lanugo (fine protective hair) covers baby body.",
            "Baby makes facial expressions like frowning and smiling."
        ],
        "mother_changes": [
            "Baby bump emerging; mild pregnancy rhinitis (stuffy nose)."
        ],
        "tips": [
            "Use saline spray for nasal congestion; eat nutrient-dense snacks."
        ]
    },
    "15": {
        "week": 15,
        "trimester": 2,
        "fruit": "Apple",
        "emoji": "🍎",
        "length_cm": 10.1,
        "weight_g": 70.0,
        "milestones": [
            "Baby senses light through fused eyelids.",
            "Legs grow longer than arms with flexible joints.",
            "Taste buds are maturing."
        ],
        "mother_changes": [
            "Pregnancy brain / forgetfulness; sensitive gums."
        ],
        "tips": [
            "Use soft toothbrush; practice good sitting posture at work."
        ]
    },
    "16": {
        "week": 16,
        "trimester": 2,
        "fruit": "Avocado",
        "emoji": "🥑",
        "length_cm": 11.6,
        "weight_g": 100.0,
        "milestones": [
            "Baby heart pumps 25 quarts of blood per day.",
            "Ears are fully formed and baby can hear mother heartbeat.",
            "Mother may feel initial fluttering movements (quickening)."
        ],
        "mother_changes": [
            "Quickening (fluttery baby kicks); skin pregnancy glow."
        ],
        "tips": [
            "Talk, sing, and read to baby; eat fiber-rich oats and prunes."
        ]
    },
    "17": {
        "week": 17,
        "trimester": 2,
        "fruit": "Pomegranate",
        "emoji": "🍎",
        "length_cm": 13.0,
        "weight_g": 140.0,
        "milestones": [
            "Fat tissue (adipose) begins accumulating for warmth.",
            "Skeleton transforms from cartilage into strong bone.",
            "Umbilical cord grows stronger and thicker."
        ],
        "mother_changes": [
            "Warm body temperature; mild lower back or sciatic pressure."
        ],
        "tips": [
            "Stretch hamstrings to ease sciatica; wear supportive flat shoes."
        ]
    },
    "18": {
        "week": 18,
        "trimester": 2,
        "fruit": "Bell Pepper",
        "emoji": "🫑",
        "length_cm": 14.2,
        "weight_g": 190.0,
        "milestones": [
            "Myelin sheath insulates nerve pathways.",
            "Baby establishes regular sleep and awake cycles.",
            "Baby yawns, stretches, and sucks on toes."
        ],
        "mother_changes": [
            "Distinct kicks; dizziness if lying flat on back."
        ],
        "tips": [
            "Never sleep flat on your back; prepare for 20-week anatomy scan."
        ]
    },
    "19": {
        "week": 19,
        "trimester": 2,
        "fruit": "Mango",
        "emoji": "🥭",
        "length_cm": 15.3,
        "weight_g": 240.0,
        "milestones": [
            "Vernix caseosa (protective white wax) coats baby skin.",
            "Sensory brain areas for smell, taste, touch, sight are active.",
            "Kidneys produce normal amounts of urine."
        ],
        "mother_changes": [
            "Linea nigra (dark belly line); night leg cramps."
        ],
        "tips": [
            "Eat magnesium foods (bananas, almonds) for leg cramps; moisturize belly."
        ]
    },
    "20": {
        "week": 20,
        "trimester": 2,
        "fruit": "Banana",
        "emoji": "🍌",
        "length_cm": 16.4,
        "weight_g": 300.0,
        "milestones": [
            "Halfway mark! Detailed anatomy ultrasound evaluation.",
            "Baby swallows amniotic fluid practicing digestive system.",
            "Kicks and turns are clearly felt daily."
        ],
        "mother_changes": [
            "Fundus reaches navel level; strong daily movements."
        ],
        "tips": [
            "Attend 20-week anatomy scan; sign up for childbirth classes."
        ]
    },
    "21": {
        "week": 21,
        "trimester": 2,
        "fruit": "Carrot",
        "emoji": "🥕",
        "length_cm": 26.7,
        "weight_g": 360.0,
        "milestones": [
            "Bone marrow takes over red blood cell production.",
            "Baby responds actively to external music and loud voices.",
            "Eyebrows and eyelashes are visible."
        ],
        "mother_changes": [
            "Braxton Hicks practice contractions; swollen feet."
        ],
        "tips": [
            "Wear compression socks if standing; drink water for Braxton Hicks."
        ]
    },
    "22": {
        "week": 22,
        "trimester": 2,
        "fruit": "Papaya",
        "emoji": "🥭",
        "length_cm": 27.8,
        "weight_g": 430.0,
        "milestones": [
            "Baby resembles a miniature newborn.",
            "Grip strength increases; baby grasps umbilical cord.",
            "Inner ear balance system is fully functional."
        ],
        "mother_changes": [
            "Stretch marks may appear; mild shortness of breath."
        ],
        "tips": [
            "Focus on protein-rich meals: eggs, lentils, chicken, tofu."
        ]
    },
    "23": {
        "week": 23,
        "trimester": 2,
        "fruit": "Grapefruit",
        "emoji": "🍊",
        "length_cm": 28.9,
        "weight_g": 500.0,
        "milestones": [
            "Rapid eye movement (REM) sleep occurs (baby is dreaming).",
            "Lungs produce surfactant-producing cells.",
            "Skin pigment begins to form."
        ],
        "mother_changes": [
            "Heat intolerance; ankle swelling at the end of the day."
        ],
        "tips": [
            "Wear non-slip shoes; remove tight rings before finger swelling."
        ]
    },
    "24": {
        "week": 24,
        "trimester": 2,
        "fruit": "Cantaloupe",
        "emoji": "🍈",
        "length_cm": 30.0,
        "weight_g": 600.0,
        "milestones": [
            "Milestone of viability reached with specialized neonatal care.",
            "Auditory pathways fully connected; startle reflex active.",
            "Facial features are fully distinct."
        ],
        "mother_changes": [
            "Glucose screening window; carpal tunnel wrist tingling."
        ],
        "tips": [
            "Complete gestational diabetes glucose test; do prenatal yoga."
        ]
    },
    "25": {
        "week": 25,
        "trimester": 2,
        "fruit": "Cauliflower",
        "emoji": "🥦",
        "length_cm": 34.6,
        "weight_g": 660.0,
        "milestones": [
            "Capillaries fill with blood giving skin a pink glow.",
            "Nostrils open and baby practices breathing motions.",
            "Spinal column structures strengthen."
        ],
        "mother_changes": [
            "Pelvic pressure; restless leg sensation in evenings."
        ],
        "tips": [
            "Increase fiber to prevent constipation; do gentle calf stretches."
        ]
    },
    "26": {
        "week": 26,
        "trimester": 2,
        "fruit": "Lettuce Head",
        "emoji": "🥬",
        "length_cm": 35.6,
        "weight_g": 760.0,
        "milestones": [
            "Baby opens eyelids for the first time!",
            "Brain wave patterns match a full-term newborn.",
            "Responds to light shone on the abdomen."
        ],
        "mother_changes": [
            "Insomnia; rib kicks as baby grows larger."
        ],
        "tips": [
            "Use U-shaped pregnancy body pillow between knees for sleep."
        ]
    },
    "27": {
        "week": 27,
        "trimester": 2,
        "fruit": "Eggplant",
        "emoji": "🍆",
        "length_cm": 36.6,
        "weight_g": 875.0,
        "milestones": [
            "Final week of 2nd Trimester.",
            "Rhythmic chest breathing motions.",
            "Baby hiccups feel like rhythmic tapping on belly."
        ],
        "mother_changes": [
            "Fatigue returns; occasional colostrum breast leakage."
        ],
        "tips": [
            "Schedule RhoGAM shot if Rh-negative; finalize birth preferences."
        ]
    },
    "28": {
        "week": 28,
        "trimester": 3,
        "fruit": "Acorn Squash",
        "emoji": "🎃",
        "length_cm": 37.6,
        "weight_g": 1000.0,
        "milestones": [
            "Welcome to 3rd Trimester! Baby weighs ~1 kg.",
            "Baby can blink, dream, and regulate body temperature.",
            "Brain develops rapid sleep cycles."
        ],
        "mother_changes": [
            "Third trimester begins; shortness of breath and backaches."
        ],
        "tips": [
            "Start daily Kick Counts (10 kicks in 2 hours); use birth ball."
        ]
    },
    "29": {
        "week": 29,
        "trimester": 3,
        "fruit": "Butternut Squash",
        "emoji": "🎃",
        "length_cm": 38.6,
        "weight_g": 1150.0,
        "milestones": [
            "Bones absorb significant calcium daily.",
            "Muscles and lungs continue maturing rapidly.",
            "Strong kicks visibly push against the belly."
        ],
        "mother_changes": [
            "Heartburn and acid reflux; heavy feeling in legs."
        ],
        "tips": [
            "Eat small snacks every 2-3 hours; avoid greasy/spicy dinners."
        ]
    },
    "30": {
        "week": 30,
        "trimester": 3,
        "fruit": "Cabbage",
        "emoji": "🥬",
        "length_cm": 39.9,
        "weight_g": 1300.0,
        "milestones": [
            "Brain surface develops intricate folds and convolutions.",
            "Bone marrow fully manages red blood cells.",
            "Eyes differentiate light from darkness."
        ],
        "mother_changes": [
            "Waddling gait; frequent Braxton Hicks contractions."
        ],
        "tips": [
            "Pack hospital bag checklist items; practice pelvic floor relaxation."
        ]
    },
    "31": {
        "week": 31,
        "trimester": 3,
        "fruit": "Coconut",
        "emoji": "🥥",
        "length_cm": 41.1,
        "weight_g": 1500.0,
        "milestones": [
            "Baby turns head from side to side in response to voices.",
            "Major weight gain spurt commences.",
            "Urinary system is fully operational."
        ],
        "mother_changes": [
            "Frequent urination returns as baby presses bladder; nesting urge."
        ],
        "tips": [
            "Do not overexert while cleaning; install and inspect infant car seat."
        ]
    },
    "32": {
        "week": 32,
        "trimester": 3,
        "fruit": "Pineapple",
        "emoji": "🍍",
        "length_cm": 42.4,
        "weight_g": 1700.0,
        "milestones": [
            "Most babies turn head-down (vertex position).",
            "Fingernails reach the ends of fingertips.",
            "Lanugo hair begins shedding into amniotic fluid."
        ],
        "mother_changes": [
            "Uterus 5 inches above navel; ankle and finger puffiness."
        ],
        "tips": [
            "Learn true labor vs Braxton Hicks signs; rest with feet elevated."
        ]
    },
    "33": {
        "week": 33,
        "trimester": 3,
        "fruit": "Celery Stalk",
        "emoji": "🥬",
        "length_cm": 43.7,
        "weight_g": 1900.0,
        "milestones": [
            "Immune system absorbs maternal antibodies through placenta.",
            "Bones harden, while skull bones remain flexible for birth.",
            "Amniotic fluid volume peaks."
        ],
        "mother_changes": [
            "Difficulty turning in bed; heavy pelvic sensation."
        ],
        "tips": [
            "Practice slow diaphragmatic breathing; prepare postpartum freezer meals."
        ]
    },
    "34": {
        "week": 34,
        "trimester": 3,
        "fruit": "Honeydew Melon",
        "emoji": "🍈",
        "length_cm": 45.0,
        "weight_g": 2150.0,
        "milestones": [
            "Central nervous system and lungs near full maturity.",
            "Fat layers fill out arms and legs.",
            "Baby establishes regular sleep-wake cycles."
        ],
        "mother_changes": [
            "Exhaustion after mild activity; stronger practice contractions."
        ],
        "tips": [
            "Report sudden severe headaches or facial swelling immediately."
        ]
    },
    "35": {
        "week": 35,
        "trimester": 3,
        "fruit": "Pineapple Large",
        "emoji": "🍍",
        "length_cm": 46.2,
        "weight_g": 2400.0,
        "milestones": [
            "Kidneys fully functional; liver processes waste.",
            "Baby movements feel like firm rolls and jabs.",
            "Grip strength is remarkably firm."
        ],
        "mother_changes": [
            "Group B Strep screening; increased downward pelvic pressure."
        ],
        "tips": [
            "Complete Group B Strep swab test; do gentle perineal massage."
        ]
    },
    "36": {
        "week": 36,
        "trimester": 3,
        "fruit": "Romaine Lettuce",
        "emoji": "🥬",
        "length_cm": 47.4,
        "weight_g": 2600.0,
        "milestones": [
            "Late Pre-term milestone; lungs produce ample surfactant.",
            "Baby drops lower into pelvis (lightening).",
            "Breathing becomes easier for mom."
        ],
        "mother_changes": [
            "Lightening (baby drops); easier breathing but frequent urination."
        ],
        "tips": [
            "Confirm birth partner/ride; have hospital pre-registration papers ready."
        ]
    },
    "37": {
        "week": 37,
        "trimester": 3,
        "fruit": "Winter Melon",
        "emoji": "🥬",
        "length_cm": 48.6,
        "weight_g": 2850.0,
        "milestones": [
            "Early Term! Baby is fully formed and ready for birth.",
            "Baby gains ~200g of protective fat per week.",
            "Firm suckling and rooting reflexes ready for nursing."
        ],
        "mother_changes": [
            "Mucus plug discharge; cervix starts effacing and dilating."
        ],
        "tips": [
            "Time contractions with 5-1-1 rule; rest to store labor energy."
        ]
    },
    "38": {
        "week": 38,
        "trimester": 3,
        "fruit": "Winter Squash",
        "emoji": "🎃",
        "length_cm": 49.8,
        "weight_g": 3100.0,
        "milestones": [
            "Full Term! All organ systems operate independently.",
            "Vocal cords strong for first cry.",
            "Eye color usually slate blue or brown at birth."
        ],
        "mother_changes": [
            "Pelvic heaviness; loose stools as body clears for labor."
        ],
        "tips": [
            "Take gentle walks to encourage cervical opening; stay positive."
        ]
    },
    "39": {
        "week": 39,
        "trimester": 3,
        "fruit": "Mini Watermelon",
        "emoji": "🍉",
        "length_cm": 50.7,
        "weight_g": 3300.0,
        "milestones": [
            "Baby continues building fat for thermal control.",
            "Placenta supplies antibodies until birth.",
            "Skull remains pliable with soft fontanelles."
        ],
        "mother_changes": [
            "Cervix softening; possible water breaking."
        ],
        "tips": [
            "Note TACO (Time, Amount, Color, Odor) if water breaks; rest up."
        ]
    },
    "40": {
        "week": 40,
        "trimester": 3,
        "fruit": "Full Watermelon",
        "emoji": "🍉",
        "length_cm": 51.2,
        "weight_g": 3500.0,
        "milestones": [
            "Due date arrived! Baby is ready to meet the world.",
            "Full newborn reflexes present.",
            "Normal delivery window spans 38 to 42 weeks."
        ],
        "mother_changes": [
            "Labor contractions (5-1-1 rule); transition to active labor."
        ],
        "tips": [
            "Trust your body and healthcare team; head to hospital when in active labor."
        ]
    }
}

NUTRITION_GUIDE = {
    'trimesters': {
        1: {
            'title': 'Trimester 1: Foundation & Cellular Growth (Weeks 1 - 12)',
            'focus': 'Folic Acid, Vitamin B6, Iron, Hydration',
            'calories_needed': 'Standard baseline or +100 kcal/day',
            'nutrients': [
                {'name': 'Folic Acid / Folate (600 mcg/day)', 'desc': 'Critical for neural tube development and preventing spina bifida.', 'foods': 'Dark leafy spinach, kale, fortified cereals, lentils, oranges, asparagus.'},
                {'name': 'Vitamin B6 (Pyridoxine)', 'desc': 'Helps soothe morning sickness and supports nervous system synthesis.', 'foods': 'Bananas, whole grains, chickpeas, poultry, baked potatoes.'},
                {'name': 'Iron (27 mg/day)', 'desc': 'Builds hemoglobin for maternal and fetal blood volume expansion.', 'foods': 'Lean meats, beans, pumpkin seeds, dried apricots, spinach with lemon.'},
                {'name': 'Hydration (2.5 - 3.0 Liters/day)', 'desc': 'Replenishes amniotic fluid and prevents urinary tract infections.', 'foods': 'Filtered water, tender coconut water, infused lemon-cucumber water.'}
            ]
        },
        2: {
            'title': 'Trimester 2: Bone & Muscle Development (Weeks 13 - 27)',
            'focus': 'Calcium, Vitamin D, Protein, Omega-3 DHA',
            'calories_needed': '+340 kcal/day (balanced healthy snacks)',
            'nutrients': [
                {'name': 'Calcium (1000 - 1200 mg/day)', 'desc': 'Builds baby bones, teeth, heart rhythm, and preserves maternal bone density.', 'foods': 'Pasteurized milk, plain Greek yogurt, cheddar cheese, fortified plant milks, sesame seeds.'},
                {'name': 'Vitamin D (600 - 800 IU/day)', 'desc': 'Ensures efficient calcium absorption and immune system health.', 'foods': 'Egg yolks, fortified milk, salmon, safe 10-15 min morning sun exposure.'},
                {'name': 'Protein (75 - 100 g/day)', 'desc': 'Fuel for rapid uterine, placental, and fetal muscular growth.', 'foods': 'Eggs, paneer, tofu, lentils, chicken breast, quinoa, walnuts.'},
                {'name': 'Omega-3 Fatty Acids / DHA (300 mg/day)', 'desc': 'Essential for fetal brain and retinal eye development.', 'foods': 'Low-mercury salmon, chia seeds, flaxseeds, walnuts, algae oil.'}
            ]
        },
        3: {
            'title': 'Trimester 3: Rapid Weight Gain & Lung Maturation (Weeks 28 - 40+)',
            'focus': 'Zinc, Vitamin C, Vitamin K, High Fiber, Iron',
            'calories_needed': '+450 kcal/day of nutrient-dense meals',
            'nutrients': [
                {'name': 'Iron & Vitamin C pairing', 'desc': 'Maximizes maternal iron stores to prepare for blood loss during delivery.', 'foods': 'Lentil soup with lemon juice, bell peppers with hummus, lean beef with broccoli.'},
                {'name': 'Zinc (11-15 mg/day)', 'desc': 'Supports rapid DNA synthesis, enzyme function, and immune defense.', 'foods': 'Cashews, pumpkin seeds, oats, chickpeas, lean poultry.'},
                {'name': 'High Dietary Fiber (28-32 g/day)', 'desc': 'Combats 3rd trimester constipation and prevents hemorrhoids.', 'foods': 'Prunes, oats, berries, chia seeds, broccoli, whole wheat.'},
                {'name': 'Electrolytes & Potassium', 'desc': 'Eases leg cramps and regulates blood pressure.', 'foods': 'Bananas, sweet potatoes, coconut water, avocados.'}
            ]
        }
    },
    'foods_to_avoid': [
        {'food': 'High-Mercury Fish (Shark, Swordfish, King Mackerel, Tilefish)', 'risk': 'Mercury is neurotoxic to the developing fetal brain and nervous system.', 'safe_alt': 'Salmon, canned light tuna, shrimp, tilapia (2-3 servings/wk max)'},
        {'food': 'Raw or Undercooked Meat & Poultry (Rare steak, pink chicken)', 'risk': 'Toxoplasmosis and Salmonella bacterial infections.', 'safe_alt': 'All meats cooked to well-done internal temp (165°F / 74°C)'},
        {'food': 'Raw / Runny Eggs & Products with raw egg (Hollandaise, raw batter)', 'risk': 'Severe Salmonella poisoning and dehydration.', 'safe_alt': 'Fully cooked hard-boiled eggs, commercial pasteurized mayonnaise'},
        {'food': 'Unpasteurized Milk, Juices & Soft Cheeses (Brie, Camembert, Feta)', 'risk': 'Listeria monocytogenes bacteria which can cross placenta and cause miscarriage.', 'safe_alt': 'Pasteurized hard cheeses (Cheddar, Mozzarella, Parmesan) or boiled milk'},
        {'food': 'Deli & Processed Cold Meats (Hot dogs, salami, deli ham)', 'risk': 'Listeria contamination on slicing equipment.', 'safe_alt': 'Steaming hot deli meats heated until bubbling hot (165°F)'},
        {'food': 'Raw Sprouts (Alfalfa, clover, radish, mung bean)', 'risk': 'Sprouts need warm moist conditions where Salmonella thrives.', 'safe_alt': 'Thoroughly cooked/stir-fried sprouts'},
        {'food': 'Excessive Caffeine (>200 mg/day, ~1.5 cups brewed coffee)', 'risk': 'Can restrict fetal growth and elevate heart rate.', 'safe_alt': 'Decaf coffee, herbal peppermint/chamomile tea, fruit-infused water'},
        {'food': 'Alcohol & Recreational Substances', 'risk': 'Fetal Alcohol Spectrum Disorder (FASD) with permanent developmental deficits.', 'safe_alt': 'Zero alcohol. Enjoy sparkling apple cider or mocktails!'}
    ]
}

EXERCISE_GUIDE = {
    'trimesters': {
        1: {
            'title': 'Trimester 1: Foundation & Low-Impact Aerobics',
            'guidelines': 'Focus on building consistency, gentle endurance, and core stability while listening to fatigue levels.',
            'exercises': [
                {'name': 'Brisk Walking', 'duration': '20-30 mins, 4-5 days/wk', 'benefits': 'Improves cardiovascular fitness without jarring joints.', 'tips': 'Wear supportive running shoes and carry a water bottle.'},
                {'name': 'Gentle Prenatal Yoga', 'duration': '20-30 mins, 3 days/wk', 'benefits': 'Improves flexibility, relieves lower back tension, promotes calm.', 'tips': 'Avoid hot/Bikram yoga and deep twists.'},
                {'name': 'Swimming & Water Aerobics', 'duration': '30 mins, 2-3 days/wk', 'benefits': 'Zero joint impact; buoyancy relieves fatigue.', 'tips': 'Keep water temperature comfortable (not hot).'}
            ]
        },
        2: {
            'title': 'Trimester 2: Strength, Stability & Pelvic Floor',
            'guidelines': 'Energy is high. Emphasize glute strength, pelvic stability, and avoid lying flat on your back.',
            'exercises': [
                {'name': 'Stationary Cycling', 'duration': '20-30 mins, 3 days/wk', 'benefits': 'Safe cardio with zero fall risk.', 'tips': 'Adjust handlebars high to avoid hunching over belly.'},
                {'name': 'Squats & Wall Sits', 'duration': '3 sets of 10-12 reps', 'benefits': 'Strengthens pelvic floor and thighs for labor.', 'tips': 'Hold a sturdy chair or doorframe for balance.'},
                {'name': 'Pelvic Tilts (Cat-Cow pose)', 'duration': '10-15 repetitions', 'benefits': 'Relieves lower back pressure and sciatica.', 'tips': 'Perform on all fours on a padded yoga mat.'}
            ]
        },
        3: {
            'title': 'Trimester 3: Labor Preparation & Relaxation',
            'guidelines': 'Gentle movements, hip openers, birth ball work, and deep diaphragmatic breathing.',
            'exercises': [
                {'name': 'Birth Ball Bouncing & Hip Circles', 'duration': '15-20 mins daily', 'benefits': 'Encourages optimal fetal positioning and opens pelvic outlet.', 'tips': 'Sit tall on a 65cm anti-burst birthing ball.'},
                {'name': 'Tailor Sitting / Butterfly Stretch', 'duration': '5-10 mins daily', 'benefits': 'Gently stretches inner thighs and groin for birth.', 'tips': 'Sit with soles together, knees relaxed outwards.'},
                {'name': 'Walking with Rest Breaks', 'duration': '15-20 mins daily', 'benefits': 'Helps baby descend into the birth canal.', 'tips': 'Stop if feeling dizzy or experiencing painful contractions.'}
            ]
        }
    },
    'kegel_guide': {
        'title': 'Kegel / Pelvic Floor Muscle Training',
        'importance': 'Strengthens the pubococcygeus (PC) hammock muscles supporting the bladder, uterus, and bowels, reducing urinary incontinence and aiding labor pushing.',
        'steps': [
            'Locate the correct muscles: Imagine trying to stop the flow of urine mid-stream (do not do this while urinating).',
            'Get into a comfortable seated, standing, or side-lying position.',
            'Inhale gently, and as you exhale, contract and lift your pelvic floor muscles upward and inward.',
            'Hold the contraction for 5 seconds without holding your breath or tightening your stomach/buttocks.',
            'Slowly release and fully relax the muscles for 5 seconds.',
            'Repeat 10 repetitions, 3 times daily.'
        ]
    },
    'stop_signals': [
        'Vaginal bleeding or sudden fluid leaking',
        'Dizziness, lightheadedness, or feeling faint',
        'Shortness of breath before starting exertion',
        'Chest pain or rapid irregular heartbeat',
        'Painful regular uterine contractions',
        'Calf pain, redness, or localized swelling (potential DVT warning)'
    ]
}

HEALTH_TIPS = {
    'sleep': {
        'title': 'Optimizing Sleep During Pregnancy',
        'points': [
            {'heading': 'The "SOS" (Sleep On Side) Position', 'detail': 'Sleeping on your left side is the gold standard. It prevents the heavy uterus from compressing the Inferior Vena Cava, ensuring maximum oxygen and nutrient blood flow to your baby and kidneys.'},
            {'heading': 'Pillow Fort Strategy', 'detail': 'Place one firm pillow between your bent knees, a wedge pillow under your growing belly, and a pillow behind your back to prevent rolling flat.'},
            {'heading': 'Evening Wind-Down', 'detail': 'Avoid screen time 1 hour before bed. Sip warm milk with a pinch of turmeric or decaf chamomile tea, and keep the bedroom at 65-68°F (18-20°C).'},
            {'heading': 'Fluid Timing', 'detail': 'Drink most of your 2.5-3.0 liters of water during daytime hours and taper fluid intake 2 hours before bedtime to minimize midnight bathroom trips.'}
        ]
    },
    'symptoms': [
        {'symptom': 'Morning Sickness & Nausea', 'remedy': 'Eat plain crackers before leaving bed. Sip iced ginger water. Eat small meals every 2 hours. Take Vitamin B6 as approved by your doctor.'},
        {'symptom': 'Heartburn & Acid Reflux', 'remedy': 'Avoid spicy, greasy, citrus, and tomato foods. Do not lie down for at least 90 minutes after eating. Elevate the head of your bed 6 inches.'},
        {'symptom': 'Backaches & Pelvic Pressure', 'remedy': 'Wear low-heeled supportive shoes with good arch support. Use a warm compress on sore back muscles. Do pelvic tilts on all fours daily.'},
        {'symptom': 'Leg Cramps & Restless Legs', 'remedy': 'Flex your foot upward toward your shin immediately when a cramp strikes. Ensure adequate daily magnesium and calcium intake. Stretch calves before bed.'},
        {'symptom': 'Constipation & Bloating', 'remedy': 'Eat 30g fiber daily (oats, chia seeds, beans, apples). Drink at least 10 glasses of water. Maintain daily walking habits.'}
    ],
    'mental_health': {
        'title': 'Maternal Mental Wellness & Emotional Self-Care',
        'points': [
            'Hormonal changes naturally cause mood shifts. Acknowledge your feelings without self-judgment.',
            'Communicate openly with your partner, family, and healthcare provider about anxieties or fears.',
            'Practice 10 minutes of daily mindfulness, box breathing (4s in, 4s hold, 4s out, 4s hold), or prenatal meditation.',
            'Join prenatal parent groups or forums to connect with other expectant mothers.',
            'If experiencing persistent sadness, severe anxiety, or inability to care for yourself, reach out to your doctor or a perinatal mental health specialist.'
        ]
    }
}

EMERGENCY_DATA = {
    'danger_signs': [
        {'sign': 'Heavy Vaginal Bleeding', 'description': 'Bright red bleeding with or without cramps, similar to or heavier than a period.', 'urgency': 'Immediate Emergency'},
        {'sign': 'Sudden Severe Swelling', 'description': 'Rapid puffiness of face, hands, or sudden unexplained weight gain (sign of Preeclampsia).', 'urgency': 'Immediate Emergency'},
        {'sign': 'Severe Headache with Blurred Vision', 'description': 'Persistent pounding headache, seeing flashing spots/aura, upper right abdominal pain.', 'urgency': 'Immediate Emergency'},
        {'sign': 'Sudden Gush or Trickle of Fluid', 'description': 'Premature rupture of membranes (water breaking) before 37 weeks or meconium-stained (greenish) fluid.', 'urgency': 'Immediate Emergency'},
        {'sign': 'Decreased or Absent Fetal Movement', 'description': 'Fewer than 10 kicks in 2 hours in the 3rd trimester, or significant reduction in normal baby movement patterns.', 'urgency': 'Urgent Checkup'},
        {'sign': 'High Fever (>100.4°F / 38°C) with Chills', 'description': 'Signs of systemic or intrauterine infection requiring prompt medical antibiotics.', 'urgency': 'Urgent Checkup'},
        {'sign': 'Persistent Severe Abdominal Pain', 'description': 'Sharp, constant, or unremitting pelvic/abdominal pain not relieved by changing positions.', 'urgency': 'Immediate Emergency'}
    ],
    'hospital_checklist': {
        'mom': [
            'Photo ID, Insurance Cards, Hospital Registration forms',
            'Birth plan copies & prenatal medical records',
            'Comfortable loose nightgown / delivery gown',
            'Warm non-skid socks and slip-on slippers',
            'Nursing bras (2-3) and breast pads',
            'Heavy-flow maternity pads & comfortable cotton underwear',
            'Lip balm, hair ties, travel toiletries (toothbrush, shampoo, lotion)',
            'Phone charger with extra-long cable & power bank'
        ],
        'baby': [
            'Rear-facing infant car seat (installed in car)',
            'Going-home outfit (sleeper, bodysuit, hat, socks)',
            'Soft receiving blankets (2)',
            'Newborn diapers and gentle baby wipes',
            'Baby mittens (to prevent fingernail scratching)'
        ],
        'partner': [
            'Change of comfortable clothes & layers',
            'Snacks, energy bars, and refillable water bottles',
            'Camera / phone for photos',
            'List of family members and friends to notify after birth'
        ]
    }
}


# Ensure integer keys for WEEKS_DATA
WEEKS_DATA = {int(k): v for k, v in _RAW_WEEKS_DATA.items()}
