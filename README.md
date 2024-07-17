# FastAPI with Azure Functions

Integrating FastAPI with Azure Functions can enhance the functionality of serverless applications, especially when you're looking to create robust APIs with Python. While FastAPI doesn't natively support Azure-specific triggers like Queue, Timer, or Blob, it's possible to set up a workaround. This involves using the Azure Functions' bindings and connecting them with FastAPI endpoints. By doing so, you can enjoy the benefits of FastAPI's features, such as automatic Swagger documentation and data validation, while also leveraging Azure Functions' powerful event-driven triggers.

## Getting Started

### Step 1 - Create a New Azure Function in VSCode

1. Open Visual Studio Code
2. Open a new folder
3. Open the *Command Palette* (Ctrl + Shift + P)
4. Choose: `Azure Function: Create Function`
5. Select: the folder where you want to add the code
6. Select: Python as your coding language
7. Select: Azure Function Model V2
8. Select: Your Python Version (ensure Python is installed on your local machine)
9. Select: `HttpTrigger` as the template
10. Choose a name for the function, e.g., `http_trigger`
11. Choose: `Anonymous` as authorization (you will need to implement your own security within your FastAPI endpoints)

![VSCode Workspace](/images/fastapi-function-1.png)

### Step 2 - Add a Trigger Function

This example uses a Blob trigger.

1. Open the *Command Palette* (Ctrl + Shift + P)
2. Choose: `Azure Function: Create Function`
3. Choose: Add `BlobTrigger` function to the main file
4. Provide a name, container (of your storage account)
5. Provide a container name (this is the container of your storage account)
6. Provide a connection string app setting variable (connection string to your storage account)

This code was added to your `function_app.py` file:

```python
@app.blob_trigger(arg_name="myblob", path="mycontainer", connection="AzureWebJobsStorage") 
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
```

### Step 3: Configure FastAPI

#### Step 3.1 - `requirements.txt`

Ensure that the FastAPI library is available by adding it to `requirements.txt`.

```text
azure-functions==1.20.0
fastapi==0.111.1
```

#### Step 3.2 - `host.json`

Update the `routePrefix` in `host.json` to remove the default `api/` prefix from your endpoints.

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    }
  },
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  },
  "extensions": {
    "http": {
      "routePrefix": ""
    }
  }
}
```

#### Step 3.3 - `function_app.py`

Add the FastAPI package:

```python
import fastapi
```

You will notice an existing `FunctionApp`:

```python
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
```

Initialize FastAPI:

```python
fastapi_app = fastapi.FastAPI(root_path="")
```

Replace the existing HTTP trigger code with the following:

```python
@app.function_name("http_trigger")
@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS)
async def register_apis(req: func.HttpRequest) -> func.HttpResponse:
    return await func.AsgiMiddleware(fastapi_app).handle_async(req)
```

### Step 4: Add a FastAPI Route

1. Create a folder `routes` in the root.
2. In that folder, create a file `hello_world.py`.
3. Add the following code to `hello_world.py`:

```python
import fastapi

router = fastapi.APIRouter()

@router.post("/hello_world")
async def chat() -> str:
    return "Hello World via POST"

@router.get("/hello_world")
async def chat() -> str:
    return "Hello World via GET"
```

Register the route in `function_app.py`:

```python
from routes import hello_world

fastapi_app = fastapi.FastAPI(
    root_path="", 
    version="v1")

fastapi_app.include_router(hello_world.router)
```

### Running and Debugging

You can now run/debug the code. Notice that no functions are added to the list. All FastAPI functions are behind the `http_trigger`.

![Running Functions](/images/fastapi-function-2.png)

### OpenAPI Documentation

FastAPI provides OpenAPI documentation out of the box. Access your endpoint at `/docs` (e.g., `http://localhost:7071/docs`).

![OpenAPI Documentation](/images/fastapi-function-4.png)

## Conclusion

By following these steps, you can successfully integrate FastAPI with Azure Functions, leveraging the strengths of both frameworks to build powerful, serverless APIs.