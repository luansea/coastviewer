import logging
import datetime

import flask
import matplotlib.cm
import matplotlib.colors

import datasets.jarkus
import utils

logger = logging.getLogger(__name__)


def transect(id) -> object:
    logger.info(flask.request)
    return {}


def transect_kml(id: int) -> str:
    """create a kml for a specific transect"""
    # only available on runtime
    flask.current_app.jinja_env.filters['kmldate'] = utils.kmldate
    transect = datasets.jarkus.get_transect(int(id))
    return flask.render_template("transect.kml", transect=transect)


def transect_overview() -> list:
    logger.info(flask.request)
    return []


def transect_overview_kml() -> str:
    """create an overview of all transects"""
    lines = datasets.jarkus.overview()
    return flask.render_template('lod.kml', lines=lines)


def styles(poly_alpha: float, outline: int, colormap: str) -> str:
    """return style information"""

    context = {}

    poly_alpha = int(float(poly_alpha) * 255)
    context['poly_alpha'] = '{:02X}'.format(poly_alpha)
    context['outline'] = int(outline)

    # Get a colormap based on the ?colormap parameter
    colormap_name = colormap
    colormap = matplotlib.cm.cmap_d.get(colormap_name, matplotlib.cm.viridis)
    colors = {}
    current_year = datetime.datetime.now().year
    N = matplotlib.colors.Normalize(1964, current_year + 1)
    for year in range(1964, current_year + 1):
        # call with float 0..1 (or int 0 .. 255)
        r, g, b, alpha = colormap(N(year))
        # r and b reversed in the google, don't forget to add alpha
        color = matplotlib.colors.rgb2hex((b, g, r)).replace('#', '')
        colors['year{0}'.format(year)] = color
    context['colors'] = colors
    return flask.render_template("styles.kml", context=context)