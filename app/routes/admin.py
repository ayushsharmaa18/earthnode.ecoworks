import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models import AdminUser, Campaign, ContactMessage, VolunteerApplication, Subscriber
from app.forms import LoginForm, CampaignForm

admin_bp = Blueprint("admin", __name__)


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("admin.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def dashboard():
    stats = {
        "campaigns": Campaign.query.count(),
        "messages": ContactMessage.query.count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
        "volunteers": VolunteerApplication.query.count(),
        "subscribers": Subscriber.query.count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/campaigns")
@login_required
def campaign_list():
    campaigns = Campaign.query.order_by(Campaign.created_at.desc()).all()
    return render_template("admin/campaign_list.html", campaigns=campaigns)


@admin_bp.route("/campaigns/new", methods=["GET", "POST"])
@login_required
def campaign_new():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            title=form.title.data,
            slug=slugify(form.title.data),
            pillar=form.pillar.data,
            summary=form.summary.data,
            description=form.description.data,
            image_url=form.image_url.data,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data,
        )
        db.session.add(campaign)
        db.session.commit()
        flash("Campaign created.", "success")
        return redirect(url_for("admin.campaign_list"))
    return render_template("admin/campaign_form.html", form=form, mode="new")


@admin_bp.route("/campaigns/<int:campaign_id>/edit", methods=["GET", "POST"])
@login_required
def campaign_edit(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    form = CampaignForm(obj=campaign)
    if form.validate_on_submit():
        form.populate_obj(campaign)
        campaign.slug = slugify(campaign.title)
        db.session.commit()
        flash("Campaign updated.", "success")
        return redirect(url_for("admin.campaign_list"))
    return render_template("admin/campaign_form.html", form=form, mode="edit", campaign=campaign)


@admin_bp.route("/campaigns/<int:campaign_id>/delete", methods=["POST"])
@login_required
def campaign_delete(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    db.session.delete(campaign)
    db.session.commit()
    flash("Campaign deleted.", "info")
    return redirect(url_for("admin.campaign_list"))


@admin_bp.route("/messages")
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=all_messages)


@admin_bp.route("/messages/<int:message_id>/read", methods=["POST"])
@login_required
def mark_read(message_id):
    msg = ContactMessage.query.get_or_404(message_id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for("admin.messages"))


@admin_bp.route("/volunteers")
@login_required
def volunteers():
    all_applications = VolunteerApplication.query.order_by(VolunteerApplication.created_at.desc()).all()
    return render_template("admin/volunteers.html", applications=all_applications)


@admin_bp.route("/volunteers/<int:application_id>/status", methods=["POST"])
@login_required
def update_status(application_id):
    application = VolunteerApplication.query.get_or_404(application_id)
    application.status = request.form.get("status", application.status)
    db.session.commit()
    return redirect(url_for("admin.volunteers"))


@admin_bp.route("/subscribers")
@login_required
def subscribers():
    all_subscribers = Subscriber.query.order_by(Subscriber.subscribed_at.desc()).all()
    return render_template("admin/subscribers.html", subscribers=all_subscribers)