#!/usr/bin/env python3
"""
DocGen CLI - أوامر مختصرة
ta   = تحليل (Overview + Architecture + Files)
tth  = توثيق (README + API)
go   = فحص إنتاجية (Production)
all  = الكل (6 تبويبات)
"""

import sys, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def do_analyze(target):
    """ta - تحليل: Overview + Architecture + Files"""
    from src.core.analyzer import analyze_file, analyze_directory
    
    if os.path.isfile(target):
        r = analyze_file(target)
        print(f"📄 {r['filename']} | {r.get('language','?')} | {len(r.get('functions',[]))} funcs | {len(r.get('classes',[]))} classes | {r.get('complexity',{}).get('total_lines',0)} lines")
    elif os.path.isdir(target):
        r = analyze_directory(target)
        s = r.get('stats',{})
        print(f"📁 {target}")
        print(f"   Files: {s.get('total_files',0)} | Lines: {s.get('total_lines',0)}")
        print(f"   Languages: {dict(s.get('languages',{}))}")
    else:
        print(f"❌ Not found: {target}")

def do_docs(target):
    """tth - توثيق: README + API"""
    from src.core.analyzer import analyze_file, analyze_directory
    from src.core.generator import generate_all_docs
    
    out_dir = os.path.join(target, 'docs') if os.path.isdir(target) else 'docs'
    os.makedirs(out_dir, exist_ok=True)
    
    if os.path.isfile(target):
        with open(target) as f:
            code = f.read()
        analysis = analyze_file(target)
        docs = generate_all_docs(code, analysis, Path(target).stem, doc_types=['readme','api'])
        for name, content in docs.items():
            path = os.path.join(out_dir, name)
            with open(path, 'w') as f:
                f.write(content)
            print(f"✅ {path}")
    elif os.path.isdir(target):
        all_code = ""
        all_funcs, all_classes, total_lines = [], [], 0
        for fp in Path(target).rglob('*.py'):
            with open(fp) as f:
                all_code += f.read() + "\n"
            a = analyze_file(str(fp))
            if 'error' not in a:
                all_funcs.extend(a.get('functions',[]))
                all_classes.extend(a.get('classes',[]))
                total_lines += a.get('complexity',{}).get('total_lines',0)
        
        analysis = {"functions":all_funcs,"classes":all_classes,"complexity":{"total_lines":total_lines},"language":"Multi-file"}
        docs = generate_all_docs(all_code, analysis, Path(target).stem, doc_types=['readme','api'])
        for name, content in docs.items():
            path = os.path.join(out_dir, name)
            with open(path, 'w') as f:
                f.write(content)
            print(f"✅ {path}")

def do_production(target):
    """go - فحص إنتاجية"""
    from src.core.analyzer import analyze_file, analyze_directory
    
    if os.path.isfile(target):
        r = analyze_file(target)
        funcs = len(r.get('functions',[]))
        classes = len(r.get('classes',[]))
        lines = r.get('complexity',{}).get('total_lines',0)
    elif os.path.isdir(target):
        r = analyze_directory(target)
        funcs = sum(len(f.get('functions',[])) for f in r.get('files',[]))
        classes = sum(len(f.get('classes',[])) for f in r.get('files',[]))
        lines = r.get('stats',{}).get('total_lines',0)
    else:
        print(f"❌ Not found: {target}")
        return
    
    score = 0
    checks = []
    
    if funcs > 0:
        score += 2; checks.append(('✅','Functions',f'{funcs} functions'))
    else:
        checks.append(('❌','Functions','None'))
    
    if classes > 0:
        score += 2; checks.append(('✅','Classes',f'{classes} classes'))
    else:
        checks.append(('❌','Classes','None'))
    
    if lines > 100:
        score += 2; checks.append(('✅','Size',f'{lines} lines'))
    else:
        checks.append(('❌','Size','Too small'))
    
    if os.path.isdir(target):
        has_readme = os.path.exists(os.path.join(target,'README.md'))
        if has_readme:
            score += 2; checks.append(('✅','README','Found'))
        else:
            checks.append(('❌','README','Missing'))
        
        has_tests = os.path.exists(os.path.join(target,'tests'))
        if has_tests:
            score += 2; checks.append(('✅','Tests','Found'))
        else:
            checks.append(('❌','Tests','Missing'))
    
    label = 'PRODUCTION READY' if score >= 8 else ('NEEDS WORK' if score >= 5 else 'NOT READY')
    print(f"\n📊 Score: {score}/10 - {label}")
    for icon, name, msg in checks:
        print(f"  {icon} {name}: {msg}")

def do_all(target):
    """all - كل شيء"""
    print("🔍 Analyzing...")
    do_analyze(target)
    print("\n📝 Generating docs...")
    do_docs(target)
    print("\n🚀 Production check...")
    do_production(target)
    print(f"\n✅ Done! Docs saved in {os.path.join(target,'docs') if os.path.isdir(target) else 'docs/'}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python cli.py ta   <path>    # تحليل")
        print("  python cli.py tth  <path>    # توثيق")
        print("  python cli.py go   <path>    # إنتاجية")
        print("  python cli.py all  <path>    # الكل")
    else:
        cmd, target = sys.argv[1], sys.argv[2]
        {'ta':do_analyze, 'tth':do_docs, 'go':do_production, 'all':do_all}.get(cmd, lambda x: print('Unknown'))(target)
