import mysql.connector
from mysql.connector import Error

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='185.190.39.252',
        user='backend',
        password='ya mahdi',
        db='BackEndFiling',
        port=3306,
    )
    cursor = conn.cursor()
    # Insert in batches, skipping duplicates
    query = f"""
    INSERT IGNORE INTO Posts_Copy (
        status, is_active, status_type, token, number, city, city_text, 
        mahal, mahal_text, type, type_text, title, price, price_two, 
        meter, desck, map, Images, details, address, malk_name, 
        is_complete, Otagh, Make_years, PARKING, ELEVATOR, CABINET, 
        BALCONY, floor, dwelling_units_per_floor, dwelling_unit_floor, 
        wc, floor_type, water_provider, cool, heat, building_directions, 
        date_created_persian, date_created
    )
    SELECT 
        status, is_active, status_type, token, number, city, city_text, 
        mahal, mahal_text, type, type_text, title, price, price_two, 
        meter, desck, map, Images, details, address, malk_name, 
        is_complete, Otagh, Make_years, PARKING, ELEVATOR, CABINET, 
        BALCONY, floor, dwelling_units_per_floor, dwelling_unit_floor, 
        wc, floor_type, water_provider, cool, heat, building_directions, 
        date_created_persian, date_created
    FROM Posts 
    ORDER BY date_created
    LIMIT 1000;
    """

    cursor.execute(query)
    conn.commit()


except Error as e:
    print(f"Database error: {e}")  # Handle connection/query errors [[4]]
finally:
    cursor.close()
    conn.close()