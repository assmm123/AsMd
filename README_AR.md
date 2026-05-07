
DocGen - مولد التوثيق الذكي

ما هو DocGen؟

DocGen هو مولد توثيق بالذكاء الاصطناعي. ارفع ملفات الكود أو حلل مستودعات GitHub واحصل على توثيق احترافي في ثواني.

الميزات

· رفع عدة ملفات برمجية (Python, JavaScript, HTML, CSS, JSON، الخ)
· تحليل ملف منفرد أو دمج الكل في توثيق واحد
· تحليل مستودعات GitHub
· توليد README، API Docs، Wiki، Changelog
· تصدير إلى Markdown، HTML، PDF، ZIP
· نسخ إلى الحافظة
· دعم PWA (تثبيت على الموبايل)
· 59 نموذج ذكاء اصطناعي عبر OpenRouter

التنصيب

```bash
git clone https://github.com/assmm123/Dokle.git
cd Dokle
pip install -r requirements.txt
```

التشغيل السريع

```bash
python main.py
```

افتح: http://127.0.0.1:5000

استخدام سطر الأوامر

```bash
# تحليل ملف
python cli.py analyze app.py

# توليد توثيق لمجلد
python cli.py generate src/ --merge

# تحليل مستودع GitHub
python cli.py github psf/requests
```

المتطلبات

· Python 3.11+
· Flask, httpx, markdown, fpdf2, requests

الرخصة

MIT
