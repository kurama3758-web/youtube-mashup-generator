from flask import Flask, render_template, request
import os
import zipfile
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from mashup_logic import generate_mashup

# Load environment variables
load_dotenv()

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


@app.route("/", methods=["GET", "POST"])
def index():
    print("INSIDE INDEX FUNCTION")

    if request.method == "POST":
        try:
            print("POST REQUEST RECEIVED")

            singer = request.form["singer"]
            num_videos = int(request.form["num_videos"])
            duration = int(request.form["duration"])
            user_email = request.form["email"]

            output_file = "mashup_output.mp3"

            # Generate mashup
            print("STEP 1: Generating mashup")
            generate_mashup(singer, num_videos, duration, output_file)

            # Zip file
            print("STEP 2: Creating zip")
            zip_filename = "mashup.zip"
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                zipf.write(output_file)

            # Send email
            print("STEP 3: Sending email")

            msg = EmailMessage()
            msg["Subject"] = "Your Mashup File"
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = user_email
            msg.set_content("Attached is your mashup file.")

            with open(zip_filename, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype="application",
                    subtype="zip",
                    filename=zip_filename,
                )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)

            print("EMAIL SENT SUCCESSFULLY")

            # Cleanup
            os.remove(output_file)
            os.remove(zip_filename)

            return "Mashup sent to your email successfully!"

        except Exception as e:
            print("ERROR OCCURRED:", e)
            return f"Error: {e}"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
