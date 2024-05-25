
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Kullanıcıdan dosya yolunu al
file_path = input("Lütfen Excel dosyasının tam yolunu girin: ")

# Excel dosyasını yükleyin
try:
    df = pd.read_excel(file_path, header=None)
except FileNotFoundError:
    print(f"Dosya bulunamadı: {file_path}")
    exit(1)

# Veriyi sepet formatına dönüştürün
transactions = df.apply(lambda row: row.dropna().tolist(), axis=1).tolist()

# Veriyi one-hot encoded formata dönüştürün
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df_trans = pd.DataFrame(te_ary, columns=te.columns_)

# Sık görülen öğe setlerini bulun
frequent_itemsets = apriori(df_trans, min_support=0.01, use_colnames=True)

# İlişkisel kuralları bulun
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Sonuçları görüntüleyin
print("Sık Görülen Öğe Setleri:")
print(frequent_itemsets)
print("\nİlişkisel Kurallar:")
print(rules)

# Daha detaylı analiz
def detailed_analysis(rules):
    print("\nTop 5 rules by support:")
    print(rules.nlargest(5, 'support')[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

    print("\nTop 5 rules by confidence:")
    print(rules.nlargest(5, 'confidence')[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

    print("\nTop 5 rules by lift:")
    print(rules.nlargest(5, 'lift')[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    
    print("\nRules with confidence > 0.8:")
    high_confidence_rules = rules[rules['confidence'] > 0.8]
    print(high_confidence_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    
    print("\nRules with lift > 2:")
    high_lift_rules = rules[rules['lift'] > 2]
    print(high_lift_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
    
    return high_confidence_rules, high_lift_rules

# Detaylı analiz
high_confidence_rules, high_lift_rules = detailed_analysis(rules)

# Kuralları ve sık görülen öğe setlerini Excel dosyasına kaydet
output_file_path = 'association_rules_and_frequent_itemsets.xlsx'

with pd.ExcelWriter(output_file_path) as writer:
    frequent_itemsets.to_excel(writer, sheet_name='Frequent Itemsets', index=False)
    rules.to_excel(writer, sheet_name='Association Rules', index=False)

print(f"\nKurallar ve sık görülen öğe setleri '{output_file_path}' dosyasına kaydedildi.")
