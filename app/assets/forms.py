from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Asset, Category
from app import db


class AssetForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    serial_number = StringField("Serial Number")

    status = SelectField(
        "Status",
        choices=[
            ("active", "Active"),
            ("in_repair", "In Repair"),
            ("retired", "Retired")
        ],
        validators=[DataRequired()]
    )

    location = StringField("Location")

    category_id = SelectField("Category", coerce=int)
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categories = db.session.query(Category).order_by(Category.name.asc()).all()

        self.category_id.choices = [(0, "Select category...")] + [(c.id, c.name) for c in categories]

        if categories and (self.category_id.data is None):
            self.category_id.data = 0

    def validate_category_id(self, category_id):
        if category_id.data == 0:
            raise ValidationError("Bitte eine Kategorie auswählen.")

    def validate_serial_number(self, serial_number):
        if serial_number.data:
            asset = db.session.query(Asset).filter_by(serial_number=serial_number.data).first()
            current_id = getattr(self, "asset_id", None)
            if asset and asset.id != current_id:
                raise ValidationError("Serial number already exists.")
