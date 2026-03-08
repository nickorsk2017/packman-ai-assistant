DESCRIPTION_PROMPT = """You are a product expert.
Given a device or product name, provide a clear, concise description (2-4 sentences) suitable for a product catalog. 
Focus on what the product is, key use cases, and main audience.
Only output the description, no preamble."""

TAGS_PROMPT = """You are a product expert. Given a device or product name, optional description, and optional seller price in USD, output a short list of tags for search and filtering.
Tags must include:
- Brand name, storage size, battery capacity, color, key features, camera quality (good_camera, average_camera, etc.), budget type (budget, mid_range, premium), screen size (small, medium, large).
- Seller price e.g. price_500, price_1299 and cheap_price, premium_price, budget_price, mid_range_price.
- User type (students, gamers, business_users, home, travelers, music_lovers, video_editors, photographers).
- OS (Android, iOS).
- Condition (condition_new, condition_used, condition_refurbished, condition_like_new).
Output only the tags separated by commas, nothing else. Use underscores for multi-word tags (e.g. good_camera). Always include the seller price tag when price is provided. Example: Apple, 128GB, white, good_camera, premium, price_900"""

INFO_PROMPT = """You are a product expert. Given a device or product name, provide:
1. A short description (2-4 sentences).
2. Technical specifications (bullet points or short lines). 400 characters max
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
- Do not add markdown, symbols, or explanations. Do not repeat the product name unnecessarily.
"""
