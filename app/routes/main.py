from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Campaign, ContactMessage, VolunteerApplication, Subscriber
from app.forms import ContactForm, VolunteerForm, NewsletterForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    featured_campaigns = (
        Campaign.query.filter_by(is_active=True, is_featured=True)
        .order_by(Campaign.created_at.desc())
        .limit(6)
        .all()
    )
    newsletter_form = NewsletterForm()
    return render_template("index.html", campaigns=featured_campaigns, newsletter_form=newsletter_form)


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/campaigns")
def campaigns():
    pillar = request.args.get("pillar")
    query = Campaign.query.filter_by(is_active=True)
    if pillar:
        query = query.filter_by(pillar=pillar)
    all_campaigns = query.order_by(Campaign.created_at.desc()).all()
    return render_template("campaigns.html", campaigns=all_campaigns, active_pillar=pillar)


@main_bp.route("/campaigns/<slug>")
def campaign_detail(slug):
    campaign = Campaign.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template("campaign_detail.html", campaign=campaign)


@main_bp.route("/get-involved", methods=["GET", "POST"])
def get_involved():
    form = VolunteerForm()
    if form.validate_on_submit():
        application = VolunteerApplication(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            interest=form.interest.data,
            message=form.message.data,
        )
        db.session.add(application)
        db.session.commit()
        flash("Thank you! We've received your application and will reach out soon.", "success")
        return redirect(url_for("main.get_involved"))
    return render_template("get_involved.html", form=form)


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data,
        )
        db.session.add(msg)
        db.session.commit()
        flash("Your message has been sent. We'll get back to you shortly.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html", form=form)


@main_bp.route("/donate")
def donate():
    return render_template("donate.html")


@main_bp.route("/newsletter/subscribe", methods=["POST"])
def newsletter_subscribe():
    form = NewsletterForm()
    if form.validate_on_submit():
        existing = Subscriber.query.filter_by(email=form.email.data).first()
        if existing:
            flash("You're already subscribed. Thanks for sticking with us!", "info")
        else:
            try:
                sub = Subscriber(email=form.email.data)
                db.session.add(sub)
                db.session.commit()
                flash("Subscribed! Watch your inbox for updates.", "success")
            except IntegrityError:
                db.session.rollback()
                flash("Something went wrong. Please try again.", "danger")
    else:
        flash("Please enter a valid email address.", "danger")
    return redirect(request.referrer or url_for("main.home"))