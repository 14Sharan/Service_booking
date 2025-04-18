
USER_ROLE = ((1,"Admin"),(2,"Student"),(3,"Mentor"))

ADMIN = 1
SERVICE_PROVIDER = 2
USER = 3

USER_STATUS = ((1,"Active"),(2,"Inactive"),(3,"Deleted"))

ACTIVE = 1
INACTIVE = 2
DELETED = 3


DOCUMENT_TYPES = (
    (1, 'Aadhaar Card'),
    (2, 'PAN Card'),
    (3, 'Business License'),
    (4, 'Other'),
)

# Verification status
VERIFICATION_STATUS = (
    (1, 'Pending'),
    (2, 'Verified'),
    (3, 'Rejected'),
)
PENDING = 1
VERIFIED = 2
REJECTED = 3

BOOKING_STATUS = (
    (1, 'Pending'),
    (2, 'Accepted'),
    (3, 'Rejected'),
)
PENDING = 1
ACCEPTED = 2
REJECTED = 3

