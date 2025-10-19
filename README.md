"# kalshi-mm" 
Recommended Cursor Rules:
Rules: 
- Be concise in explanations and code.  
- Don’t be overly confident; if unsure, ask clarifying questions.  
- Prefer short suggestions over long explanations.  
- Use examples only when they help clarity.  
- When multiple approaches exist, briefly mention them and ask which is preferred.  
- Keep tone collaborative, like a lightweight assistant.  

assistant:
  style:
    - Be concise and clear.
    - If unsure, ask clarifying questions instead of guessing.
  logging:
    - Add logging only for important steps (like fetching, processing, or errors).
    - Avoid excessive per-item or low-value logs.
    - Prefer one summary log per major step or loop, not per iteration unless necessary.
    - Use emojis sparingly for clarity, not decoration.
    - Keep log messages short but informative (e.g. “Fetching events...” instead of verbose details).

Everything should work out of the box after creating a .env file containing API credentials