from app.core.firebase import db


def get_dashboard_data():
    docs = db.collection("energy_usage").stream()

    records = [doc.to_dict() for doc in docs]

    # Handle empty database
    if not records:
        return {
            "total_records": 0,
            "total_units": 0.0,
            "average_daily": 0.0,
            "estimated_bill": 0.0,
            "latest_consumption": 0.0,
        }

    total_records = len(records)

    # Sum all units
    total_units = sum(record.get("units", 0) for record in records)

    # Average units per record
    average_daily = total_units / total_records

    # Temporary bill estimation
    estimated_bill = total_units * 8

    # Latest record
    latest_consumption = records[-1].get("units", 0)

    return {
        "total_records": total_records,
        "total_units": round(total_units, 2),
        "average_daily": round(average_daily, 2),
        "estimated_bill": round(estimated_bill, 2),
        "latest_consumption": latest_consumption,
    }

def get_chart_data():
    docs = db.collection("energy_usage").stream()

    chart_data = []

    for doc in docs:
        record = doc.to_dict()

        chart_data.append({
            "month": record.get("month", ""),
            "units": record.get("units", 0)
        })

    return chart_data