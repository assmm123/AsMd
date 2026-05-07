import os, re, sys, tempfile, zipfile, shutil
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from src.core.analyzer import analyze_file

import requests


class GitHubAnalyzer:
    def __init__(self, repo_url, token=None, max_size_mb=50):
        self.repo_url = repo_url.rstrip("/")
        if "github.com" not in self.repo_url:
            self.repo_url = "https://github.com/" + self.repo_url
        if not self.repo_url.startswith("https://"):
            self.repo_url = "https://github.com/" + self.repo_url
        self.token = token
        self.max_size = max_size_mb * 1024 * 1024
        self.user = None
        self.repo = None
        self._parse_url()

    def _parse_url(self):
        pattern = r"github\.com/([^/]+)/([^/]+?)(?:\.git)?$"
        match = re.search(pattern, self.repo_url)
        if match:
            self.user = match.group(1)
            self.repo = match.group(2)

    def _get_tree(self, files):
        tree = defaultdict(list)
        for f in files:
            folder = str(Path(f).parent) or "root"
            tree[folder].append(Path(f).name)
        lines = []
        for folder, f_list in sorted(tree.items())[:20]:
            short = folder.replace('/data/data/com.termux/files/usr/tmp/', '').split('/',1)
            if len(short)>1: short=short[1]
            else: short=short[0]
            icon = "📦" if len(f_list) > 5 else "📁"
            lines.append(f"├── {icon} {short}/ ({len(f_list)} files)")
            for fl in f_list[:3]:
                lines.append(f"│   ├── {fl}")
            if len(f_list) > 3:
                lines.append(f"│   └── ... +{len(f_list)-3} more")
        return "\n".join(lines)

    def analyze_and_generate(self, doc_types=None, language="ar"):
        return self.analyze(language=language)

    def analyze(self, language="ar"):
        if not self.user or not self.repo:
            return {"success": False, "error": "Invalid GitHub URL"}

        url = f"https://api.github.com/repos/{self.user}/{self.repo}/zipball/main"
        try:
            resp = requests.get(url, stream=True, timeout=30)
            if resp.status_code == 404:
                url = f"https://api.github.com/repos/{self.user}/{self.repo}/zipball/master"
                resp = requests.get(url, stream=True, timeout=30)
            if resp.status_code != 200:
                return {"success": False, "error": f"Not found (status {resp.status_code})"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "GitHub request timed out after 30s"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Cannot connect to GitHub"}
        except Exception as e:
            return {"success": False, "error": str(e)}

        remaining = resp.headers.get("X-RateLimit-Remaining")
        if remaining and int(remaining) < 5:
            return {"success": False, "error": "GitHub API rate limit nearly exhausted"}

        total = int(resp.headers.get("content-length", 0))
        if total > self.max_size:
            return {"success": False, "error": f"Too large ({total/1024/1024:.0f}MB > {self.max_size/1024/1024:.0f}MB)"}

        zip_path = None
        extract_dir = None

        try:
            zip_path = tempfile.mktemp(suffix=".zip")
            with open(zip_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)

            extract_dir = tempfile.mkdtemp()
            code_files = []
            langs_counter = Counter()
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)
                for name in zf.namelist():
                    ext = Path(name).suffix.lower()
                    if ext in ALLOWED_EXTENSIONS:
                        fp = os.path.join(extract_dir, name)
                        if os.path.isfile(fp) and os.path.getsize(fp) < MAX_FILE_SIZE:
                            code_files.append(fp)
                            langs_counter[ext] += 1

            if not code_files:
                return {"success": False, "error": "No supported code files found"}

            all_funcs = []
            all_classes = []
            total_lines = 0
            file_names = []

            for fp in code_files[:100]:
                a = analyze_file(fp)
                if "error" not in a:
                    all_funcs.extend(a.get("functions", []))
                    all_classes.extend(a.get("classes", []))
                    total_lines += a.get("complexity", {}).get("total_lines", 0)
                file_names.append(fp)

            func_names = list(set([f.get("name", "") for f in all_funcs if f.get("name")]))[:30]
            class_names = list(set([c.get("name", "") for c in all_classes if c.get("name")]))[:20]
            tree = self._get_tree(code_files)
            nf = len(code_files)
            nfunc = len(all_funcs)
            nclass = len(all_classes)
            nlines = total_lines

            lang_badges = " ".join([
                f"![{ext}](https://img.shields.io/badge/{ext}-{count}-{'green' if count>5 else 'gray'})"
                for ext, count in langs_counter.most_common(5)
            ])

            badges = (
                f"![Files](https://img.shields.io/badge/Files-{nf}-blue) "
                f"![Functions](https://img.shields.io/badge/Functions-{nfunc}-green) "
                f"![Classes](https://img.shields.io/badge/Classes-{nclass}-purple) "
                f"![Lines](https://img.shields.io/badge/Lines-{nlines}-orange)"
            )

            features = "\n".join([f"- **`{n}`**" for n in func_names[:15]]) or "- Core project"
            classes_list = "\n".join([f"- **`{n}`**" for n in class_names[:10]]) or "- Core classes"
            files_list_str = "\n".join([f"- `{Path(f).name}`" for f in file_names[:30]]) or "- Files"

            api_funcs_list = []
            for f in all_funcs[:20]:
                name = f.get("name", "unknown")
                args = ", ".join(f.get("args", []))
                ret = " -> value" if f.get("has_return") else ""
                doc = f.get("docstring", "")
                line = f.get("lineno", "?")
                if doc:
                    api_funcs_list.append(f"### `{name}({args}){ret}`\n- Line: {line}\n- {doc[:100]}")
                else:
                    api_funcs_list.append(f"### `{name}({args}){ret}`\n- Line: {line}")
            api_funcs_str = "\n\n".join(api_funcs_list[:20]) or "No functions"
            api_classes_str = "\n\n".join([f"### `class {n}`" for n in class_names[:10]]) or "No classes"

            if language == "ar":
                docs = {
                    "README.md": (
                        f"# {self.user}/{self.repo}\n\n"
                        f"{badges}\n\n"
                        f"{lang_badges}\n\n"
                        f"## نظرة عامة\n"
                        f"**{self.user}/{self.repo}** يحتوي على **{nf}** ملف، "
                        f"**{nfunc}** دالة، **{nclass}** كلاس، "
                        f"و **{nlines}** سطر من الكود.\n\n"
                        f"## هيكل المشروع\n{tree}\n\n"
                        f"## الميزات الرئيسية\n{features}\n\n"
                        f"## الكلاسات الرئيسية\n{classes_list}\n\n"
                        f"## الملفات\n{files_list_str}\n\n"
                        f"## إحصائيات\n"
                        f"| العنصر | العدد |\n|------|------|\n"
                        f"| الملفات | {nf} |\n| الدوال | {nfunc} |\n"
                        f"| الكلاسات | {nclass} |\n| الأسطر | {nlines} |\n\n"
                        f"---\n*تم التوليد بواسطة DocGen*"
                    ),
                    "API_DOCS.md": (
                        f"# {self.user}/{self.repo} API\n\n"
                        f"## الدوال ({nfunc})\n\n{api_funcs_str}\n\n"
                        f"## الكلاسات ({nclass})\n\n{api_classes_str}\n\n"
                        f"---\n*تم التوليد بواسطة DocGen*"
                    ),
                    "WIKI.md": (
                        f"# {self.user}/{self.repo} Wiki\n\n"
                        f"## هيكل المشروع\n{tree}\n\n"
                        f"## إحصائيات\n"
                        f"- **المالك:** {self.user}\n"
                        f"- **الملفات:** {nf}\n"
                        f"- **الدوال:** {nfunc}\n"
                        f"- **الكلاسات:** {nclass}\n"
                        f"- **الأسطر:** {nlines}\n\n"
                        f"---\n*تم التوليد بواسطة DocGen*"
                    ),
                    "CHANGELOG.md": (
                        f"# سجل التغييرات\n\n"
                        f"## [{datetime.now().strftime('%Y-%m-%d')}] تحليل\n\n"
                        f"### تمت الإضافة\n"
                        f"- {nfunc} دالة موثقة\n"
                        f"- {nclass} كلاس موثق\n"
                        f"- {nf} ملف محلل\n\n"
                        f"### إحصائيات\n"
                        f"- **الأسطر:** {nlines}\n"
                        f"- **المستودع:** {self.user}/{self.repo}\n\n"
                        f"---\n*تم التوليد بواسطة DocGen*"
                    ),
                }
            else:
                docs = {
                    "README.md": (
                        f"# {self.user}/{self.repo}\n\n"
                        f"{badges}\n\n"
                        f"{lang_badges}\n\n"
                        f"## Overview\n"
                        f"**{self.user}/{self.repo}** contains **{nf}** files, "
                        f"**{nfunc}** functions, **{nclass}** classes, "
                        f"and **{nlines}** lines of code.\n\n"
                        f"## Project Structure\n{tree}\n\n"
                        f"## Key Features\n{features}\n\n"
                        f"## Key Classes\n{classes_list}\n\n"
                        f"## Files\n{files_list_str}\n\n"
                        f"## Stats\n"
                        f"| Metric | Value |\n|------|------|\n"
                        f"| Files | {nf} |\n| Functions | {nfunc} |\n"
                        f"| Classes | {nclass} |\n| Lines | {nlines} |\n\n"
                        f"---\n*Generated by DocGen*"
                    ),
                    "API_DOCS.md": (
                        f"# {self.user}/{self.repo} API\n\n"
                        f"## Functions ({nfunc})\n\n{api_funcs_str}\n\n"
                        f"## Classes ({nclass})\n\n{api_classes_str}\n\n"
                        f"---\n*Generated by DocGen*"
                    ),
                    "WIKI.md": (
                        f"# {self.user}/{self.repo} Wiki\n\n"
                        f"## Project Structure\n{tree}\n\n"
                        f"## Stats\n"
                        f"- **Owner:** {self.user}\n"
                        f"- **Files:** {nf}\n"
                        f"- **Functions:** {nfunc}\n"
                        f"- **Classes:** {nclass}\n"
                        f"- **Lines:** {nlines}\n\n"
                        f"---\n*Generated by DocGen*"
                    ),
                    "CHANGELOG.md": (
                        f"# Changelog\n\n"
                        f"## [{datetime.now().strftime('%Y-%m-%d')}] Analysis\n\n"
                        f"### Added\n"
                        f"- {nfunc} functions documented\n"
                        f"- {nclass} classes documented\n"
                        f"- {nf} files analyzed\n\n"
                        f"### Stats\n"
                        f"- **Lines:** {nlines}\n"
                        f"- **Repo:** {self.user}/{self.repo}\n\n"
                        f"---\n*Generated by DocGen*"
                    ),
                }

            return {
                "success": True,
                "repo": f"{self.user}/{self.repo}",
                "user": self.user,
                "repo_name": self.repo,
                "url": self.repo_url,
                "files_analyzed": nf,
                "total_functions": nfunc,
                "total_classes": nclass,
                "total_lines": nlines,
                "docs": docs,
                "_tree": tree,
                "_func_names": func_names,
                "_class_names": class_names,
                "_file_names": [Path(f).name for f in file_names],
            }

        finally:
            if zip_path and os.path.exists(zip_path):
                try: os.unlink(zip_path)
                except OSError: pass
            if extract_dir and os.path.exists(extract_dir):
                try: shutil.rmtree(extract_dir, ignore_errors=True)
                except OSError: pass
