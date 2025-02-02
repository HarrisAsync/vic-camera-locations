import datetime
import logging
import azure.functions as func

app = func.FunctionApp()

@app.function_name(name="MonthlyTrigger")
@app.schedule(schedule="0 0 1 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=True)
def main(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime().isoformat()
    logging.info(f"Function triggered at {utc_timestamp}")
