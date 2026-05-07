var currentLang=localStorage.getItem('docgen_lang')||'ar';
var allDocs={},repoData={},activeTab='overview';

var TGH={
  ar:{
    title:'محلل GitHub',subtitle:'حلل أي مستودع GitHub عام',
    enterUrl:'https://github.com/user/repo',infoTitle:'📌 الاستخدام',
    info1:'• مستودع عام: user/repo أو github.com/user/repo',
    info2:'• المستودعات الخاصة غير مدعومة',
    analyzeBtn:'🔍 تحليل المستودع',downloading:'جاري تحميل المستودع...',
    complete:'اكتمل التحليل',generated:'تم التوليد بنجاح!',
    failed:'فشل التحليل',error:'خطأ: ',
    overview:'نظرة عامة',readme:'README',architecture:'الهيكل',
    api:'API',files:'الملفات',production:'الإنتاجية',
    copy:'📋 نسخ',md:'📥 MD',html:'🌐 HTML',pdf:'📕 PDF',zip:'📦 ZIP',
    copied:'✓ تم النسخ!',back:'← العودة لـ DocGen',
    filesLbl:'ملفات',funcs:'دوال',classes:'كلاسات',lines:'أسطر',
    repo:'المستودع',url:'الرابط',owner:'المالك',
    archTitle:'🏗️ هيكل المستودع',
    noReadme:'لا يوجد README',noApi:'لا يوجد API',noFiles:'لا يوجد ملفات',
    prodTitle:'📊 تقييم الإنتاجية',prodReady:'جاهز للإنتاج',
    prodNeedsWork:'يحتاج عمل',prodNotReady:'غير جاهز',
    checkFunctions:'الدوال مكتشفة',checkReadme:'توثيق README',
    checkApi:'توثيق API',checkClasses:'الكلاسات',checkSize:'حجم المشروع',
    funcsFound:'دوال مكتشفة',noFuncs:'لا دوال',
    readmeOk:'README مولّد',readmeNo:'لا README',
    apiOk:'API مولّد',apiNo:'لا API',
    classesOk:'كلاسات',classesNo:'لا كلاسات',
    sizeOk:'ملفات',sizeNo:'مشروع صغير',
    funcsTitle:'الدوال',classesTitle:'الكلاسات',
    copyTab:'نسخ التبويب',tabCopied:'تم نسخ التبويب',
    totalFiles:'إجمالي الملفات',totalFuncs:'إجمالي الدوال',
    totalClasses:'إجمالي الكلاسات',totalLines:'إجمالي الأسطر',
    downloaded:'تم التحميل',filesAnalyzed:'ملفات محللة',
    copyAll:'نسخ الكل',features:'الميزات الرئيسية',
    keyClasses:'الكلاسات الرئيسية',stats:'إحصائيات',
    projectStructure:'هيكل المشروع',allFiles:'كل الملفات',
    andMore:'و',moreFiles:'ملفات أخرى',
  },
  en:{
    title:'GitHub Analyzer',subtitle:'Analyze any public GitHub repository',
    enterUrl:'https://github.com/user/repo',infoTitle:'📌 Usage',
    info1:'• Public repo: user/repo or github.com/user/repo',
    info2:'• Private repos not supported',
    analyzeBtn:'🔍 Analyze Repository',downloading:'Downloading repository...',
    complete:'Analysis complete',generated:'Documentation generated!',
    failed:'Analysis failed',error:'Error: ',
    overview:'Overview',readme:'README',architecture:'Architecture',
    api:'API',files:'Files',production:'Production',
    copy:'📋 Copy',md:'📥 MD',html:'🌐 HTML',pdf:'📕 PDF',zip:'📦 ZIP',
    copied:'✓ Copied!',back:'← Back to DocGen',
    filesLbl:'Files',funcs:'Functions',classes:'Classes',lines:'Lines',
    repo:'Repository',url:'URL',owner:'Owner',
    archTitle:'🏗️ Repository Structure',
    noReadme:'No README',noApi:'No API',noFiles:'No files',
    prodTitle:'📊 Production Score',prodReady:'PRODUCTION READY',
    prodNeedsWork:'NEEDS WORK',prodNotReady:'NOT READY',
    checkFunctions:'Functions Detected',checkReadme:'README Documentation',
    checkApi:'API Documentation',checkClasses:'Classes Structure',checkSize:'Project Size',
    funcsFound:'functions found',noFuncs:'No functions detected',
    readmeOk:'README generated',readmeNo:'No README',
    apiOk:'API docs generated',apiNo:'No API docs',
    classesOk:'classes',classesNo:'No classes detected',
    sizeOk:'files',sizeNo:'Small project',
    funcsTitle:'Functions',classesTitle:'Classes',
    copyTab:'Copy Tab',tabCopied:'Tab Copied',
    totalFiles:'Total Files',totalFuncs:'Total Functions',
    totalClasses:'Total Classes',totalLines:'Total Lines',
    downloaded:'Downloaded',filesAnalyzed:'Files Analyzed',
    copyAll:'Copy All',features:'Key Features',
    keyClasses:'Key Classes',stats:'Stats',
    projectStructure:'Project Structure',allFiles:'All Files',
    andMore:'and',moreFiles:'more files',
  }
};

