from fastapi import BackgroundTasks, FastAPI, Request

from controllers.webhook_controller import handle_stripe_webhook

app = FastAPI(title="Stripe → Slack Notifier")


# Endpoint de santé minimal pour vérifier que le serveur est en ligne
@app.get("/")
def health_check() -> dict:
    return {"status": "ok"}


# Reçoit les webhooks Stripe et délègue le traitement au contrôleur
@app.post("/webhook")
async def webhook_stripe(request: Request, background_tasks: BackgroundTasks) -> dict:
    return await handle_stripe_webhook(request, background_tasks)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
