from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configurarea cheii API pentru Gemini
API_KEY = ""  # Înlocuiește cu cheia ta API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

def get_nutritional_advice(user_input):
    prompt = f"""
   You are a nutritional AI assistant for NaturaBox. Your goal is to help the user choose one of the NaturaBox menus (SlimBox, EasyBox, GreenBox, VeggieBox, MuscleBox) based on the following input: "{user_input}", while also providing generic health advice, such as the importance of physical activity and hydration. If the user provides their weight (in kg) and height (in cm), calculate their Body Mass Index (BMI = weight / (height in meters * height in meters)) and use it to recommend a suitable menu. If this data is missing, ask for clarification. Recommend the daily water intake (30-35 ml/kg of weight, +500 ml if the user is physically active). Respect mentioned preferences, restrictions (e.g., vegan, vegetarian) and goals (e.g., weight loss, muscle gain, general health).

### NaturaBox Menu Descriptions:
1. **SlimBox**: Perfect for healthy weight loss. Includes lunch, dinner and a nutritional snack with clean ingredients for hunger and calorie control. Ideal for those looking to lose weight. Caloric options: 1000, 1400, 1800.
2. **EasyBox**: Varied menu for those without strict restrictions who want balanced meals. Includes meat, dairy, vegetables, fruits, nuts, seeds and spices. Provides essential macro and micronutrients. Caloric options: 1400, 1800, 2200.
3. **GreenBox**: Vegan menu for plant-based diets or fasting. Rich in plant proteins, healthy fats, fiber and antioxidants. Cooked at low temperatures. Caloric options: 1400, 1800, 2200.
4. **VeggieBox**: Vegetarian menu, without meat. Includes vegetables, legumes, dairy, eggs, proteins, fiber and healthy fats. Supports digestion and energy. Caloric option: 1500.
5. **MuscleBox**: Ideal for muscle gain and sports performance. High in protein (lean meat, eggs, dairy, plant sources), complex carbs and healthy fats. Caloric option: 2600.

### Instructions:
- **Menu recommendation**: Choose a box and caloric option based on BMI, goals and restrictions. Ex. BMI > 25 → SlimBox; BMI < 18.5 → MuscleBox; BMI 18.5-24.9 → EasyBox/GreenBox/VeggieBox. Explain why it fits.
- **Physical activity**: Include generic advice, ex. "For optimal health, try 150 minutes of moderate activity per week, such as brisk walking or yoga."
- **Hydration**: Calculate required water (30-35 ml/kg weight, +500 ml if user mentions intense physical activity) and include recommendation, ex. "For 70 kg, drink about 2.1-2.5 liters of water daily."
- **Clarifications**: If input is vague or missing data (weight, height, restrictions, goals, activity level), ask for details, ex. "Please tell me your weight and height, what goals you have (weight loss, muscle gain) and if you have dietary restrictions (vegan, vegetarian)."
- **Restrictions**: Choose compatible boxes (ex. GreenBox for vegan, VeggieBox for vegetarian). If user mentions other restrictions (ex. gluten-free), note that you'll recommend a compatible box only if it aligns with available menus.
- **Tone and format**: The response should be clear, friendly, in plain text format (no lists, bold). Avoid professional medical advice.
- **Response example**: "Based on your weight of 80 kg and height of 170 cm, your BMI is 27.7, which suggests overweight. I recommend SlimBox 1400 kcal for healthy weight loss, with balanced meals that control hunger. Try 150 minutes of moderate activity per week, like brisk walking. For hydration, drink about 2.4-2.8 liters of water daily. If you have dietary restrictions, please let me know!"

Provide the response as plain text, keeping a positive and accessible tone.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Eroare: {str(e)}"

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/get_advice', methods=['POST'])
def get_advice():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({'advice': 'Te rog introdu o cerere.'})
    advice = get_nutritional_advice(user_input)
    return jsonify({'advice': advice})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
