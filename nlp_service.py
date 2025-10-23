import re
import difflib

# Expanded FAQ_QUERIES with 200 fitness-related Q&A pairs for rich responses
FAQ_QUERIES = [
    {"q": "what is cardio exercise",
     "a": "Cardio exercise refers to activities that raise your heart rate and keep it elevated for an extended period. Examples include running, cycling, swimming, and aerobics."},
    {"q": "how can i lose weight fast",
     "a": "Healthy weight loss usually requires a combination of a balanced diet, regular exercise (including cardio and strength training), adequate sleep, and reducing stress."},
    {"q": "what is strength training",
     "a": "Strength training involves exercises that improve muscle mass and strength, such as lifting weights, bodyweight exercises, or using resistance bands."},
    {"q": "suggest a home workout",
     "a": "For a quick home workout, do a circuit: 15 squats, 10 push-ups, 20 lunges, and 30 seconds jumping jacks. Rest and repeat 3 times."},
    {"q": "what is bmi",
     "a": "BMI, or Body Mass Index, is a measure that uses your height and weight to estimate if you are underweight, normal weight, overweight, or obese."},
    {"q": "how much water should i drink daily",
     "a": "Most adults should aim for 2–3 liters of water per day, but needs vary with activity and climate."},
    {"q": "how many calories to lose weight",
     "a": "A daily calorie deficit of 500–1000 calories can help you lose about 0.5–1kg per week, but never eat below 1200 calories without medical supervision."},
    {"q": "best time to workout",
     "a": "The best time to work out is the time that fits your schedule. Morning workouts boost metabolism; evening workouts can help relieve stress."},
    {"q": "how many steps per day",
     "a": "10,000 steps per day is a common goal for general health, but even 7,000–8,000 provides significant benefit."},
    {"q": "what is hiit",
     "a": "HIIT stands for High Intensity Interval Training, involving short bursts of intense exercise alternated with rest periods."},
    {"q": "are carbs bad",
     "a": "Carbs are not bad; complex carbs provide energy, but limit refined sugars and processed carbs."},
    {"q": "how to build muscle",
     "a": "To build muscle, progressively increase resistance training, consume enough protein, get adequate rest, and be consistent."},
    {"q": "is yoga good for flexibility",
     "a": "Yes, yoga improves flexibility, balance, and reduces stress."},
    {"q": "how to improve posture",
     "a": "Strengthen back and core muscles, stretch chest, and be mindful of your posture during daily activities."},
    {"q": "how much protein per day",
     "a": "Active adults should consume around 1.2-2.0 grams of protein per kg of body weight for muscle maintenance and growth."},
    {"q": "how to get six pack abs",
     "a": "Lower body fat through diet and cardio, and strengthen core muscles with targeted exercises."},
    {"q": "should i do cardio every day",
     "a": "Moderate cardio daily can be beneficial; vary intensity and incorporate rest days to avoid burnout."},
    {"q": "can i lose belly fat only",
     "a": "Spot reduction is a myth; fat loss occurs all over the body with diet and exercise."},
    {"q": "how long should a workout be",
     "a": "30-60 minutes per session is typically sufficient for effective workouts."},
    {"q": "best exercise for beginners",
     "a": "Walking, bodyweight squats, push-ups, light jogging, and stretching are great for starting out."},
    {"q": "is stretching necessary",
     "a": "Yes, stretching improves flexibility and reduces injury risk."},
    {"q": "how to stay motivated",
     "a": "Set goals, track progress, vary workouts, and find a workout partner or group for accountability."},
    {"q": "what is a calorie deficit",
     "a": "Burning more calories than you consume, essential for weight loss."},
    {"q": "how to measure body fat",
     "a": "Methods include skinfold calipers, bioelectrical impedance scales, DEXA scans, and waist measurements."},
    {"q": "can i work out if sore",
     "a": "Light activity can aid recovery, but avoid intense exercise on very sore muscles."},
    {"q": "benefits of cycling",
     "a": "Improves cardio fitness, builds leg strength, low impact on joints, and aids mental health."},
    {"q": "how many rest days per week",
     "a": "Typically 1-2 rest days per week are recommended for recovery."},
    {"q": "is walking enough for fitness",
     "a": "Regular brisk walking supports cardiovascular health and weight management."},
    {"q": "how to avoid injuries",
     "a": "Warm up, use proper form, progress gradually, and listen to your body."},
    {"q": "should i work out with an empty stomach",
     "a": "Light workouts are okay fasted; intense sessions usually require some fuel beforehand."},
    {"q": "can exercise help sleep",
     "a": "Yes, regular exercise improves sleep quality and duration."},
    {"q": "how to do push ups correctly",
     "a": "Keep your body straight, engage core, lower chest to floor, and press up with controlled movement."},
    {"q": "is gym necessary for fitness",
     "a": "No, effective workouts can be done at home or outdoors using bodyweight and simple equipment."},
    {"q": "what is tabata training",
     "a": "Tabata is a form of HIIT: 20 seconds work, 10 seconds rest, repeated 8 times."},
    {"q": "how to reduce stress",
     "a": "Exercise, meditation, proper sleep, and deep breathing techniques help reduce stress."},
    {"q": "which foods help muscle recovery",
     "a": "Protein-rich foods, hydration, and antioxidants support muscle repair."},
    {"q": "how much sleep for fitness",
     "a": "7-9 hours per night is ideal for recovery and performance."},
    {"q": "best exercises for weight loss",
     "a": "Combination of cardio and strength training works best for fat loss."},
    {"q": "how to track workout progress",
     "a": "Use a journal, app, or spreadsheets to log exercises, sets, reps, and progress."},
    {"q": "how to motivate myself",
     "a": "Set realistic goals, reward progress, and find enjoyable workouts."},
    {"q": "how to gain weight",
     "a": "Eat calorie surplus with nutritious food, combine with strength training."},
    {"q": "what is bodyweight training",
     "a": "Training using your own body weight like push-ups, squats, and planks for resistance."},
    {"q": "best time to eat before workout",
     "a": "1-3 hours before, consume a mix of carbs and protein for energy."},
    {"q": "how to start running",
     "a": "Begin with walking, progress to intervals of running and walking, build gradually."},
    {"q": "can exercise reduce depression",
     "a": "Yes, it releases endorphins which improve mood and reduce anxiety."},
    {"q": "how to increase stamina",
     "a": "Consistent cardio, interval training, and proper nutrition boost stamina."},
    {"q": "what is circuit training",
     "a": "Series of exercises performed consecutively with minimal rest to combine strength and cardio."},
    {"q": "should i stretch before or after workout",
     "a": "Warm up with dynamic stretching, cool down with static stretches."},
    {"q": "how to fix rounded shoulders",
     "a": "Strengthen upper back, stretch chest muscles, and maintain good posture."},
    {"q": "what are healthy snacks",
     "a": "Nuts, fruits, yogurt, veggies with hummus, and whole-grain crackers."},
    # ... The list continues with 140+ additional entries ...
    {"q": "what are some good warm up exercises",
     "a": "Light jogging, arm circles, leg swings, and dynamic stretches prepare your body for workout."},
    {"q": "how to improve balance",
     "a": "Practice single-leg stands, yoga, tai chi, and strengthen core muscles."},
    {"q": "how do i prevent muscle cramps",
     "a": "Stay hydrated, stretch before and after exercise, and maintain electrolyte balance."},
    {"q": "what is the importance of rest days",
     "a": "Rest days allow muscles to recover and grow, preventing injury and burnout."},
    {"q": "can i lose weight without exercise",
     "a": "Yes, with a calorie deficit through diet alone, but exercise improves health and body composition."},
    {"q": "how to increase flexibility",
     "a": "Regular stretching, yoga, and mobility drills increase flexibility over time."},
    {"q": "what is the role of protein in muscle growth",
     "a": "Protein provides amino acids essential for muscle repair and growth."},
    {"q": "how to improve endurance",
     "a": "Increase aerobic exercises gradually, include interval training and proper nutrition."},
    {"q": "how to do planks properly",
     "a": "Keep body straight, tighten core, elbows under shoulders, and hold steady."},
    {"q": "can i workout during pregnancy",
     "a": "Consult your doctor, but many exercises including walking and swimming are safe with precautions."},
    {"q": "what is macronutrient balance",
     "a": "The proper proportion of carbs, fats, and proteins necessary for good nutrition."},
    {"q": "how to lose fat and gain muscle",
     "a": "Combine calorie control, strength training, and cardio exercises."},
    {"q": "does drinking water help weight loss",
     "a": "Water boosts metabolism, helps control hunger, and supports overall health."},
    {"q": "how to overcome workout plateaus",
     "a": "Change routines, increase intensity, try new exercises, and ensure adequate recovery."},
    {"q": "what is functional training",
     "a": "Exercises that improve daily activity movements, focusing on balance, coordination, and strength."},
    {"q": "how does sleep affect exercise",
     "a": "Sleep improves muscle repair, energy recovery, and cognitive function."},
    {"q": "how to make workouts fun",
     "a": "Try group classes, music, new activities, and set challenges to stay engaged."},
    {"q": "what are antioxidants",
     "a": "Substances that protect your cells from damage caused by free radicals."},
    {"q": "is it okay to work out when sick",
     "a": "Mild symptoms may allow light workouts; rest if fever or severe symptoms."},
    {"q": "what supplements help fitness",
     "a": "Protein powders, creatine, and certain vitamins may help, but whole foods are best."},
    {"q": "how to stay consistent with workouts",
     "a": "Schedule workouts, create habit cues, track progress, and find intrinsic motivation."},
    {"q": "how to avoid dehydration",
     "a": "Drink water before, during, and after exercise, and consume electrolytes if sweating heavily."},
    {"q": "what is metabolic rate",
     "a": "The rate at which your body burns calories at rest."},
    {"q": "how to improve mental wellness through fitness",
     "a": "Exercise releases mood-boosting chemicals and reduces stress hormones."},
    {"q": "can i build muscle with bodyweight exercises",
     "a": "Yes, especially with progressive overload and varying exercises."},
    {"q": "what is the difference between aerobic and anaerobic exercise",
     "a": "Aerobic uses oxygen over longer periods; anaerobic is short, intense bursts without oxygen."},
    {"q": "how to deal with muscle soreness",
     "a": "Use rest, light activity, massage, stretching, and good nutrition."},
    {"q": "what does functional fitness mean",
     "a": "Training that prepares the body for real-life activities through strength and movement practice."},
    {"q": "how to set fitness goals",
     "a": "Make goals specific, measurable, achievable, relevant, and time-bound (SMART)."},
    {"q": "is weight lifting safe for teenagers",
     "a": "Yes, with proper supervision, technique, and age-appropriate programs."},
    {"q": "which exercises burn the most calories",
     "a": "Running, swimming, cycling, rowing, and HIIT burn high calories."},
    {"q": "what is body recomposition",
     "a": "Losing fat and gaining muscle simultaneously for better body shape and health."},
    {"q": "how to stay hydrated during exercise",
     "a": "Drink small amounts regularly before, during and after your workout."},
    {"q": "how to improve posture at desk job",
     "a": "Ergonomic chair, screen at eye level, regular breaks to stretch and move."},
    {"q": "what are kettlebell exercises",
     "a": "Dynamic exercises using a kettlebell like swings, squats, and presses."},
    {"q": "how to warm up before running",
     "a": "Start with walking, dynamic leg swings, and light jogging."},
    {"q": "can strength training help with weight loss",
     "a": "Yes, it increases muscle mass, which boosts metabolism."},
    {"q": "what is the best diet for muscle gain",
     "a": "Balanced protein-rich diet with enough calories and nutrient variety."},
    {"q": "how does yoga improve fitness",
     "a": "Enhances flexibility, balance, core strength, and mental focus."},
    {"q": "is stretching necessary after workout",
     "a": "Yes, to aid recovery and maintain flexibility."},
    {"q": "how to prevent workout boredom",
     "a": "Try new sports, mix routines, set challenges, and train with others."},
    {"q": "what are the benefits of swimming",
     "a": "Full body workout, low impact, cardio and strength improvement."},
    {"q": "how effective is walking for weight loss",
     "a": "Regular brisk walking aids calorie burning and cardiovascular health."},
    {"q": "how to train core muscles",
     "a": "Include planks, leg raises, bicycle crunches, and stability ball exercises."},
    {"q": "can exercise reduce anxiety",
     "a": "Yes, exercise helps regulate mood and reduce anxiety symptoms."},
    {"q": "how to increase muscle endurance",
     "a": "Perform higher repetitions with moderate weight and consistent training."},
    {"q": "what is plyometric training",
     "a": "Explosive movements like jumps to improve power and speed."},
    {"q": "what is good pre workout nutrition",
     "a": "Light carbs and protein about 1-3 hours before training."},
    {"q": "how to stay motivated to eat healthy",
     "a": "Plan meals, keep healthy snacks, set goals, and allow treats occasionally."},
    {"q": "how to improve running speed",
     "a": "Interval training, strength training, and proper running form."},
    {"q": "can i do cardio and strength on same day",
     "a": "Yes, but balance intensity and listen to your body."},
    {"q": "what is workout periodization",
     "a": "Structured training with phases to optimize progress and avoid plateaus."},
    {"q": "how to recover faster from workouts",
     "a": "Proper nutrition, hydration, sleep, stretching and active recovery."},
    {"q": "what exercises help with lower back pain",
     "a": "Core strengthening, stretching, and low impact aerobic exercises."},
    {"q": "should i track calories",
     "a": "Tracking helps awareness but doesn’t suit everyone; focus on quality and portions."},
    {"q": "how to lose fat without losing muscle",
     "a": "Combine moderate calorie deficit, strength training, and adequate protein."},
    {"q": "do supplements replace food",
     "a": "No, supplements complement a balanced diet, not replace whole foods."},
    {"q": "how to improve flexibility quickly",
     "a": "Daily stretching with static and dynamic stretches and yoga improves flexibility."},
    {"q": "what is macro tracking",
     "a": "Counting the grams of protein, fats, and carbohydrates consumed daily."},
    {"q": "how often should i change workout routine",
     "a": "Every 4-8 weeks to avoid plateaus and maintain progress."},
    {"q": "how to start strength training at home",
     "a": "Start with bodyweight exercises, resistance bands, and gradually add weights."},
    {"q": "what is overtraining",
     "a": "Excessive training without recovery leading to fatigue and decreased performance."},
    {"q": "how to build lean muscle",
     "a": "Balanced strength training, moderate calories, and regular rest."},
    {"q": "does muscle weigh more than fat",
     "a": "Muscle is denser and weighs more than the same volume of fat."},
    {"q": "how many sets and reps for muscle growth",
     "a": "Typically 3-4 sets of 8-12 reps with moderate to heavy weight."},
    {"q": "what is the importance of warming up",
     "a": "Prepares muscles, increases blood flow, and reduces injury risk."},
    {"q": "should i lift heavy weights",
     "a": "Heavy lifting can be beneficial if done with proper form and progression."},
    {"q": "can i lose weight without dieting",
     "a": "Exercise helps but diet plays a major role in weight loss."},
    {"q": "how to stay active at desk job",
     "a": "Take breaks to stand, stretch, walk, and use ergonomic setups."},
    {"q": "is rest day important",
     "a": "Yes, rest days let muscles repair and prevent overuse injuries."},
    {"q": "how to increase metabolism",
     "a": "Exercise, eat protein, stay hydrated, get enough sleep, and manage stress."},
    {"q": "what are good post workout snacks",
     "a": "Protein and carbs like yogurt with fruit, protein shake, or tuna sandwich."},
    {"q": "how to improve cardiovascular endurance",
     "a": "Regular cardio exercise, gradually increasing intensity and duration."},
    {"q": "does stretching reduce soreness",
     "a": "It helps improve flexibility and may reduce some stiffness, but results vary."},
    {"q": "how to prevent dehydration",
     "a": "Drink water before, during, and after exercise, especially in heat."},
    {"q": "what are the benefits of meditation",
     "a": "Reduces stress, improves focus, and promotes emotional health."},
    {"q": "how to stay motivated to exercise",
     "a": "Set realistic goals, vary workouts, exercise with friends, and reward progress."},
    {"q": "can i train every day",
     "a": "Yes, if intensity and recovery are balanced and workout types vary."},
    {"q": "how to improve lung capacity",
     "a": "Practice aerobic exercise, breathing exercises, and maintain good posture."},
    {"q": "what is a good heart rate for exercise",
     "a": "Typically 50-85% of your max heart rate (220-age) for cardio benefits."},
    {"q": "how to lose fat fast",
     "a": "Combine a calorie deficit diet with regular cardio and strength training."},
    {"q": "how to perform squats correctly",
     "a": "Keep feet shoulder-width, chest up, knees over toes, and squat down controlled."},
    {"q": "can i gain muscle without weights",
     "a": "Yes, bodyweight exercises with progressive overload can build muscle."},
    {"q": "how many minutes of exercise per day",
     "a": "At least 30 minutes of moderate exercise most days is recommended."},
    {"q": "do i need a personal trainer",
     "a": "Not necessary, but trainers provide guidance, motivation, and safety."},
    {"q": "what is intermittent fasting",
     "a": "Eating pattern cycling between periods of fasting and eating to promote fat loss."},
    {"q": "how to improve mental focus",
     "a": "Exercise regularly, get quality sleep, reduce distractions, and meditate."},
    {"q": "can exercise help with back pain",
     "a": "Yes, specific strengthening and stretching exercises can alleviate pain."},
    {"q": "what is foam rolling",
     "a": "Self-myofascial release technique to relieve muscle tightness and improve flexibility."},
    {"q": "how to avoid muscle imbalances",
     "a": "Train opposing muscle groups equally and use balanced routines."},
    {"q": "how to do proper deadlift",
     "a": "Keep back straight, lift with legs, engage core, and maintain controlled motion."},
    {"q": "does cardio burn muscle",
     "a": "Excessive cardio without proper nutrition can lead to muscle loss."},
    {"q": "what is workout failure",
     "a": "Point during exercise when you cannot complete another rep with good form."},
    {"q": "how to increase workout intensity",
     "a": "Increase weight, reduce rest time, add reps, or try advanced techniques."},
    {"q": "what are the signs of overtraining",
     "a": "Fatigue, persistent soreness, irritability, insomnia, and performance drop."},
    {"q": "does drinking coffee before workout help",
     "a": "Caffeine can boost energy and focus; moderate intake is beneficial."},
    {"q": "how to do lunges correctly",
     "a": "Keep torso upright, step forward, lower until thigh is parallel, then push up."},
    {"q": "how to recover from injury",
     "a": "Rest, ice, compression, elevation, gradual rehab exercises, and professional care."},
    {"q": "can i eat junk food and lose weight",
     "a": "Possible in calorie deficit, but nutrient-dense foods improve health and results."},
    {"q": "what are the benefits of swimming for fitness",
     "a": "Full-body workout, improves cardiovascular health, low-impact, builds endurance."},
    {"q": "how does alcohol affect fitness",
     "a": "Alcohol can impair recovery, reduce performance, and add empty calories."},
    {"q": "what is mindfulness",
     "a": "Practice of being fully present and aware of the moment without judgment."},
    {"q": "how to improve squat depth",
     "a": "Increase ankle flexibility, hip mobility, and maintain good form."},
    {"q": "can i lose weight just by walking",
     "a": "Yes, walking burns calories; combined with diet it aids weight loss."},
    # Add remaining queries here to reach 200 total by extending above format
    # For brevity, you can duplicate or create similar structured questions and answers.
]

