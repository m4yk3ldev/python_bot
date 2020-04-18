from django.db import models


# Create your models here.
class Profile(models.Model):
    external_id = models.IntegerField(verbose_name="ID Telegram", unique=True)
    username = models.CharField(max_length=250, verbose_name="Username de telegram")
    name = models.CharField(max_length=250, verbose_name="Nombre del Usuario")
    email = models.CharField(max_length=250, verbose_name="Correo del Usuario", null=True)
    telefono = models.CharField(max_length=250, verbose_name="Telefono del Usuario", null=True)
    provincia = models.CharField(max_length=50, verbose_name="Povincia del Usuario", null=True)
    is_3d = models.BooleanField(verbose_name="Tiene impresora", default=False)
    cant_fdm = models.IntegerField(verbose_name="Cantidad de impresoras FDM", default=0)
    diametro_filamento = models.CharField(max_length=100, verbose_name='Diametros de filamento', null=True)
    cant_printerSLA_DLP = models.IntegerField(verbose_name='Cantidad de impresoras SLA o DLP', default=0)
    is_cnc = models.BooleanField(default=False, verbose_name='Tiene maquina CNC')
    cant_cnc = models.IntegerField(default=0, verbose_name="Cantidad de maquinas CNC")
    materiales_cnc = models.CharField(max_length=100, verbose_name='Tipo de material de CNC', null=True)
    cant_pla = models.IntegerField(default=0, verbose_name='Cantidad de PLA')
    cant_petg = models.IntegerField(default=0, verbose_name='Cantidad de PETG')
    cant_abs = models.IntegerField(default=0, verbose_name='Cantidad de ABS')
    cant_tpu = models.IntegerField(default=0, verbose_name='Cantidad de TPU')
    cant_litro_resina = models.IntegerField(default=0, verbose_name='Cantidad de Litros de Resina')
    tipo_resina = models.CharField(max_length=50, verbose_name="Tipo de Resina", null=True)
    m2_acrilico = models.IntegerField(default=0, verbose_name="Cantidad de m2 acrilico")
    espesor_acrilico = models.CharField(max_length=100, null=True, verbose_name="Espesor del acrilico")
    m2_pvc = models.IntegerField(default=0, verbose_name="M2 de PVC")
    espesor_pvc = models.CharField(max_length=100, verbose_name="Espesor del PVC", null=True)
    m2_plied_madera = models.IntegerField(default=0, verbose_name='M2 de Plied o Madera')
    espesor_plied_madera = models.CharField(verbose_name='Espesor Plied Madera', max_length=100, null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f'ID {self.external_id} username {self.username}'
