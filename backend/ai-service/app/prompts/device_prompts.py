
TRAITS_FIELDS_DEVICE = """
- brand: specific brand name (e.g. "apple", "samsung", "google")
- model: specific model name (e.g. "iphone 15 pro", "galaxy s24 ultra")
- category: "phones", "tablets", "laptops", "cameras", "other"
- os: "ios", "android", "windows", "macos", "ipados"
- condition: "new", "used", "refurbished"
- cost_range: 
    "budget-friendly" (Phones <$300, Laptops <$500),
    "mid-range" (Phones $300-$800, Laptops $500-$1300),
    "premium" (Phones $800-$1500, Laptops $1300-$2500),
    "extra-premium" (Phones >$1500, Laptops >$2500)
- storage_capacity:
    "small" (Phones <=128GB, Laptops <=256GB),
    "medium" (Phones 256GB-512GB, Laptops 512GB-1TB),
    "large" (Phones >=1TB, Laptops >=2TB)
- screen_size:
    "small" (Phones <6.1", Tablets <9", Laptops <13.3"),
    "medium" (Phones 6.1"-6.6", Tablets 9"-11.5", Laptops 13.3"-14.9"),
    "large" (Phones >=6.7", Tablets >12", Laptops >=15.0")
- battery_life:
    "short" (<4000mAh or <6h use),
    "medium" (4000-5000mAh or 7-12h use),
    "long" (>5000mAh or >13h use like Apple M-series)
- form_factor: "phone", "tablet", "laptop", "desktop", "foldable"
- display_count: number of physical screens as integer. 1 for regular devices, 2 for dual-screen devices (second display, foldables with a cover screen)
"""

SPECIFICATIONS_FIELDS_DEVICE = """
- brand: specific brand name (e.g. "apple", "samsung", "google")
- model: specific model name (e.g. "iphone 15 pro", "galaxy s24 ultra")
- os: "ios", "android", "windows", "macos", "ipados"
- storage_capacity: e.g 128GB
- screen_size: e.g. 6.5 inches
- battery_capacity: e.g. 4000mAh
- form_factor: "phone", "tablet", "laptop", "desktop", "foldable"
- camera: e.g. 12MP, 48MP, 108MP
- processor: e.g. Apple A17 Pro, Qualcomm Snapdragon 8 Gen 3, Intel Core i9
- ram: e.g. 8GB, 16GB, 32GB
- storage: e.g. 128GB, 256GB, 512GB
- display: e.g. 6.5 inches, 1080p, 4K
- battery_life: e.g. 10 hours, 12 hours, 14 hours
- form_factor: "phone", "tablet", "laptop", "desktop", "foldable"
- camera: e.g. 12MP, 48MP, 108MP
"""


KEY_FEATURES_DEVICE_FIELDS = """
- 3-5 key features of the device.
"""

GET_TRAITS_BY_DEVICE_NAME_PROMPT = """
Fill fields with data by device name.
The user message contains the device name and may contain a seller description.
The seller description is the source of truth. It may contain facts found on the web.
Use your own knowledge only for a device you know exactly by this name. Never copy specs of a similar or older model.
Do not infer features from words in the name: "Duo", "Dual", "Fold", "Max" mean nothing without facts.

FORMAT JSON OBJECT THAT HAS THE FOLLOWING FIELDS (traits, specifications, key_features):

- traits:
{traits_fields},

- specifications:
{specifications_fields}, // splite text to 2-3 sections

- key_features:
{key_features_device_fields} // 3-5 key features of the device, use short phrases like "long-life battery"

IMPORTANT: RETURN VALID JSON PYTHON! If a value is not confirmed by the seller description or exact knowledge, use null.
THESE FIELDS MUST BE WITHOUT NEW LINES! 
"""


