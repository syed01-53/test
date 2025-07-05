import pymysql

# ✅ MySQL credentials
DB_HOST = "168.231.115.182"
DB_PORT = 3306
DB_USER = "sas_user"
DB_PASSWORD = "SecurePass123!"
DB_NAME = "sas"

# ✅ Tables to inspect
target_tables = {
    "orders": "Sales",
    "stock_history": "Stock",
    "payments": "Payments",
    "supplier": "Supplier"
}

try:
    # Connect to MySQL
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Connected to MySQL\n")

    with connection.cursor() as cursor:
        for table, label in target_tables.items():
            print(f"🔹 {label.upper()} TABLE: `{table}`")

            # Get column names
            try:
                cursor.execute(f"DESCRIBE `{table}`;")
                columns = [row["Field"] for row in cursor.fetchall()]
                print(f"   📑 Columns ({len(columns)}): {', '.join(columns)}")
            except Exception as e:
                print(f"   ❌ Failed to get columns: {e}")
                continue

            # Get row count
            try:
                cursor.execute(f"SELECT COUNT(*) AS count FROM `{table}`;")
                count = cursor.fetchone()["count"]
                print(f"   📊 Rows: {count}")
            except Exception as e:
                print(f"   ❌ Failed to count rows: {e}")

            # Sample rows
            try:
                cursor.execute(f"SELECT * FROM `{table}` LIMIT 3;")
                rows = cursor.fetchall()
                if rows:
                    print("   🔍 Sample rows:")
                    for row in rows:
                        print("     -", row)
                else:
                    print("   ⚠️ Table is empty.")
            except Exception as e:
                print(f"   ❌ Failed to fetch rows: {e}")

            print()  # separator

except Exception as e:
    print("❌ Connection error:", e)

finally:
    if 'connection' in locals() and connection.open:
        connection.close()
        print("🔌 Connection closed")
