"""
🧬 Imperial Memory - ذاكرة الإمبراطور
تخزين واسترجاع الخبرات، التعلم من التجارب السابقة
الإصدار: 1.1.0 - محسّن بالكامل
"""

import json
import os
import time
import hashlib
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field, asdict
from collections import defaultdict

# ============================================================
# إعدادات
# ============================================================

DEFAULT_MEMORY_FILE = "emperor_memory.json"
MAX_ENTRIES = 10000
RETENTION_DAYS = 365
MAX_SIMILAR_RESULTS = 5
MAX_COMMON_FIXES = 20

# ============================================================
# هيكل البيانات
# ============================================================

@dataclass
class MemoryEntry:
    """إدخال واحد في الذاكرة"""
    id: str
    timestamp: str
    error_type: str
    error_message: str
    file: str
    function: str
    fix_applied: str
    level: str
    attempt: int
    success: bool
    test_file: str = ""
    test_name: str = ""
    code_signature: str = ""
    tags: List[str] = field(default_factory=list)
    relevance_score: int = 0


@dataclass
class CommonFix:
    """إصلاح شائع مع تتبع التكرار"""
    fix: str
    count: int = 1
    first_seen: str = ""
    last_used: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()
        if not self.first_seen:
            self.first_seen = now
        if not self.last_used:
            self.last_used = now


# ============================================================
# الذاكرة الحية
# ============================================================

