from app.models import AscendantSign, AscendantTrait

def generate_ascendant_traits(ascendant_sign_name):
    # Query the AscendantSign record
    asc_sign = AscendantSign.query.filter_by(name=ascendant_sign_name).first()
    if not asc_sign:
        return None

    # Query related traits grouped by trait_type
    traits_query = AscendantTrait.query.filter_by(ascendant_sign_id=asc_sign.id).all()

    # Organize traits by type
    traits_by_type = {
        "health": [],
        "personality": [],
        "appearance": []
    }

    for trait in traits_query:
        # Assuming trait_type in DB is stored as 'health', 'personality', or 'appearance'
        if trait.trait_type in traits_by_type:
            traits_by_type[trait.trait_type].append(trait.description)

    # Construct the descriptive texts
    health_text = (
        f"As a {ascendant_sign_name} Ascendant, your health is influenced by the {asc_sign.element} element "
        f"and ruled by {asc_sign.ruling_planet}. Common concerns include " +
        ", ".join(traits_by_type["health"]) + "."
    )

    personality_text = (
        f"{ascendant_sign_name} Ascendants tend to be " +
        ", ".join(traits_by_type["personality"]) + "."
    )

    appearance_text = (
        f"Physically, {ascendant_sign_name} Ascendants often have " +
        ", ".join(traits_by_type["appearance"]) + "."
    )

    return {
        "health": health_text,
        "temperament_personality": personality_text,
        "physical_appearance": appearance_text
    }
