from shift.users.choices import *
from shift.users.models import INT_FIELD, FLOAT_FIELD, BOOL_FIELD, CHOICE_FIELD

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
# The format is (field_name, field_type)
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

PUBLIC_ATTRIBUTES = (
    ('Sex', SEX_CHOICES),
    ('Age', INT_FIELD),
    ('Height', FLOAT_FIELD),
    ('Ethnicity', ETHNICITY_CHOICES),
    ('Eye Color', EYE_COLOR_CHOICES),
    ('Hair Color', HAIR_COLOR_CHOICES),
    ('Hair Length', HAIR_LENGTH_CHOICES),
    ('Nude Ready', BOOL_FIELD),
    ('Swim Ready', BOOL_FIELD),
    ('Lingerie Ready', BOOL_FIELD),
    ('Liquor Ready', BOOL_FIELD),
    ('Gaming Ready', BOOL_FIELD),
)

PRIVATE_ATTRIBUTES = (
    ('Weight', FLOAT_FIELD),
    ('Bust/Chest', FLOAT_FIELD),
    ('Cup Size', CUP_SIZE_CHOICES),
    ('Waist', FLOAT_FIELD),
    ('Hips', FLOAT_FIELD),
    ('Inseam', FLOAT_FIELD),
    ('Dress Size', FLOAT_FIELD),
)

# Contractor Roles
# These define the attributes that will be assigned to
# a contractor in a given role. The format is: 
# (role_name, attributes) The default role is applied
# to all contractors 
CONTRACTOR_ROLES = (
    ('default', (
            'Sex',
            'Age',
         )
    ),
    ('Model', (
            'Height',
            'Ethnicity',
            'Eye Color',
            'Hair Color',
            'Hair Length',
         )
    ),
    ('Server', (
            'Liquor Ready',
         )
    ),
)
