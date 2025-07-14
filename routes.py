from flask import render_template, redirect, flash, session
from forms import RegisterForm, ProductForm, LoginForm, CommentForm
from ext import site, db
from models import Product, Comment, User
from flask_login import login_user, logout_user, login_required
import os






@site.route("/contact")
def contact_and_support():
    return render_template("contact_and_support.html")


@site.route("/all")
def all_products():
    products = Product.query.all()
    return render_template("all_products.html", products=products)

@site.route("/add_comment", methods=["GET", "POST"])
@login_required
def add_comment():
    form = CommentForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.all()]

    if form.validate_on_submit():
        new_comment = Comment(text=form.text.data, product_id=form.product_id.data)
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully!", "success")
        return redirect("/add_comment")

    return render_template("add_comment.html", form=form)

@site.route("/profile")
def profile():
    return render_template("profile.html")

@site.route("/users")
def users():
    user = User.query.filter(User.role == "Guest").all()
    return render_template("users.html", users=user)

def get_my_bag_items():
    return session.get('my_bag', [])


@site.route("/")
def home():
    role = "user"
    my_bag_items = len(get_my_bag_items())
    new_arrivals = Product.query.order_by(Product.id.desc()).limit(4).all()
    return render_template("home.html", products=new_arrivals, my_bag_items=my_bag_items)


@site.route("/my_bag")
def my_bag():
    my_bag_product_ids = get_my_bag_items()
    length = len(my_bag_product_ids)
    products = Product.query.filter(Product.id.in_(my_bag_product_ids)).all() if my_bag_product_ids else []
    total_price = sum(p.price for p in products)
    return render_template('my_bag.html', products=products, my_bag_items=length, total_price=total_price)


@site.route("/add_to_my_bag/<int:item_id>", methods=['GET', 'POST'])
def add_to_my_bag(item_id):
    my_bag = session.get('my_bag', [])
    if item_id not in my_bag:
        my_bag.append(item_id)
        session['my_bag'] = my_bag
    return redirect("/all")


@site.route("/remove_from_my_bag/<int:item_id>")
def remove_from_my_bag(item_id):
    my_bag = session.get('my_bag', [])
    if item_id in my_bag:
        my_bag.remove(item_id)
        session['my_bag'] = my_bag

    return redirect("/my_bag")





@site.route("/electric")
def electric():
    products = Product.query.filter(Product.name.ilike("%electric guitar%")).all()
    return render_template("electric.html", products=products)


@site.route("/bass")
def bass():
    products = Product.query.filter(Product.name.ilike("%Bass%")).all()
    return render_template("basses.html", products=products)


@site.route("/acoustic")
def acoustic():
    products = Product.query.filter(Product.name.ilike("%Acoustic Guitar%")).all()
    return render_template("acoustic.html", products=products)


@site.route("/classical")
def classical():
    products = Product.query.filter(Product.name.ilike("%Classical Guitar%")).all()
    return render_template("classical.html", products=products)



@site.route("/electric_guitar_amp")
def electric_guitar_amp():
    products = Product.query.filter(Product.name.ilike("%El. Guitar Amp%")).all()
    return render_template("electric_guitar_amp.html", products=products)


@site.route("/bass_amp")
def bass_amp():
    products = Product.query.filter(Product.name.ilike("%Solid State%")).all()
    return render_template("bass_amp.html", products=products)


@site.route("/acoustic_amp")
def acoustic_amp():
    products = Product.query.filter(Product.name.ilike("%Acoustic-Guitar Amplifier%")).all()
    return render_template("acoustic_amp.html", products=products)



@site.route("/electric_guitar_strings")
def electrical_guitar_strings():
    products = Product.query.filter(Product.name.ilike("%Electric-Guitar Strings%")).all()
    return render_template("electric_guitar_strings.html", products=products)


@site.route("/bass_strings")
def bass_strings():
    products = Product.query.filter(Product.name.ilike("%B-STRINGS%")).all()
    return render_template("bass_strings.html", products=products)


@site.route("/acoustic_guitar_strings")
def acoustic_strings():
    products = Product.query.filter(Product.name.ilike("%ACOUSTIC strings%")).all()
    return render_template("acoustic_guitar_strings.html", products=products)


@site.route("/classical_guitar_strings")
def classical_strings():
    products = Product.query.filter(Product.name.ilike("%classical-guitar strings%")).all()
    return render_template("classical_guitar_strings.html", products=products)


@site.route("/picks")
def picks():
    products = Product.query.filter(Product.name.ilike("%picks%")).all()
    return render_template("picks.html", products=products)


@site.route("/tuners")
def tuners():
    products = Product.query.filter(Product.name.ilike("%Tuner%")).all()
    return render_template("tuners.html", products=products)


@site.route("/straps")
def straps():
    products = Product.query.filter(Product.name.ilike("%STRAP%")).all()
    return render_template("straps.html", products=products)


@site.route("/stands")
def stands():
    products = Product.query.filter(Product.name.ilike("%GUITAR STAND%")).all()
    return render_template("stands.html", products=products)


@site.route("/processors")
def processors():
    products = Product.query.filter(Product.name.ilike("%Processor%")).all()
    return render_template("processors.html", products=products)

@site.route("/effects")
def effects():
    products = Product.query.filter(Product.name.ilike("%effect%")).all()
    return render_template("effects.html", products=products)



@site.route("/detailed/<int:product_id>")
def detailed(product_id):
    detailed_product = Product.query.get(product_id)
    comment = Comment.query.filter(Comment.product_id == product_id).all()

    return render_template("detailed.html", product=detailed_product, comments=comment)


@site.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/all")

@site.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@site.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        db.session.commit()
        return redirect("/all")

    return render_template("edit_product.html", form=form)


@site.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username is already taken. Please choose another.", "danger")
            return render_template("register.html", form=form)

        new_user = User(username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("You Registered Successfully", "success")
        return redirect("/login")

    return render_template("register.html", form=form)


@site.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

        flash("You Logged In Successfully")
        return redirect("/")
    return render_template("login.html", form=form)


@site.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@site.route("/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)
        image = form.img.data
        directory = os.path.join(site.root_path, "static", "images", image.filename)
        image.save(directory)
        new_product.img = image.filename

        db.session.add(new_product)
        db.session.commit()

        flash("You Added Product Successfully")

    return render_template("add_product.html", form=form)


