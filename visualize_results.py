#!/usr/bin/env python3
"""
LLaVA Performance Visualization
"""
import ollama
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import json
from datetime import datetime
import numpy as np

class LLaVAVisualizer:
    def __init__(self):
        self.results = []
    
    def run_benchmark(self, image_path, questions):
        """Benchmark ажиллуулах"""
        print("🔬 LLaVA Benchmark Starting...")
        print(f"📷 Зураг: {image_path}")
        print(f"❓ Асуултын тоо: {len(questions)}\n")
        
        for i, question in enumerate(questions, 1):
            print(f"[{i}/{len(questions)}] {question[:50]}...")
            
            start = time.time()
            
            try:
                response = ollama.chat(
                    model='llava:7b',
                    messages=[
                        {
                            'role': 'user',
                            'content': question,
                            'images': [image_path]
                        }
                    ]
                )
                
                duration = time.time() - start
                answer = response['message']['content']
                
                result = {
                    'question': question,
                    'answer': answer,
                    'inference_time': duration,
                    'answer_length': len(answer),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.results.append(result)
                
                print(f"   ✅ {duration:.1f}s | {len(answer)} chars")
                
            except Exception as e:
                print(f"   ❌ Алдаа: {e}")
        
        print(f"\n✅ Benchmark дууслаа! {len(self.results)} inference")
    
    def create_visualizations(self):
        """Графикууд үүсгэх"""
        if not self.results:
            print("⚠️  Үр дүн байхгүй байна")
            return
        
        # Өгөгдөл
        times = [r['inference_time'] for r in self.results]
        answer_lengths = [r['answer_length'] for r in self.results]
        
        # Графикууд үүсгэх
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('LLaVA Performance Analysis', fontsize=16, fontweight='bold')
        
        # График 1: Inference Time
        ax1 = axes[0, 0]
        colors = plt.cm.viridis(np.linspace(0, 1, len(times)))
        bars = ax1.bar(range(len(times)), times, color=colors, alpha=0.8, edgecolor='black')
        ax1.set_xlabel('Question Number', fontsize=12)
        ax1.set_ylabel('Inference Time (seconds)', fontsize=12)
        ax1.set_title('Inference Time per Question', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        for i, (bar, time_val) in enumerate(zip(bars, times)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{time_val:.1f}s',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # График 2: Answer Length vs Time
        ax2 = axes[0, 1]
        scatter = ax2.scatter(answer_lengths, times, 
                            c=range(len(times)), 
                            cmap='plasma', 
                            s=200, 
                            alpha=0.7, 
                            edgecolors='black')
        ax2.set_xlabel('Answer Length (characters)', fontsize=12)
        ax2.set_ylabel('Inference Time (seconds)', fontsize=12)
        ax2.set_title('Answer Length vs Inference Time', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        
        if len(times) > 1:
            corr = np.corrcoef(answer_lengths, times)[0, 1]
            ax2.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                    transform=ax2.transAxes, 
                    fontsize=11, 
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # График 3: Statistics
        ax3 = axes[1, 0]
        ax3.axis('off')
        
        stats_text = f"""
📊 СТАТИСТИК МЭДЭЭЛЭЛ

⏱️  Inference Time:
   • Дундаж: {np.mean(times):.2f}s
   • Min: {min(times):.2f}s
   • Max: {max(times):.2f}s
   • Стандарт хазайлт: {np.std(times):.2f}s

📝 Answer Length:
   • Дундаж: {np.mean(answer_lengths):.0f} chars
   • Min: {min(answer_lengths)} chars
   • Max: {max(answer_lengths)} chars

🔢 Total:
   • Нийт асуулт: {len(self.results)}
   • Нийт цаг: {sum(times):.1f}s
   • Дундаж хурд: {sum(answer_lengths)/sum(times):.1f} chars/s
        """
        
        ax3.text(0.1, 0.9, stats_text, 
                transform=ax3.transAxes,
                fontsize=12,
                verticalalignment='top',
                family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
        
        # График 4: Cumulative Time
        ax4 = axes[1, 1]
        cumulative_times = np.cumsum(times)
        ax4.plot(range(len(cumulative_times)), cumulative_times, 
                marker='o', linewidth=2, markersize=8, 
                color='darkred', label='Cumulative Time')
        ax4.fill_between(range(len(cumulative_times)), cumulative_times, 
                        alpha=0.3, color='red')
        ax4.set_xlabel('Question Number', fontsize=12)
        ax4.set_ylabel('Cumulative Time (seconds)', fontsize=12)
        ax4.set_title('Cumulative Inference Time', fontsize=14, fontweight='bold')
        ax4.grid(True, alpha=0.3, linestyle='--')
        ax4.legend(fontsize=11)
        
        # Хадгалах
        plt.tight_layout()
        output_file = 'llava_performance.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"\n📊 График хадгалагдсан: {output_file}")
        
        # JSON
        with open('benchmark_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"💾 JSON хадгалагдсан: benchmark_results.json")
        
        return output_file
    
    def create_comparison_chart(self):
        """Харьцуулсан график"""
        if not self.results:
            return
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        questions_short = [f"Q{i+1}" for i in range(len(self.results))]
        times = [r['inference_time'] for r in self.results]
        
        colors = plt.cm.coolwarm([(t - min(times))/(max(times) - min(times)) for t in times])
        bars = ax.barh(questions_short, times, color=colors, edgecolor='black', linewidth=1.5)
        
        ax.set_xlabel('Inference Time (seconds)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Questions', fontsize=14, fontweight='bold')
        ax.set_title('Question-by-Question Performance', fontsize=16, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (bar, time_val) in enumerate(zip(bars, times)):
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                   f'{time_val:.1f}s',
                   ha='left', va='center', fontsize=11, fontweight='bold')
        
        avg_time = np.mean(times)
        ax.axvline(avg_time, color='red', linestyle='--', linewidth=2, 
                  label=f'Average: {avg_time:.1f}s')
        ax.legend(fontsize=12)
        
        plt.tight_layout()
        output_file = 'llava_comparison.png'
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"📊 Харьцуулалт график: {output_file}")
        
        return output_file

if __name__ == "__main__":
    viz = LLaVAVisualizer()
    
    questions = [
        "What objects are visible in this room?",
        "Where is the desk located in this image?",
        "Describe the lighting in this room.",
        "What colors are dominant in this space?",
        "Is this an office, bedroom, or living room?",
        "What furniture pieces can you identify?",
        "Describe the overall ambiance of this room.",
        "Are there any windows visible? Where?"
    ]
    
    viz.run_benchmark('test_room.jpg', questions)
    
    print("\n🎨 Графикууд үүсгэж байна...")
    viz.create_visualizations()
    viz.create_comparison_chart()
    
    print("\n✅ Бүгд бэлэн!")
    print("\n📁 Үүссэн файлууд:")
    print("   - llava_performance.png")
    print("   - llava_comparison.png")
    print("   - benchmark_results.json")
