from flask import Blueprint
from app.models import User
from app.models import ChatHistory

bp = Blueprint("admin", __name__)

@bp.route("/admin")
def admin_dashboard():
    users = User.query.all()
    chats = ChatHistory.query.all()
 

    user_data = [{
        'id': user.id,
        'name': user.name,
        'email': user.email
    } for user in users]
        
    chat_data = [{
        'id': chat.id,
        'user_id': chat.user_id,
        'dob': chat.dob,
        'time': chat.time,
        'place': chat.place,
        'question': chat.question,
        'answer': chat.answer,
        'timestamp': chat.timestamp
    } for chat in chats]

        
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
        </style>
    </head>
    <body>
        <h1>Admin Dashboard</h1>
            
        <h2>Users</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
            </tr>
            {"".join(f"<tr><td>{user['id']}</td><td>{user['name']}</td><td>{user['email']}</td></tr>" for user in user_data)}
        </table>
            
        <h2>Chats</h2>
        <table>
            <tr>
                <th>ID</th>
                <th>User ID</th>
                <th>D.O.B</th>
                <th>Birth Place</th>
                <th>Birth Date</th>
                <th>Question</th>
                <th>Answer</th>
                <th>Created At</th>
            </tr>
            {"".join(f"<tr><td>{chat['id']}</td><td>{chat['user_id']}</td><td>{chat['dob']}</td><td>{chat['time']}</td><td>{chat['place']}</td><td>{chat['question']}</td><td>{chat['answer']}</td><td>{chat['timestamp']}</td></tr>" for chat in chat_data)}
        </table>
    </body>
    </html>
    """
   

