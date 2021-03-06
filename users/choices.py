GENDER_CHOICES = ((1, 'Female',), (2, 'Male',),)

ETHNICITY_CHOICES = (
    ('America', (
            (1, 'Native North American'),
            (2, 'Central American'),
            (3, 'Caribbean'),
            (4, 'South American'),
        ),
    ),
    ('Europe', (
            (5, 'Western European'),
            (6, 'Scandinavian'),
            (7, 'Mediterranean'),
            (8, 'Eastern European'),
        ),        
    ),
    ('Africa', (
            (9, 'North African'),
            (10, 'Central African'),
            (11, 'South African'),
        ),        
    ),
    ('Asia', (
            (12, 'East Asian'),
            (13, 'Southeast Asian'),
            (14, 'South Asian'),
            (15, 'Middle Eastern'),
        )        
    ),
    ('Oceania', (
            (16, 'Australasian'),
        )        
    ),
    (17, 'Mixed'),
    (18, 'Other'),
)

HAIR_COLOUR_CHOICES = (
    (1, 'Blonde'),
    (2, 'Red'),
    (3, 'Brown'),
    (4, 'Black'),
    (5, 'Grey/White'),
    (6, 'Other'),
)

HAIR_LENGTH_CHOICES = (
    (1, 'Short'),
    (2, 'Medium'),
    (3, 'Long'),
)

EYE_COLOUR_CHOICES = (
    (1, 'Black'),
    (2, 'Brown'),
    (3, 'Hazel'),
    (4, 'Green'),
    (5, 'Blue'),
    (6, 'Other'),
)

SKIN_COLOUR_CHOICES = (
    (1, 'Dark Brown'),
    (2, 'Brown'),
    (3, 'Tan'),
    (4, 'Olive'),
    (5, 'White'),
)

_cup_sizes = ('AA', 'A', 'B', 'C', 'D', 'DD', 'E', 'EE', 'F', 'FF',
              'G', 'GG', 'H', 'HH',)

CUP_SIZE_CHOICES = tuple(zip(range(1, len(_cup_sizes)), _cup_sizes))


_jacket_sizes = map(str, range(32, 62, 2))

JACKET_SIZE_CHOICES = tuple(zip(range(1, len(_jacket_sizes)), _jacket_sizes))

_dress_sizes = ['00'] + [str(n) for n in range(0, 20)]

DRESS_SIZE_CHOICES = tuple(zip(range(1, len(_dress_sizes)), _dress_sizes))
