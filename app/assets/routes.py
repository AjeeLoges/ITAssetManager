from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Asset
from app.assets.forms import AssetForm
from app import db

assets = Blueprint("assets", __name__)


@assets.route("/")
@login_required
def dashboard():
    all_assets = db.session.query(Asset).order_by(Asset.id.desc()).all()

    total = len(all_assets)
    active = len([a for a in all_assets if a.status == "active"])
    in_repair = len([a for a in all_assets if a.status == "in_repair"])
    retired = len([a for a in all_assets if a.status == "retired"])

    return render_template(
        "dashboard.html",
        assets=all_assets,
        total=total,
        active=active,
        in_repair=in_repair,
        retired=retired
    )


@assets.route("/asset/create", methods=["GET", "POST"])
@login_required
def create_asset():
    form = AssetForm()

    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            serial_number=form.serial_number.data,
            status=form.status.data,
            location=form.location.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        db.session.add(asset)
        db.session.commit()
        flash("Asset created successfully.")
        return redirect(url_for("assets.dashboard"))

    return render_template("asset_form.html", form=form, asset=None)


@assets.route("/asset/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_asset(id):
    asset = db.session.get(Asset, id)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assets.dashboard"))

    is_admin = (current_user.role == "admin")
    is_owner = (asset.user_id == current_user.id)

    if not (is_admin or is_owner):
        flash("Not authorized.")
        return redirect(url_for("assets.dashboard"))

    form = AssetForm(obj=asset)
    form.asset_id = asset.id

    if form.validate_on_submit():
        asset.name = form.name.data
        asset.serial_number = form.serial_number.data
        asset.status = form.status.data
        asset.location = form.location.data
        asset.category_id = form.category_id.data

        db.session.commit()
        flash("Asset updated.")
        return redirect(url_for("assets.dashboard"))

    return render_template("asset_form.html", form=form, asset=asset)


@assets.route("/asset/<int:id>/delete", methods=["POST"])
@login_required
def delete_asset(id):
    asset = db.session.get(Asset, id)

    if not asset:
        flash("Asset not found.")
        return redirect(url_for("assets.dashboard"))

    is_admin = (current_user.role == "admin")
    is_owner = (asset.user_id == current_user.id)

    if not (is_admin or is_owner):
        flash("Not authorized.")
        return redirect(url_for("assets.dashboard"))

    db.session.delete(asset)
    db.session.commit()
    flash("Asset deleted.")
    return redirect(url_for("assets.dashboard"))
