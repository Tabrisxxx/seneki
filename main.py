import logging
import azure.functions as func
import requests
import base64
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("ImageToBase64Function triggered.")

    try:
        req_body = req.get_json()
        image_url = req_body.get("image_url")

        if not image_url:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'image_url' parameter."}),
                status_code=400,
                mimetype="application/json"
            )

        # 下载图片
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            return func.HttpResponse(
                json.dumps({"error": "Failed to download image."}),
                status_code=400,
                mimetype="application/json"
            )

        image_bytes = response.content
        image_mime = response.headers.get("Content-Type", "image/jpeg")
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # 拼接成 data URL
        data_url = f"data:{image_mime};base64,{image_base64}"

        return func.HttpResponse(
            json.dumps({"base64_data_url": data_url}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
