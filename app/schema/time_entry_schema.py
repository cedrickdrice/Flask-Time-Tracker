from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.project import Project

class TimeEntrySchema(Schema):
    """
    Schema for creating a time entry (time-in) with project and description.
    """
    project = fields.Str(required=True)
    description = fields.Str(required=True, validate=validate.Length(max=255))

    @validates('project')
    def validate_project(self, value):
        """
        Validate if the project exist
        """
        if Project.query.get(value) is None:
            raise ValidationError('Project with the given ID does not exist.')
