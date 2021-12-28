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
    igj = models.CharField(default='No', max_length=10)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length = 255)

    # Opcionales
    public = models.CharField(max_length=255, default='No especificado')
    postal_code = models.CharField(max_length=255, default='No especificado')
    domain = models.CharField(max_length=255, default='No especificado')

    # ROAC
    roac = models.CharField(default='No', max_length=10)
    doc = models.FileField(default='', upload_to='roac/doc/',)
    msg = models.CharField(max_length=255, default='', null=True, blank=True)

    # nota_solicitud_inscripcion = models.FileField(default='', upload_to='roac/nota_solicitud_inscripcion/',)
    # acta_libro_actas = models.FileField(default='', upload_to='roac/acta_libro_actas/')
    # acta_asamblea = models.FileField(default='', upload_to='roac/acta_asamblea')
    # estatuto_social = models.FileField(default='', upload_to='roac/estatuto_social')
    # nomina_comision = models.FileField(default='', upload_to='roac/nomina_comision')
    # dni_comision = models.FileField(default='', upload_to='roac/dni_comision')
    # nomina_asociados = models.FileField(default='', upload_to='roac/nomina_asociados')
    # sede_social = models.FileField(default='', upload_to='roac/sede_social')
    # abl = models.FileField(default='', upload_to='roac/abl')
    # extras = models.FileField(default='', upload_to='roac/extras')

    # Extras
    state = models.CharField(max_length=255, default='no-registrada') # no-registrada pre-activa, firmar, activa, suspendida, editar
    created= models.DateTimeField(auto_now_add=True, null=True)
    registration_request= models.DateTimeField(null=True)
    enrolled = models.DateTimeField(null=True)
    renoved = models.DateTimeField(null=True)
    expiration = models.DateTimeField(null=True)
    modified = models.DateTimeField(null=True)
    # no-registrada <-> preactiva
    # editar <-> pre-activa
    # pre-activa <-> firmar
    # firmar -> activa
    # activa -> suspendida
