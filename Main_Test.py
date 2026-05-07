{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7afd973d-a8f2-4f9e-9ee8-f2efe784f0cc",
   "metadata": {},
   "outputs": [],
   "source": [
    "pip install deepface\n",
    "pip install tf-keras"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c26f6677-1877-483d-a520-4bc4e9e9cd7c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import numpy as np\n",
    "import tensorflow as tf\n",
    "from tensorflow.keras.utils import to_categorical\n",
    "from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping\n",
    "from tensorflow.keras.models import Sequential\n",
    "from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization\n",
    "from tensorflow.keras.optimizers import Adam\n",
    "\n",
    "from fastapi import FastAPI, File, UploadFile\n",
    "from fastapi.responses import JSONResponse\n",
    "\n",
    "from deepface import DeepFace\n",
    "import tempfile\n",
    "\n",
    "app = FastAPI()\n",
    "\n",
    "@app.post(\"/verify_images\")\n",
    "async def verify_images(\n",
    "    reference_image: UploadFile = File(...),\n",
    "    test_image: UploadFile = File(...)\n",
    "):\n",
    "    try:\n",
    "\n",
    "        # حفظ الصورة الأولى مؤقتًا\n",
    "        with tempfile.NamedTemporaryFile(delete=False, suffix=\".jpg\") as ref_file:\n",
    "            ref_file.write(await reference_image.read())\n",
    "            ref_path = ref_file.name\n",
    "\n",
    "        # حفظ الصورة الثانية مؤقتًا\n",
    "        with tempfile.NamedTemporaryFile(delete=False, suffix=\".jpg\") as test_file:\n",
    "            test_file.write(await test_image.read())\n",
    "            test_path = test_file.name\n",
    "\n",
    "        # مقارنة الصور باستخدام ArcFace\n",
    "        result = DeepFace.verify(\n",
    "            img1_path=ref_path,\n",
    "            img2_path=test_path,\n",
    "            model_name=\"ArcFace\",\n",
    "            enforce_detection=False\n",
    "        )\n",
    "\n",
    "        return {\n",
    "            \"is_verified\": bool(result[\"verified\"]),\n",
    "            \"distance\": float(result[\"distance\"])\n",
    "        }\n",
    "\n",
    "    except Exception as e:\n",
    "        return JSONResponse(\n",
    "            content={\"error\": str(e)},\n",
    "            status_code=500\n",
    "        )"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.25"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
