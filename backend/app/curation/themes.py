"""
Category-specific theme dictionaries for rule-based curation
NO EMBEDDINGS - keyword matching only
"""

# Movies theme keywords
MOVIES_THEMES = {
    "working": [
        # Existing (keep)
        "great performance", "amazing acting", "brilliant", "outstanding",
        "well directed", "great direction", "cinematography", "visuals",
        "storytelling", "narrative", "plot", "engaging", "gripping",
        "emotional", "moving", "powerful", "intense",
        "action sequences", "special effects", "soundtrack", "music",
        "loved it", "enjoyed", "amazing", "fantastic",
        "must watch", "recommend", "worth watching",

        # 🔥 Indian / regional short-form praise (CRITICAL)
        "blockbuster", "super hit", "hit", "mass",
        "super", "awesome", "full meals",
        "worth watch", "pakka hit",

        # 🔥 Telugu / Indian transliteration (NO translation)
        "bagundi",           # good
        "super undi",        # very good
        "movie bagundi",
        "hit undi",
        "mass undi",
        "super ra",
        "hit ra",
    ],

    "mixed": [
        # Existing
        "mixed feelings", "okay", "decent", "not bad",
        "could be better", "some parts", "hit or miss",
        "inconsistent", "uneven", "slow start",
        "picks up later", "dragged",

        # Indian-style mixed reactions
        "average", "routine",
        "first half good", "second half slow",
        "lag", "lengthy",
    ],

    "concerns": [
        # Existing
        "disappointed", "boring", "slow", "predictable",
        "weak script", "poor writing", "bad dialogue",
        "plot holes", "wasted potential",
        "too long", "unnecessary scenes",

        # Indian blunt criticism
        "flop", "disaster",
        "waste of money",
        "not good",
        "bad movie",
    ],

    "resonates": [
        # Existing
        "family friendly", "kids", "children",
        "nostalgic", "old school fans",
        "general audience",

        # Indian audience segments
        "family audience",
        "festival movie",
        "sankranthi",
        "pongal",
        "fans",
        "mass audience",
    ],
}


# Gadgets theme keywords
GADGETS_THEMES = {
    "working": [
        # Positive features
        "battery life", "great battery", "fast charging", "performance",
        "smooth", "fast", "powerful", "responsive", "snappy",
        "display", "screen quality", "bright", "vivid", "colors",
        "camera quality", "great camera", "photos", "video quality",
        "build quality", "premium feel", "design", "sleek", "lightweight",
        "features", "functionality", "works well", "great for",
        # Positive reception
        "love it", "impressed", "worth it", "recommend", "best",
        "upgrade", "solid", "reliable", "happy with",
    ],
    "mixed": [
        # Mixed signals
        "mixed bag", "okay", "decent", "good but", "fine for the price",
        "some issues", "hit or miss", "depends", "trade offs",
        "not perfect", "could be better", "expected more",
    ],
    "concerns": [
        # Negative aspects
        "battery drain", "poor battery", "overheating", "gets hot",
        "slow", "laggy", "stuttering", "freezes", "crashes",
        "buggy", "software issues", "glitches", "problems",
        "screen issues", "display problems", "dead pixels",
        "camera disappointing", "poor camera", "blurry",
        "build quality", "cheap feeling", "flimsy", "creaks",
        "overpriced", "not worth", "expensive", "too costly",
        "connectivity issues", "wifi problems", "bluetooth",
        "quality control", "defective", "returned",
    ],
    "resonates": [
        # Audience segments
        "gamers", "gaming", "professionals", "creators",
        "casual users", "students", "seniors", "kids",
        "photographers", "videographers", "developers",
        "power users", "everyday use", "beginners",
        "upgraders", "android users", "ios users",
        "budget conscious", "premium users", "enthusiasts",
    ],
}


# Vehicles theme keywords
VEHICLES_THEMES = {
    "working": [
        # Positive features
        "fuel efficiency", "great mileage", "good mileage", "fuel economy",
        "smooth ride", "comfortable", "performance", "powerful engine",
        "handling", "responsive", "acceleration", "braking",
        "build quality", "reliability", "reliable", "solid build",
        "features", "technology", "infotainment", "safety features",
        "space", "spacious", "interior", "cargo space", "legroom",
        "design", "looks", "styling", "premium feel",
        # Positive reception
        "love it", "impressed", "worth it", "recommend", "best",
        "happy with", "satisfied", "great car", "excellent",
    ],
    "mixed": [
        # Mixed signals
        "mixed bag", "okay", "decent", "good but", "fine for the price",
        "some issues", "hit or miss", "depends", "trade offs",
        "not perfect", "could be better", "expected more",
        "average", "nothing special",
    ],
    "concerns": [
        # Negative aspects
        "poor mileage", "fuel consumption", "bad mileage", "thirsty",
        "maintenance issues", "reliability issues", "unreliable", "breaks down",
        "expensive maintenance", "repair costs", "service costs",
        "build quality", "cheap feeling", "rattles", "squeaks",
        "ride quality", "uncomfortable", "harsh ride", "stiff suspension",
        "engine problems", "transmission issues", "electrical problems",
        "overpriced", "not worth", "expensive", "too costly",
        "resale value", "depreciation", "poor resale",
        "quality control", "defects", "problems", "issues",
    ],
    "resonates": [
        # Audience segments
        "families", "family car", "commuters", "daily driver",
        "first time buyers", "enthusiasts", "car lovers",
        "city driving", "highway driving", "off road",
        "budget conscious", "premium buyers", "luxury seekers",
        "young drivers", "seniors", "professionals",
        "eco conscious", "performance seekers", "practical buyers",
    ],
}
