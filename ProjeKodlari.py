import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# --- 3.1 GÖRÜNTÜ ÖN İŞLEME FONKSİYONLARI ---
def manuel_gri_yap(resim_matrisi):
    # Standart parlaklık formülü ile gri dönüşüm
    return np.uint8(0.299*resim_matrisi[:,:,0] + 0.587*resim_matrisi[:,:,1] + 0.114*resim_matrisi[:,:,2])

def manuel_boyutlandir(resim, hedef=256):
    # 256x256 boyutlandırma
    h, w = resim.shape
    yeni = np.zeros((hedef, hedef), dtype=np.uint8)
    for i in range(hedef):
        for j in range(hedef):
            yeni[i, j] = resim[int(i * h / hedef), int(j * w / hedef)]
    return yeni

def manuel_median_filtre(resim):
    # Gürültü azaltma için 3x3 Median filtre
    h, w = resim.shape
    cikti = np.zeros_like(resim)
    for i in range(1, h-1):
        for j in range(1, w-1):
            cikti[i, j] = np.median(resim[i-1:i+2, j-1:j+2])
    return cikti

# --- 3.2 KONTRAST ARTIRMA TEKNİKLERİ ---
def manuel_histogram_esitleme(resim):
    hist, bins = np.histogram(resim.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    return cdf_normalized[resim].astype('uint8')

def manuel_clahe_basit(resim):
    # Yerel kontrast artırma (CLAHE)
    h, w = resim.shape
    r, c = 8, 8 # 8x8 bloklar
    cikti = np.zeros_like(resim)
    for i in range(r):
        for j in range(c):
            blok = resim[i*(h//r):(i+1)*(h//r), j*(w//c):(j+1)*(w//c)]
            cikti[i*(h//r):(i+1)*(h//r), j*(w//c):(j+1)*(w//c)] = manuel_histogram_esitleme(blok)
    return cikti

def manuel_gamma_duzeltme(resim, gamma=0.6):
    return np.uint8(255 * (resim / 255) ** gamma)

# --- 3.4 KENAR TESPİT YÖNTEMLERİ ---
def evrisim(resim, K):
    h, w = resim.shape
    cikti = np.zeros_like(resim, dtype=float)
    for i in range(1, h-1):
        for j in range(1, w-1):
            cikti[i, j] = np.sum(resim[i-1:i+2, j-1:j+2] * K)
    return cikti

def manuel_sobel(resim):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    return np.uint8(np.clip(np.sqrt(evrisim(resim, Kx)**2 + evrisim(resim, Ky)**2), 0, 255))

def manuel_scharr(resim):
    Kx = np.array([[-3, 0, 3], [-10, 0, 10], [-3, 0, 3]])
    Ky = np.array([[-3, -10, -3], [0, 0, 0], [3, 10, 3]])
    return np.uint8(np.clip(np.sqrt(evrisim(resim, Kx)**2 + evrisim(resim, Ky)**2), 0, 255))

def manuel_canny_basit(resim):
    s = manuel_sobel(resim)
    return np.where(s > 100, 255, 0).astype('uint8')

# --- ANA DÖNGÜ VE ÇIKTI PANELİ ---

dosyalar = [f for f in os.listdir("images") if f.lower().endswith(('.jpg', '.png'))]

for dosya in dosyalar:
    img = np.array(Image.open(os.path.join("images", dosya)).convert('RGB'))
    print("Bulunan dosyalar:", dosyalar)
    # Adım 3.1
    temiz = manuel_median_filtre(manuel_boyutlandir(manuel_gri_yap(img)))
    
    # Adım 3.2
    he = manuel_histogram_esitleme(temiz)
    clahe = manuel_clahe_basit(temiz)
    gamma = manuel_gamma_duzeltme(temiz)
    
    # Adım 3.4
    sobel = manuel_sobel(he)
    scharr = manuel_scharr(he)
    canny = manuel_canny_basit(he)

    # GÖRSEL ÇIKTI PANELİ (SADECE BELGE İSTERLERİ)
    plt.figure(figsize=(20, 12))
    plt.suptitle(f"PROJE ANALİZİ: {dosya}", fontsize=18, fontweight='bold')

    # --- 1. Satır: Ön İşleme ve Histogram (3.1 & 3.3) ---
    plt.subplot(3, 4, 1); plt.title("1. Orijinal"); plt.imshow(img)
    plt.subplot(3, 4, 2); plt.title("2. Gri Seviye (3.1)"); plt.imshow(manuel_gri_yap(img), cmap='gray')
    plt.subplot(3, 4, 3); plt.title("3. Median Filtre (3.1)"); plt.imshow(temiz, cmap='gray')
    plt.subplot(3, 4, 4); plt.title("4. Gamma Correction (3.2-3)"); plt.imshow(gamma, cmap='gray')

    # --- 2. Satır: Kontrast ve Histogram Analizi (3.2 & 3.3) ---
    plt.subplot(3, 4, 5); plt.title("Önce Histogram (3.3)"); plt.hist(temiz.ravel(), 256, color='black')
    plt.subplot(3, 4, 6); plt.title("Sonra Histogram (3.3)"); plt.hist(he.ravel(), 256, color='blue')
    plt.subplot(3, 4, 7); plt.title("5. Hist. Eq. (3.2-1)"); plt.imshow(he, cmap='gray')
    plt.subplot(3, 4, 8); plt.title("6. CLAHE (3.2-2)"); plt.imshow(clahe, cmap='gray')

    # --- 3. Satır: Kenar Tespit Yöntemleri (3.4) ---
    plt.subplot(3, 4, 9); plt.title("7. Sobel (3.4)"); plt.imshow(sobel, cmap='gray')
    plt.subplot(3, 4, 10); plt.title("8. Scharr (3.4)"); plt.imshow(scharr, cmap='gray')
    plt.subplot(3, 4, 11); plt.title("9. Canny (3.4)"); plt.imshow(canny, cmap='gray')
    plt.subplot(3, 4, 12); plt.title("10. Kombine Analiz (3.5)"); plt.imshow(canny, cmap='magma')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

