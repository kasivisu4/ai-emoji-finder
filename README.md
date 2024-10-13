# ai-emoji-finder
W1: Find emoji using AI Tech Stack

- SQL + Redis + FastAPI + Streamlit + Docker + Grafana/DataDog

T1: As a user, I want to find emoji that are related to the provided description so that i could use it for text messages efficiently

T2: As a developer, I want to keep the track of emojis so that i could find the trending emoji. 
- How can we know/change the most frequent accessed emojis?

T3: Monitor the performance for Transformers model b/w local vs inference API


Input Dataset:
Ex : 
🏥,hospital
🏦,bank
🏧,ATM

### API's

- /search/
description : smile 
result : 😀|😃|😄|😆

- /trending-emoji
based on user queries displays top 5 emojis
