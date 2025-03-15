### **🚀 Lightweight Virtual Environment Setup for Raspberry Pi**

## **1️⃣ Create & Activate a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

## **2️⃣ Install Dependencies**
```bash
pip install --no-cache-dir -r requirements.txt
```

## **3️⃣ Verify Installation**
```bash
python -c "import cv2, flask, numpy; print('OpenCV:', cv2.__version__, 'Flask:', flask.__version__, 'NumPy:', numpy.__version__)"
```

## **4️⃣ Run Flask App**
```bash
python app.py
```
Now, open **`http://<your_raspberry_pi_ip>:5000/`** in a browser to see the video stream.

## **✅ Quick Commands Summary**
| Action | Command |
|------------|------------|
| **Create virtual environment** | `python3 -m venv venv` |
| **Activate virtual environment** | `source venv/bin/activate` |
| **Install dependencies** | `pip install --no-cache-dir -r requirements.txt` |
| **Verify installation** | `python -c "import cv2, flask, numpy; print('OpenCV:', cv2.__version__, 'Flask:', flask.__version__, 'NumPy:', numpy.__version__)"` |
| **Run Flask app** | `python app.py` |

🚀 **Now your Raspberry Pi is optimized for Flask video streaming!** 🎉