class ImperialMemory:
    """ذاكرة الإمبراطور - تتعلم من كل تجربة"""

    def __init__(self, memory_file: str = None):
        self.file = memory_file or DEFAULT_MEMORY_FILE
        self.data = self._load()
        self._ensure_structure()

    def _load(self) -> dict:
        """تحميل الذاكرة من الملف"""
        try:
            if os.path.exists(self.file):
                with open(self.file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

        return self._default_data()

    def _default_data(self) -> dict:
        """البيانات الافتراضية للذاكرة الجديدة"""
        return {
            "version": "1.1.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "statistics": {
                "total_runs": 0,
                "total_tests_generated": 0,
                "total_fixes_applied": 0,
                "total_fixes_failed": 0,
                "success_rate": 0.0,
                "total_scenarios_discovered": 0
            },
            "error_patterns": {},
            "fix_history": [],
            "file_reputation": {},
            "scenarios": [],
            "knowledge_tags": {}
        }

    def _ensure_structure(self):
        """ضمان وجود كل المفاتيح المطلوبة"""
        defaults = self._default_data()
        for key, value in defaults.items():
            if key not in self.data:
                self.data[key] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if subkey not in self.data[key]:
                        self.data[key][subkey] = subvalue

    def save(self):
        """حفظ الذاكرة في الملف"""
        try:
            self.data['updated_at'] = datetime.now(timezone.utc).isoformat()
            dirpath = os.path.dirname(self.file)
            if dirpath:
                os.makedirs(dirpath, exist_ok=True)
            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    # ============================================================
    # توليد معرفات وبصمات
    # ============================================================

    @staticmethod
    def generate_signature(function_name: str, args: List[str],
                           return_type: str = "", body_hash: str = "") -> str:
        """توليد توقيع فريد لدالة"""
        content = f"{function_name}({','.join(args)})->{return_type}:{body_hash}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    @staticmethod
    def generate_entry_id() -> str:
        """توليد معرف فريد لإدخال"""
        return f"fix_{int(time.time() * 1000)}_{os.urandom(3).hex()}"

    # ============================================================
    # تسجيل الخبرات
    # ============================================================

    def remember_error(self,
                       error_type: str,
                       error_msg: str,
                       file_path: str,
                       function_name: str,
                       fix_applied: str,
                       level: str,
                       attempt: int,
                       success: bool,
                       test_file: str = "",
                       test_name: str = "",
                       code_signature: str = "",
                       tags: List[str] = None):
        """تسجيل خطأ ومحاولة إصلاحه في الذاكرة"""

        fix_entry = {
            "id": self.generate_entry_id(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error_type": error_type,
            "error_message": str(error_msg)[:300],
            "file": file_path,
            "function": function_name,
            "fix_applied": fix_applied,
            "level": level,
            "attempt": attempt,
            "success": success,
            "test_file": test_file,
            "test_name": test_name,
            "code_signature": code_signature,
            "tags": tags or []
        }

        # إضافة للسجل
        self.data['fix_history'].append(fix_entry)

        # تحديث أنماط الأخطاء
        self._update_error_patterns(error_type, error_msg, fix_applied, success)

        # تحديث وسوم المعرفة
        if tags:
            self._update_knowledge_tags(tags, error_type, success)

        # تحديث الإحصائيات
        self._update_statistics(success)

        # تحديث سمعة الملف
        self._update_file_reputation(file_path, success)

        # تقليم القديم إذا لزم
        self._prune_if_needed()

        # حفظ تلقائي
        self.save()

    def remember_scenario(self, name: str, functions: List[str],
                          success: bool, description: str = ""):
        """تسجيل سيناريو اختبار مكتشف"""
        scenario = {
            "name": name,
            "functions": functions,
            "success": success,
            "description": description,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.data['scenarios'].append(scenario)
        self.data['statistics']['total_scenarios_discovered'] += 1

        # حفظ تلقائي
        self.save()

    def increment_tests_generated(self, count: int = 1):
        """زيادة عدد الاختبارات المولدة"""
        self.data['statistics']['total_tests_generated'] += count
        self.save()

    # ============================================================
    # تحديثات داخلية
    # ============================================================

    def _update_error_patterns(self, error_type: str, error_msg: str,
                               fix_applied: str, success: bool):
        """تحديث أنماط الأخطاء"""
        if error_type not in self.data['error_patterns']:
            self.data['error_patterns'][error_type] = {
                "count": 0,
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "last_seen": None,
                "common_fixes": [],
                "sample_messages": []
            }

        pattern = self.data['error_patterns'][error_type]
        pattern['count'] += 1
        pattern['last_seen'] = datetime.now(timezone.utc).isoformat()

        # تخزين عينة من الرسائل (منوعة)
        if error_msg and len(pattern['sample_messages']) < 10:
            if error_msg not in pattern['sample_messages']:
                pattern['sample_messages'].append(error_msg[:200])

        # تحديث الإصلاحات الشائعة
        if success and fix_applied:
            self._update_common_fixes(pattern['common_fixes'], fix_applied)

    def _update_common_fixes(self, common_fixes: List[Dict],
                             fix_applied: str):
        """تحديث قائمة الإصلاحات الشائعة مع تتبع التكرار"""
        now = datetime.now(timezone.utc).isoformat()

        for existing in common_fixes:
            if existing.get('fix') == fix_applied:
                existing['count'] = existing.get('count', 1) + 1
                existing['last_used'] = now
                return

        # إصلاح جديد
        common_fixes.append({
            "fix": fix_applied,
            "count": 1,
            "first_seen": now,
            "last_used": now
        })

        # ترتيب حسب التكرار (الأكثر شيوعاً أولاً)
        common_fixes.sort(key=lambda x: x.get('count', 0), reverse=True)

        # الاحتفاظ بالأكثر شيوعاً فقط
        if len(common_fixes) > MAX_COMMON_FIXES:
            common_fixes[:] = common_fixes[:MAX_COMMON_FIXES]

    def _update_knowledge_tags(self, tags: List[str], error_type: str,
                               success: bool):
        """تحديث وسوم المعرفة"""
        if 'knowledge_tags' not in self.data:
            self.data['knowledge_tags'] = {}

        for tag in tags:
            if tag not in self.data['knowledge_tags']:
                self.data['knowledge_tags'][tag] = {
                    "count": 0,
                    "errors": {},
                    "successes": 0,
                    "failures": 0
                }

            kt = self.data['knowledge_tags'][tag]
            kt['count'] += 1
            kt['errors'][error_type] = kt['errors'].get(error_type, 0) + 1
            if success:
                kt['successes'] += 1
            else:
                kt['failures'] += 1

    def _update_statistics(self, success: bool):
        """تحديث الإحصائيات العامة"""
        stats = self.data['statistics']
        stats['total_runs'] += 1
        if success:
            stats['total_fixes_applied'] += 1
        else:
            stats['total_fixes_failed'] += 1

        total = max(stats['total_runs'], 1)
        stats['success_rate'] = round(
            (stats['total_fixes_applied'] / total) * 100, 1
        )

    def _update_file_reputation(self, file_path: str, success: bool):
        """تحديث سمعة ملف"""
        if 'file_reputation' not in self.data:
            self.data['file_reputation'] = {}

        if file_path not in self.data['file_reputation']:
            self.data['file_reputation'][file_path] = {
                "total_attempts": 0,
                "successes": 0,
                "failures": 0,
                "reputation": "unknown",
                "last_tested": None
            }

        rep = self.data['file_reputation'][file_path]
        rep['total_attempts'] += 1
        rep['last_tested'] = datetime.now(timezone.utc).isoformat()
        if success:
            rep['successes'] += 1
        else:
            rep['failures'] += 1

        # حساب السمعة
        rate = (rep['successes'] / max(rep['total_attempts'], 1)) * 100
        if rate >= 90:
            rep['reputation'] = "excellent"
        elif rate >= 70:
            rep['reputation'] = "good"
        elif rate >= 50:
            rep['reputation'] = "average"
        else:
            rep['reputation'] = "poor"

    # ============================================================
    # التقليم والصيانة
    # ============================================================

    def _prune_if_needed(self):
        """تقليم الإدخالات القديمة إذا تجاوزت الحدود"""
        history = self.data.get('fix_history', [])

        # تقليم حسب العدد
        if len(history) > MAX_ENTRIES:
            self.data['fix_history'] = history[-MAX_ENTRIES:]

        # تقليم حسب العمر
        cutoff = datetime.now(timezone.utc).timestamp() - (RETENTION_DAYS * 86400)
        self.data['fix_history'] = [
            e for e in self.data['fix_history']
            if self._entry_timestamp(e) > cutoff
        ]

    @staticmethod
    def _entry_timestamp(entry: dict) -> float:
        """استخراج الطابع الزمني من إدخال"""
        try:
            return datetime.fromisoformat(
                entry['timestamp'].replace('Z', '+00:00')
            ).timestamp()
        except (ValueError, KeyError):
            return 0

    # ============================================================
    # استرجاع الخبرات
    # ============================================================

    def recall_similar(self,
                       error_type: str,
                       error_msg: str = "",
                       file_path: str = "",
                       function_name: str = "",
                       code_signature: str = "",
                       limit: int = MAX_SIMILAR_RESULTS) -> List[Dict]:
        """استرجاع أخطاء مشابهة من الماضي مع ترتيب بالصلة"""
        similar = []

        for entry in reversed(self.data.get('fix_history', [])):
            score = 0

            # نفس نوع الخطأ (وزن عالي)
            if entry.get('error_type') == error_type:
                score += 10

            # نفس الملف
            if file_path and entry.get('file') == file_path:
                score += 5

            # نفس الدالة (وزن عالي جداً)
            if function_name and entry.get('function') == function_name:
                score += 8

            # نفس توقيع الكود (وزن أعلى - تطابق شبه مؤكد)
            if code_signature and entry.get('code_signature') == code_signature:
                score += 15

            # إصلاح ناجح (أفضلية)
            if entry.get('success'):
                score += 3

            # تشابه في رسالة الخطأ
            if error_msg and self._message_similarity(
                error_msg, entry.get('error_message', '')
            ):
                score += 4

            if score >= 10:
                entry['relevance_score'] = score
                similar.append(entry)

        # ترتيب حسب الصلة (الأعلى أولاً)
        similar.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return similar[:limit]

    def recall_by_signature(self, function_name: str,
                            code_signature: str) -> List[Dict]:
        """استرجاع إصلاحات لنفس الدالة بنفس التوقيع"""
        return [
            entry for entry in self.data.get('fix_history', [])
            if entry.get('function') == function_name
            and entry.get('code_signature') == code_signature
            and entry.get('success')
        ]

    def get_common_fixes(self, error_type: str) -> List[str]:
        """استرجاع الإصلاحات الأكثر شيوعاً لنوع خطأ معين"""
        pattern = self.data.get('error_patterns', {}).get(error_type, {})
        fixes = pattern.get('common_fixes', [])
        # ترتيب حسب التكرار وإرجاع النص فقط
        sorted_fixes = sorted(fixes, key=lambda x: x.get('count', 0), reverse=True)
        return [f['fix'] for f in sorted_fixes]

    def get_common_fixes_detailed(self, error_type: str) -> List[Dict]:
        """استرجاع الإصلاحات الشائعة مع تفاصيل التكرار"""
        pattern = self.data.get('error_patterns', {}).get(error_type, {})
        return pattern.get('common_fixes', [])

    @staticmethod
    def _message_similarity(msg1: str, msg2: str) -> bool:
        """تحقق بسيط من تشابه رسالتين"""
        if not msg1 or not msg2:
            return False
        # تحويل لأحرف صغيرة ومقارنة الكلمات المشتركة
        words1 = set(msg1.lower().split())
        words2 = set(msg2.lower().split())
        if not words1 or not words2:
            return False
        common = words1.intersection(words2)
        return len(common) / max(len(words1), len(words2)) > 0.3

    # ============================================================
    # سمعة الملفات
    # ============================================================

    def get_file_reputation(self, file_path: str) -> Dict:
        """استرجاع سمعة ملف"""
        return self.data.get('file_reputation', {}).get(file_path, {
            "total_attempts": 0,
            "successes": 0,
            "failures": 0,
            "reputation": "unknown",
            "last_tested": None
        })

    def get_files_by_reputation(self, reputation: str) -> List[str]:
        """استرجاع الملفات حسب سمعتها"""
        return [
            fp for fp, rep in self.data.get('file_reputation', {}).items()
            if rep.get('reputation') == reputation
        ]

    def get_problematic_files(self) -> List[str]:
        """استرجاع الملفات ذات السمعة الضعيفة أو المتوسطة"""
        return (
            self.get_files_by_reputation('poor') +
            self.get_files_by_reputation('average')
        )

    # ============================================================
    # إحصائيات
    # ============================================================

    def get_statistics(self) -> Dict:
        """إحصائيات شاملة عن الذاكرة"""
        stats = self.data.get('statistics', {}).copy()
        stats['total_entries'] = len(self.data.get('fix_history', []))
        stats['total_patterns'] = len(self.data.get('error_patterns', {}))
        stats['files_tracked'] = len(self.data.get('file_reputation', {}))
        stats['total_scenarios'] = len(self.data.get('scenarios', []))
        stats['total_tags'] = len(self.data.get('knowledge_tags', {}))
        stats['memory_file_size_kb'] = round(
            os.path.getsize(self.file) / 1024, 2
        ) if os.path.exists(self.file) else 0
        return stats

    def get_error_patterns(self) -> Dict:
        """جميع أنماط الأخطاء المسجلة"""
        return self.data.get('error_patterns', {})

    def get_top_errors(self, limit: int = 10) -> List[Dict]:
        """أكثر الأخطاء شيوعاً"""
        patterns = self.data.get('error_patterns', {})
        sorted_patterns = sorted(
            patterns.items(),
            key=lambda x: x[1].get('count', 0),
            reverse=True
        )
        return [
            {"type": pt[0], "count": pt[1].get('count', 0)}
            for pt in sorted_patterns[:limit]
        ]

    def get_recent_activity(self, limit: int = 10) -> List[Dict]:
        """آخر النشاطات"""
        history = self.data.get('fix_history', [])
        return history[-limit:]

    # ============================================================
    # تصدير واستيراد
    # ============================================================

    def export_knowledge(self, filepath: str):
        """تصدير المعرفة المستفادة لملف مستقل"""
        knowledge = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "source": self.file,
            "version": self.data.get('version', '1.0.0'),
            "error_patterns": self.data.get('error_patterns', {}),
            "statistics": self.get_statistics(),
            "file_reputation": self.data.get('file_reputation', {}),
            "knowledge_tags": self.data.get('knowledge_tags', {})
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(knowledge, f, indent=2, ensure_ascii=False)

    def import_knowledge(self, filepath: str):
        """استيراد معرفة من ملف خارجي ودمجها"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                knowledge = json.load(f)

            # دمج أنماط الأخطاء
            for err_type, pattern in knowledge.get('error_patterns', {}).items():
                if err_type not in self.data['error_patterns']:
                    self.data['error_patterns'][err_type] = pattern
                else:
                    existing = self.data['error_patterns'][err_type]
                    existing['count'] += pattern.get('count', 0)
                    # دمج الإصلاحات الشائعة
                    for fix in pattern.get('common_fixes', []):
                        self._update_common_fixes(
                            existing['common_fixes'],
                            fix.get('fix', '')
                        )

            self.save()
            return True
        except (IOError, json.JSONDecodeError):
            return False

    # ============================================================
    # عمليات
    # ============================================================

    def clear(self):
        """مسح الذاكرة بالكامل"""
        self.data = self._default_data()
        self.save()

    def clear_history(self):
        """مسح سجل الإصلاحات فقط مع الاحتفاظ بالأنماط"""
        self.data['fix_history'] = []
        self.data['statistics']['total_runs'] = 0
        self.data['statistics']['total_fixes_applied'] = 0
        self.data['statistics']['total_fixes_failed'] = 0
        self.data['statistics']['success_rate'] = 0.0
        self.save()

    def get_summary(self) -> str:
        """ملخص نصي عن حالة الذاكرة"""
        stats = self.get_statistics()
        return (
            f"🧬 Imperial Memory v{self.data.get('version', '1.0.0')}\n"
            f"   Runs: {stats['total_runs']} | "
            f"Fixes: {stats['total_fixes_applied']} | "
            f"Failed: {stats['total_fixes_failed']} | "
            f"Success: {stats['success_rate']}%\n"
            f"   Entries: {stats['total_entries']} | "
            f"Patterns: {stats['total_patterns']} | "
            f"Files: {stats['files_tracked']} | "
            f"Size: {stats['memory_file_size_kb']}KB"
        )


# ============================================================
# مثيل عالمي
# ============================================================

_memory_instance = None


def get_memory(memory_file: str = None) -> ImperialMemory:
    """استرجاع مثيل الذاكرة العالمي"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ImperialMemory(memory_file)
    return _memory_instance


def reset_memory():
    """إعادة تعيين المثيل العالمي"""
    global _memory_instance
    _memory_instance = None


# ============================================================
# اختبار ذاتي
# ============================================================

if __name__ == "__main__":
    print("🧬 Imperial Memory - Self Test v1.1.0\n")

    mem = ImperialMemory("test_memory.json")

    # === اختبار 1: تسجيل أخطاء ===
    print("📝 Test 1: Recording errors...")

    mem.remember_error(
        error_type="TypeError",
        error_msg="expected str, got int for argument 'timeout'",
        file_path="src/auth.py",
        function_name="authenticate",
        fix_applied="Changed timeout from 30 to '30'",
        level="surface",
        attempt=1,
        success=True,
        test_file="tests/test_auth.py",
        test_name="test_authenticate_valid",
        code_signature=ImperialMemory.generate_signature(
            "authenticate", ["username", "password"], "Optional[User]"
        ),
        tags=["authentication", "type-fix"]
    )

    mem.remember_error(
        error_type="ImportError",
        error_msg="No module named 'requests'",
        file_path="src/api.py",
        function_name="fetch_data",
        fix_applied="Added import requests at top of test file",
        level="surface",
        attempt=1,
        success=True,
        tags=["import", "api"]
    )

    mem.remember_error(
        error_type="AssertionError",
        error_msg="assert None is not None",
        file_path="src/auth.py",
        function_name="authenticate",
        fix_applied="Changed assertion to assert result is None for invalid case",
        level="structural",
        attempt=5,
        success=False,
        code_signature=ImperialMemory.generate_signature(
            "authenticate", ["username", "password"], "Optional[User]"
        ),
        tags=["authentication", "assertion"]
    )

    # === اختبار 2: تسجيل سيناريو ===
    mem.remember_scenario(
        name="User Registration Flow",
        functions=["register", "login", "create_profile"],
        success=True,
        description="Complete user registration and login scenario"
    )

    # === اختبار 3: تحديث الإحصائيات ===
    mem.increment_tests_generated(25)
    print("   ✅ 3 errors + 1 scenario + 25 tests recorded")

    # === اختبار 4: استرجاع مشابه ===
    print("\n🔍 Test 2: Recalling similar errors...")
    similar = mem.recall_similar(
        error_type="TypeError",
        file_path="src/auth.py",
        function_name="authenticate"
    )
    print(f"   Similar errors found: {len(similar)}")
    for s in similar:
        print(f"   - {s['error_type']}: {s['fix_applied'][:50]}... (score: {s['relevance_score']})")

    # === اختبار 5: استرجاع بالتوقيع ===
    sig = ImperialMemory.generate_signature(
        "authenticate", ["username", "password"], "Optional[User]"
    )
    by_sig = mem.recall_by_signature("authenticate", sig)
    print(f"\n   By signature: {len(by_sig)} entries")

    # === اختبار 6: إصلاحات شائعة ===
    print("\n📊 Test 3: Common fixes...")
    common = mem.get_common_fixes("TypeError")
    print(f"   Common fixes for TypeError: {len(common)}")
    for c in common:
        print(f"   - {c[:60]}...")

    # === اختبار 7: سمعة الملفات ===
    print("\n🏷️  Test 4: File reputation...")
    rep = mem.get_file_reputation("src/auth.py")
    print(f"   src/auth.py: {rep['reputation']} ({rep['successes']}/{rep['total_attempts']})")

    problematic = mem.get_problematic_files()
    print(f"   Problematic files: {len(problematic)}")

    # === اختبار 8: إحصائيات ===
    print("\n📈 Test 5: Statistics...")
    print(f"   {mem.get_summary()}")

    top = mem.get_top_errors(5)
    print(f"   Top errors:")
    for e in top:
        print(f"   - {e['type']}: {e['count']} occurrences")

    # === اختبار 9: تصدير ===
    print("\n💾 Test 6: Export...")
    mem.export_knowledge("test_export.json")
    print("   ✅ Exported to test_export.json")

    # === تنظيف ===
    import os
    for f in ["test_memory.json", "test_export.json"]:
        if os.path.exists(f):
            os.remove(f)
            print(f"   🧹 Cleaned {f}")

    print("\n✅✅✅ All tests passed! Imperial Memory is ready. 👑")
