import json
import datetime
import requests
import gspread

# ==== CONFIGURATION ====
OPENROUTER_API_KEY = "your_openrouter_key_here"
SHEET_NAME = "Weekly_Learning_Plan"

gc = gspread.service_account(filename="sheets_service.json")
sheet = gc.open(SHEET_NAME).sheet1

def generate_weekly_plan():
    today = datetime.date.today()
    week = today.isocalendar()[1]
    prompt = """
    You are a technical mentor for a new automation engineer in the basalt fiber industry.
    Generate a JSON weekly to-do list with 5–7 tasks that mix automation engineering
    and basalt fiber production learning. Each task should include title, description, and free resource link.
    """

    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    data = {
        "model": "mistralai/mixtral-8x7b",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    text = response.json()["choices"][0]["message"]["content"]

    try:
        plan = json.loads(text)
    except:
        plan = {"week": f"Week {week}", "tasks": [{"title": "Error", "description": text, "resource": ""}]}

    # Save to Google Sheet
    sheet.append_row([f"Week {week}", json.dumps(plan)])
    print("✅ Weekly plan generated and saved!")

if __name__ == "__main__":
    generate_weekly_plan()
