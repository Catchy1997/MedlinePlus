# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MedlineplusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    Causes = scrapy.Field()
    Symptoms = scrapy.Field()
    ExamsandTests = scrapy.Field()
    Treatment = scrapy.Field()
    Prognosis = scrapy.Field()
    PossibleComplications = scrapy.Field()
    WhentoContactaMedicalProfessional = scrapy.Field()
    Prevention = scrapy.Field()
    AlternativeNames = scrapy.Field()
    Images = scrapy.Field()
    url = scrapy.Field()

    HowtoPreparefortheTest = scrapy.Field()
    WhytheTestisPerformed = scrapy.Field()
    NormalResults = scrapy.Field()
    WhatAbnormalResultsMean = scrapy.Field()

    summary = scrapy.Field()
    other = scrapy.Field()
    pass
