# Django Import:
from django.db import models

class BaseModel(models.Model):

    # Creation data values:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Status values:
    root = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    # Model representation:
    def __str__(self) -> str:
        return f"{self.pk}"

    # Override default Delete method:
    def delete(self):
        """
            Override the default Delete method to see if the device was created by the Root user,
            if true don't change anything, otherwise change deleted value to true.
        """
        # Check if root value is True:
        if self.root == True:
            # Inform the user that the object cannot be deleted because is a root object:
            assert self.pk is not None, (
                f"{self._meta.object_name} object can't be deleted because its a root object.")
        else:
            # Change deleted value to True, to inform that object is deleted:
            self.deleted = True
            self.save()

    class Meta:
        default_permissions = ['read', 'read_write']
        permissions = []
        abstract = True


class BaseMainModel(BaseModel):

    model_name = BaseModel.__class__.__name__

    # Main model values:
    name = models.CharField(
        max_length=32,
        blank=False,
        unique=True,
        error_messages={
            'null': 'Name field is mandatory.',
            'blank': 'Name field is mandatory.',
            'unique': f'{model_name} with this name already exists.',
            'invalid': 'Enter the correct name value. It must contain 4 to 32 digits, letters and special characters -, _ or spaces.',
        },
    )
    description = models.CharField(
        max_length=256, default=f'{model_name} description.',
        error_messages={
            'invalid': 'Enter the correct description value. It must contain 8 to 256 digits, letters and special characters -, _, . or spaces.',
        },
    )

    # Model representation:
    def __str__(self) -> str:
        return f"{self.pk}: {self.name}"

    class Meta:
        default_permissions = ['read_only', 'read_write']
        permissions = []
        abstract = True


class BaseSubModel(BaseModel):

    class Meta:
        default_permissions = ['read', 'read_write']
        permissions = []
        abstract = True
