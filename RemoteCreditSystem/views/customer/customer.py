# coding:utf-8
import hashlib

from RemoteCreditSystem import User
from RemoteCreditSystem.models.system_usage.Rcs_Customer_Information import Rcs_Customer_Information
from flask import request, render_template,flash,redirect
from flask.ext.login import login_user, logout_user, current_user, login_required
from RemoteCreditSystem import app
from RemoteCreditSystem import db
from RemoteCreditSystem.config import PER_PAGE



