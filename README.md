# AI API Proxy

This application provides a proxy for the OpenAI and Vertex AI APIs. It's designed to be deployed to Cloud Run and includes a Dockerfile for easy containerization.

## Features

* Proxies requests to both the OpenAI and Vertex AI APIs.
* Uses FastAPI for a modern and efficient backend.
* Leverages Google Cloud's authentication system for secure access to Vertex AI.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Build the Docker image:**
```bash
docker build -t ai-api-proxy .
```

## Running locally

```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

This will start the application locally. Remember to update the proxy URLs in `app.py` if needed.

## Deployment to Cloud Run

1. **Build and push the Docker image to Google Container Registry:**
```bash
# Replace PROJECT_ID with your Google Cloud project ID
docker tag ai-api-proxy gcr.io/PROJECT_ID/ai-api-proxy
docker push gcr.io/PROJECT_ID/ai-api-proxy
```

2. **Deploy to Cloud Run:**
```bash
# Replace SERVICE_NAME with your desired Cloud Run service name
gcloud run deploy SERVICE_NAME \
--image gcr.io/PROJECT_ID/ai-api-proxy \
--region us-central1 \
--platform managed \
--allow-unauthenticated
```

**Note:** The `--allow-unauthenticated` flag is for demonstration purposes only. In a production environment, you should configure authentication and authorization appropriately.

## Usage

Once deployed, you can send requests to the proxy's endpoint, which will be provided by Cloud Run. The proxy will forward your requests to the corresponding API based on the URL path.

**Example:**

```
# OpenAI API request
POST https://your-cloud-run-url/openai/v1/completions

# Vertex AI API request
POST https://your-cloud-run-url/vertexai/v1/projects/your-project-id/locations/us-central1/publishers/google/models/text-bison@001:generateText
```

## Configuration

You can adjust the following settings in `app.py`:

* `OPENAI_API_URL`: Base URL for the OpenAI API.
* `VERTEX_API_URL`: Base URL for the Vertex AI API.
* `Authorization` header: Currently using a placeholder. You'll need to update this with your actual OpenAI API key.

## Security Considerations

* **API Keys:** Do not hardcode API keys directly in the code. Use environment variables or a secure secret management system.
* **Authentication and Authorization:** Implement proper authentication and authorization mechanisms to control access to your API proxy.
* **Input Validation:** Sanitize and validate all user inputs to prevent vulnerabilities like SQL injection or cross-site scripting.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or bug reports.
