from flask import render_template, flash, url_for, redirect, request
from app import app
from app.forms import AdmissionForm, BlueBadgeForm, TextInputForm # Ensure BlueBadgeForm is imported


@app.route("/")
def home():
    # Minimal home page route
    return render_template('home.html', title="Home")

@app.route("/form_success")
def form_success():
    return render_template("success.html", title="Success")

@app.route("/admission_form", methods=["GET", "POST"])
def admission_form():
    form = AdmissionForm()
    if form.validate_on_submit():
        # On valid form submission
        flash("Admission form submitted successfully!", "success")
        return redirect(url_for("home"))
    # Render the form template if GET or if validation fails
    return render_template("admission_form.html", title='Admission Form', form=form)

@app.route("/register_household_form", methods=["GET", "POST"])
def register_household_form():
    if request.method == "POST":
        return redirect(url_for("form_success"))
    return render_template("register_household_form.html", title='Register Household')

# 3. Council Tax Form
@app.route("/council_tax_form", methods=["GET", "POST"])
def council_tax_form():
    if request.method == "POST":
        return redirect(url_for("form_success"))
    return render_template("council_tax_form.html", title='Council Tax Form')

# 4. Bulky Waste Form
@app.route("/bulky_waste_form", methods=["GET", "POST"])
def bulky_waste_form():
    if request.method == "POST":
        return redirect(url_for("form_success"))
    return render_template("bulky_waste_form.html", title='Bulky Waste Form')

# 5. Housing Benefit Form
@app.route("/housing_benefit_form", methods=["GET", "POST"])
def housing_benefit_form():
    if request.method == "POST":
        return redirect(url_for("form_success"))
    return render_template("housing_benefit_form.html", title='Housing Benefit Form')

# 6. Missed Bin Report
@app.route("/missed_bin_report", methods=["GET", "POST"])
def missed_bin_report():
    if request.method == "POST":
        return redirect(url_for("form_success"))
    return render_template("missed_bin_report.html", title='Missed Bin Report')

# 7. Blue Badge Form

@app.route("/tts", methods=["GET", "POST"])
def tts():
    form = TextInputForm()
    if form.validate_on_submit():
        # You can process the form data here (e.g., save or pass to TTS logic)
        text = form.text_input.data
        # For now, just redirect back to the same page
        return redirect(url_for("tts"))
    return render_template("tts.html", form=form, title="TTS")

@app.route("/blue_badge_form", methods=["GET", "POST"])
def blue_badge_form():
    form = BlueBadgeForm()
    if form.validate_on_submit():
        test = str(form.addressLine1.data)
        flash(f"Admission form submitted successfully!"
              f"{test}", "success")

        # No additional processing required—simply redirect on POST.
        return redirect(url_for("form_success"))
    return render_template("blue_badge_form.html", title='Blue Badge Form', form=form)
# ----------------------------------------------------------------
# Error handlers
# ----------------------------------------------------------------

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404


@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500
