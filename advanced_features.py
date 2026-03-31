import cv2
from textblob import TextBlob
import time

def run_face_detection(save_path="patient.jpg"):
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Camera not accessible")
            return False

        detected = False
        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(100, 100)
            )

            for (x, y, w, h) in faces:
                detected = True

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                cv2.putText(
                    frame,
                    "Patient Detected",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("AI Hospital - Face Detection", frame)

            if detected:
                cv2.imwrite(save_path, frame)
                print(f"Image saved: {save_path}")
                time.sleep(1)
                break

            if time.time() - start_time > 10:
                print("No face detected")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return detected

    except Exception as e:
        print("Face Detection Error:", e)
        return False

def analyze_feedback(text):
    try:
        if not text or text.strip() == "":
            return None

        blob = TextBlob(text)

        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # Classification
        if polarity > 0.2:
            sentiment = "Positive Feedback"
            suggestion = "Keep up the excellent service!"
        elif polarity < -0.2:
            sentiment = "Negative Feedback"
            suggestion = "Needs immediate improvement!"
        else:
            sentiment = "Neutral Feedback"
            suggestion = "Service is acceptable, but can improve."

        return {
            "sentiment": sentiment,
            "polarity": round(polarity, 2),
            "subjectivity": round(subjectivity, 2),
            "suggestion": suggestion
        }

    except Exception as e:
        print("NLP Error:", e)
        return None


if __name__ == "__main__":
    print("=== TESTING ADVANCED FEATURES ===")

    sample_text = "The hospital service was very good and doctors were kind."
    result = analyze_feedback(sample_text)
    print("\nNLP Result:", result)

    print("\nStarting Face Detection...")
    run_face_detection()