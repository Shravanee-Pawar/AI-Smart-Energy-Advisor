from app.core.firebase import db
from app.schemas.energy import EnergyRequest, EnergyResponse


def save_energy(request: EnergyRequest) -> EnergyResponse:
    """
    Save one month's energy usage to Firestore.
    """

    # Create a new document (Firestore generates the ID)
    doc_ref = db.collection("energy_usage").document()

    # Data to store
    data = {
    "uid": request.uid,
    "month": request.month,
    "units": request.units,
    "bill": request.bill,

    "rate": request.rate,
    "family_members": request.family_members,
    "house_type": request.house_type,

    "ac_hours": request.ac_hours,
    "fan_hours": request.fan_hours,
    "tv_hours": request.tv_hours,

    "refrigerator": request.refrigerator,
    "washing_machine": request.washing_machine,
    "cooler": request.cooler,
    "other_appliances": request.other_appliances
}
    # Save data
    doc_ref.set(data)

    # Return response
    return EnergyResponse(
        record_id=doc_ref.id,
        uid=request.uid,
        month=request.month,
        units=request.units,
        bill=request.bill
    )


def get_all_energy():
    """
    Return all energy records.
    """

    docs = db.collection("energy_usage").stream()

    energy_list = []

    for doc in docs:
        data = doc.to_dict()

        energy_list.append(
            EnergyResponse(
                record_id=doc.id,
                uid=data["uid"],
                month=data["month"],
                units=data["units"],
                bill=data["bill"]
            )
        )

    return energy_list


def get_energy_by_user(uid: str):
    """
    Return all energy records for one user.
    """

    docs = (
        db.collection("energy_usage")
        .where("uid", "==", uid)
        .stream()
    )

    energy_list = []

    for doc in docs:
        data = doc.to_dict()

        energy_list.append(
            EnergyResponse(
                record_id=doc.id,
                uid=data["uid"],
                month=data["month"],
                units=data["units"],
                bill=data["bill"]
            )
        )

    return energy_list