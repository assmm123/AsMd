# DocGen - Smart Documentation Generator

مولد توثيق احترافي بالذكاء الاصطناعي. يحلل أي مشروع Python ويولد توثيق كامل.

## الميزات
- تحليل Python, JavaScript, HTML, CSS, JSON
- 7 تبويبات: README, API, Wiki, Changelog, Overview, Issues, Security
- GitHub Integration
- تصدير Markdown, HTML, PDF, ZIP
- PWA - تطبيق موبايل
- AI-Powered (59 مفتاح OpenRouter)
- نظام مصادقة (Email + Google + JWT)
- أمان 4 طبقات
- Docker, CLI, CI/CD

## التثبيت
```bash
git clone https://github.com/assmm123/Dokle.git
cd Dokle
pip install -r requirements.txt
```

التشغيل

```bash
python main.py
```

افتح: http://127.0.0.1:5000

CLI

```bash
python cli.py analyze app.py
python cli.py github user/repo
```

Docker

```bash
docker build -t docgen .
docker run -p 5000:5000 docgen
```

المتطلبات

· Python 3.11+
· Flask, httpx, markdown, fpdf2, pyjwt, requests

الترخيص

MIT
