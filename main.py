import tkinter as tk
import math
import random

class PumpVolumeController:
    def __init__(self, root):
        self.root = root
        self.root.title("🎈 Pump the Volume! 🎈")
        self.root.geometry("500x600")
        self.root.configure(bg="#2C3E50")
        
        self.volume = 0
        self.max_volume = 100
        self.pump_power = 8
        self.decay_rate = 0.3
        self.is_pumping = False
        self.shake_offset = 0
        
        # Title
        self.title_label = tk.Label(
            root, 
            text="PUMP TO INCREASE VOLUME!", 
            font=("Arial", 18, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        self.title_label.pack(pady=20)
        
        # Canvas for animation
        self.canvas = tk.Canvas(root, width=400, height=400, bg="#34495E", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Volume display
        self.volume_label = tk.Label(
            root,
            text="Volume: 0%",
            font=("Arial", 24, "bold"),
            fg="#E74C3C",
            bg="#2C3E50"
        )
        self.volume_label.pack(pady=10)
        
        # Pump button
        self.pump_btn = tk.Button(
            root,
            text="💨 PUMP! 💨",
            font=("Arial", 20, "bold"),
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            width=15,
            height=2,
            relief="raised",
            bd=5
        )
        self.pump_btn.pack(pady=10)
        self.pump_btn.bind("<ButtonPress>", self.start_pump)
        self.pump_btn.bind("<ButtonRelease>", self.stop_pump)
        
        # Draw initial balloon
        self.balloon = None
        self.balloon_string = None
        self.particles = []
        
        self.draw_balloon()
        self.animate()
    
    def draw_balloon(self):
        self.canvas.delete("all")
        
        # Calculate balloon size based on volume
        base_size = 50
        size = base_size + (self.volume / 100) * 150
        
        # Balloon position with shake effect
        cx = 200 + self.shake_offset
        cy = 200
        
        # Draw balloon string
        self.canvas.create_line(
            cx, cy + size/2, 
            cx, 380,
            width=3,
            fill="#95A5A6"
        )
        
        # Draw balloon (oval shape)
        x1 = cx - size
        y1 = cy - size * 1.2
        x2 = cx + size
        y2 = cy + size * 0.8
        
        # Color changes with volume
        if self.volume < 30:
            color = "#3498DB"  # Blue
        elif self.volume < 60:
            color = "#F39C12"  # Orange
        elif self.volume < 90:
            color = "#E74C3C"  # Red
        else:
            color = "#9B59B6"  # Purple (danger zone!)
        
        self.balloon = self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=color,
            outline="#2C3E50",
            width=3
        )
        
        # Draw shine effect
        shine_x = cx - size * 0.3
        shine_y = cy - size * 0.6
        self.canvas.create_oval(
            shine_x - 15, shine_y - 15,
            shine_x + 15, shine_y + 15,
            fill="white",
            outline=""
        )
        
        # Draw particles when pumping
        for px, py, life in self.particles:
            opacity = int(255 * life)
            particle_color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
            self.canvas.create_oval(
                px-3, py-3, px+3, py+3,
                fill=particle_color,
                outline=""
            )
    
    def start_pump(self, event):
        self.is_pumping = True
        self.pump_btn.configure(relief="sunken")
        
    def stop_pump(self, event):
        self.is_pumping = False
        self.pump_btn.configure(relief="raised")
    
    def animate(self):
        # Pump volume up
        if self.is_pumping and self.volume < self.max_volume:
            self.volume = min(self.max_volume, self.volume + self.pump_power)
            self.shake_offset = random.randint(-5, 5)
            
            # Add particles
            cx = 200 + self.shake_offset
            cy = 380
            for _ in range(3):
                px = cx + random.randint(-20, 20)
                py = cy + random.randint(-10, 10)
                self.particles.append([px, py, 1.0])
        else:
            self.shake_offset = 0
        
        # Decay volume slowly
        if not self.is_pumping and self.volume > 0:
            self.volume = max(0, self.volume - self.decay_rate)
        
        # Update particles
        new_particles = []
        for p in self.particles:
            p[1] -= 2  # Move up
            p[2] -= 0.05  # Fade out
            if p[2] > 0:
                new_particles.append(p)
        self.particles = new_particles
        
        # Update displays
        self.volume_label.config(text=f"Volume: {int(self.volume)}%")
        
        # Change volume label color
        if self.volume < 30:
            self.volume_label.config(fg="#3498DB")
        elif self.volume < 60:
            self.volume_label.config(fg="#F39C12")
        elif self.volume < 90:
            self.volume_label.config(fg="#E74C3C")
        else:
            self.volume_label.config(fg="#9B59B6")
        
        self.draw_balloon()
        
        # Continue animation
        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = PumpVolumeController(root)
    root.mainloop()