GET_DEVICE_TRAITS_BY_USER_REQUEST_PROMPT = """
Define structured fields from user prompt.

From the given information by user, fill in the following fields (ONLY DEFINED FIELDS):
- price: maximum budget in USD as a number, e.g. 800 // ONLY IF USER PROVIDED A PRICE OR BUDGET!
{traits_fields}

Set display_count only if the user asks for dual screen, two screens, second display or similar.

IMPORTANT: RETURN VALID JSON PYTHON! IF FIELD IS NOT DEFINED, DON'T RETURN IT!
THESE FIELDS MUST BE WITHOUT NEW LINES! 
"""


GET_SHORT_DEVICE_DESCRIPTION_PROMPT = """
You are a consumer tech expert.

Your task is to describe a device in simple language that normal users understand.

Rules:
- Do NOT list raw traits.
- Explain what the device is good for.
- Describe the type of user it fits.
- Mention 5 main strengths.
- Keep it short (3-5 sentences).
- Use natural marketing-style language.
- Don't show name of device.
- Use beautiful and elegant html markup, use only H1, P, B tags.
- Use ONLY facts from the input: seller description, specifications, key features, traits.
- Do not add features that are not in the input. Do not infer features from the device name.
- If the device has 2 screens (display_count 2), mention it as a main strength.

Input: the user message contains the device name, seller description, extracted specifications and seller price.

Output format:
A short user-friendly description of the device.
"""


GET_DEVICE_INFO_PROMPT = """You are a device expert. Given a device or device name, provide:
1. A short description (2-4 sentences).
2. Technical traits (bullet points or short lines). 400 characters max
3. Best for. Identify the target audience. Use list types of users like "Gamers", "Business users", "Students", "Home users", "Travelers", "Music lovers", "Video editors", "Photographers". 
4. Key advantages compared to competitors in marketing language. 
List killer 3-6 features, for example "Budget-friendly", "Long battery life", "Fast charging", "High-quality display", "Good camera", "Long battery life", "High-quality display", "Good camera", "Price".
5. Budget range. For example "Budget-friendly", "Mid-range", "Premium".

Format your response as:
DESCRIPTION:
<text>

SPECIFICATIONS:
<text>

BEST FOR:
<text>

IMPORTANT RULES:
- The total response MUST NOT exceed 1500 characters.
- If needed, shorten descriptions.
- Be concise.
- No extra commentary.
- Plain text only.
- SPECIFICATIONS should have only the key important specs (display, processor, storage, battery, etc.) - 400 characters max. 
- BEST FOR is most important.
- Do not add markdown, symbols, or explanations. Do not repeat the device name unnecessarily.
"""


RERANK_DEVICES_PROMPT = """
You filter search results for a device catalog.

The user message is JSON with "request" (what the buyer wants) and "candidates" (devices found by vector search).
Keep only candidates that satisfy every explicit requirement of the request: features (e.g. dual screen, stylus, 5G), brand, OS, budget, size.
Use name, key_features, specifications and traits of each candidate.
A similar word is not a match: "dual camera" or "dual SIM" does not satisfy "dual screen".
If the request has no hard requirements (e.g. "good phone for students"), keep candidates that fit its intent.
Order kept candidates from best to worst match.

Return JSON: {"ids": [<candidate id>, ...]}. Return {"ids": []} if nothing matches.
"""


RESEARCH_DEVICE_PROMPT = """
You research consumer devices for a marketplace catalog.
The user message is a device name. Search the web for this exact device: manufacturer site, press releases, GSMArena, trusted tech media.
Collect only facts confirmed by sources. Do not guess and do not use specs of other models.

Output format (plain text, no markdown):
FOUND: yes or no
Brand: ...
Model: ...
Release date: ...
Screens: number of physical displays and their sizes/types
Display: ...
Processor: ...
RAM: ...
Storage: ...
Camera: ...
Battery: ...
SIM: ...
OS: ...
Launch price: ...
Key features: 3-5 short phrases

Skip a line if the fact is not found.
If there are no sources about this exact device, return only "FOUND: no".
"""
