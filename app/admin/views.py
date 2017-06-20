# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .. import db
from ..models import User
from ..models import Insurance

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Department Views

@admin.route('/flights', methods=['GET', 'POST'])
@login_required
def list_users_admin():
    """
    List all Users with insurance
    """
    check_admin()

    users = User.query.all()

    return render_template('admin/users.html',
                           users=users, title="All Users")
