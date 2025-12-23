"""
===============================================================================
STAGECOACH PROBLEMİ - DİNAMİK PROGRAMLAMA İLE EN KISA YOL BULMA
===============================================================================

Problem Tanımı:
    Bir posta arabasının A noktasından J noktasına, farklı aşamalardan (stage)
    geçerek en düşük maliyetle ulaşmasını sağlayan en kısa yolu bulmak.

Kullanılan Algoritma:
    Dinamik Programlama - Geriye Doğru Tümevarım (Backward Induction)
    
Bellman Denklemi:
    f(mevcut) = min { Geçiş Maliyeti + f(Gelecekteki Düğüm) }

Zaman Karmaşıklığı: O(V + E) - V: düğüm sayısı, E: kenar sayısı

Yazar: Ahmet Yeşil
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
import matplotlib.patheffects as path_effects
import numpy as np
import random

# ============================================================================
# BÖLÜM 1: VERİ YAPILARI VE GRAF TANIMI
# ============================================================================

class StagecoachProblem:
    """
    Stagecoach problemini temsil eden sınıf.
    
    Attributes:
        stages (dict): Her aşamadaki düğümleri tanımlar
        default_edges (dict): Varsayılan kenar ağırlıkları
        edges (dict): Mevcut kenar ağırlıkları
        cost_to_go (dict): Her düğümden hedefe olan minimum maliyet (DP tablosu)
        next_node (dict): En kısa yolda bir sonraki düğüm (yol yeniden inşası için)
    """
    
    def __init__(self):
        """
        Graf yapısını başlatır.
        Düğümler aşamalara (stage) göre organize edilir.
        Bu yapı, problemin bir DAG (Yönlü Asiklik Graf) olmasını garanti eder.
        """
        
        # Aşama tanımları: Her aşamada hangi şehirler var?
        self.stages = {
            0: ['A'],           # Başlangıç noktası
            1: ['B', 'C', 'D'], # Aşama 1 şehirleri
            2: ['E', 'F', 'G'], # Aşama 2 şehirleri
            3: ['H', 'I'],      # Aşama 3 şehirleri
            4: ['J']            # Hedef noktası
        }
        
        # Tüm düğümlerin listesi (geriye doğru sırayla işlenecek)
        self.all_nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        # Varsayılan kenar ağırlıkları (görseldeki değerler)
        # Her düğümün bağlı olduğu düğümler ve maliyetler
        self.default_edges = {
            # A'dan Stage 1'e
            'A': {'B': 2, 'C': 4, 'D': 3},
            # Stage 1'den Stage 2'ye
            'B': {'E': 7, 'F': 4},
            'C': {'E': 6, 'F': 3, 'G': 4},
            'D': {'F': 1, 'G': 5},
            # Stage 2'den Stage 3'e
            'E': {'H': 1, 'I': 6},
            'F': {'H': 6, 'I': 3},
            'G': {'H': 3, 'I': 3},
            # Stage 3'ten J'ye
            'H': {'J': 3},
            'I': {'J': 4},
            # J hedef düğüm, çıkışı yok
            'J': {}
        }
        
        # Mevcut kenar ağırlıkları (başlangıçta varsayılan değerler)
        self.edges = self._deep_copy_edges(self.default_edges)
        
        # DP tabloları (memoization)
        self.cost_to_go = {}  # Her düğümden hedefe minimum maliyet
        self.next_node = {}   # En kısa yolda bir sonraki düğüm
        
    def _deep_copy_edges(self, edges):
        """Kenar sözlüğünün derin kopyasını oluşturur."""
        return {node: dict(neighbors) for node, neighbors in edges.items()}
    
    def reset_to_default(self):
        """Kenar ağırlıklarını varsayılan değerlere döndürür."""
        self.edges = self._deep_copy_edges(self.default_edges)
        
    def set_random_weights(self, min_val=1, max_val=10):
        """
        Tüm kenar ağırlıklarını rastgele değerlerle değiştirir.
        
        Args:
            min_val: Minimum ağırlık değeri
            max_val: Maximum ağırlık değeri
        """
        for node in self.edges:
            for neighbor in self.edges[node]:
                self.edges[node][neighbor] = random.randint(min_val, max_val)
    
    def set_edge_weight(self, from_node, to_node, weight):
        """
        Belirli bir kenarın ağırlığını günceller.
        
        Args:
            from_node: Başlangıç düğümü
            to_node: Hedef düğümü
            weight: Yeni ağırlık değeri
        """
        if from_node in self.edges and to_node in self.edges[from_node]:
            self.edges[from_node][to_node] = weight

# ============================================================================
# BÖLÜM 2: DİNAMİK PROGRAMLAMA ALGORİTMASI (BACKWARD INDUCTION)
# ============================================================================

    def solve_backward_induction(self):
        """
        Geriye Doğru Tümevarım (Backward Induction) algoritması ile
        en kısa yolu hesaplar.
        
        Bu algoritma Bellman Optimizasyon İlkesi'ni kullanır:
        "Optimal bir politikanın herhangi bir alt politikası da optimaldir."
        
        Çalışma Prensibi:
        1. Hedef düğümden (J) başla, maliyeti 0 olarak ata
        2. Geriye doğru (J → A) her düğüm için:
           - Tüm komşulara gitme maliyetlerini hesapla
           - En düşük maliyetli komşuyu seç
           - Bu değeri kaydet (memoization)
        
        Returns:
            tuple: (minimum_maliyet, optimal_yol)
        """
        
        # Adım 1: DP tablolarını sıfırla
        # cost_to_go: Her düğümden hedefe olan minimum maliyet
        # Başlangıçta tüm değerler sonsuz (∞)
        self.cost_to_go = {node: float('inf') for node in self.all_nodes}
        self.next_node = {node: None for node in self.all_nodes}
        
        # Adım 2: Hedef düğümün (J) maliyeti 0
        # J'den J'ye gitmenin maliyeti sıfırdır
        self.cost_to_go['J'] = 0
        
        # Adım 3: Düğümleri geriye doğru sırala
        # J'den A'ya doğru gideceğiz (Backward Induction)
        nodes_reversed = list(reversed(self.all_nodes))
        
        # Adım 4: Her düğüm için Bellman denklemini uygula
        for current_node in nodes_reversed:
            # J zaten 0 maliyetli, atla
            if current_node == 'J':
                continue
                
            # Bu düğümün komşularını al
            neighbors = self.edges.get(current_node, {})
            
            # Her komşu için: geçiş maliyeti + komşudan hedefe maliyet
            for neighbor, transition_cost in neighbors.items():
                # Bellman Denklemi: f(current) = min{c(current,next) + f(next)}
                total_cost = transition_cost + self.cost_to_go[neighbor]
                
                # Eğer bu yol daha kısa ise, güncelle
                if total_cost < self.cost_to_go[current_node]:
                    self.cost_to_go[current_node] = total_cost
                    self.next_node[current_node] = neighbor
        
        # Adım 5: Optimal yolu yeniden inşa et (Path Reconstruction)
        optimal_path = self._reconstruct_path()
        
        return self.cost_to_go['A'], optimal_path
    
    def _reconstruct_path(self):
        """
        DP tabloları kullanarak optimal yolu yeniden inşa eder.
        
        Mantık:
        - A'dan başla
        - next_node tablosunu takip ederek J'ye kadar git
        - Her adımda ziyaret edilen düğümü listeye ekle
        
        Returns:
            list: Optimal yoldaki düğümlerin sıralı listesi
        """
        path = []
        current = 'A'
        
        # J'ye ulaşana kadar devam et
        while current is not None:
            path.append(current)
            current = self.next_node.get(current)
            
        return path
    
    def get_path_details(self):
        """
        Optimal yolun detaylı bilgilerini döndürür.
        
        Returns:
            list: Her adım için (from, to, cost) tuple'ları
        """
        path = self._reconstruct_path()
        details = []
        
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            cost = self.edges[from_node][to_node]
            details.append((from_node, to_node, cost))
            
        return details


# ============================================================================
# BÖLÜM 3: GRAFİK KULLANICI ARAYÜZÜ (GUI)
# ============================================================================

class StagecoachGUI:
    """
    Stagecoach problemi için grafiksel kullanıcı arayüzü.
    
    Özellikler:
    - Kenar ağırlıklarını manuel veya rastgele belirleme
    - Optimal yolu hesaplama ve gösterme
    - Grafı görselleştirme
    """
    
    def __init__(self, root):
        """
        GUI bileşenlerini başlatır.
        
        Args:
            root: Tkinter ana penceresi
        """
        self.root = root
        self.root.title("Stagecoach Problemi - Dinamik Programlama")
        self.root.geometry("1600x950")
        self.root.configure(bg='#f5f5dc')
        
        # Problem nesnesi
        self.problem = StagecoachProblem()
        
        # Ağırlık giriş alanları için sözlük
        self.weight_entries = {}
        
        # GUI'yi oluştur
        self._create_widgets()
        
        # Varsayılan graf'ı göster
        self._visualize_graph()
        
    def _create_widgets(self):
        """Tüm GUI bileşenlerini oluşturur - Üstte kontroller, altta tam genişlik harita."""
        
        # ==================== ÜST PANEL - KONTROLLER ====================
        top_panel = ttk.Frame(self.root)
        top_panel.pack(fill=tk.X, padx=10, pady=5)
        
        # --- Butonlar ---
        btn_frame = ttk.Frame(top_panel)
        btn_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(btn_frame, text="⚙️ Ağırlık Seçimi:", font=('Helvetica', 11, 'bold')).pack(anchor='w')
        
        ttk.Button(btn_frame, text="🎲 Rastgele", width=10,
                  command=self._set_random_weights).pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(btn_frame, text="📋 Varsayılan", width=10,
                  command=self._reset_to_default).pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(btn_frame, text="🔄 Sıfırla", width=10,
                  command=self._reset_to_zero).pack(side=tk.LEFT, padx=2, pady=5)
        ttk.Button(btn_frame, text="🔍 EN KISA YOLU BUL", width=18,
                  command=self._solve_and_display).pack(side=tk.LEFT, padx=10, pady=5)
        
        # --- Manuel Ağırlık Girişleri (Yatay) ---
        weights_frame = ttk.LabelFrame(top_panel, text="✏️ Manuel Ağırlık Girişi", padding=5)
        weights_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        
        # İç frame - yatay yerleşim
        inner_frame = ttk.Frame(weights_frame)
        inner_frame.pack(fill=tk.X)
        
        # Kenar ağırlık girişlerini yatay olarak oluştur
        self._create_weight_entries_horizontal(inner_frame)
        
        # --- Sonuç ---
        result_frame = ttk.LabelFrame(top_panel, text="📊 Sonuç", padding=5)
        result_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_label = ttk.Label(
            result_frame,
            text="Çözmek için butona tıklayın...",
            wraplength=250,
            justify=tk.LEFT,
            font=('Helvetica', 10)
        )
        self.result_label.pack()
        
        # ==================== ALT PANEL - HARİTA (TAM GENİŞLİK) ====================
        graph_frame = ttk.Frame(self.root)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Matplotlib figure - tam genişlik
        self.fig, self.ax = plt.subplots(figsize=(16, 9))
        self.fig.patch.set_facecolor('#f5f5dc')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def _create_weight_entries_horizontal(self, parent):
        """
        Kenar ağırlık girişlerini yatay grid olarak oluşturur.
        
        Args:
            parent: Üst widget
        """
        col = 0
        row = 0
        max_cols = 9  # Her satırda maksimum kenar sayısı
        
        for from_node in self.problem.all_nodes:
            neighbors = self.problem.edges.get(from_node, {})
            
            if neighbors:
                for to_node, weight in neighbors.items():
                    # Mini frame her kenar için
                    edge_frame = ttk.Frame(parent)
                    edge_frame.grid(row=row, column=col, padx=3, pady=2)
                    
                    # Etiket
                    ttk.Label(edge_frame, text=f"{from_node}→{to_node}", 
                             font=('Helvetica', 9)).pack(side=tk.LEFT)
                    
                    # Giriş alanı
                    entry = ttk.Entry(edge_frame, width=4, font=('Helvetica', 10))
                    entry.insert(0, str(weight))
                    entry.pack(side=tk.LEFT, padx=2)
                    
                    self.weight_entries[(from_node, to_node)] = entry
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
                    
    def _set_random_weights(self):
        """Rastgele ağırlıklar atar ve giriş alanlarını günceller."""
        self.problem.set_random_weights(1, 10)
        self._update_entries_from_problem()
        self._visualize_graph()
        messagebox.showinfo("Bilgi", "Rastgele ağırlıklar atandı!")
        
    def _reset_to_default(self):
        """Varsayılan ağırlıklara döner ve giriş alanlarını günceller."""
        self.problem.reset_to_default()
        self._update_entries_from_problem()
        self._visualize_graph()
        messagebox.showinfo("Bilgi", "Varsayılan ağırlıklar yüklendi!")
        
    def _reset_to_zero(self):
        """Tüm ağırlıkları sıfırlar."""
        for node in self.problem.edges:
            for neighbor in self.problem.edges[node]:
                self.problem.edges[node][neighbor] = 0
        self._update_entries_from_problem()
        self._visualize_graph()
        messagebox.showinfo("Bilgi", "Tüm ağırlıklar sıfırlandı!")
        
    def _update_entries_from_problem(self):
        """Problem nesnesindeki değerleri giriş alanlarına yansıtır."""
        for (from_node, to_node), entry in self.weight_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, str(self.problem.edges[from_node][to_node]))
            
    def _solve_and_display(self):
        """
        Problemi çözer ve sonuçları gösterir.
        
        Bu fonksiyon:
        1. Giriş alanlarındaki ağırlıkları otomatik uygular
        2. Backward Induction algoritmasını çalıştırır
        3. Sonuçları metin olarak gösterir
        4. Grafı optimal yol vurgulanmış şekilde yeniden çizer
        """
        # Önce giriş alanlarındaki ağırlıkları uygula
        try:
            for (from_node, to_node), entry in self.weight_entries.items():
                weight = int(entry.get())
                if weight < 0:
                    raise ValueError("Negatif ağırlık!")
                self.problem.set_edge_weight(from_node, to_node, weight)
        except ValueError as e:
            messagebox.showerror("Hata", f"Geçersiz ağırlık değeri!\nLütfen pozitif tam sayı girin.\n{e}")
            return
        
        # Algoritmayı çalıştır
        min_cost, optimal_path = self.problem.solve_backward_induction()
        
        # Sonuç metnini oluştur
        result_text = f"🎯 Minimum Maliyet: {min_cost}\n\n"
        result_text += f"📍 Optimal Rota:\n{' → '.join(optimal_path)}\n\n"
        result_text += "📝 Adım Detayları:\n"
        
        path_details = self.problem.get_path_details()
        for i, (from_n, to_n, cost) in enumerate(path_details, 1):
            result_text += f"  {i}. {from_n} → {to_n} (maliyet: {cost})\n"
            
        self.result_label.config(text=result_text)
        
        # Grafı optimal yol ile birlikte çiz
        self._visualize_graph(optimal_path)


# ============================================================================
# BÖLÜM 4: GRAF GÖRSELLEŞTİRME
# ============================================================================

    def _visualize_graph(self, highlight_path=None):
        """
        Graf yapısını görselleştirir.
        
        Args:
            highlight_path: Vurgulanacak yol (optimal yol)
        """
        self.ax.clear()
        
        # Arka plan rengi - eski kağıt görünümü
        self.ax.set_facecolor('#f5f5dc')
        
        # Düğüm konumları - daha geniş yayılım
        positions = {
            'A': (0, 5),
            'B': (5, 9),
            'C': (5, 5),
            'D': (5, 1),
            'E': (10, 9),
            'F': (10, 5),
            'G': (10, 1),
            'H': (15, 7.5),
            'I': (15, 2.5),
            'J': (20, 5)
        }
        
        # Aşama x konumları
        stage_x_positions = {
            'start': 0,      # A
            'stage1': 5,     # B, C, D
            'stage2': 10,    # E, F, G
            'stage3': 15,    # H, I
            'target': 20     # J
        }
        
        # Highlight edilecek kenarları belirle
        highlight_edges = set()
        has_solution = highlight_path is not None and len(highlight_path) > 0
        if has_solution:
            for i in range(len(highlight_path) - 1):
                highlight_edges.add((highlight_path[i], highlight_path[i+1]))
        
        # Önce normal kenarları çiz (çözüm varsa silik, yoksa normal)
        for from_node, neighbors in self.problem.edges.items():
            for to_node, weight in neighbors.items():
                x1, y1 = positions[from_node]
                x2, y2 = positions[to_node]
                
                is_highlighted = (from_node, to_node) in highlight_edges
                
                if not is_highlighted:
                    # Çözüm bulunmuşsa diğer yollar çok silik
                    if has_solution:
                        self._draw_edge(x1, y1, x2, y2, weight, 
                                       color='#c4b8a8', linewidth=1, alpha=0.25, faded=True)
                    else:
                        self._draw_edge(x1, y1, x2, y2, weight, 
                                       color='#8b7355', linewidth=2, alpha=0.6)
        
        # Sonra vurgulu kenarları çiz (üstte olsun)
        for from_node, to_node in highlight_edges:
            weight = self.problem.edges[from_node][to_node]
            x1, y1 = positions[from_node]
            x2, y2 = positions[to_node]
            
            self._draw_edge(x1, y1, x2, y2, weight,
                           color='#c41e3a', linewidth=4, alpha=1.0, highlight=True)
        
        # Düğümleri çiz (çember yok, sadece metin)
        for node, (x, y) in positions.items():
            is_highlighted = highlight_path and node in highlight_path
            is_faded = has_solution and not is_highlighted
            self._draw_node(x, y, node, is_highlighted, is_faded)
        
        # A ve J altına küçük "Start" ve "Target" yazısı
        self.ax.text(positions['A'][0], positions['A'][1] - 1.2, "Start",
                    ha='center', va='top', fontsize=11, style='italic',
                    color='#4a3728', fontfamily='serif')
        self.ax.text(positions['J'][0], positions['J'][1] - 1.2, "Target",
                    ha='center', va='top', fontsize=11, style='italic',
                    color='#4a3728', fontfamily='serif')
        
        # Çözüm bulunduğunda: kesikli çizgiler ve stage etiketleri
        if has_solution:
            # Stage ayırıcı kesikli çizgiler - sadece ortadaki 2 tane
            # Stage1(5) ile Stage2(10) arası: 7.5
            # Stage2(10) ile Stage3(15) arası: 12.5
            stage_dividers = [7.5, 12.5]
            y_bottom = -0.5  # Çerçeve alt sınırı civarı
            y_top = 10       # Çerçeve üst sınırı civarı
            
            for x_div in stage_dividers:
                self.ax.plot([x_div, x_div], [y_bottom, y_top], 
                            color='#b0a090', linestyle='--', 
                            linewidth=1, alpha=0.4, zorder=1)
            
            # Stage etiketleri (altta, her stage'in kendi konumunda)
            stage_label_positions = {
                "Stage 1": 5,     # B, C, D konumu
                "Stage 2": 10,    # E, F, G konumu
                "Stage 3": 15     # H, I konumu
            }
            for label, x_pos in stage_label_positions.items():
                self.ax.text(x_pos, -1.0, label,
                            ha='center', va='top', fontsize=11,
                            color='#6a5a4a', style='italic',
                            fontfamily='serif', alpha=0.6)
        
        # Başlık - çerçeve ÜSTÜNDE
        self.ax.text(10, 11.8, "Stagecoach Problem: Shortest Path (A → J)",
                    ha='center', va='bottom', fontsize=20, fontweight='bold',
                    color='#2b1810', fontfamily='serif')
        
        # Eksen ayarları - daha geniş alan
        self.ax.set_xlim(-2, 22)
        self.ax.set_ylim(-2.5, 13)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        # Dekoratif çerçeve
        self._add_decorative_border()
        
        # Canvas'ı güncelle
        self.fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
        self.canvas.draw()
        
    def _draw_node(self, x, y, label, is_highlighted=False, is_faded=False):
        """
        Bir düğümü çizer - çember olmadan, sadece metin.
        
        Args:
            x, y: Düğüm konumu
            label: Düğüm etiketi
            is_highlighted: Vurgu durumu
            is_faded: Silik durumu (çözüm bulunduğunda optimal yol dışındaki düğümler)
        """
        # Renk seçimi
        if is_highlighted:
            text_color = '#c41e3a'  # Kırmızı (vurgulu)
            font_size = 28
            alpha = 1.0
        elif is_faded:
            text_color = '#a09080'  # Silik gri-kahve
            font_size = 24
            alpha = 0.4
        else:
            text_color = '#2b1810'  # Koyu kahve
            font_size = 26
            alpha = 1.0
        
        # Sadece büyük harf metin - çember yok
        self.ax.text(x, y, label, ha='center', va='center',
                    fontsize=font_size, fontweight='bold', color=text_color,
                    fontfamily='serif', zorder=11, alpha=alpha)
        
    def _draw_edge(self, x1, y1, x2, y2, weight, color='#8b7355', 
                   linewidth=2, alpha=0.7, highlight=False, faded=False):
        """
        Bir kenarı (ok) çizer.
        
        Args:
            x1, y1: Başlangıç noktası
            x2, y2: Bitiş noktası
            weight: Kenar ağırlığı
            color: Kenar rengi
            linewidth: Çizgi kalınlığı
            alpha: Şeffaflık
            highlight: Vurgu durumu
            faded: Silik durumu (optimal yol dışındaki kenarlar)
        """
        # Düğüm metin alanı için offset
        node_offset = 0.5
        
        # Vektör hesapla
        dx = x2 - x1
        dy = y2 - y1
        length = np.sqrt(dx**2 + dy**2)
        
        # Normalize et
        dx_norm = dx / length
        dy_norm = dy / length
        
        # Başlangıç ve bitiş noktalarını ayarla (düğüm merkezinden uzaklaştır)
        start_x = x1 + dx_norm * node_offset
        start_y = y1 + dy_norm * node_offset
        end_x = x2 - dx_norm * node_offset
        end_y = y2 - dy_norm * node_offset
        
        # Ok stilini ayarla
        style = "Simple, head_width=10, head_length=8"
        if highlight:
            style = "Simple, head_width=14, head_length=10"
        
        # Eğrilik oranı
        curve_rad = 0.05
        
        # Ok çiz
        arrow = FancyArrowPatch(
            (start_x, start_y), (end_x, end_y),
            arrowstyle=style,
            color=color,
            linewidth=linewidth,
            alpha=alpha,
            connectionstyle=f"arc3,rad={curve_rad}",
            zorder=5
        )
        self.ax.add_patch(arrow)
        
        # Ağırlık etiketi konumu
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Perpendicular offset - daha büyük mesafe
        perp_x = -dy_norm * 0.9
        perp_y = dx_norm * 0.9
        
        # Renk ve boyut ayarları
        if highlight:
            text_color = '#c41e3a'
            font_size = 15
            text_alpha = 1.0
            bbox_facecolor = '#fff5e6'
            bbox_edgecolor = '#c41e3a'
            bbox_linewidth = 1.5
            bbox_alpha = 0.95
        elif faded:
            text_color = '#b0a090'
            font_size = 11
            text_alpha = 0.4
            bbox_facecolor = '#f5f5dc'
            bbox_edgecolor = '#d0c8b8'
            bbox_linewidth = 0.5
            bbox_alpha = 0.3
        else:
            text_color = '#5a3d2b'
            font_size = 13
            text_alpha = 1.0
            bbox_facecolor = '#fffef0'
            bbox_edgecolor = '#8b7355'
            bbox_linewidth = 1
            bbox_alpha = 0.95
        
        # Ağırlık arka plan kutusu
        bbox_props = dict(
            boxstyle='round,pad=0.2', 
            facecolor=bbox_facecolor,
            edgecolor=bbox_edgecolor,
            linewidth=bbox_linewidth,
            alpha=bbox_alpha
        )
        
        self.ax.text(mid_x + perp_x, mid_y + perp_y, str(weight),
                    ha='center', va='center', fontsize=font_size,
                    color=text_color, fontweight='bold',
                    fontfamily='serif',
                    bbox=bbox_props,
                    zorder=8,
                    alpha=text_alpha)
        
    def _add_decorative_border(self):
        """Dekoratif kenarlık ekler."""
        border = FancyBboxPatch(
            (-1.5, -2), 23, 12.5,
            boxstyle="round,pad=0.05,rounding_size=0.3",
            facecolor='none',
            edgecolor='#8b7355',
            linewidth=3,
            zorder=0
        )
        self.ax.add_patch(border)


# ============================================================================
# BÖLÜM 5: ANA PROGRAM
# ============================================================================

def main():
    """
    Ana program fonksiyonu.
    Tkinter ana döngüsünü başlatır.
    """
    # Stil ayarları
    root = tk.Tk()
    
    # ttk stilini ayarla
    style = ttk.Style()
    style.theme_use('clam')
    
    # Özel stiller
    style.configure('TFrame', background='#f5f5dc')
    style.configure('TLabel', background='#f5f5dc', foreground='#2b1810')
    style.configure('TLabelframe', background='#f5f5dc')
    style.configure('TLabelframe.Label', background='#f5f5dc', foreground='#2b1810', font=('Helvetica', 10, 'bold'))
    style.configure('TButton', font=('Helvetica', 10))
    
    # GUI'yi başlat
    app = StagecoachGUI(root)
    
    # Ana döngü
    root.mainloop()


# Programı çalıştır
if __name__ == "__main__":
    main()

