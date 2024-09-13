from langchain.tools import BaseTool
import requests
import json

class ImageCaptionTool(BaseTool):
    name = "Image captioner"
    description = "Use this tool when given the path to an image that you would like to be described. " \
                  "It will return a simple caption describing the image."

    def _run(self, img_path):
        try:
            with open(img_path, 'rb') as image_file:
                api_url = "https://copilot5.p.rapidapi.com/copilot"
                api_key = "93cbb16e85mshd7eae7b8414948dp11ff2cjsne8b79ba01cb3"  # Updated API key

                # Optional: If you need to upload the image somewhere to get a URL, do that here.
                # Otherwise, if the API directly accepts image bytes, adjust accordingly.

                payload = {
                    "message": "Describe this image",
                    "conversation_id": None,
                    "tone": "BALANCED",
                    "markdown": False,
                    "photo_url": None  # If the image needs to be a URL, update this field
                }
                headers = {
                    "Content-Type": "application/json",
                    "x-rapidapi-host": "copilot5.p.rapidapi.com",
                    "x-rapidapi-key": api_key
                }

                response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    caption = response.json().get("data", {}).get("message", "No caption returned")  # Adjust to extract the 'message'
                else:
                    caption = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            caption = f"Error loading image or contacting API: {e}"

        return caption

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")


class ObjectDetectionTool(BaseTool):
    name = "Object detector"
    description = "Use this tool when given the path to an image that you would like to detect objects. " \
                  "It will return a list of all detected objects. Each element in the list is in the format: " \
                  "[x1, y1, x2, y2] class_name confidence_score."

    def _run(self, img_path):
        try:
            with open(img_path, 'rb') as image_file:
                api_url = "https://copilot5.p.rapidapi.com/copilot"
                api_key = "93cbb16e85mshd7eae7b8414948dp11ff2cjsne8b79ba01cb3"  # Updated API key

                # Optional: Same as above, if you need to process the image into a URL or another format.

                payload = {
                    "message": "Detect objects in this image",
                    "conversation_id": None,
                    "tone": "BALANCED",
                    "markdown": False,
                    "photo_url": None  # Update this if you need a URL
                }
                headers = {
                    "Content-Type": "application/json",
                    "x-rapidapi-host": "copilot5.p.rapidapi.com",
                    "x-rapidapi-key": api_key
                }

                response = requests.post(api_url, headers=headers, data=json.dumps(payload))

                if response.status_code == 200:
                    detections = response.json().get("data", {}).get("message", "No detections returned")  # Adjust based on response format
                else:
                    detections = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            detections = f"Error loading image or contacting API: {e}"

        return detections

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")
