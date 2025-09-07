#!/usr/bin/env python3
"""
Database verification script to check if tracking events are being persisted correctly.
"""

import sqlite3
import json
from datetime import datetime


def check_database():
    """Check the database for tracking events"""
    try:
        # Connect to the database
        conn = sqlite3.connect("tracking_service.db")
        cursor = conn.cursor()

        # Get table info
        cursor.execute("PRAGMA table_info(tracking_events);")
        columns = cursor.fetchall()
        print("📋 Database schema:")
        for col in columns:
            print(f"   {col[1]} ({col[2]})")

        # Get count of records
        cursor.execute("SELECT COUNT(*) FROM tracking_events;")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total tracking events: {count}")

        if count > 0:
            # Get last 5 records
            cursor.execute(
                """
                SELECT tracking_event_id, partner_id, campaign_id, visitor_id, 
                       interaction_type, source_url, destination_url, recorded_at, created_at
                FROM tracking_events 
                ORDER BY created_at DESC 
                LIMIT 5
            """
            )

            records = cursor.fetchall()
            print("\n🔍 Last 5 tracking events:")
            print("-" * 100)

            for record in records:
                print(f"ID: {record[0]}")
                print(
                    f"Partner: {record[1]} | Campaign: {record[2]} | Visitor: {record[3]}"
                )
                print(f"Type: {record[4]} | Created: {record[8]}")
                print(f"Source: {record[5]}")
                print(f"Destination: {record[6]}")
                print("-" * 100)
        else:
            print("\n💡 No tracking events found. Try sending a POST request to:")
            print("   http://localhost:8000/api/v1/tracking/events")
            print("\n   Example payload:")
            example = {
                "partner_id": "google-ads",
                "campaign_id": "summer-sale-2025",
                "visitor_id": "user123",
                "interaction_type": "click",
                "source_url": "https://google.com/ad",
                "destination_url": "https://mystore.com/products",
            }
            print(json.dumps(example, indent=2))

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🔍 Checking tracking service database...\n")
    check_database()
