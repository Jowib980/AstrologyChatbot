from flask import Blueprint, jsonify, request, current_app, render_template_string, url_for
from app.models import Rashis, db
from werkzeug.utils import secure_filename
import os
import glob


bp = Blueprint('rashis', __name__)

@bp.route('/rashis', methods=['GET'])
def get_rashis():
    rashis = Rashis.query.all()
    data = []
    for s in rashis:
        data.append({
            "card_id": s.card_id,
            "icon": s.icon,
            "title": s.title,
            "img": url_for('uploaded_file', filename=s.img, _external=True),
            "description": s.description,
            "route": s.route,
            "short_description": s.short_description
        })
    return jsonify(data)

@bp.route('/rashi/<route>', methods=['GET'])
def get_rashi_by_route(route):
    rashi = Rashis.query.filter_by(route=route).first()
    if not rashi:
        return jsonify({"error": "Rashi not found"}), 404   
    
    return jsonify({
        "title": rashi.title,
        "img": url_for('uploaded_file', filename=rashi.img, _external=True),
        "description": rashi.description,
        "short_description": rashi.short_description
    })


##################UPDATE RASHI IMAGE PATH#########

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



# ---------- 1) Simple HTML form page ----------
@bp.route('/admin/rashis-image', methods=['GET'])
def service_image_form():
    html = """
    <!doctype html>
    <html>
    <head>
        <title>Update Rashi Image</title>
        <style>
            body { font-family: sans-serif; max-width: 560px; margin: 40px auto; }
            form { border: 1px solid #ddd; padding: 16px; border-radius: 10px; }
            input, button { padding: 10px; margin: 6px 0; width: 100%; }
            small { color: #666; }
        </style>
    </head>
    <body>
        <h2>Update Rashi Image</h2>
        <form action="/api/rashis/update_image" method="POST" enctype="multipart/form-data">
            <label>Rashi ID</label>
            <input type="number" name="rashi_id" placeholder="e.g. 1" required />

            <label>Choose Image</label>
            <input type="file" name="image" accept=".png,.jpg,.jpeg,.webp,.gif" required />

            <button type="submit">Upload & Update</button>
            <small>Allowed: png, jpg, jpeg, webp, gif (max ~8MB)</small>
        </form>
    </body>
    </html>
    """
    return render_template_string(html)

# ---------- 2) Handler for the form POST ----------
@bp.route('/rashis/update_image', methods=['POST'])
def update_rashi_image_form():
    # Read inputs
    rashi_id = request.form.get('rashi_id', type=int)
    file = request.files.get('image')

    if not rashi_id:
        return jsonify({"error": "Missing rashi_id"}), 400
    if not file or file.filename == '':
        return jsonify({"error": "No image uploaded"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Find rashi by id OR by card_id (covers both schemas)
    rashi = Rashis.query.get(rashi_id) or Rashis.query.filter_by(card_id=rashi_id).first()
    if not rashi:
        return jsonify({"error": f"Rashis with id/card_id {rashi_id} not found"}), 404

    # Prepare upload dir: /uploads/rashis
    upload_root = current_app.config['UPLOAD_FOLDER']
    rashis_dir = os.path.join(upload_root, "rashis")
    os.makedirs(rashis_dir, exist_ok=True)

    # Use stable filename based on rashi_id
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"rashi_{rashi_id}.{ext}")
    filepath = os.path.join(rashis_dir, filename)

    # Remove any previous image for this rashi (rashi_1.*)
    for old in glob.glob(os.path.join(rashis_dir, f"rashi_{rashi_id}.*")):
        try:
            os.remove(old)
        except OSError:
            pass

    # Save new image
    file.save(filepath)

    # Store a relative path for portability (served via /uploads/…)
    relative_path = f"rashis/{filename}"
    rashi.img = relative_path  # e.g., "rashis/rashi_1.jpg"
    db.session.commit()

    # Public URL to view it:
    public_url = f"/uploads/{relative_path}"

    # If you want to redirect back to the form with a message, you can:
    # return redirect(url_for('rashis.rashi_image_form'))

    return jsonify({
        "message": "Image uploaded and rashi updated",
        "rashi_id": getattr(rashi, "id", None) or getattr(rashi, "card_id", rashi_id),
        "image_path": relative_path,
        "image_url": public_url
    }), 200



# ---------- 3) (Optional) Programmatic endpoint with path param ----------
@bp.route('/rashis/<int:rashi_id>/update_image', methods=['POST'])
def update_rashi_image_api(rashi_id):
    file = request.files.get('image')
    if not file or file.filename == '':
        return jsonify({"error": "No image uploaded"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    rashi = Rashis.query.get(rashi_id) or Rashis.query.filter_by(card_id=rashi_id).first()
    if not rashi:
        return jsonify({"error": "Rashis not found"}), 404

    upload_root = current_app.config['UPLOAD_FOLDER']
    rashis_dir = os.path.join(upload_root, "rashis")
    os.makedirs(rashis_dir, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"rashi_{rashi_id}.{ext}")
    filepath = os.path.join(rashis_dir, filename)

    for old in glob.glob(os.path.join(rashis_dir, f"rashi_{rashi_id}.*")):
        try:
            os.remove(old)
        except OSError:
            pass

    file.save(filepath)

    relative_path = f"rashis/{filename}"
    rashi.img = relative_path
    db.session.commit()

    public_url = f"/uploads/{relative_path}"
    return jsonify({
        "message": "Image uploaded and rashi updated",
        "rashi_id": getattr(rashi, "id", None) or getattr(rashi, "card_id", rashi_id),
        "image_path": relative_path,
        "image_url": public_url
    }), 200
