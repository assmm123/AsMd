# Project - API Documentation
![Language](https://img.shields.io/badge/Language-Multi-file-green)
![Functions](https://img.shields.io/badge/Functions-127-blue)
---
## الدوال
### `analyze_file(filepath)`
- السطر: 429
- القيمة المرجعة: نعم
- الوصف: تحليل ملف برمجي واستخراج هيكله

Args:
    filepath: مسار الملف

Returns:
    قاموس بنتيجة التحليل
---
### `analyze_directory(directory)`
- السطر: 484
- القيمة المرجعة: نعم
- الوصف: تحليل مجلد كامل

Args:
    directory: مسار المجلد

Returns:
    قاموس بإحصائيات المجلد
---
### `analyze(self)`
- السطر: 47
- القيمة المرجعة: نعم
- الوصف: تحليل كامل
---
### `analyze(self)`
- السطر: 222
- القيمة المرجعة: نعم
- الوصف: تحليل كامل
---
### `analyze(self)`
- السطر: 320
- القيمة المرجعة: نعم
---
### `analyze(self)`
- السطر: 353
- القيمة المرجعة: نعم
---
### `analyze(self)`
- السطر: 383
- القيمة المرجعة: نعم
---
### `analyze(self)`
- السطر: 410
- القيمة المرجعة: نعم
---
### `generate_readme_advanced(analysis, style, language, project_name, description, author, repo_url, license_type)`
- السطر: 58
- القيمة المرجعة: نعم
---
### `generate_api_docs_advanced(analysis, style, language)`
- السطر: 95
- القيمة المرجعة: نعم
---
### `generate_wiki(analysis, language)`
- السطر: 133
- القيمة المرجعة: نعم
---
### `generate_changelog(analysis, version)`
- السطر: 190
- القيمة المرجعة: نعم
---
### `generate_all_docs(source_code, analysis, project_name, style, language, doc_types)`
- السطر: 246
- القيمة المرجعة: نعم
---
### `get_quality_report(docs)`
- السطر: 260
- القيمة المرجعة: نعم
---
### `get_badge(label, message, color)`
- السطر: 10
- القيمة المرجعة: نعم
---
### `get_table(headers, rows)`
- السطر: 14
- القيمة المرجعة: نعم
---
### `get_code_block(code, language)`
- السطر: 22
- القيمة المرجعة: نعم
---
### `get_alert(text, alert_type)`
- السطر: 26
- القيمة المرجعة: نعم
---
### `get_section(title, content, level)`
- السطر: 32
- القيمة المرجعة: نعم
---
### `check_readme(content)`
- السطر: 38
- القيمة المرجعة: نعم
---
### `get_engine(keys_file)`
- السطر: 223
- القيمة المرجعة: نعم
---
### `get_key(self)`
- السطر: 61
- القيمة المرجعة: نعم
---
### `mark_success(self, key, tokens)`
- السطر: 87
- القيمة المرجعة: لا
---
### `mark_failure(self, key, error)`
- السطر: 94
- القيمة المرجعة: لا
---
### `get_stats(self)`
- السطر: 105
- القيمة المرجعة: نعم
---
### `print_report(self)`
- السطر: 124
- القيمة المرجعة: لا
---
### `chat(self, messages, model, temperature, max_tokens)`
- السطر: 159
- القيمة المرجعة: نعم
---
### `generate_docs(self, code, language, doc_type)`
- السطر: 205
- القيمة المرجعة: نعم
---
### `validate_username(username)`
- السطر: 5
- القيمة المرجعة: نعم
---
### `validate_email(email)`
- السطر: 14
- القيمة المرجعة: نعم
---
### `validate_password(password)`
- السطر: 21
- القيمة المرجعة: نعم
---
### `detect_language(filename)`
- السطر: 28
- القيمة المرجعة: نعم
- الوصف: تحديد لغة البرمجة من امتداد الملف
---
### `validate_file_extension(filename)`
- السطر: 65
- القيمة المرجعة: نعم
- الوصف: التحقق من أن امتداد الملف مسموح به
---
### `validate_file_size(content, max_size)`
- السطر: 71
- القيمة المرجعة: نعم
- الوصف: التحقق من أن حجم الملف تحت الحد المسموح
---
### `validate_file_content(content)`
- السطر: 77
- القيمة المرجعة: نعم
- الوصف: التحقق من أن المحتوى خالي من تهديدات
---
### `sanitize_filename(filename)`
- السطر: 86
- القيمة المرجعة: نعم
- الوصف: تنظيف اسم الملف من المسارات الخطيرة
---
### `validate_file(filename, content)`
- السطر: 98
- القيمة المرجعة: نعم
- الوصف: التحقق الكامل من الملف
---
### `get_file_stats(filepath)`
- السطر: 104
- القيمة المرجعة: نعم
- الوصف: الحصول على إحصائيات الملف
---
### `sanitize_text(text, max_length)`
- السطر: 57
- القيمة المرجعة: نعم
- الوصف: تنظيف النص العام

Args:
    text: النص المراد تنظيفه
    max_length: أقصى طول مسموح

Returns:
    (النص المنظف, قائمة التحذيرات)
---
### `sanitize_filename(filename)`
- السطر: 89
- القيمة المرجعة: نعم
- الوصف: تنظيف اسم الملف

Args:
    filename: اسم الملف

Returns:
    (الاسم المنظف, تحذيرات)
---
### `sanitize_code(code, max_length)`
- السطر: 133
- القيمة المرجعة: نعم
- الوصف: تنظيف الكود البرمجي

Args:
    code: الكود
    max_length: أقصى طول

Returns:
    (الكود المنظف, تحذيرات)
---
### `sanitize_url(url)`
- السطر: 160
- القيمة المرجعة: نعم
- الوصف: تنظيف الرابط
---
### `detect_threats(text)`
- السطر: 182
- القيمة المرجعة: نعم
- الوصف: كشف التهديدات في النص

Returns:
    قاموس بنوع التهديد وخطورته
---
### `deep_clean(text, max_length)`
- السطر: 217
- القيمة المرجعة: نعم
- الوصف: تنظيف عميق - يستخدم قبل التخزين أو العرض

Args:
    text: النص الخام
    max_length: أقصى طول

Returns:
    نص نظيف وآمن
---
### `get_limiter()`
- السطر: 84
- القيمة المرجعة: نعم
---
### `check_rate_limit(ip)`
- السطر: 87
- القيمة المرجعة: نعم
---
### `check(self, ip)`
- السطر: 33
- القيمة المرجعة: نعم
---
### `get_stats(self, ip)`
- السطر: 64
- القيمة المرجعة: نعم
---
### `reset(self, ip)`
- السطر: 76
- القيمة المرجعة: لا
---
### `hash_data(data, salt)`
- السطر: 123
- القيمة المرجعة: نعم
---
### `verify_hash(data, hash_value, salt)`
- السطر: 129
- القيمة المرجعة: نعم
---
### `generate_token(length)`
- السطر: 133
- القيمة المرجعة: نعم
---
### `encrypt(self, plaintext)`
- السطر: 40
- القيمة المرجعة: نعم
- الوصف: تشفير النص باستخدام Fernet
---
### `decrypt(self, ciphertext)`
- السطر: 46
- القيمة المرجعة: نعم
- الوصف: فك التشفير - يجرب Fernet أولاً ثم XOR للترحيل من البيانات القديمة
---
### `needs_reencryption(self, ciphertext)`
- السطر: 67
- القيمة المرجعة: نعم
- الوصف: هل البيانات مشفرة بـ XOR وتحتاج ترقية إلى Fernet؟
---
### `reencrypt(self, ciphertext)`
- السطر: 77
- القيمة المرجعة: نعم
- الوصف: ترقية بيانات قديمة من XOR إلى Fernet
---
### `store(self, name, value)`
- السطر: 94
- القيمة المرجعة: لا
- الوصف: تخزين قيمة مشفرة بـ Fernet
---
### `retrieve(self, name)`
- السطر: 98
- القيمة المرجعة: نعم
- الوصف: استرجاع وفك تشفير قيمة
---
### `rotate_key(self, new_secret)`
- السطر: 103
- القيمة المرجعة: لا
- الوصف: تدوير المفتاح - إعادة تشفير كل المخزن بمفتاح جديد
---
### `upgrade_all(self)`
- السطر: 112
- القيمة المرجعة: لا
- الوصف: ترقية كل البيانات المخزنة من XOR إلى Fernet
---
### `track_request(self)`
- السطر: 7
- القيمة المرجعة: لا
---
### `track_error(self)`
- السطر: 10
- القيمة المرجعة: لا
---
### `get_stats(self)`
- السطر: 13
- القيمة المرجعة: نعم
---
### `analyze_and_generate(self, doc_types, language)`
- السطر: 56
- القيمة المرجعة: نعم
---
### `analyze(self, language)`
- السطر: 59
- القيمة المرجعة: نعم
---
### `get_logger(name, env)`
- السطر: 73
- القيمة المرجعة: نعم
---
### `format(self, record)`
- السطر: 23
- القيمة المرجعة: نعم
---
### `debug(self, msg)`
- السطر: 62
- القيمة المرجعة: لا
---
### `info(self, msg)`
- السطر: 63
- القيمة المرجعة: لا
---
### `warning(self, msg)`
- السطر: 64
- القيمة المرجعة: لا
---
### `error(self, msg)`
- السطر: 65
- القيمة المرجعة: لا
---
### `critical(self, msg)`
- السطر: 66
- القيمة المرجعة: لا
---
### `get_stats(self)`
- السطر: 68
- القيمة المرجعة: نعم
---
### `export_docs(docs, metadata)`
- السطر: 222
- القيمة المرجعة: نعم
- الوصف: دالة مساعدة سريعة
---
### `export_markdown(self, doc_type)`
- السطر: 52
- القيمة المرجعة: نعم
- الوصف: تصدير Markdown خام
---
### `export_all_markdown(self)`
- السطر: 56
- القيمة المرجعة: نعم
- الوصف: دمج كل الملفات في Markdown واحد
---
### `export_html(self, doc_type)`
- السطر: 64
- القيمة المرجعة: نعم
- الوصف: تحويل Markdown لـ HTML مع CSS مدمج
---
### `export_all_html(self)`
- السطر: 90
- القيمة المرجعة: نعم
- الوصف: تصدير كل الملفات كـ HTML واحد
---
### `export_pdf(self, doc_type, output_path)`
- السطر: 117
- القيمة المرجعة: نعم
- الوصف: تصدير PDF - يرجع dict موحد
---
### `export_zip(self, output_path)`
- السطر: 191
- القيمة المرجعة: نعم
- الوصف: تصدير ZIP - يرجع dict موحد
---
### `hash_password(password)`
- السطر: 19
- القيمة المرجعة: نعم
- الوصف: تشفير كلمة المرور بـ PBKDF2 مع salt عشوائي
---
### `generate_activation_code(tier)`
- السطر: 26
- القيمة المرجعة: نعم
- الوصف: توليد كود تفعيل حسب المستوى
---
### `save_db()`
- السطر: 121
- القيمة المرجعة: لا
- الوصف: حفظ قاعدة البيانات إلى ملف JSON
---
### `load_db()`
- السطر: 126
- القيمة المرجعة: لا
- الوصف: تحميل قاعدة البيانات من ملف JSON
---
### `create_user(self, username, password, email)`
- السطر: 49
- القيمة المرجعة: نعم
- الوصف: إنشاء مستخدم جديد
---
### `create_google_user(self, google_id, email, name)`
- السطر: 70
- القيمة المرجعة: نعم
- الوصف: إنشاء مستخدم عبر Google OAuth
---
### `authenticate(self, username, password)`
- السطر: 92
- القيمة المرجعة: نعم
- الوصف: التحقق من اسم المستخدم وكلمة المرور
---
### `get_user(self, username)`
- السطر: 102
- القيمة المرجعة: نعم
- الوصف: استرجاع مستخدم بالاسم
---
### `get_all_users(self)`
- السطر: 106
- القيمة المرجعة: نعم
- الوصف: استرجاع كل المستخدمين
---
### `create_token(user_id, role)`
- السطر: 20
- القيمة المرجعة: نعم
- الوصف: إنشاء JWT token - للهوية فقط
Args:
    user_id: معرف المستخدم الثابت
    role: صلاحية المستخدم (user/admin)
Returns:
    JWT token string
---
### `verify_token(token)`
- السطر: 39
- القيمة المرجعة: نعم
- الوصف: فك والتحقق من JWT token
Args:
    token: JWT token string
Returns:
    payload dict إذا كان التوكن صالحاً، None إذا كان غير صالح
---
### `backup_database()`
- السطر: 4
- القيمة المرجعة: نعم
---
### `auto_backup()`
- السطر: 12
- القيمة المرجعة: لا
---
### `validate_username(username)`
- السطر: 3
- القيمة المرجعة: نعم
---
### `validate_email(email)`
- السطر: 12
- القيمة المرجعة: نعم
---
### `validate_password(password)`
- السطر: 19
- القيمة المرجعة: نعم
---
### `send_email(to, subject, body)`
- السطر: 10
- القيمة المرجعة: نعم
---
### `send_verification(email, username, code)`
- السطر: 27
- القيمة المرجعة: نعم
---
### `send_reset_password(email, username, token)`
- السطر: 35
- القيمة المرجعة: نعم
---
### `get_token_from_request()`
- السطر: 15
- القيمة المرجعة: نعم
- الوصف: استخراج JWT من الطلب - Header أو Cookie
---
### `login_required(f)`
- السطر: 30
- القيمة المرجعة: نعم
- الوصف: ديكور: يتحقق من JWT ويجيب المستخدم من قاعدة البيانات
JWT للهوية فقط - user_id و role
---
### `admin_required(f)`
- السطر: 75
- القيمة المرجعة: نعم
- الوصف: ديكور: يتحقق من صلاحية admin
يجب استخدامه بعد login_required
---
### `decorated_function()`
- السطر: 36
- القيمة المرجعة: نعم
---
### `decorated_function()`
- السطر: 81
- القيمة المرجعة: نعم
---
### `reset_daily_if_new_day(user)`
- السطر: 27
- القيمة المرجعة: لا
- الوصف: تصفير العداد إذا تغير اليوم
---
### `check_quota(user_id)`
- السطر: 35
- القيمة المرجعة: نعم
- الوصف: التحقق من حد المستخدم - يرجع (مسموح, رسالة)
---
### `track_request(user_id)`
- السطر: 60
- القيمة المرجعة: لا
- الوصف: تسجيل طلب وزيادة العداد
---
### `get_usage(user_id)`
- السطر: 71
- القيمة المرجعة: نعم
- الوصف: إحصائيات استخدام المستخدم
---
### `activate_tier(user_id, tier, duration_days)`
- السطر: 91
- القيمة المرجعة: نعم
- الوصف: تفعيل اشتراك لمستخدم
---
### `require_quota(f)`
- السطر: 11
- القيمة المرجعة: نعم
- الوصف: ديكور: يتحقق من حد المستخدم قبل تنفيذ الطلب
يوضع بعد @login_required
---
### `decorated_function()`
- السطر: 17
- القيمة المرجعة: نعم
---
### `load_keys()`
- السطر: 19
- القيمة المرجعة: نعم
- الوصف: تحميل المفاتيح من .env فقط - لا fallback
---
### `ai_generate(func_code, func_name)`
- السطر: 530
- القيمة المرجعة: نعم
---
### `find_related_functions(filepath)`
- السطر: 555
- القيمة المرجعة: نعم
---
### `gen_integration_tests(filepath)`
- السطر: 582
- القيمة المرجعة: نعم
---
### `html_report(results, output)`
- السطر: 623
- القيمة المرجعة: نعم
---
### `gen_tests(source, output, auto_fix, js)`
- السطر: 665
- القيمة المرجعة: نعم
---
### `gen_all(source, output, auto_fix)`
- السطر: 707
- القيمة المرجعة: نعم
---
### `infer(cls, node)`
- السطر: 42
- القيمة المرجعة: نعم
---
### `get(cls, name, hint)`
- السطر: 77
- القيمة المرجعة: نعم
---
### `analyze(self)`
- السطر: 141
- القيمة المرجعة: نعم
---
### `analyze(self)`
- السطر: 235
- القيمة المرجعة: نعم
---
### `get_assertion(cls, func)`
- السطر: 259
- القيمة المرجعة: نعم
---
### `generate(cls, func)`
- السطر: 291
- القيمة المرجعة: نعم
---
### `generate(self)`
- السطر: 351
- القيمة المرجعة: نعم
---
### `generate(self)`
- السطر: 447
- القيمة المرجعة: نعم
---
### `run(test_file, attempts)`
- السطر: 482
- القيمة المرجعة: نعم
---
## الكلاسات
### class PythonAnalyzer
---
### class JavaScriptAnalyzer
---
### class HTMLAnalyzer
---
### class CSSAnalyzer
---
### class JSONAnalyzer
---
### class GeneralAnalyzer
---
### class TemplateEngine
---
### class QualityChecker
---
### class KeyInfo
---
### class KeyManager
---
### class AIEngine
---
### class RateLimiter
---
### class SimpleEncryption
---
### class KeyVault
---
### class SystemMonitor
---
### class GitHubAnalyzer
---
### class ColoredFormatter
---
### class LoggerManager
---
### class Exporter
---
### class UserDB
---
### class TypeInferrer
---
### class SmartArg
---
### class DeepAnalyzer
---
### class JSAnalyzer
---
### class ValueExpector
---
### class EdgeCases
---
### class TestGenerator
---
### class JSTestGenerator
---
### class AutoFixEngine
---
*تم التوليد: 2026-05-03 22:46:25*