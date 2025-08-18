from flask import Blueprint, jsonify, request, current_app, render_template_string
from app.models import Service, db
import os
import glob
from werkzeug.utils import secure_filename

bp = Blueprint('services', __name__)

@bp.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    data = []
    for s in services:
        data.append({
            "card_id": s.card_id,
            "title": s.title,
            "img": f"/uploads/{s.img}",
            "description": s.description,
            "route": s.route,
            "fields": s.fields.split(",") if s.fields else [],
            "link": s.link
        })
    return jsonify(data)

#####################IMAGE PATH UPDATE API#################


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- 1) Simple HTML form page ----------
@bp.route('/admin/service-image', methods=['GET'])
def service_image_form():
    html = """
    <!doctype html>
    <html>
    <head>
        <title>Update Service Image</title>
        <style>
            body { font-family: sans-serif; max-width: 560px; margin: 40px auto; }
            form { border: 1px solid #ddd; padding: 16px; border-radius: 10px; }
            input, button { padding: 10px; margin: 6px 0; width: 100%; }
            small { color: #666; }
        </style>
    </head>
    <body>
        <h2>Update Service Image</h2>
        <form action="/api/services/update_image" method="POST" enctype="multipart/form-data">
            <label>Service ID</label>
            <input type="number" name="service_id" placeholder="e.g. 1" required />

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
@bp.route('/services/update_image', methods=['POST'])
def update_service_image_form():
    # Read inputs
    service_id = request.form.get('service_id', type=int)
    file = request.files.get('image')

    if not service_id:
        return jsonify({"error": "Missing service_id"}), 400
    if not file or file.filename == '':
        return jsonify({"error": "No image uploaded"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Find service by id OR by card_id (covers both schemas)
    service = Service.query.get(service_id) or Service.query.filter_by(card_id=service_id).first()
    if not service:
        return jsonify({"error": f"Service with id/card_id {service_id} not found"}), 404

    # Prepare upload dir: /uploads/services
    upload_root = current_app.config['UPLOAD_FOLDER']
    services_dir = os.path.join(upload_root, "services")
    os.makedirs(services_dir, exist_ok=True)

    # Use stable filename based on service_id
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"service_{service_id}.{ext}")
    filepath = os.path.join(services_dir, filename)

    # Remove any previous image for this service (service_1.*)
    for old in glob.glob(os.path.join(services_dir, f"service_{service_id}.*")):
        try:
            os.remove(old)
        except OSError:
            pass

    # Save new image
    file.save(filepath)

    # Store a relative path for portability (served via /uploads/…)
    relative_path = f"services/{filename}"
    service.img = relative_path  # e.g., "services/service_1.jpg"
    db.session.commit()

    # Public URL to view it:
    public_url = f"/uploads/{relative_path}"

    # If you want to redirect back to the form with a message, you can:
    # return redirect(url_for('services.service_image_form'))

    return jsonify({
        "message": "Image uploaded and service updated",
        "service_id": getattr(service, "id", None) or getattr(service, "card_id", service_id),
        "image_path": relative_path,
        "image_url": public_url
    }), 200

# ---------- 3) (Optional) Programmatic endpoint with path param ----------
@bp.route('/services/<int:service_id>/update_image', methods=['POST'])
def update_service_image_api(service_id):
    file = request.files.get('image')
    if not file or file.filename == '':
        return jsonify({"error": "No image uploaded"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    service = Service.query.get(service_id) or Service.query.filter_by(card_id=service_id).first()
    if not service:
        return jsonify({"error": "Service not found"}), 404

    upload_root = current_app.config['UPLOAD_FOLDER']
    services_dir = os.path.join(upload_root, "services")
    os.makedirs(services_dir, exist_ok=True)

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = secure_filename(f"service_{service_id}.{ext}")
    filepath = os.path.join(services_dir, filename)

    for old in glob.glob(os.path.join(services_dir, f"service_{service_id}.*")):
        try:
            os.remove(old)
        except OSError:
            pass

    file.save(filepath)

    relative_path = f"services/{filename}"
    service.img = relative_path
    db.session.commit()

    public_url = f"/uploads/{relative_path}"
    return jsonify({
        "message": "Image uploaded and service updated",
        "service_id": getattr(service, "id", None) or getattr(service, "card_id", service_id),
        "image_path": relative_path,
        "image_url": public_url
    }), 200
