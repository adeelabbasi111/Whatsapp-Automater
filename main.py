# main.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from whatsapp_handler import WhatsApp
from campaign_manager import WhatsAppCampaignManager

if __name__ == "__main__":
    print("🔹 Initializing Automation...")
    bot = WhatsApp()
    if not bot.initialize():
        print("❌ WA Web init failed. Check browser/UI."); sys.exit(1)

    campaign = WhatsAppCampaignManager()
    print("🚀 Starting Campaign...")
    campaign.run(
        bot=bot,
        delay_min=60, delay_max=150,
        batch_limit=10,  # Set to None for full run
        retry_failed=False
    )
    print("\n📊 Summary:", campaign.summary())