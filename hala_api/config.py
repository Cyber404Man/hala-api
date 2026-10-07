"""إعدادات HALA API"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """إعدادات التطبيق — تُقرأ من متغيرات البيئة."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    app_name: str = "HALA API"
    app_version: str = "0.1.0"
    debug: bool = False

    # API
    api_prefix: str = "/v1"
    cors_origins: list[str] = ["*"]

    # Rate Limiting
    free_tier_daily_limit: int = 100
    pro_tier_daily_limit: int = 10000

    # API Keys (للمستخدمين المدفوعين — لاحقًا DB)
    # مؤقتًا: قائمة مفاتيح ثابتة
    admin_api_key: str = "hala_admin_change_me"

    # External APIs (اختياري)
    urlscan_key: str = ""
    virustotal_key: str = ""


settings = Settings()