function T(key){return (TGH[currentLang]&&TGH[currentLang][key])||key}
function D(id){return document.getElementById(id)}

function switchLang(lang){
  currentLang=lang;localStorage.setItem('docgen_lang',lang);
  document.getElementById('btnAr').classList.remove('active');
  document.getElementById('btnEn').classList.remove('active');
  if(lang==='ar'){document.getElementById('btnAr').classList.add('active');document.body.dir='rtl'}
  else{document.getElementById('btnEn').classList.add('active');document.body.dir='ltr'}
  applyGhLang()
}

function applyGhLang(){
  var el=document.querySelector('h1');if(el)el.textContent='🔗 '+T('title');
  el=document.querySelector('.subtitle');if(el)el.textContent=T('subtitle');
  el=D('githubUrl');if(el)el.placeholder=T('enterUrl');
  el=document.querySelector('.btn-primary');if(el)el.textContent=T('analyzeBtn');
  var tabs=document.querySelectorAll('.tab');
  var keys=['overview','readme','architecture','api','files','production'];
  for(var i=0;i<tabs.length;i++){tabs[i].textContent=T(keys[i])}
  if(repoData.repo){renderAllTabs()}
}

function showStatus(msg,type){
  var s=D('statusMsg');s.textContent=msg;s.style.display='block';
  s.className='status '+(type||'error');
  setTimeout(function(){s.style.display='none'},5000);
}

function showProgress(show,text,type){
  var bar=D('progressBar'),txt=D('progressText');
  if(show){bar.style.display='block';txt.style.display='block';txt.textContent=T(text)||text||'';
    bar.className='progress-bar '+(type||'');bar.style.width=type==='success'?'100%':'60%'}
  else{bar.style.display='none';txt.style.display='none'}
}

document.querySelectorAll('.tab').forEach(function(t){
  t.onclick=function(){
    document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active')});
    document.querySelectorAll('.tab-content').forEach(function(x){x.classList.remove('active')});
    t.classList.add('active');activeTab=t.dataset.tab;
    D('tab-'+t.dataset.tab).classList.add('active');
  }
});

async function analyzeRepo(){
  var url=D('githubUrl').value.trim();
  if(!url){showStatus(T('enterUrl'),'error');return}
  if(!url.includes('github.com'))url='https://github.com/'+url;

  showProgress(true,'downloading','');
  D('resultsArea').style.display='none';
  D('statsBar').style.display='none';

  try{
    var token=localStorage.getItem('token')||'';
    var r=await fetch('/github',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},body:JSON.stringify({url:url,language:currentLang})});
    var d=await r.json();

    if(d.success){
      repoData=d;allDocs=d.docs||{};
      D('resultsArea').style.display='block';
      showStats(d);renderAllTabs();applyGhLang();
      showProgress(true,'complete','success');
      showStatus(T('generated'),'success');
    }else{
      showProgress(true,d.error||T('failed'),'error');
      showStatus(d.error||T('failed'),'error');
    }
  }catch(e){
    showProgress(true,'error','error');
    showStatus(T('error')+e.message,'error');
  }
  setTimeout(function(){showProgress(false)},2500);
}

