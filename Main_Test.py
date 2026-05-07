from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from deepface import DeepFace
import tempfile

app = FastAPI()

@app.post("/verify_images")
async def verify_images(
    reference_image: UploadFile = File(...),
    test_image: UploadFile = File(...)
):
    try:

        # حفظ الصورة الأولى مؤقتًا
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as ref_file:
            ref_file.write(await reference_image.read())
            ref_path = ref_file.name

        # حفظ الصورة الثانية مؤقتًا
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as test_file:
            test_file.write(await test_image.read())
            test_path = test_file.name

        # مقارنة الصور باستخدام ArcFace
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
