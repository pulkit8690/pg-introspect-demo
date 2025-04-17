# PostgreSQL Schema Introspection Tool 🧠

This Python tool introspects a PostgreSQL database and generates:
- ✅ JSON + YAML exports of the schema
- 🔗 Foreign key relationships
- ⚠️ Primary key anomaly detection
- 📈 Graphviz-based ER diagrams

---

## 🚀 Features

| Feature                | Status |
|------------------------|--------|
| Schema → JSON          | ✅     |
| Schema → YAML          | ✅     |
| Detect missing PKs     | ✅     |
| Detect FK relationships| ✅     |
| ER Diagram (PNG)       | ✅     |

---

## 📁 Sample Output

```json
{
  "users": [
    { "id": "integer" },
    { "name": "text" }
  ]
}
