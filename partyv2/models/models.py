# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import re

_logger = logging.getLogger(__name__)  # Obtenemos el archivo donde se almacenan los LOGS


class films(models.Model):
    _name = 'partyv2.films'
    _description = 'partyv2.films'

    photo = fields.Image(max_width="6 0", max_height="150")
    name = fields.Char(string="Title")
    description = fields.Text(string="Synopsis")
    country = fields.Char()
    # genres = fields.Selection([('Horror', 'Horror'), ('Animation', 'Animation'), ('Action', 'Action'),
    #                            ('Comedy', 'Comedy'), ('Fantasy', 'Fantasy')])
    premiere_date = fields.Date(default=lambda d: fields.Date.today())
    duration = fields.Integer()
    years_old = fields.Integer(compute="_get_years", store=True)
    genre = fields.Many2many(comodel_name="partyv2.genres", relation="films_genres", column1="films_id",
                             column2="genres_id")
    language = fields.Many2many(comodel_name="partyv2.languages", relation="films_languages", column1="films_id",
                                column2="languages_id")
    directors = fields.Many2many(comodel_name="partyv2.directors", relation="films_directors", column1="films_id",
                                 column2="directors_id")
    scriptwriters = fields.Many2many(comodel_name="partyv2.scriptwriters", relation="films_scriptwriters",
                                     column1="films_id", column2="scriptwriters_id")
    producers = fields.Many2many(comodel_name="partyv2.producers", relation="films_producers", column1="films_id",
                                 column2="producers_id")
    party = fields.Many2many(comodel_name="partyv2.party", relation="party_films",
                             column1="films_id", column2="party_id")
    all_parties = fields.Many2many('partyv2.party', compute='_get_parties')

    _sql_constraints = [('title_film_uniq', 'unique(name)', 'The title already exists')]

    @api.onchange('premiere_date')
    def _get_years(self):
        for film in self:
            film.years_old = fields.Date.today().year - film.premiere_date.year

    @api.constrains('party')
    def _get_parties(self):
        for film in self:
            film.all_parties = film.party


class genres(models.Model):
    _name = 'partyv2.genres'
    _description = 'partyv2.genres'

    name = fields.Char()
    films = fields.Many2many(comodel_name="partyv2.films", relation="films_genres", column1="genres_id",
                             column2="films_id")
    musical_themes = fields.Many2many(comodel_name="partyv2.musical_themes", relation="music_genres",
                                      column1="genres_id",
                                      column2="musical_themes_id")
    _sql_constraints = [('genres_uniq', 'unique(name)', 'The Genre already exists')]


class languages(models.Model):
    _name = 'partyv2.languages'
    _description = 'partyv2.languages'

    name = fields.Char()
    country = fields.Char()
    films = fields.Many2many(comodel_name="partyv2.films", relation="films_languages", column1="languages_id",
                             column2="films_id")
    _sql_constraints = [('languages_uniq', 'unique(name)', 'The Language already exists')]


class directors(models.Model):
    _name = 'partyv2.directors'
    _description = 'partyv2.directors'

    name = fields.Char(string="Director")
    photo = fields.Image(width="100", height="100")
    films = fields.Many2many(comodel_name="partyv2.films", relation="films_directors", column1="directors_id",
                             column2="films_id")


class scriptwriters(models.Model):
    _name = 'partyv2.scriptwriters'
    _description = 'partyv2.scriptwriters'

    name = fields.Char()
    photo = fields.Image(width="20", height="20")
    films = fields.Many2many(comodel_name="partyv2.films", relation="films_scriptwriters",
                             column1="scriptwriters_id", column2="films_id")


class producers(models.Model):
    _name = 'partyv2.producers'
    _description = 'partyv2.producers'

    name = fields.Char()
    photo = fields.Image(width="20", height="20")
    films = fields.Many2many(comodel_name="partyv2.films", relation="films_producers",
                             column1="producers_id", column2="films_id")


class musical_themes(models.Model):
    _name = 'partyv2.musical_themes'
    _description = 'partyv2.musical_themes'

    name = fields.Char(string="Title")
    album = fields.Many2one('partyv2.albums')
    genres = fields.Many2many(comodel_name="partyv2.genres", relation="music_genres", column1="musical_themes_id",
                              column2="genres_id")
    premiere_date = fields.Date(default=lambda d: fields.Date.today())
    duration = fields.Float(digits=(6, 2))
    format = fields.Char()
    discography = fields.Many2one('partyv2.discographys')
    authors = fields.Many2many(comodel_name="partyv2.authors", relation="musical_authors", column1="musical_themes_id",
                               column2="authors_id")
    producers = fields.Many2many(comodel_name="partyv2.producers", relation="musical_producers",
                                 column1="musical_themes_id",
                                 column2="producers_id")
    band = fields.Many2one('partyv2.bands')


