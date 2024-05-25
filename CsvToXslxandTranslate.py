import pandas as pd
from deep_translator import GoogleTranslator

def csv_to_excel(csv_file_path, excel_file_path, translate=False):
    try:
        # CSV dosyasını oku
        df = pd.read_csv(csv_file_path, engine='python')
        
        if translate:
            # Türkçe'ye çevirme
            translator = GoogleTranslator(source='auto', target='tr')
            for col in df.columns:
                try:
                    # Sütunu çevirmeC:\Users\kadir\OneDrive\Desktop\denemecsvdosyası.csv
                    df[col] = df[col].apply(lambda x: translator.translate(x) if isinstance(x, str) else x)
                except Exception as e:
                    print(f"Hata sütun {col} çevirilirken: {e}")
                    continue
        
        # DataFrame'i XLSX dosyasına yaz
        df.to_excel(excel_file_path, index=False)
        print(f"Başarılı: {csv_file_path} dosyası {excel_file_path} olarak kaydedildi.")
    except FileNotFoundError:
        print(f"Hata: {csv_file_path} dosyası bulunamadı.")
    except pd.errors.EmptyDataError:
        print(f"Hata: {csv_file_path} dosyası boş.")
    except Exception as e:
        print(f"Beklenmedik Hata: {e}")

# Kullanıcıdan dosya yollarını alma
csv_file_path = input("CSV dosyasının yolunu girin: ")
# Türkçeye çevirmek isteyip istemediğini sor
translate_to_turkish = input("Türkçe'ye çevirmek ister misiniz? (Evet/Hayır): ").lower().strip() == 'evet'
# Kullanıcıdan dosya yollarını alma
excel_file_path = input("Kaydedilecek XLSX dosyasının yolunu girin: ")



# Çift tırnakları kaldırın ve dosya yollarını doğru şekilde girin
csv_file_path = csv_file_path.strip('"')
excel_file_path = excel_file_path.strip('"')

# Dosya uzantısını kontrol edin ve gerekirse ekleyin
if not excel_file_path.endswith('.xlsx'):
    excel_file_path += '.xlsx'

csv_to_excel(csv_file_path, excel_file_path, translate_to_turkish)
