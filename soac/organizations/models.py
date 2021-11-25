from django.db import models

class Org(models.Model):
    # Obligatorios
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    dpto = models.CharField(max_length=5)
    nhood = models.CharField(max_length=255)
    commune = models.CharField(max_length=3)
    areas = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    igj = models.BooleanField(default=False)

    # Opcionales
    public = models.CharField(max_length=255, default='No especificado')
    postal_code = models.CharField(max_length=10, default='No especificado')
    domain = models.CharField(max_length=255, default='No especificado')

    # ROAC
    roac = models.BooleanField(default=False)
    nota_solicitud_inscripcion = models.FileField(upload_to='Org')
    acta_libro_actas = models.FileField(upload_to='Org')
    acta_asamblea = models.FileField(upload_to='Org')
    estatuto_social = models.FileField(upload_to='Org')
    nomina_comision = models.FileField(upload_to='Org')
    dni_comision = models.FileField(upload_to='Org')
    nomina_asociados = models.FileField(upload_to='Org')
    sede_social = models.FileField(upload_to='Org')
    abl = models.FileField(upload_to='Org')
    extra = models.FileField(upload_to='Org')

    # Extras
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()