class albums(models.Model):
    _name = 'partyv2.albums'
    _description = 'partyv2.albums'

    photo = fields.Image(max_width="100", max_height="100")
    name = fields.Char(string="Title")
    premiere_date = fields.Date(default=lambda d: fields.Date.today())
    musical_themes = fields.One2many('partyv2.musical_themes', 'album')
    discography = fields.Many2one('partyv2.discographys')
    authors = fields.Many2many(comodel_name="partyv2.authors", relation="albums_authors",
                               column1="albums_id", column2="authors_id")
    all_authors = fields.Many2many('partyv2.authors', compute='_get_authors')

    @api.constrains('authors')
    def _get_authors(self):
        for album in self:
            album.all_authors = album.musical_themes.authors


class discographys(models.Model):
    _name = 'partyv2.discographys'
    _description = 'partyv2.discographys'

    name = fields.Char()
    creation_date = fields.Date(default=lambda d: fields.Date.today())
    creation_year = fields.Integer(compute="_get_year", store=True)
    musical_themes = fields.One2many('partyv2.albums', 'discography')
    album = fields.One2many('partyv2.albums', 'discography')

    _sql_constraints = [('discographys_uniq', 'unique(name)', 'This discography already exists')]

    @api.constrains('creation_date')
    def _get_year(self):
        for discography in self:
            discography.creation_year = discography.creation_date.year


class authors(models.Model):
    _name = 'partyv2.authors'
    _description = 'partyv2.authors'

    name = fields.Char()
    photo = fields.Image()
    birth = fields.Date(default=lambda d: fields.Date.today())
    birth_year = fields.Integer(compute="_get_year", store=True)
    belong_band = fields.Boolean()
    albums = fields.Many2many(comodel_name="partyv2.albums", relation="albums_authors",
                              column1="authors_id",
                              column2="albums_id")
    musical_themes = fields.Many2many(comodel_name="partyv2.albums", relation="musical_authors",
                                      column1="authors_id",
                                      column2="musical_themes_id")
    bands = fields.Many2many(comodel_name="partyv2.bands", relation="band_authors",
                             column1="authors_id",
                             column2="bands_id")

    @api.constrains('birth')
    def _get_year(self):
        for author in self:
            author.birth_year = author.birth.year


class bands(models.Model):
    _name = 'partyv2.bands'
    _description = 'partyv2.bands'

    name = fields.Char()
    photo = fields.Image(max_width=50, max_height=50)
    creation_date = fields.Date(default=lambda d: fields.Date.today())
    creation_year = fields.Integer()
    members = fields.Many2many(comodel_name="partyv2.authors", relation="band_authors",
                               column1="bands_id",
                               column2="authors_id")

    _sql_constraints = [('bands_uniq', 'unique(name)', 'This band already exists')]

    @api.onchange('creation_date')
    def _get_year(self):
        for band in self:
            band.creation_year = band.creation_date.year


class party(models.Model):
    _name = 'partyv2.party'
    _description = 'partyv2.party'

    name = fields.Char()
    date = fields.Date(default=lambda d: fields.Date.today())
    finish_date = fields.Date(default=lambda d: fields.Date.today())
    place = fields.Char()
    organicer = fields.Char()
    total = fields.Integer(compute="_total_goers", store=True)
    is_for_adults = fields.Boolean()
    goers = fields.Many2many(comodel_name="partyv2.goers", relation="party_goers", column1="party_id",
                             column2="goers_id")
    films = fields.Many2many(comodel_name="partyv2.films", relation="party_films",
                             column1="party_id", column2="films_id")
    musical_themes = fields.Many2many(comodel_name="partyv2.albums", relation="party_musical",
                                      column1="party_id",
                                      column2="musical_themes_id")

    @api.onchange('goers')
    def _total_goers(self):
        counter = 0
        for goer in party.goers:
            counter = counter + 1
        party.total = counter


    @api.onchange('goers')
    def _compute_overdue(self):
        for party in self:
            if party.is_for_adults and not party.goers.is_overdue:
                raise ValidationError('The goer is not of legal age')


class goers(models.Model):
    _name = 'partyv2.goers'
    _description = 'partyv2.goers'

    name = fields.Char()
    photo = fields.Image()
    birth_year = fields.Char()
    inscription_date = fields.Date(default=lambda d: fields.Date.today())
    is_overdue = fields.Boolean(compute='_compute_overdue', default=False, store=True)
    party = fields.Many2many(comodel_name="partyv2.party", relation="party_goers", column1="goers_id",
                             column2="party_id")

    @api.constrains('birth_year')
    def _compute_overdue(self):
        today = fields.Date.today()
        for goer in self:
            if today.year - int(goer.birth_year) >= 18:
                goer.is_overdue = True
            else:
                goer.is_overdue = False

    @api.constrains('birth_year')
    def _check_year(self):
        regex = re.compile('[0-9]{4}')
        for goer in self:
            if not regex.match(goer.birth_year):
                raise ValidationError('The year entered in the birth year field is not correct ')
