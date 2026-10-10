# Curiosity Feed

Personalized, static daily discovery feed. Mobile-first HTML with no JavaScript required for article visibility.

## Setup

1. In **Settings → Secrets and variables → Actions**, create a repository secret named `OPENAI_API_KEY` (an OpenAI API key, billed separately from ChatGPT).
2. In **Settings → Pages**, select **Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
3. Open **Actions → Daily Curiosity Feed → Run workflow**. Enable Actions if prompted.
4. Visit https://julianboyce.github.io/curiosity-feed/ and add it to your iPhone Home Screen from Safari.

The workflow runs daily at 06:15 UTC, fetches recent public Google News RSS headlines, asks the OpenAI API to select ten, and writes the homepage, JSON, and dated HTML archive. The initial `index.html` is a sample static edition and is replaced by the first successful run.

**Editorial limitation:** The model only sees headlines, not full article bodies. Summaries are necessarily headline-based and should be verified against the linked reporting. The initial sample edition is from the prior manually curated feed. API calls cost money separately from ChatGPT. Never commit credentials.
