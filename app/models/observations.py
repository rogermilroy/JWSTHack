from peewee import (
    Model,
    CharField,
    IntegerField,
    FloatField,
    ForeignKeyField,
    BooleanField,
)
from .database import db


class MastObservation(Model):
    dataproduct_type = CharField()
    calib_level = IntegerField()
    obs_collection = CharField()
    obs_id = CharField()
    target_name = CharField()
    s_ra = FloatField()
    s_dec = FloatField()
    t_min = FloatField()
    t_max = FloatField()
    t_exptime = FloatField()
    wavelength_region = CharField()
    filters = CharField()
    em_min = FloatField()
    em_max = FloatField()
    target_classification = CharField(null=True)
    obs_title = CharField()
    t_obs_release = FloatField()
    instrument_name = CharField()
    proposal_pi = CharField()
    proposal_id = CharField()
    proposal_type = CharField()
    project = CharField()
    sequence_number = IntegerField(null=True)
    provenance_name = CharField()
    s_region = CharField()
    jpegURL = CharField()
    dataURL = CharField()
    dataRights = CharField()
    mtFlag = BooleanField()
    srcDen = FloatField(null=True)
    intentType = CharField()
    obsid = CharField()
    objID = CharField()

    class Meta:
        database = db


class DataProduct(Model):
    obsID = CharField()
    obs_id = CharField()
    description = CharField()
    type = CharField()
    dataURI = CharField()
    observation = ForeignKeyField(MastObservation, backref="data_products")

    class Meta:
        database = db


db.connect()
db.create_tables([MastObservation, DataProduct])
db.close()
