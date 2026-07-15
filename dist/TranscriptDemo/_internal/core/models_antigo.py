# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categoria(models.Model):
    categoria = models.IntegerField(primary_key=True)
    desc_categoria = models.CharField(max_length=255, blank=True, null=True)
    mark_categoria = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CATEGORIA'


class Fornecedor(models.Model):
    ean = models.CharField(db_column='EAN', primary_key=True, max_length=255)  # Field name made lowercase.
    sku_f = models.CharField(db_column='SKU_f', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao_f = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoria', blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    preco_fornecedor = models.FloatField(blank=True, null=True)
    embalagem_f = models.IntegerField(blank=True, null=True)
    preco_u_f = models.FloatField(blank=True, null=True)
    credito_icms_fornecedor = models.FloatField(blank=True, null=True)
    viab = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FORNECEDOR'


class Marca(models.Model):
    fabricante = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'MARCA'


class Oferta(models.Model):
    ean = models.OneToOneField(Fornecedor, models.DO_NOTHING, db_column='EAN', primary_key=True)  # Field name made lowercase.
    sku_f = models.CharField(max_length=255, blank=True, null=True)
    sku_r = models.CharField(max_length=255, blank=True, null=True)
    descricao_r = models.CharField(max_length=255, blank=True, null=True)
    preco_oferta = models.FloatField(blank=True, null=True)
    preco_u_tab = models.FloatField(blank=True, null=True)
    embalagem_f = models.IntegerField(blank=True, null=True)
    data_tab = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OFERTA'


class Opera(models.Model):
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='categoria', blank=True, null=True)
    log_opera = models.FloatField(blank=True, null=True)
    mark_opera = models.FloatField(db_column='Mark_opera', blank=True, null=True)  # Field name made lowercase.
    tributo_opera = models.FloatField(blank=True, null=True)
    promotor_opera = models.FloatField(blank=True, null=True)
    total_opera = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OPERA'


class Pedido(models.Model):
    num_ped = models.AutoField(primary_key=True)
    data_ped = models.DateTimeField(blank=True, null=True)
    ean = models.ForeignKey(Fornecedor, models.DO_NOTHING, db_column='EAN', blank=True, null=True)  # Field name made lowercase.
    sku_r = models.CharField(max_length=255, blank=True, null=True)
    sku_f = models.CharField(max_length=255, blank=True, null=True)
    descricao_r = models.CharField(max_length=255, blank=True, null=True)
    preco_tab = models.FloatField(blank=True, null=True)
    qnt_ped = models.IntegerField(blank=True, null=True)
    subtotal_ped = models.FloatField(blank=True, null=True)
    valortotal_ped = models.FloatField(blank=True, null=True)
    qntt_ped = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PEDIDO'


class Pesquisa(models.Model):
    ean = models.ForeignKey(Fornecedor, models.DO_NOTHING, db_column='EAN', blank=True, null=True)  # Field name made lowercase.
    preco_pesq = models.FloatField(blank=True, null=True)
    promocao_pesq = models.IntegerField(blank=True, null=True)
    local_pesq = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PESQUISA'


class Rede(models.Model):
    ean = models.OneToOneField(Fornecedor, models.DO_NOTHING, db_column='EAN', primary_key=True)  # Field name made lowercase.
    sku_r = models.CharField(db_column='SKU_r', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao_r = models.CharField(max_length=255, blank=True, null=True)
    preco_venda_r = models.FloatField(blank=True, null=True)
    preco_ultima_compra = models.FloatField(blank=True, null=True)
    contrato_r = models.FloatField(blank=True, null=True, db_comment='valores % de vantagens do Fornecedor')
    mark_r = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REDE'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CoreProduto(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    preco = models.FloatField()

    class Meta:
        managed = False
        db_table = 'core_produto'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
