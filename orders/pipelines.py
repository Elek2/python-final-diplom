import logging
# from social_core.pipeline.user import get_user

logger = logging.getLogger(__name__)

def log_social_auth_registered(request, user, *args, **kwargs):
    logger.info(f"Пользователь {user.username} успешно зарегистрирован через {kwargs['backend'].name}")

def log_social_auth_login(request, user, *args, **kwargs):
    logger.info(f"Пользователь {user.username} успешно аутентифицирован через {kwargs['backend'].name}")

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'orders.pipelines.log_social_auth_registered',  # Здесь указывайте полный путь к вашему пайплайну
    'orders.pipelines.log_social_auth_login',  # Здесь указывайте полный путь к вашему пайплайну
)