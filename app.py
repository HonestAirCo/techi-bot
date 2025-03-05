from flask import Flask, request, jsonify
import os
import slack_sdk

app = Flask(__name__)

SLACK_BOT_TOKEN = "xoxb-xxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxxx"
client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

data = {
    "ICP": {
        "brands": ["Comfortmaker", "Arcoaire", "Grandaire"],
        "warranty": "https://productregistration2.icpusa.com/public/ManageRegistration?brand=ICP",
        "tech_support": {
            "Eddie Golden": "901-508-1385",
            "Jared Sellers": "479-970-7249"
        },
        "distributors": ["Sanders Supply", "United Refrigeration", "Baker Distributing"]
    },
    "Goodman": {
        "warranty": "https://www.goodmanmfg.com/warranty",
        "tech_support": {
            "General": "877-254-4729",
            "Pete (Ferguson)": "615-569-9744"
        },
        "distributors": ["Ferguson (Hendersonville)", "Ferguson (Nashville)", "Johnston Supply"]
    }
}

@app.route("/slack/events", methods=["POST"])
def slack_events():
    event_data = request.json
    if "event" in event_data:
        event = event_data["event"]
        if event.get("type") == "app_mention":
            channel = event["channel"]
            user_query = event["text"].lower()

            response_message = "I couldn't find that. Try asking about a brand or distributor."

            for brand, details in data.items():
                if brand.lower() in user_query:
                    response_message = f"*{brand} Support Information:*\nWarranty: {details['warranty']}\nTech Support: {details['tech_support']}\nDistributors: {', '.join(details['distributors'])}"
                    break

            client.chat_postMessage(channel=channel, text=response_message)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
