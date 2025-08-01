def match_all_kootas(boy_moon, girl_moon):
    result = []

    # Example Kootas - for demo only
    result.append({"koota": "Varna", "score": 1, "max": 1, "description": "Spiritual compatibility based on varna"})
    result.append({"koota": "Vashya", "score": 2, "max": 2, "description": "Mutual attraction and control"})
    result.append({"koota": "Tara", "score": 2, "max": 3, "description": "Birth star compatibility"})
    result.append({"koota": "Yoni", "score": 3, "max": 4, "description": "Sexual compatibility"})
    result.append({"koota": "Graha Maitri", "score": 4, "max": 5, "description": "Friendship between lords of Moon signs"})
    result.append({"koota": "Gana", "score": 5, "max": 6, "description": "Nature and temperament compatibility"})
    result.append({"koota": "Bhakoot", "score": 7, "max": 7, "description": "Emotional bonding and family prosperity"})
    result.append({"koota": "Nadi", "score": 8, "max": 8, "description": "Health and genetic compatibility"})

    total_score = sum(k["score"] for k in result)
    max_score = sum(k["max"] for k in result)

    return {
        "total_score": total_score,
        "max_score": max_score,
        "kootas": result,
        "mangal_dosh": False,  # Add real logic later
        "note": "Basic match score calculated using placeholder rules"
    }
