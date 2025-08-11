# app/utils/ascendant_traits.py

ascendant_base_traits = {
    "Aries": {
        "element": "Fire",
        "ruling_planet": "Mars",
        "health_points": [
            "Headaches and sinus problems",
            "Risk of injuries to head or face",
            "Stress-related issues and blood pressure fluctuations"
        ],
        "personality_points": [
            "Energetic, assertive, and pioneering",
            "Sometimes impatient or impulsive",
            "Courageous in facing challenges and natural leaders"
        ],
        "appearance_points": [
            "Strong facial features, sharp jawline",
            "Athletic build with confident posture"
        ]
    },
    "Taurus": {
        "element": "Earth",
        "ruling_planet": "Venus",
        "health_points": [
            "Throat and neck issues",
            "Prone to weight gain",
            "Thyroid and vocal cord problems"
        ],
        "personality_points": [
            "Calm, stable, and determined",
            "Loyal and persistent",
            "Sometimes stubborn and resistant to change"
        ],
        "appearance_points": [
            "Broad shoulders and sturdy build",
            "Pleasing facial features with attractive eyes"
        ]
    },
    "Gemini": {
        "element": "Air",
        "ruling_planet": "Mercury",
        "health_points": [
            "Respiratory issues like asthma or bronchitis",
            "Nervous system imbalances",
            "Shoulder and arm strain"
        ],
        "personality_points": [
            "Adaptable, witty, and curious",
            "Excellent communication skills",
            "Sometimes restless and inconsistent"
        ],
        "appearance_points": [
            "Slender build with expressive face",
            "Quick, lively movements"
        ]
    },
    "Cancer": {
        "element": "Water",
        "ruling_planet": "Moon",
        "health_points": [
            "Digestive problems and acidity",
            "Water retention issues",
            "Emotional stress affecting health"
        ],
        "personality_points": [
            "Nurturing, sensitive, and intuitive",
            "Protective of loved ones",
            "Sometimes moody or overly emotional"
        ],
        "appearance_points": [
            "Round face and soft features",
            "Expressive eyes, often with a caring look"
        ]
    },
    "Leo": {
        "element": "Fire",
        "ruling_planet": "Sun",
        "health_points": [
            "Heart and spine problems",
            "High blood pressure",
            "Overexertion-related fatigue"
        ],
        "personality_points": [
            "Confident, generous, and charismatic",
            "Natural leaders with a dramatic flair",
            "Sometimes prideful or self-centered"
        ],
        "appearance_points": [
            "Broad chest and strong posture",
            "Radiant smile and commanding presence"
        ]
    },
    "Virgo": {
        "element": "Earth",
        "ruling_planet": "Mercury",
        "health_points": [
            "Issues with intestines and digestion",
            "Prone to anxiety-related disorders",
            "Need for careful diet"
        ],
        "personality_points": [
            "Analytical, detail-oriented, and practical",
            "Reserved yet helpful",
            "Can be overly critical of self and others"
        ],
        "appearance_points": [
            "Petite or spare build",
            "Symmetrical body with youthful features"
        ]
    },
    "Libra": {
        "element": "Air",
        "ruling_planet": "Venus",
        "health_points": [
            "Kidney and urinary tract issues",
            "Lower back pain",
            "Skin-related sensitivities"
        ],
        "personality_points": [
            "Diplomatic, charming, and fair-minded",
            "Seeks harmony and avoids conflict",
            "Sometimes indecisive"
        ],
        "appearance_points": [
            "Graceful posture and balanced features",
            "Attractive smile and well-groomed appearance"
        ]
    },
    "Scorpio": {
        "element": "Water",
        "ruling_planet": "Mars",
        "health_points": [
            "Reproductive organ issues",
            "Urinary infections",
            "Stress affecting overall health"
        ],
        "personality_points": [
            "Intense, passionate, and determined",
            "Resourceful and secretive",
            "Sometimes overly suspicious or controlling"
        ],
        "appearance_points": [
            "Deep, penetrating eyes",
            "Strong and magnetic presence"
        ]
    },
    "Sagittarius": {
        "element": "Fire",
        "ruling_planet": "Jupiter",
        "health_points": [
            "Hip, thigh, and liver issues",
            "Weight fluctuations",
            "Accidents during travel or sports"
        ],
        "personality_points": [
            "Optimistic, adventurous, and philosophical",
            "Independent and freedom-loving",
            "Sometimes careless or overconfident"
        ],
        "appearance_points": [
            "Tall or athletic build",
            "Friendly smile and open body language"
        ]
    },
    "Capricorn": {
        "element": "Earth",
        "ruling_planet": "Saturn",
        "health_points": [
            "Joint, knee, and bone issues",
            "Skin problems",
            "Slow recovery from illness"
        ],
        "personality_points": [
            "Disciplined, ambitious, and responsible",
            "Practical and cautious",
            "Sometimes pessimistic or overly serious"
        ],
        "appearance_points": [
            "Lean or bony frame",
            "Sharp facial features with serious expression"
        ]
    },
    "Aquarius": {
        "element": "Air",
        "ruling_planet": "Saturn",
        "health_points": [
            "Circulatory system issues",
            "Ankle and calf injuries",
            "Nervous tension"
        ],
        "personality_points": [
            "Innovative, independent, and humanitarian",
            "Forward-thinking and unique",
            "Sometimes detached or unpredictable"
        ],
        "appearance_points": [
            "Tall, slim build",
            "Distinctive facial features and expressive eyes"
        ]
    },
    "Pisces": {
        "element": "Water",
        "ruling_planet": "Jupiter",
        "health_points": [
            "Feet and immune system weaknesses",
            "Prone to colds and allergies",
            "Sensitivity to toxins and drugs"
        ],
        "personality_points": [
            "Compassionate, imaginative, and spiritual",
            "Gentle and adaptable",
            "Sometimes escapist or overly idealistic"
        ],
        "appearance_points": [
            "Soft, dreamy eyes",
            "Graceful movements and rounded body features"
        ]
    }
}


def generate_ascendant_traits(ascendant_sign):
    traits = ascendant_base_traits.get(ascendant_sign)
    if not traits:
        return None

    health_text = (
        f"As a {ascendant_sign} Ascendant, your health is influenced by the {traits['element']} element "
        f"and ruled by {traits['ruling_planet']}. Common concerns include " +
        ", ".join(traits["health_points"]) + "."
    )

    personality_text = (
        f"{ascendant_sign} Ascendants tend to be " +
        ", ".join(traits["personality_points"]) + "."
    )

    appearance_text = (
        f"Physically, {ascendant_sign} Ascendants often have " +
        ", ".join(traits["appearance_points"]) + "."
    )

    return {
        "health": health_text,
        "temperament_personality": personality_text,
        "physical_appearance": appearance_text
    }
