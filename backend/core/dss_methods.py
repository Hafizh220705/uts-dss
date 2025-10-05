import numpy as np

def calculate_saw(data, bobot, tipe_kriteria):
    """Menghitung skor dan peringkat SAW."""
    # Pastikan tipe data float untuk perhitungan
    data = data.astype(float)
    
    # 1. Normalisasi Matriks
    norm_data = np.zeros_like(data)
    for j in range(data.shape[1]):
        col = data[:, j]
        if tipe_kriteria[j].lower() == 'benefit':
            norm_data[:, j] = col / np.max(col)
        else:  # cost
            norm_data[:, j] = np.min(col) / col

    # 2. Perangkingan
    scores = np.sum(norm_data * bobot, axis=1)
    rank_indices = np.argsort(scores)[::-1]
    
    return scores, rank_indices


def calculate_wp(data, bobot, tipe_kriteria):
    """Menghitung skor dan peringkat WP."""
    # Pastikan tipe data float untuk perhitungan
    data = data.astype(float)
    
    # 1. Normalisasi Bobot (walaupun di frontend sudah divalidasi, ini best practice)
    normalized_weights = bobot / np.sum(bobot)

    # 2. Hitung Vektor S
    # Buat salinan bobot untuk dimodifikasi
    powered_weights = normalized_weights.copy()
    for i in range(len(tipe_kriteria)):
        if tipe_kriteria[i].lower() == 'cost':
            powered_weights[i] *= -1
            
    s_scores = np.prod(data ** powered_weights, axis=1)

    # 3. Hitung Vektor V (Hasil Akhir)
    scores = s_scores / np.sum(s_scores)
    rank_indices = np.argsort(scores)[::-1]
    
    return scores, rank_indices


def calculate_topsis(data, bobot, tipe_kriteria):
    """Menghitung skor dan peringkat TOPSIS."""
    # Pastikan tipe data float untuk perhitungan
    data = data.astype(float)
    
    # 1. Normalisasi Matriks
    norm_divider = np.sqrt(np.sum(data**2, axis=0))
    norm_data = data / norm_divider

    # 2. Normalisasi Terbobot
    weighted_norm_data = norm_data * bobot

    # 3. Tentukan Solusi Ideal Positif (A+) dan Negatif (A-)
    ideal_positive = np.zeros(data.shape[1])
    ideal_negative = np.zeros(data.shape[1])
    for j in range(data.shape[1]):
        col = weighted_norm_data[:, j]
        if tipe_kriteria[j].lower() == 'benefit':
            ideal_positive[j] = np.max(col)
            ideal_negative[j] = np.min(col)
        else:  # cost
            ideal_positive[j] = np.min(col)
            ideal_negative[j] = np.max(col)

    # 4. Hitung Jarak ke Solusi Ideal
    dist_positive = np.sqrt(np.sum((weighted_norm_data - ideal_positive)**2, axis=1))
    dist_negative = np.sqrt(np.sum((weighted_norm_data - ideal_negative)**2, axis=1))

    # 5. Hitung Nilai Preferensi (Skor Akhir)
    # Tambahkan epsilon kecil untuk menghindari pembagian dengan nol
    scores = dist_negative / (dist_positive + dist_negative + 1e-9)
    rank_indices = np.argsort(scores)[::-1]
    
    return scores, rank_indices


def calculate_ahp_weights(comparison_matrix):
    """Menghitung bobot kriteria dan Consistency Ratio (CR) dari matriks perbandingan AHP."""
    matrix = np.array(comparison_matrix, dtype=float)
    n = matrix.shape[0]

    # Indeks Konsistensi Random (RI) dari Saaty
    RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    
    # Normalisasi matriks dan hitung bobot (eigenvector)
    col_sums = np.sum(matrix, axis=0)
    norm_matrix = matrix / col_sums
    bobot = np.mean(norm_matrix, axis=1)
    
    # Hitung Rasio Konsistensi (CR)
    if n <= 2:
        return bobot, 0.0 # Selalu konsisten jika n <= 2
        
    lambda_max = np.mean(np.dot(matrix, bobot) / bobot)
    CI = (lambda_max - n) / (n - 1)
    # Gunakan RI yang sesuai, atau default ke 1.49 jika n > 10
    CR = CI / RI.get(n, 1.49)

    return bobot, CR