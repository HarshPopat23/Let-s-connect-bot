# Deploy on Render.com (100% Free Tier 24/7)

This setup runs your Telegram Bot 24/7 on Render's free tier, using **Groq** for fast AI generation and **Qdrant Cloud** for vector storage.

---

## Prerequisites

1. **Telegram Bot Token** from `@BotFather`.
2. **Groq API Key** from [console.groq.com](https://console.groq.com).
3. **Qdrant Cloud Cluster URL & API Key** from [cloud.qdrant.io](https://cloud.qdrant.io).

---

## 1-Click / Blueprint Deployment on Render

1. Sign in to **[Render.com](https://render.com/)** with GitHub.
2. Click **New +** $\rightarrow$ **Blueprint**.
3. Select your repository: `HarshPopat23/Let-s-connect-bot`.
4. Render will read `render.yaml` and prompt you for the secret environment variables:
   * `TELEGRAM_BOT_TOKEN`: Your Telegram Bot token.
   * `GROQ_API_KEY`: Your Groq API key (`gsk_...`).
   * `QDRANT_URL`: Your Qdrant Cloud Cluster URL (`https://...sa-east-1-0.aws.cloud.qdrant.io:6333`).
   * `QDRANT_API_KEY`: Your Qdrant Cloud API key.
5. Click **Apply**.

---

## Manual Web Service Setup (Alternative)

If setting up manually:
1. Click **New +** $\rightarrow$ **Web Service**.
2. Connect your GitHub repo `HarshPopat23/Let-s-connect-bot`.
3. Set the following:
   * **Name:** `let-s-connect-bot`
   * **Runtime:** `Python 3` (or `Docker`)
   * **Build Command:** `pip install -e . && python -c "from fastembed import TextEmbedding; TextEmbedding('BAAI/bge-small-en-v1.5', cache_dir='/tmp/fastembed', threads=1)"`
   * **Start Command:** `ollm-index && ollm`
   * **Instance Type:** `Free ($0/month)`
4. Add the Environment Variables under the **Environment** tab:
   * `TELEGRAM_BOT_TOKEN`
   * `GROQ_API_KEY`
   * `QDRANT_URL`
   * `QDRANT_API_KEY`
   * `EMBEDDING_PROVIDER` = `fastembed`
   * `FASTEMBED_MODEL` = `BAAI/bge-small-en-v1.5`
   * `FASTEMBED_THREADS` = `1`
   * `OMP_NUM_THREADS` = `1`
   * `OPENBLAS_NUM_THREADS` = `1`
   * `MKL_NUM_THREADS` = `1`
   * `FASTEMBED_CACHE_PATH` = `/tmp/fastembed`
   * `HF_HOME` = `/tmp/fastembed/hf`
   * `MODEL_EASY` = `openai/gpt-oss-20b`
   * `MODEL_STANDARD` = `openai/gpt-oss-120b`
   * `MODEL_COMPLEX` = `openai/gpt-oss-120b`
5. Click **Create Web Service**.
