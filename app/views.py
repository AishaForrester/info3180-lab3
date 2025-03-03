from app import mail
from flask_mail import Message

from app import app
from app.forms import ContactForm
from flask import render_template, request, redirect, url_for, flash

"""

Note: The requirement.txt had dependencies that were deprecated. Also, because the Flask==2.3.2 was updated,
the other dependencies were incompatible, therefore I had to update them to the latest version. If this
code does not work on your end, please check the dependencies in the requirements.txt file and update them
accordingly.

"""

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route("/contact", methods=["Get", "Post"])
def contact():

    #creating a form object
    form = ContactForm()

    if request.method == "POST":
        if form.validate_on_submit():

            #Using the Flask-WTF way instead of the vanilla Flask way to grab data from the form object
            name = form.name.data
            email = form.email.data
            subject = form.subject.data
            message = form.message.data

                # Prepare the email
            msg = Message(subject,
                        sender=(name, email),  # Use name and email from the form for sender
                        recipients=["dummy-email@example.com"])  # Use dummy email for Mailtrap testing 

            msg.body = message

            try:
                mail.send(msg)
                flash("Message sent successfully", "success")
                return redirect(url_for("home"))  # Redirect after success
            except Exception as e:
                flash(f"An error occurred: {e}", "danger")
                print("something went wrong")
                return redirect(url_for("contact"))  # Redirect on failure

            
    return render_template("contact.html", form=form)

###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
