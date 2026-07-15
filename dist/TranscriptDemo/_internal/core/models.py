# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Base(models.Model):
    ean = models.OneToOneField('Fornecedor', models.DO_NOTHING, db_column='EAN', primary_key=True)  # Field name made lowercase.
    ncm = models.CharField(db_column='NCM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sku_f = models.CharField(db_column='SKU_f', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao_f = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.ForeignKey('Categoria', models.DO_NOTHING, db_column='categoria', blank=True, null=True)
    industria = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    preco_custo_embalagem_f = models.FloatField(blank=True, null=True)
    preco_venda_embalagem_f = models.FloatField(blank=True, null=True)
    embalagem_f = models.IntegerField(blank=True, null=True)
    preco_unitario_f = models.FloatField(blank=True, null=True)
    estoque_f = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'BASE'


class Categoria(models.Model):
    categoria = models.IntegerField(primary_key=True)
    desc_categoria = models.CharField(max_length=255, blank=True, null=True)
    mark_categoria = models.FloatField(blank=True, null=True)
    prioridade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CATEGORIA'


class Fornecedor(models.Model):
    ean = models.CharField(db_column='EAN', primary_key=True, max_length=255)  # Field name made lowercase.
    ncm = models.CharField(db_column='NCM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sku_f = models.CharField(db_column='SKU_f', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao_f = models.CharField(max_length=255, blank=True, null=True)
    industria = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    preco_custo_embalagem_f = models.FloatField(blank=True, null=True)
    preco_venda_embalagem_f = models.FloatField(blank=True, null=True)
    embalagem_f = models.IntegerField(blank=True, null=True)
    preco_unitario_f = models.FloatField(blank=True, null=True)
    estoque_f = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'FORNECEDOR'


class Ncm(models.Model):
    ncm = models.CharField(db_column='NCM', primary_key=True, max_length=255)  # Field name made lowercase.
    descricao_n = models.CharField(max_length=255, blank=True, null=True)
    tributo_n = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'NCM'


class Oferta(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    ean = models.OneToOneField(Base, models.DO_NOTHING, db_column='EAN', blank=True, null=True)  # Field name made lowercase.
    sku_f = models.CharField(max_length=255, blank=True, null=True)
    sku_r = models.CharField(max_length=255, blank=True, null=True)
    descricao_r = models.CharField(max_length=255, blank=True, null=True)
    preco_embalagem_oferta = models.FloatField(blank=True, null=True)
    preco_unitario_oferta = models.FloatField(blank=True, null=True)
    embalagem_f = models.IntegerField(blank=True, null=True)
    data_tab = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'OFERTA'


class Opera(models.Model):
    categoria = models.OneToOneField(Categoria, models.DO_NOTHING, db_column='categoria', primary_key=True)
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
    ean = models.ForeignKey('Rede', models.DO_NOTHING, db_column='EAN', blank=True, null=True)  # Field name made lowercase.
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


class Rede(models.Model):
    ean = models.OneToOneField(Fornecedor, models.DO_NOTHING, db_column='EAN', primary_key=True)  # Field name made lowercase.
    sku_r = models.CharField(db_column='SKU_r', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao_r = models.CharField(max_length=255, blank=True, null=True)
    preco_venda_r = models.FloatField(blank=True, null=True)
    preco_ultima_compra = models.FloatField(blank=True, null=True)
    contrato_r = models.FloatField(blank=True, null=True, db_comment='valores % de vantagens do Fornecedor')
    mark_r = models.FloatField(blank=True, null=True)
    venda_diaria_r = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'REDE'
