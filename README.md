# 🚌 Stagecoach Problemi - Dinamik Programlama Çözücü

Bu proje, **Stagecoach Problemi**ni (En Kısa Yol Problemi) **Dinamik Programlama** algoritması kullanarak çözen interaktif bir Python uygulamasıdır.

## 📋 İçindekiler

- [Problem Tanımı](#problem-tanımı)
- [Algoritma](#algoritma)
- [Özellikler](#özellikler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Kod Yapısı](#kod-yapısı)
- [Teknik Detaylar](#teknik-detaylar)

---

## 🎯 Problem Tanımı

**Stagecoach Problemi**, bir posta arabasının (veya modern bir aracın) **A noktasından J noktasına**, farklı duraklardan (stage) geçerek **en düşük maliyetle** (zaman, para veya enerji) ulaşmasını sağlayan optimal rotayı bulma problemidir.

### Yapı

- **5 Aşama (Stage):**
  - **Start:** A
  - **Stage 1:** B, C, D
  - **Stage 2:** E, F, G
  - **Stage 3:** H, I
  - **Target:** J

- **Toplam 10 düğüm** ve **18 kenar** (yönlü bağlantı)
- Her kenarın bir **ağırlığı** (maliyeti) vardır
- Graf **DAG** (Directed Acyclic Graph - Yönlü Asiklik Graf) yapısındadır

---

## 🧮 Algoritma

### Dinamik Programlama - Geriye Doğru Tümevarım (Backward Induction)

Bu algoritma, **Bellman Optimizasyon İlkesi**'ni kullanır:
> "Optimal bir politikanın herhangi bir alt politikası da optimaldir."

### Çalışma Prensibi

1. **Hedef düğümden (J) başla** - J'den J'ye gitmenin maliyeti 0
2. **Geriye doğru ilerle** (J → A)
3. Her düğüm için **Bellman Denklemi**'ni uygula:
   ```
   f(mevcut) = min { Geçiş Maliyeti + f(Gelecekteki Düğüm) }
   ```
4. En düşük maliyetli komşuyu seç ve kaydet (memoization)
5. Optimal yolu **yeniden inşa et** (Path Reconstruction)

### Zaman Karmaşıklığı

**O(V + E)** 
- V: Düğüm sayısı (10)
- E: Kenar sayısı (18)

Her düğüm ve kenar sadece bir kez işlendiği için lineer zaman karmaşıklığına sahiptir.

---

## ✨ Özellikler

### 🎨 Grafiksel Kullanıcı Arayüzü (GUI)

- **Modern ve kullanıcı dostu** Tkinter tabanlı arayüz
- **Canlı graf görselleştirme** (Matplotlib)
- **Optimal yol vurgulama** - En kısa yol kırmızı renkte gösterilir
- **Silikleştirme** - Çözüm bulunduğunda diğer yollar soluklaşır

### ⚙️ Ağırlık Yönetimi

- **🎲 Rastgele Ağırlıklar:** Tüm kenar ağırlıklarını rastgele değerlerle doldurur
- **📋 Varsayılan Ağırlıklar:** Problemin orijinal ağırlıklarına döner
- **🔄 Sıfırla:** Tüm ağırlıkları 0 yapar
- **✏️ Manuel Giriş:** Her kenar için ağırlık değeri girilebilir

### 📊 Sonuç Gösterimi

- **Minimum Maliyet:** Toplam en düşük maliyet
- **Optimal Rota:** A'dan J'ye en kısa yol
- **Adım Detayları:** Her adımın maliyeti ile birlikte gösterilir

### 🗺️ Görselleştirme Özellikleri

- **Stage ayırıcı çizgiler:** Çözüm sonrası stage'ler arası kesikli çizgiler
- **Stage etiketleri:** Her stage'in konumu altta belirtilir
- **Start/Target etiketleri:** A ve J düğümlerinin altında küçük etiketler
- **Geniş harita:** Tam ekran genişliğinde graf görüntüleme

---

## 📦 Kurulum

### Gereksinimler

- Python 3.7 veya üzeri
- Gerekli kütüphaneler:
  - `tkinter` (genellikle Python ile birlikte gelir)
  - `matplotlib`
  - `numpy`

### Kurulum Adımları

1. **Projeyi klonlayın veya indirin:**
   ```bash
   git clone <repository-url>
   cd "bilgi islem"
   ```

2. **Gerekli kütüphaneleri yükleyin:**
   ```bash
   pip install matplotlib numpy
   ```

3. **Programı çalıştırın:**
   ```bash
   python3 stagecoach_solver.py
   ```

---

## 🚀 Kullanım

### Temel Kullanım

1. **Programı başlatın** - GUI otomatik olarak açılır
2. **Ağırlıkları ayarlayın:**
   - Rastgele ağırlıklar için "🎲 Rastgele" butonuna tıklayın
   - Varsayılan ağırlıklar için "📋 Varsayılan" butonuna tıklayın
   - Manuel giriş için üstteki input alanlarını kullanın
3. **"🔍 EN KISA YOLU BUL"** butonuna tıklayın
4. **Sonuçları görüntüleyin:**
   - Sağ üstte minimum maliyet ve optimal rota
   - Haritada kırmızı renkte vurgulanmış optimal yol

### Manuel Ağırlık Girişi

Üst paneldeki "Manuel Ağırlık Girişi" bölümünden her kenar için ağırlık değeri girebilirsiniz:
- Format: `A→B: [değer]`
- Sadece pozitif tam sayılar kabul edilir
- Değerleri değiştirdikten sonra "EN KISA YOLU BUL" butonuna tıklayın

---

## 🏗️ Kod Yapısı

### Ana Bileşenler

#### 1. `StagecoachProblem` Sınıfı

Graf yapısını ve dinamik programlama algoritmasını içerir.

**Önemli Metodlar:**
- `__init__()`: Graf yapısını başlatır
- `solve_backward_induction()`: Ana algoritma - geriye doğru tümevarım
- `_reconstruct_path()`: Optimal yolu yeniden inşa eder
- `set_random_weights()`: Rastgele ağırlıklar atar
- `reset_to_default()`: Varsayılan ağırlıklara döner

**Veri Yapıları:**
- `edges`: Mevcut kenar ağırlıkları (dict)
- `cost_to_go`: Her düğümden hedefe minimum maliyet (DP tablosu)
- `next_node`: Optimal yolda bir sonraki düğüm

#### 2. `StagecoachGUI` Sınıfı

Grafiksel kullanıcı arayüzünü yönetir.

**Önemli Metodlar:**
- `__init__()`: GUI bileşenlerini başlatır
- `_create_widgets()`: Tüm GUI elemanlarını oluşturur
- `_visualize_graph()`: Grafı görselleştirir
- `_solve_and_display()`: Problemi çözer ve sonuçları gösterir
- `_draw_node()`: Düğümleri çizer
- `_draw_edge()`: Kenarları (oklar) çizer

**Layout:**
- **Üst Panel:** Butonlar, manuel giriş alanları, sonuç paneli
- **Alt Panel:** Tam genişlikte graf görselleştirme

### Kod Organizasyonu

```
stagecoach_solver.py
├── BÖLÜM 1: Veri Yapıları ve Graf Tanımı
│   └── StagecoachProblem sınıfı
├── BÖLÜM 2: Dinamik Programlama Algoritması
│   └── Backward Induction implementasyonu
├── BÖLÜM 3: Grafik Kullanıcı Arayüzü
│   └── StagecoachGUI sınıfı
├── BÖLÜM 4: Graf Görselleştirme
│   └── Matplotlib ile çizim fonksiyonları
└── BÖLÜM 5: Ana Program
    └── main() fonksiyonu
```

---

## 🔧 Teknik Detaylar

### Algoritma Detayları

#### Backward Induction Adımları

```python
1. cost_to_go['J'] = 0  # Hedef düğüm maliyeti 0

2. Düğümleri geriye doğru sırala: ['J', 'I', 'H', ..., 'A']

3. Her düğüm için (J hariç):
   - Tüm komşuları kontrol et
   - Her komşu için: transition_cost + cost_to_go[komşu]
   - En küçük değeri seç
   - cost_to_go[mevcut] = min_değer
   - next_node[mevcut] = optimal_komşu

4. Path Reconstruction:
   - A'dan başla
   - next_node['A'] → next_node[next_node['A']] → ... → J
```

### Görselleştirme Detayları

#### Düğüm Çizimi
- Çember yok, sadece büyük harf metin
- Optimal yol dışındaki düğümler soluklaştırılır (alpha=0.4)
- Vurgulu düğümler kırmızı renkte

#### Kenar Çizimi
- Matplotlib `FancyArrowPatch` kullanılır
- Optimal yol: Kırmızı, kalın (linewidth=4)
- Diğer yollar: Gri, ince, soluk (alpha=0.25)
- Ağırlık etiketleri: Arka plan kutusu ile

#### Stage Ayırıcılar
- Çözüm bulunduğunda kesikli dikey çizgiler
- Stage 1-2 ve Stage 2-3 arasında
- Silik renk (alpha=0.4)

### Performans

- **Zaman Karmaşıklığı:** O(V + E) = O(10 + 18) = O(28) ≈ O(1)
- **Uzay Karmaşıklığı:** O(V) = O(10)
- **Memoization:** Her düğümün maliyeti sadece bir kez hesaplanır

---

## 📝 Örnek Kullanım Senaryosu

### Senaryo 1: Varsayılan Ağırlıklar

1. Programı başlatın
2. "📋 Varsayılan" butonuna tıklayın
3. "🔍 EN KISA YOLU BUL" butonuna tıklayın
4. **Sonuç:** Minimum maliyet ve optimal rota gösterilir

### Senaryo 2: Rastgele Ağırlıklar

1. "🎲 Rastgele" butonuna tıklayın
2. "🔍 EN KISA YOLU BUL" butonuna tıklayın
3. Farklı ağırlıklar için farklı optimal yollar görebilirsiniz

### Senaryo 3: Manuel Giriş

1. Üst paneldeki input alanlarına istediğiniz ağırlıkları girin
2. "🔍 EN KISA YOLU BUL" butonuna tıklayın
3. Özel senaryolarınızı test edin

---

## 🎓 Eğitimsel Değer

Bu proje şunları öğretir:

1. **Dinamik Programlama:** Bellman denklemi ve memoization
2. **Graf Algoritmaları:** En kısa yol problemleri
3. **Geriye Doğru Tümevarım:** Optimizasyon problemlerinde yaygın teknik
4. **GUI Geliştirme:** Tkinter ve Matplotlib entegrasyonu
5. **Görselleştirme:** Algoritma sonuçlarının görsel sunumu

---

## 🐛 Bilinen Sorunlar ve Sınırlamalar

- Sadece pozitif tam sayı ağırlıklar desteklenir
- Graf yapısı sabittir (10 düğüm, 5 stage)
- Negatif ağırlıklar veya döngüler desteklenmez

---

## 📄 Lisans

Bu proje eğitim amaçlıdır ve açık kaynak kodludur.

---

## 👤 Yazar

Dinamik Programlama Projesi

---

## 🙏 Teşekkürler

- **Bellman** - Dinamik Programlama teorisi
- **Python Topluluğu** - Tkinter ve Matplotlib kütüphaneleri

---

## 📚 Referanslar

- Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.
- Cormen, T. H., et al. (2009). *Introduction to Algorithms*. MIT Press.

---

**Not:** Bu proje, dinamik programlama algoritmalarının öğretilmesi ve görselleştirilmesi amacıyla geliştirilmiştir.

