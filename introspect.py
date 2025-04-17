import psycopg2
import json
import yaml
from graphviz import Digraph

# Database credentials
conn = psycopg2.connect(
    database="test_db",
    user="postgres",
    password="yourpass",  # Change this!
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Extract schema structure
cur.execute("""
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public';
""")
columns = cur.fetchall()

schema = {}
for table, col, dtype in columns:
    schema.setdefault(table, []).append({col: dtype})

# Export JSON
with open("example_output.json", "w") as f_json:
    json.dump(schema, f_json, indent=2)
print("✅ Saved: example_output.json")

# Export YAML
with open("example_output.yaml", "w") as f_yaml:
    yaml.dump(schema, f_yaml, sort_keys=False)
print("✅ Saved: example_output.yaml")

# Anomaly Detection
print("\n🚨 Tables with No Primary Keys:")
cur.execute("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE'
AND table_name NOT IN (
    SELECT table_name
    FROM information_schema.table_constraints
    WHERE constraint_type = 'PRIMARY KEY'
    AND table_schema = 'public'
);
""")
no_pk_tables = cur.fetchall()
if no_pk_tables:
    for (table,) in no_pk_tables:
        print(f"  - {table}")
else:
    print("  ✅ All tables have primary keys.")

# Foreign Key Relationships
print("\n🔗 Foreign Key Relationships:")
cur.execute("""
SELECT
    tc.table_name AS source_table,
    kcu.column_name AS source_column,
    ccu.table_name AS target_table,
    ccu.column_name AS target_column
FROM 
    information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
WHERE 
    constraint_type = 'FOREIGN KEY';
""")
fk_relationships = cur.fetchall()
if fk_relationships:
    for row in fk_relationships:
        print(f"  {row[0]}.{row[1]} → {row[2]}.{row[3]}")
else:
    print("  ℹ️ No foreign key relationships found.")

# ER Diagram using Graphviz
print("\n📈 Generating schema diagram...")
dot = Digraph(comment="PostgreSQL Schema ERD", format="png")
for table in schema:
    dot.node(table)

for source_table, source_col, target_table, target_col in fk_relationships:
    dot.edge(source_table, target_table, label=f"{source_col} → {target_col}")

dot.render("schema_diagram", cleanup=True)
print("✅ Saved: schema_diagram.png")

cur.close()
conn.close()
print("\n🏁 Introspection complete.")
