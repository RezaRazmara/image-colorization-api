from fastapi import FastAPI,UploadFile,Request
import datetime
import uvicorn
from script import *
import cv2
from fastapi.responses import HTMLResponse,StreamingResponse,FileResponse
import os
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
def main():
    return HTMLResponse("""
        <html>
            <body>
                <form action="/upload_image" enctype="multipart/form-data" method="post">
                    <input name="file" type="file">
                    <input type="submit">
                </form>
            </body>
        </html>
    """)

@app.post("/upload_image")
async def upload_image(file: UploadFile,request: Request):
    
    data = await file.read()
    nparr = np.frombuffer(data, np.uint8)
    colorize_image(nparr)
    
    file_path  = "colorized_image.png"

    # move file to static folder
    os.rename("colorized_image.png", "static/colorized_image.png")
    

    download_link = "/static/colorized_image.png"
    return HTMLResponse(f"""
        <html>
            <body>
                <h1>Image uploaded and processed successfully!</h1>
                <p>Download the processed image: <a href="{download_link}" download>Download</a></p>
            </body>
        </html>
    """)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)