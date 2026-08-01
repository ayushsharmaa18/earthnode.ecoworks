from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Campaign, ContactMessage, VolunteerApplication, Subscriber
from app.forms import ContactForm, VolunteerForm, NewsletterForm
from sqlalchemy.exc import SQLAlchemyError

main_bp = Blueprint("main", __name__)


DATABASE_UNAVAILABLE_MESSAGE = (
    "This feature is temporarily unavailable while our data service is being configured."
)


def database_is_available():
    """Return whether persistence is configured and usable for this request."""
    return current_app.config["DATABASE_CONFIGURED"]


@main_bp.route("/")
def home():
    database_unavailable = not database_is_available()
    try:
        if database_unavailable:
            raise SQLAlchemyError()
        featured_campaigns = (
            Campaign.query.filter_by(
                is_active=True,
                is_featured=True
            )
            .order_by(Campaign.created_at.desc())
            .limit(6)
            .all()
        )
    except SQLAlchemyError:
        featured_campaigns = []
    newsletter_form = NewsletterForm()
    return render_template("Index.html", campaigns=featured_campaigns, newsletter_form=newsletter_form)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/campaigns")
def campaigns():
    pillar = request.args.get("pillar")
    database_unavailable = not database_is_available()
    try:
        if database_unavailable:
            raise SQLAlchemyError()
        query = Campaign.query.filter_by(is_active=True)
        if pillar:
            query = query.filter_by(pillar=pillar)
        all_campaigns = query.order_by(Campaign.created_at.desc()).all()
    except SQLAlchemyError:
        all_campaigns = []
        database_unavailable = True
    return render_template(
        "campaigns.html",
        campaigns=all_campaigns,
        active_pillar=pillar,
        database_unavailable=database_unavailable,
    )


@main_bp.route("/campaigns/<slug>")
def campaign_detail(slug):
    if not database_is_available():
        flash(DATABASE_UNAVAILABLE_MESSAGE, "info")
        return redirect(url_for("main.campaigns"))
    try:
        campaign = Campaign.query.filter_by(slug=slug, is_active=True).first_or_404()
    except SQLAlchemyError:
        flash(DATABASE_UNAVAILABLE_MESSAGE, "info")
        return redirect(url_for("main.campaigns"))
    return render_template("campaign_detail.html", campaign=campaign)


@main_bp.route("/get-involved", methods=["GET", "POST"])
def get_involved():
    form = VolunteerForm()
    if form.validate_on_submit():
        if not database_is_available():
            flash(DATABASE_UNAVAILABLE_MESSAGE + " Please contact us by email.", "info")
            return redirect(url_for("main.get_involved"))
        application = VolunteerApplication(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            interest=form.interest.data,
            message=form.message.data,
        )
        try:
            db.session.add(application)
            db.session.commit()
            flash("Thank you! We've received your application and will reach out soon.", "success")
        except SQLAlchemyError:
            db.session.rollback()
            flash(DATABASE_UNAVAILABLE_MESSAGE + " Please contact us by email.", "info")
        return redirect(url_for("main.get_involved"))
    return render_template("get_involved.html", form=form)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if not database_is_available():
            flash(DATABASE_UNAVAILABLE_MESSAGE + " Please email us directly.", "info")
            return redirect(url_for("main.contact"))
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data,
        )
        try:
            db.session.add(msg)
            db.session.commit()
            flash("Your message has been sent. We'll get back to you shortly.", "success")
        except SQLAlchemyError:
            db.session.rollback()
            flash(DATABASE_UNAVAILABLE_MESSAGE + " Please email us directly.", "info")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)


@main_bp.route("/donate")
def donate():
    razorpay_enabled = current_app.razorpay_client is not None
    return render_template(
        "donate.html",
        razorpay_enabled=razorpay_enabled,
        razorpay_key_id=current_app.config["RAZORPAY_KEY_ID"] if razorpay_enabled else None,
    )


@main_bp.route("/newsletter/subscribe", methods=["POST"])
def newsletter_subscribe():
    form = NewsletterForm()
    if form.validate_on_submit():
        if not database_is_available():
            flash(DATABASE_UNAVAILABLE_MESSAGE, "info")
        else:
            try:
                existing = Subscriber.query.filter_by(email=form.email.data).first()
                if existing:
                    flash("You're already subscribed. Thanks for sticking with us!", "info")
                else:
                    sub = Subscriber(email=form.email.data)
                    db.session.add(sub)
                    db.session.commit()
                    flash("Subscribed! Watch your inbox for updates.", "success")
            except (IntegrityError, SQLAlchemyError):
                db.session.rollback()
                flash(DATABASE_UNAVAILABLE_MESSAGE, "info")
    else:
        flash("Please enter a valid email address.", "danger")
    return redirect(request.referrer or url_for("main.home"))