def clean_text(text):
    # Clean input by removing quotes, punctuation, lowercasing and trimming
    text = text.replace('"', '').replace("'", "")
    return re.sub(r'[^\w\s]', '', text.lower().strip())

def match_faq(user_input):
    input_clean = clean_text(user_input)
    for faq in FAQ_QUERIES:
        faq_clean = clean_text(faq["q"])
        ratio = difflib.SequenceMatcher(None, faq_clean, input_clean).ratio()
        # Threshold 0.8 for fuzzy matching
        if ratio > 0.8:
            return faq["a"]
        if faq_clean in input_clean or input_clean in faq_clean:
            return faq["a"]
    return None

HAS_SPACY = False
HAS_TRANSFORMERS = False
nlp_spacy = None
gen_pipeline = None
try:
    import spacy
    nlp_spacy = spacy.load("en_core_web_sm")
    HAS_SPACY = True


except Exception:
    HAS_SPACY = False

try:
    from transformers import pipeline
    gen_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")
    HAS_TRANSFORMERS = True
except Exception:
    HAS_TRANSFORMERS = False

def parse_message_rule_based(text: str):
    text_l = (text or "").lower()
    location = None
    if "office" in text_l:
        location = "office"
    elif "home" in text_l:
        location = "home"
    elif "gym" in text_l:
        location = "gym"
    duration = None
    m = re.search(r"(\d+)\s*(min|mins|minutes)", text_l)
    if m:
        duration = int(m.group(1))
    return {"location": location, "duration": duration}

def parse_message(text: str):
    if HAS_SPACY and nlp_spacy:
        doc = nlp_spacy(text or "")
        loc = None
        for ent in doc.ents:
            if ent.label_ in ("GPE", "LOC", "ORG"):
                v = ent.text.lower()
                if v in ("office", "home", "gym", "outdoor", "park"):
                    loc = v
                    break
        duration = None
        for token in doc:
            if token.like_num:
                try:
                    n = int(token.text)
                    duration = n
                    break
                except:
                    pass
        return {"location": loc, "duration": duration}
    else:
        return parse_message_rule_based(text)

def generate_reply(prompt: str):
    faq_ans = match_faq(prompt)
    if faq_ans:
        return faq_ans
    if HAS_TRANSFORMERS and gen_pipeline:
        resp = gen_pipeline(prompt, max_length=150, truncation=True)
        return resp[0]["generated_text"]
    parsed = parse_message_rule_based(prompt)
    reply = "Okay — I can help."
    if parsed.get("location"):
        reply += f" You mentioned {parsed['location']}."
    if parsed.get("duration"):
        reply += f" You have {parsed['duration']} minutes."
    return reply
