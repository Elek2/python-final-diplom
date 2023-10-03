import logging

# from social_core.pipeline.user import get_user

logger = logging.getLogger(__name__)


def log_social_auth_registered(request, user, *args, **kwargs):
    logger.info(f"Пользователь {user.username} успешно зарегистрирован через {kwargs['backend'].name}")


def log_social_auth_login(request, user, *args, **kwargs):
    logger.info(f"Пользователь {user.username} успешно аутентифицирован через {kwargs['backend'].name}")
