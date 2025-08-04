from datetime import datetime
from geopy.geocoders import Nominatim
import swisseph as swe

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

nakshatra_traits = {
    "Ashwini": {
        "keywords": ["initiative", "courage", "healing"],
        "padas": {
            1: {
                "personality": "Bold, ambitious, and highly active.",
                "strengths": ["Leadership", "Healing", "Energy"],
                "weaknesses": ["Impulsiveness", "Restlessness"],
                "career": ["Surgeon", "Athlete", "Entrepreneur"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "a passionate yet composed individual"
            },
            2: {
                "personality": "Practical with a strategic mind.",
                "strengths": ["Organization", "Discipline"],
                "weaknesses": ["Stubbornness"],
                "career": ["Manager", "Engineer"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "someone who values stability"
            },
            3: {
                "personality": "Communicative and curious.",
                "strengths": ["Communication", "Adaptability"],
                "weaknesses": ["Scattered energy"],
                "career": ["Writer", "Speaker"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            4: {
                "personality": "Emotionally intelligent and intuitive.",
                "strengths": ["Empathy", "Creativity"],
                "weaknesses": ["Mood swings"],
                "career": ["Counselor", "Artist"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "a passionate yet composed individual"
            },
        },
    },
    "Bharani": {
        "keywords": ["responsibility", "creativity", "transformation"],
        "padas": {
            1: {
                "personality": "Passionate and driven.",
                "strengths": ["Determination", "Courage"],
                "weaknesses": ["Jealousy"],
                "career": ["Artist", "Military"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            2: {
                "personality": "Strong moral compass and values.",
                "strengths": ["Discipline", "Loyalty"],
                "weaknesses": ["Rigidity"],
                "career": ["Teacher", "Judge"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "a creative and fun-loving companion"
            },
            3: {
                "personality": "Highly expressive and magnetic.",
                "strengths": ["Creativity", "Charm"],
                "weaknesses": ["Self-indulgence"],
                "career": ["Performer", "Public speaker"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            4: {
                "personality": "Nurturing and intuitive.",
                "strengths": ["Empathy", "Healing"],
                "weaknesses": ["Over-sensitivity"],
                "career": ["Nurse", "Counselor"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "a loyal and honest romantic"
            },
        },
    },
    "Krittika": {
        "keywords": ["sharpness", "discipline", "purification"],
        "padas": {
            1: {
                "personality": "Aggressive and confident.",
                "strengths": ["Boldness", "Clarity"],
                "weaknesses": ["Harsh speech"],
                "career": ["Lawyer", "Military"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who values stability"
            },
            2: {
                "personality": "Practical and hardworking.",
                "strengths": ["Dedication", "Persistence"],
                "weaknesses": ["Stubbornness"],
                "career": ["Engineer", "Builder"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "an adventurous and independent soul"
            },
            3: {
                "personality": "Artistic and visionary.",
                "strengths": ["Creativity", "Vision"],
                "weaknesses": ["Unrealistic goals"],
                "career": ["Designer", "Artist"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "an adventurous and independent soul"
            },
            4: {
                "personality": "Intuitive and service-oriented.",
                "strengths": ["Empathy", "Healing"],
                "weaknesses": ["Emotional dependency"],
                "career": ["Social worker", "Psychologist"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "an emotionally intelligent partner"
            },
        },
    },
    "Rohini": {
        "keywords": ["beauty", "growth", "sensuality"],
        "padas": {
            1: {
                "personality": "Charming and loving.",
                "strengths": ["Affection", "Creativity"],
                "weaknesses": ["Possessiveness"],
                "career": ["Artist", "Model"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "someone who provides security and openness"
            },
            2: {
                "personality": "Practical and security-oriented.",
                "strengths": ["Reliability", "Patience"],
                "weaknesses": ["Stubbornness"],
                "career": ["Banking", "Finance"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            3: {
                "personality": "Friendly and social.",
                "strengths": ["Communication", "Adaptability"],
                "weaknesses": ["Inconsistency"],
                "career": ["Sales", "Marketing"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "a communicative and trustworthy partner"
            },
            4: {
                "personality": "Sensitive and spiritual.",
                "strengths": ["Intuition", "Compassion"],
                "weaknesses": ["Escapism"],
                "career": ["Healer", "Priest"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "an emotionally intelligent partner"
            },
        },
    },
    "Mrigashira": {
        "keywords": ["curiosity", "search", "exploration"],
        "padas": {
            1: {
                "personality": "Adventurous and alert.",
                "strengths": ["Curiosity", "Intelligence"],
                "weaknesses": ["Anxiety"],
                "career": ["Explorer", "Scientist"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "a loyal and honest romantic"
            },
            2: {
                "personality": "Disciplined and practical.",
                "strengths": ["Stability", "Hardwork"],
                "weaknesses": ["Over-caution"],
                "career": ["Engineer", "Administrator"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            3: {
                "personality": "Expressive and creative.",
                "strengths": ["Artistic talent", "Communication"],
                "weaknesses": ["Scattered energy"],
                "career": ["Writer", "Media"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "an emotionally intelligent partner"
            },
            4: {
                "personality": "Spiritual and gentle.",
                "strengths": ["Empathy", "Sensitivity"],
                "weaknesses": ["Over-sensitivity"],
                "career": ["Priest", "Therapist"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "someone who matches your depth and intensity"
            },
        },
    },
    "Ardra": {
        "keywords": ["transformation", "intensity", "learning"],
        "padas": {
            1: {
                "personality": "Energetic and analytical.",
                "strengths": ["Research", "Observation"],
                "weaknesses": ["Restlessness"],
                "career": ["Scientist", "Technologist"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "a communicative and trustworthy partner"
            },
            2: {
                "personality": "Logical and organized.",
                "strengths": ["Clarity", "Focus"],
                "weaknesses": ["Rigidity"],
                "career": ["Teacher", "Manager"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            3: {
                "personality": "Visionary and expressive.",
                "strengths": ["Creativity", "Communication"],
                "weaknesses": ["Impatience"],
                "career": ["Speaker", "Artist"],
                "emotional_traits": "expressive and warm-hearted",
                "ideal_partner": "a creative and fun-loving companion"
            },
            4: {
                "personality": "Emotional and deep thinker.",
                "strengths": ["Sensitivity", "Insight"],
                "weaknesses": ["Overthinking"],
                "career": ["Psychologist", "Poet"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "someone who values stability"
            },
        },
    },
    "Punarvasu": {
        "keywords": ["renewal", "nurturing", "optimism"],
        "padas": {
            1: {
                "personality": "Caring and optimistic.",
                "strengths": ["Nurturing", "Faith"],
                "weaknesses": ["Naivety"],
                "career": ["Doctor", "Teacher"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "a loyal and honest romantic"
            },
            2: {
                "personality": "Organized and thoughtful.",
                "strengths": ["Planning", "Responsibility"],
                "weaknesses": ["Overthinking"],
                "career": ["Engineer", "Manager"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "an emotionally intelligent partner"
            },
            3: {
                "personality": "Expressive and cheerful.",
                "strengths": ["Communication", "Positivity"],
                "weaknesses": ["Inconsistency"],
                "career": ["Writer", "Public Relations"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "an adventurous and independent soul"
            },
            4: {
                "personality": "Emotionally intelligent and wise.",
                "strengths": ["Compassion", "Spirituality"],
                "weaknesses": ["Emotional fatigue"],
                "career": ["Spiritual Leader", "Counselor"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "a passionate yet composed individual"
            },
        },
    },
    "Pushya": {
        "keywords": ["support", "nourishment", "spirituality"],
        "padas": {
            1: {
                "personality": "Disciplined and loyal.",
                "strengths": ["Commitment", "Reliability"],
                "weaknesses": ["Rigidity"],
                "career": ["Police", "Judge"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "an adventurous and independent soul"
            },
            2: {
                "personality": "Balanced and efficient.",
                "strengths": ["Management", "Patience"],
                "weaknesses": ["Indecisiveness"],
                "career": ["Teacher", "Advisor"],
                "emotional_traits": "expressive and warm-hearted",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            3: {
                "personality": "Communicative and nurturing.",
                "strengths": ["Empathy", "Teaching"],
                "weaknesses": ["Overgiving"],
                "career": ["Nurse", "Therapist"],
                "emotional_traits": "protective and affectionate",
                "ideal_partner": "someone who provides security and openness"
            },
            4: {
                "personality": "Emotionally intelligent and calm.",
                "strengths": ["Compassion", "Spiritual depth"],
                "weaknesses": ["Withdrawn nature"],
                "career": ["Healer", "Spiritual guide"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "a creative and fun-loving companion"
            },
        },
    },
    "Ashlesha": {
        "keywords": ["mystery", "intuition", "transformation"],
        "padas": {
            1: {
                "personality": "Intelligent and strategic.",
                "strengths": ["Manipulation", "Focus"],
                "weaknesses": ["Deception"],
                "career": ["Spy", "Psychologist"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who values stability"
            },
            2: {
                "personality": "Introspective and intense.",
                "strengths": ["Self-awareness", "Discipline"],
                "weaknesses": ["Emotional control issues"],
                "career": ["Scientist", "Detective"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "someone who encourages your dreams"
            },
            3: {
                "personality": "Creative and mysterious.",
                "strengths": ["Imagination", "Insight"],
                "weaknesses": ["Moody"],
                "career": ["Artist", "Occultist"],
                "emotional_traits": "expressive and warm-hearted",
                "ideal_partner": "someone who encourages your dreams"
            },
            4: {
                "personality": "Spiritual and emotional.",
                "strengths": ["Healing", "Perception"],
                "weaknesses": ["Trust issues"],
                "career": ["Healer", "Mystic"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "someone who encourages your dreams"
            },
        },
    },
    "Magha": {
        "keywords": ["royalty", "ancestry", "authority"],
        "padas": {
            1: {
                "personality": "Powerful and disciplined.",
                "strengths": ["Leadership", "Respect for tradition"],
                "weaknesses": ["Pride"],
                "career": ["Politician", "Judge"],
                "emotional_traits": "protective and affectionate",
                "ideal_partner": "a communicative and trustworthy partner"
            },
            2: {
                "personality": "Organized and responsible.",
                "strengths": ["Structure", "Diligence"],
                "weaknesses": ["Rigidity"],
                "career": ["Administrator", "Planner"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            3: {
                "personality": "Expressive and ambitious.",
                "strengths": ["Confidence", "Presentation"],
                "weaknesses": ["Vanity"],
                "career": ["Actor", "Influencer"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "someone who provides security and openness"
            },
            4: {
                "personality": "Emotionally strong and spiritual.",
                "strengths": ["Compassion", "Heritage values"],
                "weaknesses": ["Overbearing nature"],
                "career": ["Priest", "Historian"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "a creative and fun-loving companion"
            },
        },
    },
    "Purva Phalguni": {
        "keywords": ["pleasure", "creativity", "relationships"],
        "padas": {
            1: {
                "personality": "Attractive, sociable, and expressive.",
                "strengths": ["Charm", "Creativity"],
                "weaknesses": ["Overindulgence"],
                "career": ["Artist", "Entertainer"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who provides security and openness"
            },
            2: {
                "personality": "Practical and stable in love and life.",
                "strengths": ["Loyalty", "Patience"],
                "weaknesses": ["Laziness"],
                "career": ["Counselor", "Designer"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "an adventurous and independent soul"
            },
            3: {
                "personality": "Witty and entertaining.",
                "strengths": ["Communication", "Humor"],
                "weaknesses": ["Inconsistency"],
                "career": ["Comedian", "Marketing"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "an emotionally intelligent partner"
            },
            4: {
                "personality": "Sensitive and artistic.",
                "strengths": ["Empathy", "Romance"],
                "weaknesses": ["Emotional dependence"],
                "career": ["Actor", "Poet"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who matches your depth and intensity"
            },
        },
    },
    "Uttara Phalguni": {
        "keywords": ["helpfulness", "commitment", "prosperity"],
        "padas": {
            1: {
                "personality": "Supportive and generous.",
                "strengths": ["Stability", "Charity"],
                "weaknesses": ["Too self-sacrificing"],
                "career": ["NGO worker", "Therapist"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "someone who encourages your dreams"
            },
            2: {
                "personality": "Responsible and family-oriented.",
                "strengths": ["Loyalty", "Dependability"],
                "weaknesses": ["Rigidity"],
                "career": ["Manager", "Banker"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            3: {
                "personality": "Creative and expressive.",
                "strengths": ["Communication", "Empathy"],
                "weaknesses": ["Mood swings"],
                "career": ["Teacher", "Artist"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "someone who encourages your dreams"
            },
            4: {
                "personality": "Disciplined and spiritual.",
                "strengths": ["Wisdom", "Compassion"],
                "weaknesses": ["Withdrawal"],
                "career": ["Spiritual advisor", "Counselor"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "a communicative and trustworthy partner"
            },
        },
    },
    "Hasta": {
        "keywords": ["skill", "dexterity", "humor"],
        "padas": {
            1: {
                "personality": "Skillful and grounded.",
                "strengths": ["Craftsmanship", "Focus"],
                "weaknesses": ["Stubbornness"],
                "career": ["Craftsman", "Engineer"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            2: {
                "personality": "Balanced and intelligent.",
                "strengths": ["Wisdom", "Calm"],
                "weaknesses": ["Aloofness"],
                "career": ["Writer", "Technician"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "a creative and fun-loving companion"
            },
            3: {
                "personality": "Charming and witty.",
                "strengths": ["Communication", "Social skills"],
                "weaknesses": ["Sarcasm"],
                "career": ["Comedian", "Teacher"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "a passionate yet composed individual"
            },
            4: {
                "personality": "Sensitive and intuitive.",
                "strengths": ["Empathy", "Healing"],
                "weaknesses": ["Overthinking"],
                "career": ["Therapist", "Spiritualist"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
        },
    },
    "Chitra": {
        "keywords": ["beauty", "brilliance", "structure"],
        "padas": {
            1: {
                "personality": "Creative and bold.",
                "strengths": ["Vision", "Courage"],
                "weaknesses": ["Aggression"],
                "career": ["Architect", "Artist"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "an adventurous and independent soul"
            },
            2: {
                "personality": "Disciplined and methodical.",
                "strengths": ["Planning", "Execution"],
                "weaknesses": ["Control issues"],
                "career": ["Engineer", "Planner"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            3: {
                "personality": "Charming and aesthetic-minded.",
                "strengths": ["Style", "Design sense"],
                "weaknesses": ["Vanity"],
                "career": ["Fashion", "Interior Designer"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            4: {
                "personality": "Spiritual and philosophical.",
                "strengths": ["Insight", "Mysticism"],
                "weaknesses": ["Detachment"],
                "career": ["Monk", "Philosopher"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who values stability"
            },
        },
    },
    "Swati": {
        "keywords": ["freedom", "adaptability", "independence"],
        "padas": {
            1: {
                "personality": "Adventurous and lively.",
                "strengths": ["Exploration", "Joyfulness"],
                "weaknesses": ["Inconsistency"],
                "career": ["Travel blogger", "Performer"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            2: {
                "personality": "Balanced and fair-minded.",
                "strengths": ["Justice", "Calmness"],
                "weaknesses": ["Indecisiveness"],
                "career": ["Judge", "Consultant"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "an emotionally intelligent partner"
            },
            3: {
                "personality": "Persuasive and creative.",
                "strengths": ["Communication", "Marketing"],
                "weaknesses": ["Manipulative tendencies"],
                "career": ["Sales", "Diplomat"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            4: {
                "personality": "Idealistic and spiritual.",
                "strengths": ["Vision", "Detachment"],
                "weaknesses": ["Escapism"],
                "career": ["Writer", "Spiritual guide"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "an emotionally intelligent partner"
            },
        },
    },
    "Vishakha": {
        "keywords": ["determination", "goal-oriented", "duality"],
        "padas": {
            1: {
                "personality": "Focused and goal-driven.",
                "strengths": ["Ambition", "Persistence"],
                "weaknesses": ["Impatience"],
                "career": ["Entrepreneur", "Politician"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "a loyal and honest romantic"
            },
            2: {
                "personality": "Balanced and diplomatic.",
                "strengths": ["Fairness", "Strategy"],
                "weaknesses": ["Conflicted loyalties"],
                "career": ["Lawyer", "Negotiator"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            3: {
                "personality": "Intelligent and philosophical.",
                "strengths": ["Wisdom", "Logic"],
                "weaknesses": ["Overthinking"],
                "career": ["Professor", "Writer"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "someone who encourages your dreams"
            },
            4: {
                "personality": "Emotionally intense and idealistic.",
                "strengths": ["Determination", "Devotion"],
                "weaknesses": ["Stubbornness"],
                "career": ["Activist", "Spiritual Leader"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "a communicative and trustworthy partner"
            },
        },
    },
    "Anuradha": {
        "keywords": ["friendship", "discipline", "devotion"],
        "padas": {
            1: {
                "personality": "Loyal and loving.",
                "strengths": ["Faithful", "Trustworthy"],
                "weaknesses": ["Over-attachment"],
                "career": ["Psychologist", "Human resources"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            2: {
                "personality": "Disciplined and structured.",
                "strengths": ["Persistence", "Work ethic"],
                "weaknesses": ["Rigidity"],
                "career": ["Administrator", "Military"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "an emotionally intelligent partner"
            },
            3: {
                "personality": "Charismatic and persuasive.",
                "strengths": ["Leadership", "Communication"],
                "weaknesses": ["Pride"],
                "career": ["Speaker", "Sales"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "someone who provides security and openness"
            },
            4: {
                "personality": "Spiritual and emotionally deep.",
                "strengths": ["Intuition", "Compassion"],
                "weaknesses": ["Emotional turmoil"],
                "career": ["Healer", "Poet"],
                "emotional_traits": "protective and affectionate",
                "ideal_partner": "someone who matches your depth and intensity"
            },
        },
    },
    "Jyeshtha": {
        "keywords": ["maturity", "power", "responsibility"],
        "padas": {
            1: {
                "personality": "Protective and responsible.",
                "strengths": ["Leadership", "Loyalty"],
                "weaknesses": ["Control issues"],
                "career": ["Police", "Government officer"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "someone who provides security and openness"
            },
            2: {
                "personality": "Sharp and strategic.",
                "strengths": ["Intellect", "Focus"],
                "weaknesses": ["Secretive"],
                "career": ["Detective", "Scientist"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "someone who provides security and openness"
            },
            3: {
                "personality": "Independent and confident.",
                "strengths": ["Self-reliance", "Authority"],
                "weaknesses": ["Isolation"],
                "career": ["CEO", "Consultant"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "a loyal and honest romantic"
            },
            4: {
                "personality": "Emotionally wise and intuitive.",
                "strengths": ["Sensitivity", "Insight"],
                "weaknesses": ["Anxiety"],
                "career": ["Therapist", "Writer"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "a communicative and trustworthy partner"
            },
        },
    },
    "Mula": {
        "keywords": ["roots", "transformation", "spiritual growth"],
        "padas": {
            1: {
                "personality": "Deep thinker and researcher.",
                "strengths": ["Focus", "Intuition"],
                "weaknesses": ["Obsession"],
                "career": ["Scientist", "Occultist"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            2: {
                "personality": "Rebellious and determined.",
                "strengths": ["Fearlessness", "Persistence"],
                "weaknesses": ["Aggression"],
                "career": ["Reformer", "Activist"],
                "emotional_traits": "protective and affectionate",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            3: {
                "personality": "Spiritual and philosophical.",
                "strengths": ["Wisdom", "Detachment"],
                "weaknesses": ["Loneliness"],
                "career": ["Sage", "Counselor"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "an adventurous and independent soul"
            },
            4: {
                "personality": "Emotional and artistic.",
                "strengths": ["Creativity", "Compassion"],
                "weaknesses": ["Emotional instability"],
                "career": ["Artist", "Healer"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "someone who provides security and openness"
            },
        },
    },
    "Purva Ashadha": {
        "keywords": ["invincibility", "ambition", "expansion"],
        "padas": {
            1: {
                "personality": "Ambitious and outgoing.",
                "strengths": ["Confidence", "Optimism"],
                "weaknesses": ["Pride"],
                "career": ["Politician", "Coach"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "a loyal and honest romantic"
            },
            2: {
                "personality": "Strategic and diplomatic.",
                "strengths": ["Planning", "Social grace"],
                "weaknesses": ["Manipulation"],
                "career": ["Advisor", "Marketing"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "someone who encourages your dreams"
            },
            3: {
                "personality": "Creative and idealistic.",
                "strengths": ["Vision", "Artistry"],
                "weaknesses": ["Fantasy-prone"],
                "career": ["Filmmaker", "Author"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "someone who values stability"
            },
            4: {
                "personality": "Spiritual and generous.",
                "strengths": ["Charity", "Philosophy"],
                "weaknesses": ["Naivety"],
                "career": ["Priest", "Guru"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "an adventurous and independent soul"
            },
        },
    },
    "Uttara Ashadha": {
        "keywords": ["truth", "leadership", "perseverance"],
        "padas": {
            1: {
                "personality": "Honest and committed.",
                "strengths": ["Integrity", "Reliability"],
                "weaknesses": ["Rigidity"],
                "career": ["Judge", "Manager"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            2: {
                "personality": "Hardworking and traditional.",
                "strengths": ["Discipline", "Focus"],
                "weaknesses": ["Conservatism"],
                "career": ["Civil servant", "Engineer"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "someone who values stability"
            },
            3: {
                "personality": "Responsible and fair-minded.",
                "strengths": ["Balance", "Justice"],
                "weaknesses": ["Judgmental"],
                "career": ["Leader", "Social worker"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "someone spiritual and emotionally tuned in"
            },
            4: {
                "personality": "Spiritual and philosophical.",
                "strengths": ["Morality", "Wisdom"],
                "weaknesses": ["Detached"],
                "career": ["Preacher", "Mentor"],
                "emotional_traits": "expressive and warm-hearted",
                "ideal_partner": "a passionate yet composed individual"
            },
        },
    },
    "Shravana": {
        "keywords": ["listening", "learning", "tradition"],
        "padas": {
            1: {
                "personality": "Studious and curious.",
                "strengths": ["Knowledge", "Listening"],
                "weaknesses": ["Introversion"],
                "career": ["Scholar", "Researcher"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "a creative and fun-loving companion"
            },
            2: {
                "personality": "Disciplined and traditional.",
                "strengths": ["Order", "Focus"],
                "weaknesses": ["Inflexibility"],
                "career": ["Teacher", "Historian"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "an adventurous and independent soul"
            },
            3: {
                "personality": "Empathetic and gentle.",
                "strengths": ["Care", "Patience"],
                "weaknesses": ["Sensitivity"],
                "career": ["Nurse", "Healer"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "someone who values stability"
            },
            4: {
                "personality": "Wise and spiritually inclined.",
                "strengths": ["Insight", "Morality"],
                "weaknesses": ["Retreat"],
                "career": ["Philosopher", "Priest"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "a creative and fun-loving companion"
            },
        },
    },
    "Dhanishta": {
        "keywords": ["wealth", "rhythm", "community"],
        "padas": {
            1: {
                "personality": "Charismatic and bold.",
                "strengths": ["Leadership", "Confidence"],
                "weaknesses": ["Pride"],
                "career": ["Performer", "Politician"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "someone who encourages your dreams"
            },
            2: {
                "personality": "Musical and expressive.",
                "strengths": ["Artistry", "Harmony"],
                "weaknesses": ["Distraction"],
                "career": ["Musician", "Artist"],
                "emotional_traits": "passionate but thoughtful",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            3: {
                "personality": "Organized and ambitious.",
                "strengths": ["Discipline", "Strategy"],
                "weaknesses": ["Rigidity"],
                "career": ["Manager", "Engineer"],
                "emotional_traits": "highly empathetic",
                "ideal_partner": "an emotionally intelligent partner"
            },
            4: {
                "personality": "Spiritual and service-oriented.",
                "strengths": ["Compassion", "Insight"],
                "weaknesses": ["Over-responsibility"],
                "career": ["Healer", "Mentor"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "a communicative and trustworthy partner"
            },
        },
    },
    "Shatabhisha": {
        "keywords": ["healing", "secrecy", "innovation"],
        "padas": {
            1: {
                "personality": "Innovative and independent.",
                "strengths": ["Creativity", "Intellect"],
                "weaknesses": ["Aloofness"],
                "career": ["Scientist", "Inventor"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "an adventurous and independent soul"
            },
            2: {
                "personality": "Mysterious and analytical.",
                "strengths": ["Research", "Focus"],
                "weaknesses": ["Detachment"],
                "career": ["Detective", "Philosopher"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            3: {
                "personality": "Humanitarian and visionary.",
                "strengths": ["Compassion", "Idealism"],
                "weaknesses": ["Overwhelm"],
                "career": ["NGO work", "Social reformer"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            4: {
                "personality": "Spiritual and introverted.",
                "strengths": ["Healing", "Wisdom"],
                "weaknesses": ["Isolation"],
                "career": ["Mystic", "Healer"],
                "emotional_traits": "rational yet loving",
                "ideal_partner": "an emotionally intelligent partner"
            },
        },
    },
    "Purva Bhadrapada": {
        "keywords": ["intensity", "occult", "transformation"],
        "padas": {
            1: {
                "personality": "Mysterious and intense.",
                "strengths": ["Focus", "Insight"],
                "weaknesses": ["Extremism"],
                "career": ["Occultist", "Psychologist"],
                "emotional_traits": "protective and affectionate",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            2: {
                "personality": "Philosophical and truthful.",
                "strengths": ["Wisdom", "Honesty"],
                "weaknesses": ["Bluntness"],
                "career": ["Spiritual teacher", "Analyst"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "someone who provides security and openness"
            },
            3: {
                "personality": "Reformative and unconventional.",
                "strengths": ["Rebellion", "Innovation"],
                "weaknesses": ["Recklessness"],
                "career": ["Activist", "Technologist"],
                "emotional_traits": "calm and emotionally balanced",
                "ideal_partner": "an adventurous and independent soul"
            },
            4: {
                "personality": "Devoted and mystical.",
                "strengths": ["Faith", "Vision"],
                "weaknesses": ["Fanaticism"],
                "career": ["Priest", "Astrologer"],
                "emotional_traits": "sensitive and compassionate",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
        },
    },
    "Uttara Bhadrapada": {
        "keywords": ["depth", "stability", "benevolence"],
        "padas": {
            1: {
                "personality": "Calm and philosophical.",
                "strengths": ["Wisdom", "Peace"],
                "weaknesses": ["Detachment"],
                "career": ["Sage", "Scholar"],
                "emotional_traits": "expressive and warm-hearted",
                "ideal_partner": "a passionate yet composed individual"
            },
            2: {
                "personality": "Stable and grounded.",
                "strengths": ["Practicality", "Supportiveness"],
                "weaknesses": ["Boredom"],
                "career": ["Mentor", "Social worker"],
                "emotional_traits": "reserved but deeply connected",
                "ideal_partner": "a communicative and trustworthy partner"
            },
            3: {
                "personality": "Emotionally balanced and kind.",
                "strengths": ["Compassion", "Balance"],
                "weaknesses": ["Indecisiveness"],
                "career": ["Healer", "Mediator"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "a grounded yet passionate soulmate"
            },
            4: {
                "personality": "Visionary and introspective.",
                "strengths": ["Insight", "Creativity"],
                "weaknesses": ["Isolation"],
                "career": ["Poet", "Spiritual guide"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "an adventurous and independent soul"
            },
        },
    },
    "Revati": {
        "keywords": ["nourishment", "compassion", "completion"],
        "padas": {
            1: {
                "personality": "Caring and nurturing.",
                "strengths": ["Empathy", "Patience"],
                "weaknesses": ["Overgiving"],
                "career": ["Doctor", "Caretaker"],
                "emotional_traits": "emotionally intense but caring",
                "ideal_partner": "an adventurous and independent soul"
            },
            2: {
                "personality": "Spiritual and musical.",
                "strengths": ["Intuition", "Harmony"],
                "weaknesses": ["Escapism"],
                "career": ["Musician", "Spiritualist"],
                "emotional_traits": "loyal and dependable",
                "ideal_partner": "someone who matches your depth and intensity"
            },
            3: {
                "personality": "Creative and gentle.",
                "strengths": ["Artistry", "Sensitivity"],
                "weaknesses": ["Emotional ups & downs"],
                "career": ["Artist", "Counselor"],
                "emotional_traits": "adventurous in love",
                "ideal_partner": "someone who encourages your dreams"
            },
            4: {
                "personality": "Idealistic and wise.",
                "strengths": ["Vision", "Peacefulness"],
                "weaknesses": ["Indecision"],
                "career": ["Philosopher", "Writer"],
                "emotional_traits": "intuitive and nurturing",
                "ideal_partner": "someone who provides security and openness"
            },
        },
    }
}


def generate_nakshatra_prediction(dob, tob, place):
    geolocator = Nominatim(user_agent="nakshatra_api")
    location = geolocator.geocode(place)

    if not location:
        return {"error": "Location not found."}

    # Combine DOB and TOB
    dt_str = f"{dob} {tob}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    
    # Get Julian Day
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

    # Set geographic location for swisseph
    swe.set_topo(location.longitude, location.latitude, 0)

    # Get Moon's position
    moon_pos = swe.calc_ut(jd, swe.MOON)[0]
    moon_long = moon_pos[0]

    # Calculate nakshatra index (27 divisions of 13°20′)
    nakshatra_index = int(moon_long // (360 / 27))
    nakshatra_name = NAKSHATRAS[nakshatra_index]

    # Calculate pada (4 padas of 3°20′ in each nakshatra)
    pada = int((moon_long % (360 / 27)) // (360 / 108)) + 1  # 108 padas in total

    # Look up prediction
    data = nakshatra_traits.get(nakshatra_name, {})
    pada_data = data.get("padas", {}).get(pada, {})

    if not pada_data:
        return {"error": f"No data available for {nakshatra_name} Pada {pada}"}

    return {
        "nakshatra": nakshatra_name,
        "pada": pada,
        "personality": pada_data["personality"],
        "strengths": pada_data["strengths"],
        "weaknesses": pada_data["weaknesses"],
        "career": pada_data["career"],
        "keywords": data.get("keywords", [])
    }
