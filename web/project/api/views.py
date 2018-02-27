# project/api/views.py
from flask import render_template, Blueprint, request, redirect, url_for, abort, jsonify, g
from project import db, auth, auth_token, app, images
from project.models import User
from .decorators import no_cache, etag
