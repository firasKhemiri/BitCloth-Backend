from common.exceptions import ValidationErrorBase


class PostValidationError(ValidationErrorBase):
    MESSAGE = "Invalid post."


class InvalidDescriptionValidator(PostValidationError):
    MESSAGE = "Invalid description."
