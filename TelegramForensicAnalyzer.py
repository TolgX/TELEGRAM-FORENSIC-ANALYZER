import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedTk, ThemedStyle
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageOps
import os
from wordcloud import WordCloud
import numpy as np
from collections import Counter
import random
import math
import colorsys

# Binary arka plan animasyonu için sınıf
class BinaryBackground(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#0A1929', highlightthickness=0)
        
        self.binary_chars = "01"
        self.chars = []
        self.char_size = 14
        self.update_size()
        self.animate()
    
    def update_size(self):
        width = self.winfo_width()
        height = self.winfo_height()
        if width > 0 and height > 0:
            cols = width // self.char_size
            rows = height // self.char_size
            
            for char in self.chars:
                self.delete(char)
            self.chars.clear()
            
            for i in range(cols):
                for j in range(rows):
                    x = i * self.char_size
                    y = j * self.char_size
                    char = self.create_text(x, y,
                                          text=random.choice(self.binary_chars),
                                          fill='#00FF4120',
                                          font=('Consolas', 10),
                                          anchor='nw')
                    self.chars.append(char)
    
    def animate(self):
        for char in self.chars:
            if random.random() < 0.02:
                self.itemconfig(char, text=random.choice(self.binary_chars))
        self.after(100, self.animate)

# Radar animasyonu için sınıf
class RadarAnimation(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#0A1929', highlightthickness=0)
        
        # Başlangıç değerleri
        self.angle = 0
        self.angle_speed = -5  # Derece/saniye
        self.blips = []
        self.width = kwargs.get('width', 200)
        self.height = kwargs.get('height', 200)
        self.config(width=self.width, height=self.height)
        
        # Animasyonu başlat
        self.sweep()
    
    def sweep(self):
        """Radar taraması animasyonu"""
        self.delete('all')  # Canvas'ı temizle
        
        # Radar merkezi ve yarıçapı
        center_x = self.width // 2
        center_y = self.height // 2
        radius = min(self.width, self.height) // 2 - 10
        
        # Ana çember
        self.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline='#00FF41',
            width=2
        )
        
        # İç çemberler ve mesafe etiketleri
        for i in range(1, 3):
            r = radius * (i / 3)
            self.create_oval(
                center_x - r,
                center_y - r,
                center_x + r,
                center_y + r,
                outline='#00FF41',
                width=1
            )
            # Mesafe etiketleri
            self.create_text(
                center_x + 5, 
                center_y - r, 
                text=f"{int(r)}m", 
                fill='#00FF41',
                font=('Consolas', 8),
                anchor='w'
            )
        
        # Izgara çizgileri ve koordinat sayıları
        for i in range(0, 360, 45):
            x = center_x + radius * math.cos(math.radians(i))
            y = center_y + radius * math.sin(math.radians(i))
            self.create_line(center_x, center_y, x, y, fill='#003311', width=1)
            
            # Koordinat sayıları
            angle_rad = math.radians(i)
            text_radius = radius + 15
            text_x = center_x + text_radius * math.cos(angle_rad)
            text_y = center_y + text_radius * math.sin(angle_rad)
            self.create_text(text_x, text_y, text=f"{i}°", fill='#00FF41', font=('Consolas', 8))
        
        # Tarama çizgisi
        sweep_x = center_x + radius * math.cos(math.radians(self.angle))
        sweep_y = center_y + radius * math.sin(math.radians(self.angle))
        self.create_line(
            center_x, center_y,
            sweep_x, sweep_y,
            fill='#00FF41',
            width=2
        )
        
        # Parlama efekti
        glow_coords = [
            (center_x, center_y),
            (sweep_x, sweep_y),
            (
                center_x + radius * math.cos(math.radians(self.angle - 10)),
                center_y + radius * math.sin(math.radians(self.angle - 10))
            )
        ]
        self.create_polygon(
            glow_coords,
            fill='#003311',
            outline=''
        )
        
        # Rastgele noktalar
        if random.random() < 0.1:
            rand_angle = random.uniform(0, 360)
            rand_radius = random.uniform(0, radius)
            x = center_x + rand_radius * math.cos(math.radians(rand_angle))
            y = center_y + rand_radius * math.sin(math.radians(rand_angle))
            self.blips.append([x, y, 255])
        
        # Mevcut noktaları çiz ve güncelle
        new_blips = []
        for x, y, intensity in self.blips:
            if intensity > 0:
                size = 3
                # Hedef yanıp sönme efekti
                if random.random() < 0.2:  # %20 şansla parlama efekti
                    size = 4
                    self.create_oval(
                        x - size - 2,
                        y - size - 2,
                        x + size + 2,
                        y + size + 2,
                        fill='',
                        outline='#00FF41'
                    )
                
                self.create_oval(
                    x - size,
                    y - size,
                    x + size,
                    y + size,
                    fill='#00FF41',
                    outline=''
                )
                new_blips.append([x, y, intensity - 3])
        self.blips = new_blips
        
        # Hedef bilgisi göster
        if self.blips:
            target_info = f"TARGETS: {len(self.blips)}"
            self.create_text(
                10, 10, 
                text=target_info,
                fill='#00FF41',
                font=('Consolas', 9),
                anchor='nw'
            )
        
        # Tarama hızı göstergesi
        speed_text = f"SCAN SPEED: {abs(self.angle_speed)}°/s"
        self.create_text(
            10,              # Soldan mesafe
            30,              # Üstten mesafe (TARGETS yazısının altına)
            text=speed_text,
            fill='#00FF41',
            font=('Consolas', 9),
            anchor='nw'      # 'nw' = north-west (sol üst köşe hizalama)
        )
        
        # Açıyı güncelle
        self.angle = (self.angle + self.angle_speed) % 360
        
        # Animasyonu devam ettir
        self.after(50, self.sweep)

class TelegramForensicAnalyzer:
    def __init__(self):
        self.root = ThemedTk()
        self.root.title("Telegram Adli Analiz Aracı")
        self.root.geometry("1400x900")
        
        # Tam ekran yapma
        self.root.state('zoomed')
        
        # Pencere yeniden boyutlandırıldığında binary arka planı güncelle
        self.root.bind('<Configure>', lambda e: self.update_binary_background())
        # Pencere kapatıldığında animasyonu durdur
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # İkon ekle (isteğe bağlı)
        if os.path.exists("icon.png"):
            icon = ImageTk.PhotoImage(file="icon.png")
            self.root.iconphoto(False, icon)
        
        self.data = None
        self.photo_frames = []
        self.create_gui()
        
    def on_closing(self):
        if hasattr(self, 'radar'):
           self.radar.stop()
           self.root.destroy()

    def update_binary_background(self):
        if hasattr(self, 'binary_bg'):
            self.binary_bg.update_size()

    def create_gui(self):
        # Siber güvenlik teması renkleri
        CYBER_COLORS = {
            'background': '#1E1E1E',  # Daha koyu bir arka plan
            'accent': '#4CAF50',      # Daha canlı bir yeşil
            'secondary': '#2196F3',   # Daha açık bir mavi
            'warning': '#FF5722',     # Uyarı için turuncu
            'text': '#FFFFFF'         # Beyaz metin
        }
        
        # Ana pencere ayarları
        self.root.configure(bg=CYBER_COLORS['background'])
        
        # Binary arka plan
        self.binary_bg = BinaryBackground(self.root, width=1400, height=900)
        self.binary_bg.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Ana frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        # Sol panel
        left_frame = ttk.Frame(self.main_frame, width=400)  # Sol panel genişliği
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Radar için frame
        radar_frame = tk.Frame(left_frame, bg='#0A1929')
        radar_frame.pack(pady=20)
        
        # Radar animasyonu
        self.radar = RadarAnimation(radar_frame, width=200, height=200)
        self.radar.pack(padx=10, pady=10)
        
        # Logo
        logo_text = """
    ╔══════════════════════╗
    ║ TELEGRAM FORENSICS   ║
    ║    ANALYZER v1.0     ║
    ╚══════════════════════╝
        """
        
        logo_label = tk.Label(left_frame,
                            text=logo_text,
                            font=('Courier New', 16, 'bold'),  # Daha büyük yazı tipi
                            fg=CYBER_COLORS['accent'],
                            bg=CYBER_COLORS['background'],
                            justify='left')
        logo_label.pack(pady=20)
        
        # Butonlar
        buttons = [
            ("🔍 GENEL İSTATİSTİKLER", self.show_general_stats),
            ("💬 MESAJ ANALİZİ", self.analyze_messages),
            ("🖼️ MEDYA ANALİZİ", self.analyze_media),
            ("👥 KİŞİ ANALİZİ", self.analyze_contacts),
            ("⏰ ZAMAN ANALİZİ", self.analyze_timeline),
            ("📁 JSON DOSYASI YÜKLE", self.load_data),
        ]
        
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=20)
        
        for text, command in buttons:
            btn = tk.Button(button_frame,
                          text=text,
                          command=command,
                          font=('Arial', 12, 'bold'),  # Farklı yazı tipi
                          bg=CYBER_COLORS['background'],
                          fg=CYBER_COLORS['accent'],
                          activebackground=CYBER_COLORS['secondary'],
                          activeforeground='white',
                          relief='raised',
                          borderwidth=2,
                          width=30,  # Genişlik artırıldı
                          height=2)
            btn.pack(pady=10)  # Düğmeler arasındaki boşluk artırıldı
            
            # Hover efekti
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=CYBER_COLORS['secondary']))
            btn.bind('<Leave>', lambda e, b=btn: b.configure(bg=CYBER_COLORS['background']))
        
        # Sağ panel
        right_container = ttk.Frame(self.main_frame, width=800)  # Sağ panel genişliği
        right_container.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10)
        
        # Terminal benzeri sonuç alanı
        self.result_text = tk.Text(right_container,
            wrap=tk.WORD,
            width=80,
            height=30,
            font=('Consolas', 11),
            bg='#001100',
            fg=CYBER_COLORS['accent'],
            insertbackground=CYBER_COLORS['accent'],
            selectbackground=CYBER_COLORS['secondary'],
            selectforeground='black',
            padx=20,
            pady=20)
        self.result_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Terminal başlığı
        self.result_text.insert('1.0', '=== TELEGRAM FORENSICS TERMINAL ===\n\n')
        self.result_text.insert('end', 'System ready...\nAwaiting commands...\n\n')
        
        # Fotoğraflar için frame
        self.photos_frame = ttk.Frame(right_container)
        self.photos_frame.pack(fill="both", expand=True, pady=10)
        
        # Durum çubuğu
        status_frame = tk.Frame(self.root, bg=CYBER_COLORS['background'])
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.status_bar = tk.Label(status_frame,
                                 text="[ SYSTEM READY ]",
                                 font=('Consolas', 10),
                                 fg=CYBER_COLORS['accent'],
                                 bg=CYBER_COLORS['background'])
        self.status_bar.pack(side='left', padx=10)
        
        # Durum çubuğuna CPU ve bellek bilgisi ekleyin
        status_right = tk.Label(status_frame,
                              font=('Consolas', 10),
                              fg=CYBER_COLORS['secondary'],
                              bg=CYBER_COLORS['background'])
        status_right.pack(side='right', padx=10)
        
        def update_status():
            cpu = random.randint(1, 100)
            mem = random.randint(1, 100)
            status_right.config(text=f"CPU: {cpu}% | MEM: {mem}% | {datetime.now().strftime('%H:%M:%S')}")
            self.root.after(1000, update_status)
        
        update_status()

    def load_data(self):
        file_path = filedialog.askopenfilename(
            title="Telegram JSON Dosyası Seç",
            filetypes=[('JSON dosyaları', '*.json')]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                self.json_directory = os.path.dirname(file_path)
                messagebox.showinfo("Başarılı", "Veriler başarıyla yüklendi!")
                self.show_general_stats()
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya yüklenirken hata oluştu: {str(e)}")

    def show_general_stats(self):
        if not self.data:
            messagebox.showwarning("Uyarı", "Lütfen önce veri dosyası yükleyin!")
            return
        
        self.clear_display()
        self.result_text.insert(tk.END, "GENEL İSTATİSTİKLER\n\n")
        
        try:
            # Medya istatistikleri
            profile_photos = self.data.get('profile_pictures', [])
            stories = self.data.get('stories', [])
            
            # Mesaj ve kullanıcı istatistikleri
            chats = self.data.get('chats', {})
            messages = []
            users = set()
            words = []
            
            if isinstance(chats, dict):
                chat_list = chats.get('list', [])
            else:
                chat_list = []
            
            for chat in chat_list:
                if 'messages' in chat:
                    for msg in chat['messages']:
                        if isinstance(msg, dict):
                            messages.append(msg)
                            user = msg.get('from', '')
                            if user:
                                users.add(user)
                            
                            # Kelime analizi için metin toplama
                            text = msg.get('text', '')
                            if isinstance(text, str):
                                words.extend(text.lower().split())
                            elif isinstance(text, list):
                                for item in text:
                                    if isinstance(item, str):
                                        words.extend(item.lower().split())
            
            stats = f"""
            Profil Fotoğrafı Sayısı: {len(profile_photos)}
            Hikaye Sayısı: {len(stories)}
            Toplam Mesaj Sayısı: {len(messages)}
            Toplam Kullanıcı Sayısı: {len(users)}
            Toplam Kelime Sayısı: {len(words)}
            """
            
            self.result_text.insert(tk.END, stats + "\n")
            
            # En çok kullanılan kelimeler
            if words:
                word_counts = Counter(words)
                self.result_text.insert(tk.END, "\nEn Çok Kullanılan 10 Kelime:\n" + "-"*40 + "\n")
                for word, count in word_counts.most_common(10):
                    self.result_text.insert(tk.END, f"{word}: {count} kez\n")
                
                # Kelime bulutu oluştur
                wordcloud = WordCloud(
                    width=800, 
                    height=400,
                    background_color='white',
                    max_words=100
                ).generate(' '.join(words))
                
                # Kelime bulutunu göster
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                plt.title('Kelime Bulutu')
                
                # Grafiği yeni pencerede göster
                top = tk.Toplevel(self.root)
                top.title("Kelime Bulutu")
                
                canvas = FigureCanvasTkAgg(plt.gcf(), master=top)
                canvas.draw()
                canvas.get_tk_widget().pack()
                
                # Pasta grafik için kullanıcı mesaj dağılımı
                user_messages = {}
                for msg in messages:
                    if isinstance(msg, dict):
                        user = msg.get('from', '')
                        if user:
                            user_messages[user] = user_messages.get(user, 0) + 1
                
                if user_messages:
                    plt.figure(figsize=(8, 6))
                    users_sorted = dict(sorted(user_messages.items(), 
                                             key=lambda x: x[1], 
                                             reverse=True)[:5])
                    
                    plt.pie(users_sorted.values(), 
                           labels=users_sorted.keys(), 
                           autopct='%1.1f%%')
                    plt.title('En Aktif 5 Kullanıcı')
                    
                    # Grafiği yeni pencerede göster
                    top = tk.Toplevel(self.root)
                    top.title("Kullanıcı Dağılımı")
                    
                    canvas = FigureCanvasTkAgg(plt.gcf(), master=top)
                    canvas.draw()
                    canvas.get_tk_widget().pack()
            
        except Exception as e:
            error_msg = f"İstatistikler hesaplanırken hata oluştu: {str(e)}"
            print("Hata detayı:", str(e))
            self.result_text.insert(tk.END, f"\nHATA: {error_msg}")

    def analyze_media(self):
        if not self.data:
            messagebox.showwarning("Uyarı", "Lütfen önce veri dosyası yükleyin!")
            return
        
        self.clear_display()
        self.result_text.insert(tk.END, "MEDYA ANALİZİ\n\n")
        
        try:
            # Medya bilgilerini topla
            profile_photos = []
            story_photos = []
            
            # Profil fotoğraflarını topla
            if 'profile_pictures' in self.data:
                for photo in self.data['profile_pictures']:
                    if 'photo' in photo:
                        profile_photos.append({
                            'path': photo['photo'],
                            'date': photo['date'],
                            'type': 'Profil Fotoğrafı'
                        })
            
            # Hikaye fotoğraflarını topla
            if 'stories' in self.data:
                for story in self.data['stories']:
                    if 'media' in story and story['media'].endswith(('.jpg', '.jpeg', '.png')):
                        story_photos.append({
                            'path': story['media'],
                            'date': story['date'],
                            'type': 'Hikaye Fotoğrafı',
                            'expires': story.get('expires', '')
                        })
            
            # İstatistikleri göster
            self.result_text.insert(tk.END, f"Toplam Profil Fotoğrafı: {len(profile_photos)}\n")
            self.result_text.insert(tk.END, f"Toplam Hikaye Fotoğrafı: {len(story_photos)}\n\n")
            
            # Fotoğrafları göster
            row = 0
            col = 0
            max_cols = 3  # Bir satırda gösterilecek maksimum fotoğraf sayısı
            
            # Profil fotoğraflarını göster
            if profile_photos:
                self.result_text.insert(tk.END, "PROFİL FOTOĞRAFLARI:\n" + "-"*40 + "\n\n")
                
                for photo in profile_photos:
                    try:
                        # Fotoğraf dosyasının tam yolunu oluştur
                        photo_path = os.path.join(self.json_directory, photo['path'])
                        
                        if os.path.exists(photo_path):
                            # Fotoğrafı yükle ve boyutlandır
                            img = Image.open(photo_path)
                            img.thumbnail((200, 200))  # Thumbnail boyutu
                            photo_img = ImageTk.PhotoImage(img)
                            
                            # Fotoğraf için frame oluştur
                            photo_frame = ttk.LabelFrame(self.photos_frame, text=f"Tarih: {photo['date']}")
                            photo_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                            
                            # Fotoğrafı göster
                            label = ttk.Label(photo_frame, image=photo_img)
                            label.image = photo_img  # Referansı koru
                            label.pack(padx=5, pady=5)
                            
                            # Dosya yolunu göster
                            ttk.Label(photo_frame, text=photo['path'], wraplength=200).pack(padx=5, pady=5)
                            
                            # Bir sonraki pozisyona geç
                            col += 1
                            if col >= max_cols:
                                col = 0
                                row += 1
                            
                    except Exception as e:
                        print(f"Fotoğraf yüklenirken hata: {str(e)}")
                        continue
            
            # Hikaye fotoğraflarını göster
            if story_photos:
                self.result_text.insert(tk.END, "\nHİKAYE FOTOĞRAFLARI:\n" + "-"*40 + "\n\n")
                
                for photo in story_photos:
                    try:
                        # Fotoğraf dosyasının tam yolunu oluştur
                        photo_path = os.path.join(self.json_directory, photo['path'])
                        
                        if os.path.exists(photo_path):
                            # Fotoğrafı yükle ve boyutlandır
                            img = Image.open(photo_path)
                            img.thumbnail((200, 200))  # Thumbnail boyutu
                            photo_img = ImageTk.PhotoImage(img)
                            
                            # Fotoğraf için frame oluştur
                            photo_frame = ttk.LabelFrame(self.photos_frame, 
                                text=f"Tarih: {photo['date']}\nBitiş: {photo['expires']}")
                            photo_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                            
                            # Fotoğrafı göster
                            label = ttk.Label(photo_frame, image=photo_img)
                            label.image = photo_img  # Referansı koru
                            label.pack(padx=5, pady=5)
                            
                            # Dosya yolunu göster
                            ttk.Label(photo_frame, text=photo['path'], wraplength=200).pack(padx=5, pady=5)
                            
                            # Bir sonraki pozisyona geç
                            col += 1
                            if col >= max_cols:
                                col = 0
                                row += 1
                            
                    except Exception as e:
                        print(f"Fotoğraf yüklenirken hata: {str(e)}")
                        continue
            
            # Pasta grafik oluştur
            if profile_photos or story_photos:
                plt.figure(figsize=(8, 6))
                labels = ['Profil Fotoğrafları', 'Hikaye Fotoğrafları']
                sizes = [len(profile_photos), len(story_photos)]
                
                plt.pie(sizes, labels=labels, autopct='%1.1f%%')
                plt.title('Medya Dağılımı')
                
                # Grafiği yeni pencerede göster
                top = tk.Toplevel(self.root)
                top.title("Medya Analizi Grafiği")
                
                canvas = FigureCanvasTkAgg(plt.gcf(), master=top)
                canvas.draw()
                canvas.get_tk_widget().pack()
            
            # Eğer hiç medya yoksa
            if not profile_photos and not story_photos:
                self.result_text.insert(tk.END, "Medya dosyası bulunamadı!")
        
        except Exception as e:
            error_msg = f"Medya analizi sırasında hata oluştu: {str(e)}"
            print(error_msg)
            print("Hata detayı:", str(e))
            self.result_text.insert(tk.END, f"\nHATA: {error_msg}")

    def analyze_messages(self):
        if not self.data:
            messagebox.showwarning("Uyarı", "Lütfen önce veri dosyası yükleyin!")
            return
        
        self.clear_display()
        self.result_text.insert(tk.END, "MESAJ ANALİZİ\n\n")
        
        try:
            chats = self.data.get('chats', {})
            if isinstance(chats, dict):
                chat_list = chats.get('list', [])
            else:
                chat_list = []
            
            messages = []
            for chat in chat_list:
                if 'messages' in chat:
                    messages.extend(chat['messages'])
            
            if messages:
                self.result_text.insert(tk.END, f"Toplam Mesaj Sayısı: {len(messages)}\n\n")
                self.result_text.insert(tk.END, "Son 100 Mesaj:\n" + "-"*40 + "\n\n")
                
                for msg in messages[:100]:
                    if isinstance(msg, dict):
                        date = msg.get('date', '')
                        text = msg.get('text', '')
                        if isinstance(text, list):
                            text = ' '.join(str(t) for t in text if isinstance(t, (str, int, float)))
                        from_user = msg.get('from', 'Bilinmeyen')
                        
                        if text:
                            self.result_text.insert(tk.END, f"[{date}] {from_user}: {text}\n")
            else:
                self.result_text.insert(tk.END, "Mesaj bulunamadı!")
                
        except Exception as e:
            error_msg = f"Mesaj analizi sırasında hata oluştu: {str(e)}"
            self.result_text.insert(tk.END, f"\nHATA: {error_msg}")

    def analyze_contacts(self):
        if not self.data:
            messagebox.showwarning("Uyarı", "Lütfen önce veri dosyası yükleyin!")
            return
        
        self.clear_display()
        self.result_text.insert(tk.END, "KULLANICI ANALİZİ\n\n")
        
        try:
            users = {}
            chats = self.data.get('chats', {})
            
            if isinstance(chats, dict):
                chat_list = chats.get('list', [])
            else:
                chat_list = []
            
            for chat in chat_list:
                if 'messages' in chat:
                    for msg in chat['messages']:
                        if isinstance(msg, dict):
                            user = msg.get('from', '')
                            if user:
                                users[user] = users.get(user, 0) + 1
            
            if users:
                self.result_text.insert(tk.END, f"Toplam Kullanıcı Sayısı: {len(users)}\n\n")
                self.result_text.insert(tk.END, "Kullanıcı Mesaj İstatistikleri:\n" + "-"*40 + "\n\n")
                
                for user, count in sorted(users.items(), key=lambda x: x[1], reverse=True):
                    self.result_text.insert(tk.END, f"{user}: {count} mesaj\n")
                
                # Pasta grafik oluştur
                plt.figure(figsize=(8, 6))
                top_users = dict(sorted(users.items(), key=lambda x: x[1], reverse=True)[:5])
                
                plt.pie(top_users.values(), labels=top_users.keys(), autopct='%1.1f%%')
                plt.title('En Aktif 5 Kullanıcı')
                
                # Grafiği yeni pencerede göster
                top = tk.Toplevel(self.root)
                top.title("Kullanıcı Analizi Grafiği")
                
                canvas = FigureCanvasTkAgg(plt.gcf(), master=top)
                canvas.draw()
                canvas.get_tk_widget().pack()
                
            else:
                self.result_text.insert(tk.END, "Kullanıcı bilgisi bulunamadı!")
                
        except Exception as e:
            error_msg = f"Kullanıcı analizi sırasında hata oluştu: {str(e)}"
            self.result_text.insert(tk.END, f"\nHATA: {error_msg}")

    def analyze_timeline(self):
        if not self.data:
            messagebox.showwarning("Uyarı", "Lütfen önce veri dosyası yükleyin!")
            return
        
        self.clear_display()
        self.result_text.insert(tk.END, "ZAMAN ANALİZİ\n\n")
        
        try:
            timeline = {}
            chats = self.data.get('chats', {})
            
            if isinstance(chats, dict):
                chat_list = chats.get('list', [])
            else:
                chat_list = []
            
            for chat in chat_list:
                if 'messages' in chat:
                    for msg in chat['messages']:
                        if isinstance(msg, dict) and 'date' in msg:
                            try:
                                date = msg['date']
                                if isinstance(date, (int, float)):
                                    date_str = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
                                elif isinstance(date, str):
                                    try:
                                        date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                                    except ValueError:
                                        try:
                                            date_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                                        except ValueError:
                                            date_obj = datetime.strptime(date.split()[0], '%Y-%m-%d')
                                    date_str = date_obj.strftime('%Y-%m-%d')
                                else:
                                    continue
                                
                                timeline[date_str] = timeline.get(date_str, 0) + 1
                            except:
                                continue
            
            if timeline:
                sorted_dates = sorted(timeline.items(), reverse=True)
                
                total_messages = sum(timeline.values())
                total_days = len(timeline)
                avg_messages = total_messages / total_days if total_days > 0 else 0
                
                self.result_text.insert(tk.END, f"Toplam Mesaj Sayısı: {total_messages}\n")
                self.result_text.insert(tk.END, f"Toplam Gün Sayısı: {total_days}\n")
                self.result_text.insert(tk.END, f"Günlük Ortalama Mesaj: {avg_messages:.2f}\n\n")
                
                self.result_text.insert(tk.END, "Günlük Mesaj Dağılımı (Son 30 gün):\n")
                self.result_text.insert(tk.END, "-" * 40 + "\n")
                
                for date, count in sorted_dates[:30]:
                    self.result_text.insert(tk.END, f"{date}: {count} mesaj\n")
                
                plt.figure(figsize=(12, 6))
                dates = [date for date, _ in sorted_dates[:30]]
                counts = [count for _, count in sorted_dates[:30]]
                
                plt.plot(dates, counts, marker='o')
                plt.title('Son 30 Günün Mesaj Dağılımı')
                plt.xlabel('Tarih')
                plt.ylabel('Mesaj Sayısı')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                top = tk.Toplevel(self.root)
                top.title("Zaman Analizi Grafiği")
                
                canvas = FigureCanvasTkAgg(plt.gcf(), master=top)
                canvas.draw()
                canvas.get_tk_widget().pack()
                
            else:
                self.result_text.insert(tk.END, "Tarih bilgisi bulunamadı!")
                
        except Exception as e:
            error_msg = f"Zaman analizi sırasında hata oluştu: {str(e)}"
            print(error_msg)
            print("Hata detayı:", str(e))
            self.result_text.insert(tk.END, f"\nHATA: {error_msg}")

    def clear_display(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert('1.0', '=== TELEGRAM FORENSICS TERMINAL ===\n\n')
        self.result_text.insert('end', 'Initializing analysis...\n\n')
        
        for widget in self.photos_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = TelegramForensicAnalyzer()
    app.root.mainloop()