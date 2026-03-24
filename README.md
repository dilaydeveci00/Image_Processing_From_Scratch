# 🩺 Ultrason Görüntü İşleme Projesi

Bu projede, ultrason görüntüleri üzerinde temel görüntü işleme algoritmaları Python kullanılarak **manuel (from scratch)** şekilde gerçekleştirilmiştir. Amaç, hazır kütüphaneler yerine algoritmaların mantığını doğrudan kodlayarak daha derin bir anlayış kazanmaktır.


## 🎯 Proje Amacı

Ultrason görüntülerinde:

- Gürültüyü azaltmak  
- Kontrastı artırmak  
- Kenarları belirgin hale getirmek  

ve bu işlemlerin görüntü üzerindeki etkilerini analiz etmek.


## ⚙️ Uygulanan Yöntemler

🔹 1. Ön İşleme
- RGB → Grayscale dönüşümü  
- Görüntü boyutlandırma (256x256)  
- Median filtre ile gürültü azaltma  

🔹 2. Kontrast Artırma
- Histogram eşitleme  
- CLAHE (Adaptive Histogram Equalization)  
- Gamma düzeltme  

🔹 3. Kenar Tespiti
- Sobel operatörü  
- Scharr operatörü  
- Basitleştirilmiş Canny algoritması  

---

## 🧠 Kullanılan Teknolojiler

- Python  
- NumPy  
- Matplotlib  
- Pillow (PIL)  

## 📊 Program Çıktısı

Her bir ultrason görüntüsü için:

- Orijinal görüntü  
- Ön işleme sonuçları  
- Histogram analizleri  
- Kontrast artırma çıktıları  
- Kenar tespiti sonuçları  

tek bir görsel panel üzerinde gösterilmektedir.





