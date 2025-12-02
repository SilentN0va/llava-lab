#!/usr/bin/env python3
"""
Машины зургийн интерактив шинжилгээ - ЗӨВӨӨР
"""
import ollama

print("🚗 Машины зургийн интерактив шинжилгээ")
print("=" * 60)
print("Зураг: test_car.png")
print("Асуултаа англиар оруулна уу ('exit' гэж бичвэл гарна)")
print()

image_file = 'room.jpg'  # ← Энэ зөв!

while True:
    question = input("\n❓ Асуулт: ").strip()
    
    if question.lower() in ['exit', 'quit', 'q']:
        print("\n👋 Баяртай!")
        break
    
    if not question:
        continue
    
    print("⏳ Боловсруулж байна...")
    
    try:
        response = ollama.chat(
            model='llava:7b',
            messages=[
                {'role': 'user', 'content': question, 'images': [image_file]}
            ]
        )
        
        answer = response['message']['content']
        print(f"\n🤖 {answer}")
        
    except Exception as e:
        print(f"\n❌ Алдаа: {e}")
