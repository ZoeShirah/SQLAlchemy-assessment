"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?
#
# It is a query object, to fetch the records we must use .one(),
# .all(), or .first()


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?
#
# Most tables have a one to many relationship, e.g. there are many car models
# per brand.  When there is a more complex many to many realtionship, e.g.
# a car may have parts manufactured in many different places, and each of those
# factories may make parts for many different cars, to represent this we need a
# table just for handling that realtionship: a "middle table" if there is a
# natural way to relate the tables (e.g, "parts", each part would have a
# relationship to where it was made and the make/model of the car it is for)
# or an "association table" if there is not a natural way to unify them (a family
# owns many cars, to join the family members who drive and cars they own tables
# need an association table, called DriversCars)



# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the ``id`` of "ram."
q1 = Brand.query.filter_by(brand_id='ram').all()

# Get all models with the name "Corvette" and the brand_id "che."
q2 = Model.query.filter(Model.name == 'Corvette',
                        Model.brand_id == 'che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor."
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter_by(founded = 1903).filter_by(discontinued = None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.

from sqlalchemy import or_
q7 = Brand.query.filter(or_(Brand.discontinued != None, Brand.founded < 1950)).all()

# Get any model whose brand_id is not "for."
q8 = Model.query.filter(Model.brand_id != 'for').all()


# -------------------------------------------------------------------
# Part 4: Write Functions

def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models = db.session.query(Model.name,
                              Brand.name,
                              Brand.headquarters).join(Brand).all()
    for model in models:
        print "Model:", model[0]
        print "Brand:", model[1]
        print "Headquarters:", model[2], "\n"


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""

    brands = db.session.query(Brand.name,
                              Model.name,
                              Model.year).join(Model).order_by(Brand.name).all()

    for brand in brands:
        print brand[0]
        print"\t", brand[1]
        print"\t", brand[2], "\n"



def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    return Brand.query.filter(Brand.name.ilike('%'+mystr+'%')).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year,
                              Model.year < end_year).all()
