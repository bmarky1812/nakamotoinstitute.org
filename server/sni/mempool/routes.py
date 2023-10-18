from typing import List

from flask import Blueprint, g, jsonify

from sni.extensions import db
from sni.models import BlogPost, BlogPostTranslation, BlogSeries, BlogSeriesTranslation
from sni.shared.schemas import SlugParamModel
from sni.utils.decorators import response_model

from .schemas import (
    MempoolPostIndexModel,
    MempoolPostModel,
    MempoolSeriesFullModel,
    MempoolSeriesModel,
)

blueprint = Blueprint("mempool", __name__, url_prefix="/mempool")


@blueprint.route("/", methods=["GET"])
@response_model(List[MempoolPostIndexModel])
def get_mempool_posts():
    posts = db.session.scalars(
        db.select(BlogPostTranslation)
        .join(BlogPost)
        .filter(BlogPostTranslation.locale == g.locale)
        .order_by(BlogPost.added.desc())
    ).all()
    return posts


@blueprint.route("/<string:slug>", methods=["GET"])
@response_model(MempoolPostModel)
def get_mempool_post(slug):
    post = db.first_or_404(
        db.select(BlogPostTranslation).filter_by(slug=slug, locale=g.locale)
    )
    return post


@blueprint.route("/params", methods=["GET"])
@response_model(List[SlugParamModel])
def get_mempool_params():
    posts = db.session.scalars(db.select(BlogPostTranslation)).all()
    return [{"locale": post.locale, "slug": post.slug} for post in posts]


@blueprint.route("/latest", methods=["GET"])
@response_model(MempoolPostModel)
def get_latest_mempool_post():
    post = db.first_or_404(
        db.select(BlogPostTranslation)
        .filter_by(locale=g.locale)
        .join(BlogPost)
        .order_by(BlogPost.added.desc())
    )
    return post


@blueprint.route("/series", methods=["GET"])
@response_model(List[MempoolSeriesModel])
def get_all_mempool_series():
    series = db.session.scalars(
        db.select(BlogSeriesTranslation)
        .join(BlogSeries)
        .filter(BlogSeriesTranslation.locale == g.locale)
    ).all()
    return series


@blueprint.route("/series/<string:slug>", methods=["GET"])
def get_mempool_series(slug):
    series = db.first_or_404(
        db.select(BlogSeriesTranslation).filter_by(slug=slug, locale=g.locale)
    )

    posts = db.session.scalars(
        db.select(BlogPostTranslation)
        .join(BlogPost)
        .join(BlogSeries)
        .filter(BlogPostTranslation.locale == g.locale, BlogSeries.id == series.id)
    ).all()

    response_data = MempoolSeriesFullModel(series=series, posts=posts)

    return jsonify(response_data.dict(by_alias=True))


@blueprint.route("/series/params", methods=["GET"])
@response_model(List[SlugParamModel])
def get_mempool_series_params():
    all_series = db.session.scalars(db.select(BlogSeriesTranslation)).all()
    return [{"locale": series.locale, "slug": series.slug} for series in all_series]
