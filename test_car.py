#!/usr/bin/env python3
"""
Машины зургийг LLaVA-аар шинжлэх
"""
import ollama
import time

print("🚗 Машины зургийн шинжилгээ\n")
print("=" * 60)

image_file = 'test_car.png'

# Машины зургад тохирсон асуултууд
questions = [
    "What do you see in this image? Describe in detail.",
    "What type of vehicle is shown in the image?",
    "What is the color of the vehicle?",
    "Describe the vehicle's condition and appearance.",
    "What is the background or setting of this image?",
    "Can you identify the make or model of this vehicle?",
    "Are there any distinctive features or details visible?",
    "What is the angle or perspective of this photo?"
]

results = []

for i, question in enumerate(questions, 1):
    print(f"\n[{i}/{len(questions)}] ❓ {question}")
    print("⏳ Боловсруулж байна...")
    
    start = time.time()
    
    try:
        response = ollama.chat(
            model='llava:7b',
            messages=[
                {
                    'role': 'user',
                    'content': question,
                    'images': [image_file]
                }
            ]
        )
        
        duration = time.time() - start
        answer = response['message']['content']
        
        results.append({
            'question': question,
            'answer': answer,
            'time': duration
        })
        
        print(f"✅ Хариу ({duration:.1f}s):")
        print(f"🤖 {answer}")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Алдаа: {e}")

# Дүгнэлт
print("\n" + "=" * 60)
print("📊 Дүгнэлт:")
times = [r['time'] for r in results]
print(f"   • Нийт асуулт: {len(times)}")
print(f"   • Дундаж цаг: {sum(times)/len(times):.1f}s")
print(f"   • Нийт цаг: {sum(times):.1f}s ({sum(times)/60:.1f} мин)")

# Хадгалах
import json
with open('car_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n💾 Үр дүн хадгалагдсан: car_analysis.json")
