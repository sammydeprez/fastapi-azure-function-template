import azure.functions as func
import logging
import fastapi
from routes import hello_world

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

fastapi_app = fastapi.FastAPI(
    root_path="", 
    version="v1")

fastapi_app.include_router(hello_world.router)

@app.blob_trigger(arg_name="myblob", path="mycontainer",
                               connection="AzureWebJobsStorage") 
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")

@app.function_name("http_trigger")
@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS)
async def register_apis(req: func.HttpRequest) -> func.HttpResponse:
    return await func.AsgiMiddleware(fastapi_app).handle_async(req)