from shift.users.choices import *

MAX_CANDIDATES = 10

CHAR_FIELD = 'char'
INT_FIELD = 'int'
FLOAT_FIELD = 'float'
BOOL_FIELD = 'bool'
CHOICE_FIELD = 'choice'

# Groups:
# These define the django.contrib.auth groups that are
# used to differentiate between manager roles and by 
# user types. The format is (group_name, permissions)
# where a permission is defined as (app_name, model)
# which gives that group full admin control of a given
# model. If no model is provided, they get access to the
# entire app's models
GROUPS = (
    ('clientmanager', (
            ('users', 'client'),
            ('jobs', 'job'),
            ('jobs', 'shift'),
        )
    ),
    ('talentmanager', (
            ('users', 'contractor'),
        )
    ),
    ('shiftleader', (
            ('jobs', ''),
        )
    ),
    ('contractor', ()),
    ('client', ()),
)

# Attributes:
# The format is (attr_set_name, ((field_name, field_type),))
# If the field has discrete choices (sex, eye color, etc)
# then the field_type should be a choices list in the
# same format that django uses for model fields: i.e.
# ( (1, 'Female'), 
#   (2, 'Male'), )

# Attributes defined in PUBLIC_ATTRIBUTES can be set
# and seen by clients when they create a job, while
# PRIVATE attributes

# Note: if the lowercase and space->underscore version of
# a field name exists as a property on the Contractor model,
# it will be used when performing filters

ATTRIBUTES = (
    ('General', (
            ('Gender', GENDER_CHOICES),
            ('Age', INT_FIELD),
        ),
    ),
    ('Measurements', (
            ('Height', FLOAT_FIELD),
            ('Weight', FLOAT_FIELD),
            ('Bust', FLOAT_FIELD),
            ('Cup Size', CUP_SIZE_CHOICES),
            ('Waist', FLOAT_FIELD),
            ('Hips', FLOAT_FIELD),
            ('Inseam', FLOAT_FIELD),
            ('Jacket Size', JACKET_SIZE_CHOICES),
            ('Sleeve Length', FLOAT_FIELD),
            ('Neck', FLOAT_FIELD),
            ('Chest', FLOAT_FIELD),
            ('Dress Size', FLOAT_FIELD),
            ('Shoe Size', FLOAT_FIELD),
        ),
    ), 
    ('Physical', (
            ('Ethnicity', ETHNICITY_CHOICES),
            ('Skin Colour', SKIN_COLOUR_CHOICES),
            ('Eye Colour', EYE_COLOUR_CHOICES),
            ('Hair Colour', HAIR_COLOUR_CHOICES),
            ('Hair Length', HAIR_LENGTH_CHOICES),
        ),
    ),
    ('Qualifications', (
            ('Nude Ready', BOOL_FIELD),
            ('Swimwear Ready', BOOL_FIELD),
            ('Lingerie Ready', BOOL_FIELD),
            ('Liquor Ready', BOOL_FIELD),
            ('Gaming Ready', BOOL_FIELD),
            ('Acting Experience', BOOL_FIELD),
            ('Dance Experience', BOOL_FIELD),
            ('Access to Vehicle', BOOL_FIELD),
            ('Education', CHAR_FIELD),
        ),
    ),
)




MALE_ONLY_ATTRIBUTES = ('Chest', 'Neck', 'Inseam', 'Jacket Size', 'Sleeve Length')
FEMALE_ONLY_ATTRIBUTES = ('Bust', 'Hips', 'Cup Size', 'Dress Size',)


# Contractor Roles
# These define the attributes that will be assigned to
# a contractor in a given role. The format is: 
# (role_name, attributes) The default role is applied
# to all contractors 
CONTRACTOR_ROLES = (
    ('Fashion', (
            'Gender',
            'Age',
            'Height',
            'Weight',
            'Bust',
            'Chest',
            'Cup Size',
            'Waist',
            'Hips',
            'Inseam',
            'Jacket Size',
            'Dress Size',
            'Shoe Size',
            'Ethnicity',
            'Skin Colour',
            'Eye Colour',
            'Hair Colour',
            'Hair Length',
            'Nude Ready',
            'Swimwear Ready',
            'Lingerie Ready',
            'Liquor Ready',
            'Gaming Ready',
            'Acting Experience',
            'Dance Experience',
            'Access to Vehicle',
            'Education',
        )
    ),
    ('Nightlife', (
            'Gender',
            'Age',
            'Height',
            'Bust',
            'Chest',
            'Cup Size',
            'Waist',
            'Hips',
            'Inseam',
            'Jacket Size',
            'Dress Size',
            'Shoe Size',
            'Ethnicity',
            'Eye Colour',
            'Hair Colour',
            'Hair Length',
            'Swimwear Ready',
            'Lingerie Ready',
            'Liquor Ready',
            'Gaming Ready',
            'Acting Experience',
            'Dance Experience',
            'Access to Vehicle',
            'Education',
         )
    ),
    ('Promo/Sales', (
            'Gender',
            'Age',
            'Jacket Size',
            'Dress Size',
            'Shoe Size',
            'Ethnicity',
            'Eye Colour',
            'Hair Colour',
            'Hair Length',
            'Swimwear Ready',
            'Lingerie Ready',
            'Liquor Ready',
            'Gaming Ready',
            'Acting Experience',
            'Dance Experience',
            'Access to Vehicle',
            'Education',
        )
    ),
    ('Flyers', (
            'Gender',
            'Jacket Size',
            'Dress Size',
            'Shoe Size',
            'Ethnicity',
            'Swimwear Ready',
            'Liquor Ready',
            'Gaming Ready',
            'Access to Vehicle',
            'Education',
        )
    ),
)

ATTRIBUTE_WEIGHTS = (
    ('Gender', 1),
    ('Age', 1),
    ('Height', 1),
    ('Weight', 1),
    ('Bust', 1),
    ('Cup Size', 1),
    ('Waist', 1),
    ('Hips', 1),
    ('Inseam', 1),
    ('Jacket Size', 1),
    ('Sleeve Length', 1),
    ('Neck', 1),
    ('Chest', 1),
    ('Dress Size', 1),
    ('Shoe Size', 1),
    ('Ethnicity', 1),
    ('Skin Colour', 1),
    ('Eye Colour', 1),
    ('Hair Colour', 1),
    ('Hair Length', 1),
    ('Nude Ready', 1),
    ('Swimwear Ready', 1),
    ('Lingerie Ready', 1),
    ('Liquor Ready', 1),
    ('Gaming Ready', 1),
    ('Acting Experience', 1),
    ('Dance Experience', 1),
    ('Access to Vehicle', 1),
    ('Education', 1),
)


_ATTR_MAP = {}
for grp_name, attrs in ATTRIBUTES:
    for attr in attrs:
        _ATTR_MAP[attr[0]] = (grp_name, attr[1])
        
def attr_info(attr):
    "returns (group_name, field_type)"
    return _ATTR_MAP.get(attr, None)

_ATTR_WEIGHTS = {}
for field_name, weight in ATTRIBUTE_WEIGHTS:
    _ATTR_WEIGHTS[field_name] = weight
    
def attr_weight(attr):
    return _ATTR_WEIGHTS.get(attr, None)
