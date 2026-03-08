import sqlite3

conn = sqlite3.connect('contractorpro.db')
cursor = conn.cursor()
cursor.execute('SELECT id, name, tier, tier_label FROM trade_category ORDER BY tier, order_index LIMIT 8')

print('\nTrade categories with tiers:')
for row in cursor.fetchall():
    print(f'  [Tier {row[2]}] {row[1]:25} - {row[3]}')

conn.close()
