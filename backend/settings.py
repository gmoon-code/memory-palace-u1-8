from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
CONTENT_DIR = ROOT / "content"
APBIO_DIR = CONTENT_DIR / "ap-biology"
UNIT1_DIR = APBIO_DIR / "unit-1"
UNIT2_DIR = APBIO_DIR / "unit-2"
UNIT3_DIR = APBIO_DIR / "unit-3"
UNIT4_DIR = APBIO_DIR / "unit-4"
UNIT5_DIR = APBIO_DIR / "unit-5"
UNIT6_DIR = APBIO_DIR / "unit-6"
UNIT7_DIR = APBIO_DIR / "unit-7"
UNIT8_DIR = APBIO_DIR / "unit-8"
HOST = os.getenv("MEMORY_PALACE_HOST", "0.0.0.0")
PORT = int(os.getenv("MEMORY_PALACE_PORT", "8000"))
ENV = os.getenv("MEMORY_PALACE_ENV", "development")
