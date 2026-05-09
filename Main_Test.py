from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from deepface import DeepFace
import tempfile

app = FastAPI()

# تحميل الموديل مرة واحدة عند بدء التشغيل
@app.on_event("startup")
async def load_model():
    DeepFace.build_model("ArcFace")

@app.post("/verify_images")
async def verify_images(
    reference_image: UploadFile = File(...),
    test_image: UploadFile = File(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as ref_file:
            ref_file.write(await reference_image.read())
            ref_path = ref_file.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as test_file:
            test_file.write(await test_image.read())
            test_path = test_file.name

        result = DeepFace.verify(
            img1_path=ref_path,
            img2_path=test_path,
            model_name="ArcFace",
            enforce_detection=False
        )

        return {
            "is_verified": bool(result["verified"]),
            "distance": float(result["distance"])
        }

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
