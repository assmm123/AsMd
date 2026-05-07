# DocGen - دليل التثبيت والأوامر

## 📥 التثبيت

```bash
cd ~
git clone https://github.com/assmm123/Docmd.git
cd Docmd
pip install -r requirements.txt
```

⚡ اختصارات (مرة واحدة)

```bash
echo 'alias ta="python ~/Docmd/cli.py ta"' >> ~/.bashrc
echo 'alias tth="python ~/Docmd/cli.py tth"' >> ~/.bashrc
echo 'alias go="python ~/Docmd/cli.py go"' >> ~/.bashrc
echo 'alias all="python ~/Docmd/cli.py all"' >> ~/.bashrc
echo 'alias etest="python ~/Docmd/src/testing/emperor/emperor.py"' >> ~/.bashrc
source ~/.bashrc
```

---

📂 أوامر التحليل والتوثيق

الأمر الوظيفة مثال
ta تحليل ta app.py / ta src/
tth توثيق tth src/
go إنتاجية go .
all الكل all .

أمثلة مع نتائج

```bash
$ ta app.py
📄 app.py | Python | 12 funcs | 3 classes | 450 lines

$ tth src/
✅ docs/README.md (934 chars)
✅ docs/API_DOCS.md (2300 chars)

$ go .
📊 Score: 10/10 - PRODUCTION READY
✅ Functions: 503 | ✅ README: Found | ✅ Tests: Found

$ python cli.py github user/repo
🔍 Analyzing user/repo...
📦 user/repo
📄 Files: 51 | ⚡ Functions: 593 | 📏 Lines: 12498
```

---

⚡ أوامر الاختبار

الأمر الوظيفة مثال
etest تحليل + توليد + إصلاح etest src/
etest -f إصلاح اختبارات etest -f tests/
etest -w مراقبة مستمرة etest -w
etest -r تقرير etest -r
etest -i تكامل etest -i a.py b.py

أمثلة مع نتائج

```bash
$ etest src/auth.py
🧠 3 functions, 1 class
🤲 12 tests → tests/test_auth.py
🧪 10 passed, 2 failed
🔧 2 healed ✅

$ etest -f tests/
📄 test_auth.py: 12 tests
   ✅ 10 passed (untouched)
   ❌ 2 failed → 🔧 healed

$ etest -w
👁️ Watching ~ src/
[14:30] auth.py → ✅ 12 tests

$ etest -r
📊 Sessions: 42 | Tests: 1,250 | Healed: 89 | Rate: 88%

$ etest -i src/auth.py src/db.py
🔗 auth.py ↔ db.py
🤲 8 integration tests
🧪 8 passed ✅
```

---

🌐 تشغيل الويب

```bash
cd ~/Docmd
python main.py
# افتح http://127.0.0.1:5000
```

---

📁 هيكل المشروع

```
Docmd/
├── main.py              # خادم الويب
├── cli.py               # أوامر Termux
├── src/
│   ├── core/            # تحليل وتوليد
│   ├── auth/            # مصادقة
│   ├── saas/            # اشتراكات
│   ├── security/        # أمان
│   ├── integrations/    # GitHub
│   └── testing/emperor/ # مولد الاختبارات
├── templates/           # صفحات الويب
├── static/              # CSS, JS
└── tests/               # اختبارات
```