function showStats(d){
  D('statFiles').textContent=d.files_analyzed||0;
  D('statFuncs').textContent=d.total_functions||0;
  D('statClasses').textContent=d.total_classes||0;
  D('statLines').textContent=d.total_lines||0;
  D('statsBar').style.display='flex';
}

function renderAllTabs(){
  renderOverview();renderReadme();renderArchitecture();
  renderApi();renderFiles();renderProduction();
}

function cleanPath(p){return p.replace(/.*\/tmp\/[^\/]+\//,'').replace(/^\/data\/data\/.*\/tmp\/[^\/]+\//,'')}

function getTreeHTML(){
  if(!repoData._tree)return '';
  var tree=repoData._tree;
  if(typeof tree==='string')return '<pre style="color:#a78bfa;font-size:12px;line-height:1.6">'+fmt(tree)+'</pre>';
  return '';
}

function getFuncNames(){
  if(!repoData._func_names)return [];
  return repoData._func_names||[];
}

function getClassNames(){
  if(!repoData._class_names)return [];
  return repoData._class_names||[];
}

function getFileNames(){
  if(!repoData._file_names)return [];
  return repoData._file_names||[];
}

function renderOverview(){
  var d=repoData;
  var treeHTML=getTreeHTML();
  var funcNames=getFuncNames();
  var classNames=getClassNames();
  var h='<div style="padding:10px">';
  h+='<h3 style="color:#a78bfa;margin-bottom:10px">📦 '+d.repo+'</h3>';
  h+='<div class="overview-grid">';
  h+='<div class="overview-card"><div class="num">'+d.files_analyzed+'</div><div class="lbl">'+T('filesLbl')+'</div></div>';
  h+='<div class="overview-card"><div class="num">'+d.total_functions+'</div><div class="lbl">'+T('funcs')+'</div></div>';
  h+='<div class="overview-card"><div class="num">'+d.total_classes+'</div><div class="lbl">'+T('classes')+'</div></div>';
  h+='<div class="overview-card"><div class="num">'+d.total_lines+'</div><div class="lbl">'+T('lines')+'</div></div>';
  h+='</div>';
  h+='<table style="width:100%;margin-top:15px;border-collapse:collapse">';
  h+='<tr><td style="color:#888;padding:4px">'+T('repo')+'</td><td><strong>'+d.repo+'</strong></td></tr>';
  h+='<tr><td style="color:#888;padding:4px">'+T('url')+'</td><td><a href="'+d.url+'" target="_blank">'+d.url+'</a></td></tr>';
  h+='<tr><td style="color:#888;padding:4px">'+T('owner')+'</td><td>'+d.user+'</td></tr>';
  h+='<tr><td style="color:#888;padding:4px">'+T('totalFiles')+'</td><td>'+d.files_analyzed+'</td></tr>';
  h+='<tr><td style="color:#888;padding:4px">'+T('totalFuncs')+'</td><td>'+d.total_functions+'</td></tr>';
  h+='<tr><td style="color:#888;padding:4px">'+T('totalClasses')+'</td><td>'+d.total_classes+'</td></tr>';
  h+='<tr><td style="color:#888;padding:4px">'+T('totalLines')+'</td><td>'+d.total_lines+'</td></tr>';
  h+='</table>';

  if(treeHTML){
    h+='<h4 style="color:#a78bfa;margin:15px 0 8px">📁 '+T('projectStructure')+'</h4>';
    h+=treeHTML;
  }

  if(funcNames.length){
    h+='<h4 style="color:#a78bfa;margin:15px 0 8px">⭐ '+T('features')+'</h4>';
    for(var i=0;i<Math.min(funcNames.length,15);i++){h+='<span style="display:inline-block;background:#1a1a2e;padding:2px 8px;border-radius:4px;margin:2px;font-size:12px;color:#e0e0e0"><code>'+funcNames[i]+'</code></span> '}
  }

  if(classNames.length){
    h+='<h4 style="color:#a78bfa;margin:15px 0 8px">🏗️ '+T('keyClasses')+'</h4>';
    for(var i=0;i<Math.min(classNames.length,10);i++){h+='<span style="display:inline-block;background:#1a1a2e;padding:2px 8px;border-radius:4px;margin:2px;font-size:12px;color:#c4b5fd"><code>'+classNames[i]+'</code></span> '}
  }

  h+='<div style="text-align:center;margin-top:15px"><button class="btn btn-sm btn-secondary" onclick="copyCurrentTab()">📋 '+T('copyTab')+'</button></div>';
  h+='</div>';
  D('tab-overview').innerHTML=h;
}

function renderReadme(){
  var h='<div style="padding:10px">';
  for(var k in allDocs){if(k.toLowerCase().indexOf('readme')>=0){h+=fmt(allDocs[k]);break}}
  if(h==='<div style="padding:10px">')h+='<p style="color:#555">'+T('noReadme')+'</p>';
  h+='<div style="text-align:center;margin-top:10px"><button class="btn btn-sm btn-secondary" onclick="copyCurrentTab()">📋 '+T('copyTab')+'</button></div>';
  h+='</div>';
  D('tab-readme').innerHTML=h;
}

function renderArchitecture(){
  var d=repoData;
  var treeHTML=getTreeHTML();
  var h='<div style="padding:10px">';
  h+='<h3 style="color:#a78bfa">'+T('archTitle')+'</h3>';
  h+='<p style="color:#888;margin:10px 0"><strong>'+d.repo+'</strong> - '+d.files_analyzed+' '+T('filesAnalyzed')+'</p>';

  if(treeHTML){
    h+='<div style="background:#1a1a2e;border-radius:8px;padding:12px;margin:10px 0">'+treeHTML+'</div>';
  }

  h+='<div class="overview-grid" style="margin-top:10px">';
  h+='<div class="overview-card"><div class="num">'+d.files_analyzed+'</div><div class="lbl">'+T('filesLbl')+'</div></div>';
  h+='<div class="overview-card"><div class="num">'+d.total_functions+'</div><div class="lbl">'+T('funcs')+'</div></div>';
  h+='<div class="overview-card"><div class="num">'+d.total_classes+'</div><div class="lbl">'+T('classes')+'</div></div>';
  h+='<div class="overview-card"><div class="num">'+d.total_lines+'</div><div class="lbl">'+T('lines')+'</div></div>';
  h+='</div>';

  var files=getFileNames();
  if(files.length){
    h+='<h4 style="color:#a78bfa;margin:15px 0 8px">📄 '+T('allFiles')+'</h4>';
    for(var i=0;i<Math.min(files.length,20);i++){
      var clean=files[i].replace(/.*\/tmp\/[^\/]+\//,'');
      h+='<div class="file-row"><span class="fname">📄 '+clean+'</span></div>';
    }
    if(files.length>20)h+='<p style="color:#888;font-size:11px">... '+T('andMore')+' '+(files.length-20)+' '+T('moreFiles')+'</p>';
  }

  h+='<div style="text-align:center;margin-top:15px"><button class="btn btn-sm btn-secondary" onclick="copyCurrentTab()">📋 '+T('copyTab')+'</button></div>';
  h+='</div>';
  D('tab-architecture').innerHTML=h;
}

function renderApi(){
  var h='<div style="padding:10px">';
  for(var k in allDocs){if(k.toLowerCase().indexOf('api')>=0){h+=fmt(allDocs[k]);break}}
  if(h==='<div style="padding:10px">')h+='<p style="color:#555">'+T('noApi')+'</p>';
  h+='<div style="text-align:center;margin-top:10px"><button class="btn btn-sm btn-secondary" onclick="copyCurrentTab()">📋 '+T('copyTab')+'</button></div>';
  h+='</div>';
  D('tab-api').innerHTML=h;
}

function renderFiles(){
  var d=repoData;
  var files=getFileNames();
  var h='<div style="padding:10px">';
  h+='<h3 style="color:#a78bfa">📄 '+T('files')+' ('+d.files_analyzed+')</h3>';
  if(files.length){
    h+='<div style="margin-top:10px;max-height:400px;overflow-y:auto">';
    for(var i=0;i<files.length;i++){
      var clean=files[i].replace(/.*\/tmp\/[^\/]+\//,'');
      var ext=clean.split('.').pop();
      h+='<div class="file-row"><span class="fname">📄 '+clean+'</span><span class="flang">'+ext+'</span></div>';
    }
    h+='</div>';
  }else{
    h+='<p style="color:#888">'+T('noFiles')+'</p>';
  }
  h+='<div style="text-align:center;margin-top:10px"><button class="btn btn-sm btn-secondary" onclick="copyCurrentTab()">📋 '+T('copyTab')+'</button></div>';
  h+='</div>';
  D('tab-files').innerHTML=h;
}

function renderProduction(){
  var d=repoData;
  var score=0;
  var checks=[];
  var hasFuncs=d.total_functions>0;
  var hasReadme=allDocs['README.md']&&allDocs['README.md'].length>100;
  var hasApi=allDocs['API_DOCS.md']&&allDocs['API_DOCS.md'].length>100;
  var hasClasses=d.total_classes>0;
  var hasFiles=d.files_analyzed>5;

  if(hasFuncs){score+=2;checks.push({name:T('checkFunctions'),pass:true,msg:d.total_functions+' '+T('funcsFound')})}
  else{checks.push({name:T('checkFunctions'),pass:false,msg:T('noFuncs')})}
  if(hasReadme){score+=2;checks.push({name:T('checkReadme'),pass:true,msg:T('readmeOk')})}
  else{checks.push({name:T('checkReadme'),pass:false,msg:T('readmeNo')})}
  if(hasApi){score+=2;checks.push({name:T('checkApi'),pass:true,msg:T('apiOk')})}
  else{checks.push({name:T('checkApi'),pass:false,msg:T('apiNo')})}
  if(hasClasses){score+=2;checks.push({name:T('checkClasses'),pass:true,msg:d.total_classes+' '+T('classesOk')})}
  else{checks.push({name:T('checkClasses'),pass:false,msg:T('classesNo')})}
  if(hasFiles){score+=2;checks.push({name:T('checkSize'),pass:true,msg:d.files_analyzed+' '+T('sizeOk')})}
  else{checks.push({name:T('checkSize'),pass:false,msg:T('sizeNo')})}

  var cls=score>=8?'ready':(score>=5?'warn':'fail');
  var label=score>=8?T('prodReady'):(score>=5?T('prodNeedsWork'):T('prodNotReady'));
  var h='<div style="padding:10px">';
  h+='<h3 style="color:#a78bfa">'+T('prodTitle')+'</h3>';
  h+='<div class="prod-score '+cls+'">'+score+'/10</div>';
  h+='<p style="text-align:center;color:#888;margin-bottom:15px">'+label+'</p>';
  h+='<div class="prod-checks">';
  for(var i=0;i<checks.length;i++){
    var c=checks[i];
    h+='<div class="prod-check '+(c.pass?'pass':'fail')+'"><h4>'+(c.pass?'✅':'❌')+' '+c.name+'</h4><p>'+c.msg+'</p></div>';
  }
  h+='</div>';
  h+='<div style="text-align:center;margin-top:10px"><button class="btn btn-sm btn-secondary" onclick="copyCurrentTab()">📋 '+T('copyTab')+'</button></div>';
  h+='</div>';
  D('tab-production').innerHTML=h;
}

function fmt(t){
  if(!t)return'';
  return t.replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/### (.*)/g,'<h3>$1</h3>').replace(/## (.*)/g,'<h2>$1</h2>').replace(/# (.*)/g,'<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/!\[.*?\]\(.*?\)/g,'').replace(/\n/g,'<br>');
}

function copyCurrentTab(){
  var el=D('tab-'+activeTab);
  if(!el)return;
  navigator.clipboard.writeText(el.textContent||'').then(function(){
    var t=D('copyToast');t.textContent=T('tabCopied');
    t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000);
  }).catch(function(){showStatus('Copy failed','error')});
}

async function exportDoc(fmt){
  var token=localStorage.getItem('token')||'';
  var r=await fetch('/export?format='+fmt,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},body:JSON.stringify({docs:allDocs})});
  if(r.ok){var b=await r.blob();var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='docs.'+(fmt==='markdown'?'md':fmt);a.click();showStatus(T('downloaded'),'success')}
}
