import logging
import time
import azure.functions as func

app = func.FunctionApp()

@app.route(route="AddSubtitle", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def HttpEndpoint(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start = time.time()

    req_body = req.get_json()
    subtitle = req_body.get("subtitle")

    time.sleep(5) # Simulating 5 seconds of cpu-intensive processing
    end = time.time()
    processingTime = end - start

    return func.HttpResponse(
        f"Processing took {str(processingTime)} seconds. Translation is: {subtitle}",
        status_code=200
    )
