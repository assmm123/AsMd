var currentLang=localStorage.getItem('docgen_lang')||'ar';
var allResults={},activeTab='overview',uploadedFile=null;

function D(id){return document.getElementById(id)}

function switchLang(lang){
  currentLang=lang;localStorage.setItem('docgen_lang',lang);
  document.getElementById('btnAr').classList.remove('active');
  document.getElementById('btnEn').classList.remove('active');
  if(lang==='ar'){document.getElementById('btnAr').classList.add('active');document.body.dir='rtl'}
  else{document.getElementById('btnEn').classList.add('active');document.body.dir='ltr'}
}

function updatePlaceholder(){
  var type=D('inputType').value;
  var inp=D('testTarget');
  if(type==='github'){inp.placeholder='user/repo | github.com/user/repo'}
  else{inp.placeholder='src/auth.py | src/'}
}

function handleFileUpload(e){
  var file=e.target.files[0];
  if(file){uploadedFile=file;D('testTarget').value='📎 '+file.name;D('testTarget').style.color='#a78bfa'}
}

document.querySelectorAll('.tab').forEach(function(t){
  t.onclick=function(){
    document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active')});
    document.querySelectorAll('.tab-content').forEach(function(x){x.classList.remove('active')});
    t.classList.add('active');activeTab=t.dataset.tab;
    D('tab-'+t.dataset.tab).classList.add('active');
  }
});

function showStatus(msg,type){
  var s=D('statusMsg');s.textContent=msg;s.style.display='block';
  s.className='status '+(type||'error');
  setTimeout(function(){s.style.display='none'},5000);
}

async function runTestGen(){
  D('loading').style.display='block';D('resultsArea').style.display='none';
  try{
    var token=localStorage.getItem('token')||'';
    var d;
    
    if(uploadedFile){
      var formData=new FormData();
      formData.append('file',uploadedFile);
      var r=await fetch('/api/test-generate',{method:'POST',headers:{'Authorization':'Bearer '+token},body:formData});
      d=await r.json();
    }else{
      var target=D('testTarget').value.trim();
      var type=D('inputType').value;
      if(!target){showStatus('Enter path, upload file, or GitHub URL','error');D('loading').style.display='none';return}
      var r=await fetch('/api/test-generate',{method:'POST',headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({target:target,type:type})});
      d=await r.json();
    }
    
    if(d.success){allResults=d;renderAll();D('resultsArea').style.display='block';showStatus('Done!','success')}
    else{showStatus(d.error||'Failed','error')}
  }catch(e){showStatus(e.message,'error')}
  D('loading').style.display='none';
}

async function runFix(){
  D('loading').style.display='block';D('resultsArea').style.display='none';
  try{
    var token=localStorage.getItem('token')||'';
    var r=await fetch('/api/test-fix',{method:'POST',headers:{'Authorization':'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify({target:'tests'})});
    var d=await r.json();
    if(d.success){allResults=d;renderAll();D('resultsArea').style.display='block';showStatus('Fix complete!','success')}
    else{showStatus(d.error||'Failed','error')}
  }catch(e){showStatus(e.message,'error')}
  D('loading').style.display='none';
}

async function runReport(){
  D('loading').style.display='block';D('resultsArea').style.display='none';
  try{
    var token=localStorage.getItem('token')||'';
    var r=await fetch('/api/test-report',{method:'GET',headers:{'Authorization':'Bearer '+token}});
    var d=await r.json();
    if(d.success){allResults=d;renderAll();D('resultsArea').style.display='block';showStatus('Report ready!','success')}
    else{showStatus(d.error||'Failed','error')}
  }catch(e){showStatus(e.message,'error')}
  D('loading').style.display='none';
}

function renderAll(){
  D('tab-overview').innerHTML=allResults.overview||'<p style="color:#555">No data</p>';
  D('tab-functions').innerHTML=allResults.functions||'<p style="color:#555">No data</p>';
  D('tab-tests').innerHTML=allResults.tests||'<p style="color:#555">No data</p>';
  D('tab-healing').innerHTML=allResults.healing||'<p style="color:#555">No data</p>';
  D('tab-report').innerHTML=allResults.report||'<p style="color:#555">No data</p>';
}

function copyTab(){
  var el=D('tab-'+activeTab);
  navigator.clipboard.writeText(el.textContent||'').then(function(){showStatus('Copied!','success')});
}

function exportResult(fmt){showStatus('Export not available','error');}
