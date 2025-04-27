from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.transformer import Transformer
import pandas as pd
import os

DATA_DIR = "./data/uploads"
OUTPUT_FILE = "./data/output/output.csv"

scheduler = BackgroundScheduler()

def scheduled_report_generation():
    input_path = os.path.join(DATA_DIR, "input.csv")
    reference_path = os.path.join(DATA_DIR, "reference.csv")

    if not os.path.exists(input_path) or not os.path.exists(reference_path):
        print("[Scheduler] Skipping: input/reference file missing")
        return

    input_df = pd.read_csv(input_path)
    reference_df = pd.read_csv(reference_path)
    transformer = Transformer()
    output_df = transformer.apply_transformations(input_df, reference_df)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print("[Scheduler] Report generated successfully.")

def start_scheduler():
    trigger = CronTrigger.from_crontab("0 * * * *")  # Every hour
    scheduler.add_job(scheduled_report_generation, trigger)
    scheduler.start()
    print("[Scheduler] Started with hourly job.")
