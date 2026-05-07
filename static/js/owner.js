var currentTab='dashboard';
var apiBase='/owner/api';
var requestsChart=null;

function D(id){return document.getElementById(id)}

document.querySelectorAll('.sidebar a').forEach(function(a){
  a.onclick=function(){
    document.querySelectorAll('.sidebar a').forEach(function(x){x.classList.remove('active')});
    a.classList.add('active');
    document.querySelectorAll('.tab-content').forEach(function(x){x.classList.remove('active')});
    D('tab-'+a.dataset.tab).classList.add('active');
    currentTab=a.dataset.tab;
    if(currentTab=='dashboard') loadDashboard();
    if(currentTab=='users') loadUsers();
    if(currentTab=='wallets') loadWallets();
    if(currentTab=='pricing') loadPricing();
    if(currentTab=='logs') loadLogs();
  }
});

function showMsg(el,text,type){el.textContent=text;el.className='msg '+type;setTimeout(function(){el.className='msg'},3000)}

async function api(url,method,body){
  var headers={'Content-Type':'application/json'};
  var t=localStorage.getItem('owner_token');
  if(t)headers['Authorization']='Bearer '+t;
  var opts={method:method||'GET',headers:headers};
  if(body)opts.body=JSON.stringify(body);
  var r=await fetch(apiBase+url,opts);
  return r.json();
}

async function login(){
  var pass=D('ownerPass').value;
  var r=await api('/login','POST',{password:pass});
  if(r.success){localStorage.setItem('owner_token',r.token);D('loginBox').style.display='none';D('appBox').style.display='flex';loadDashboard()}
  else{showMsg(D('loginMsg'),r.error||'Wrong password','error')}
}

function logout(){localStorage.removeItem('owner_token');location.reload()}

// Dashboard
async function loadDashboard(){
  var d=await api('/dashboard');
  if(d.success){
    D('totalUsers').textContent=d.total_users||0;
    D('totalRequests').textContent=d.requests_today||0;
    D('activeUsers').textContent=d.active_users||0;
    D('revenue').textContent='$'+(d.revenue||0);
    renderChart(d.requests_history||[]);
    renderTopUsers(d.top_users||[]);
    renderRecentLogs(d.recent_logs||[]);
  }
}

function renderChart(data){
  var ctx=D('requestsChart').getContext('2d');
  if(requestsChart)requestsChart.destroy();
  requestsChart=new Chart(ctx,{
    type:'bar',
    data:{
      labels:data.map(function(d){return d.date}),
      datasets:[{label:'طلبات',data:data.map(function(d){return d.count}),backgroundColor:'#7c3aed',borderRadius:8}]
    },
    options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'#333'},ticks:{color:'#888'}},x:{grid:{color:'#333'},ticks:{color:'#888'}}}}
  });
}

function renderTopUsers(users){
  var html='<tr><th>المستخدم</th><th>الخطة</th><th>طلبات اليوم</th></tr>';
  users.forEach(function(u){html+='<tr><td>'+u.username+'</td><td><span class="badge badge-'+u.tier+'">'+u.tier+'</span></td><td>'+u.daily+'</td></tr>'});
  D('topUsers').innerHTML=html||'<tr><td>No data</td></tr>';
}

function renderRecentLogs(logs){
  var html='<tr><th>الوقت</th><th>المستخدم</th><th>الحدث</th></tr>';
  logs.forEach(function(l){html+='<tr><td>'+l.time+'</td><td>'+l.user+'</td><td>'+l.action+'</td></tr>'});
  D('recentLogs').innerHTML=html||'<tr><td>No data</td></tr>';
}

// Users
var allUsers=[];
async function loadUsers(){
  var d=await api('/users');
  if(d.success){allUsers=d.users;renderUsers(allUsers)}
}

function renderUsers(users){
  var html='<tr><th>المستخدم</th><th>البريد</th><th>الخطة</th><th>الطلبات</th><th>إجراءات</th></tr>';
  users.forEach(function(u){
    var blockBtn=u.is_blocked?'<button class="success" onclick="blockUser(\''+u.username+'\')">فك حظر</button>':'<button onclick="blockUser(\''+u.username+'\')">حظر</button>';
    html+='<tr><td><a href="#" onclick="showUserDetail(\''+u.username+'\')">'+u.username+'</a></td><td>'+u.email+'</td><td><span class="badge badge-'+u.tier+'">'+u.tier+'</span></td><td>'+u.daily_requests+'</td><td><button onclick="changeTier(\''+u.username+'\',\'basic\')">Basic</button><button onclick="changeTier(\''+u.username+'\',\'pro\')">Pro</button><button onclick="changeTier(\''+u.username+'\',\'unlimited\')">Unlim</button>'+blockBtn+'<button class="danger" onclick="deleteUser(\''+u.username+'\')">حذف</button></td></tr>';
  });
  D('usersTable').innerHTML=html||'<tr><td colspan="5">No users</td></tr>';
}

function searchUsers(){
  var q=D('userSearch').value.toLowerCase();
  var filtered=allUsers.filter(function(u){return u.username.toLowerCase().includes(q)||u.email.toLowerCase().includes(q)});
  renderUsers(filtered);
}

async function showUserDetail(username){
  var d=await api('/users/'+username);
  if(d.success){
    var u=d.user;
    var act=u.recent_activity.map(function(a){return '<li>'+a.time+' - '+a.action+'</li>'}).join('');
    D('userDetail').style.display='block';
    D('userDetail').innerHTML='<div class="card"><h3>👤 '+u.username+'</h3><p><b>البريد:</b> '+u.email+'</p><p><b>الخطة:</b> <span class="badge badge-'+u.tier+'">'+u.tier+'</span></p><p><b>طلبات اليوم:</b> '+u.daily_requests+'</p><p><b>تاريخ التسجيل:</b> '+u.created_at+'</p><p><b>انتهاء الاشتراك:</b> '+u.expires_at+'</p><p><b>آخر دخول:</b> '+u.last_login+'</p><p><b>محظور:</b> '+(u.is_blocked?'نعم':'لا')+'</p><h4>آخر النشاطات</h4><ul>'+act+'</ul><button onclick="D(\'userDetail\').style.display=\'none\'">إغلاق</button></div>';
  }
}

async function changeTier(username,tier){await api('/users/tier','POST',{username:username,tier:tier});loadUsers()}
async function deleteUser(username){if(confirm('حذف '+username+'؟')){await api('/users/'+username,'DELETE');loadUsers()}}
async function blockUser(username){await api('/users/'+username+'/block','POST');loadUsers()}

// Wallets
async function loadWallets(){
  var d=await api('/wallets');
  if(d.success){
    var html='';
    for(var k in d.wallets){html+='<div class="card"><h3>'+k+'</h3><input value="'+d.wallets[k]+'" id="wallet_'+k+'"><button onclick="saveWallet(\''+k+'\')">حفظ</button></div>'}
    D('walletsList').innerHTML=html;
  }
}
async function saveWallet(name){var val=D('wallet_'+name).value;await api('/wallets','POST',{name:name,address:val});showMsg(D('walletMsg'),'Saved','success')}

// Pricing
async function loadPricing(){
  var d=await api('/pricing');
  if(d.success){
    var html='';
    for(var k in d.prices){html+='<div class="card"><h3>'+k+'</h3><input type="number" value="'+d.prices[k]+'" id="price_'+k+'"><button onclick="savePrice(\''+k+'\')">حفظ</button></div>'}
    D('pricingList').innerHTML=html;
  }
}
async function savePrice(tier){var val=D('price_'+tier).value;await api('/pricing','POST',{tier:tier,price:parseInt(val)});showMsg(D('pricingMsg'),'Saved','success')}

// Logs
async function loadLogs(){
  var d=await api('/logs');
  if(d.success){
    var html='<tr><th>الوقت</th><th>المستخدم</th><th>الحدث</th></tr>';
    d.logs.forEach(function(l){html+='<tr><td>'+l.time+'</td><td>'+l.user+'</td><td>'+l.action+'</td></tr>'});
    D('logsTable').innerHTML=html||'<tr><td>No logs</td></tr>';
  }
}

// Export
function exportCSV(){window.open(apiBase+'/users/export/csv')}

// Init
if(localStorage.getItem('owner_token')){
  D('loginBox').style.display='none';
  D('appBox').style.display='flex';
  loadDashboard();
}

// === Wallets Enhanced ===
async function loadWallets(){
  var d=await api('/wallets');
  if(d.success){
    var html='<button onclick="addWallet()" style="margin-bottom:15px">➕ إضافة محفظة</button>';
    for(var k in d.wallets){
      var w=d.wallets[k];
      var status=w.active?'🟢 نشط':'🔴 معطل';
      html+='<div class="card"><h3>'+k+' <span style="font-size:12px;color:#888">'+status+'</span></h3>';
      html+='<p><b>العنوان:</b> <code style="font-size:11px">'+w.masked+'</code> <button onclick="copyWallet(\''+w.address+'\')">📋</button></p>';
      if(w.network)html+='<p><b>الشبكة:</b> '+w.network+'</p>';
      if(w.currency)html+='<p><b>العملة:</b> '+w.currency+'</p>';
      if(w.notes)html+='<p><b>ملاحظات:</b> '+w.notes+'</p>';
      html+='<p><b>أضيف:</b> '+w.added_at+'</p>';
      html+='<button onclick="toggleWallet(\''+k+'\')">'+(w.active?'تعطيل':'تفعيل')+'</button> ';
      html+='<button onclick="editWallet(\''+k+'\',\''+w.address+'\',\''+w.network+'\',\''+w.currency+'\',\''+w.notes+'\')">✏️ تعديل</button> ';
      html+='<button onclick="previewWallet(\''+k+'\')">👁️ معاينة</button> ';
      html+='<button class="danger" onclick="deleteWallet(\''+k+'\')">🗑️ حذف</button>';
      html+='</div>';
    }
    D('walletsList').innerHTML=html;
  }
}

function addWallet(){
  var name=prompt('اسم المحفظة:');
  if(!name)return;
  var addr=prompt('العنوان:');
  if(!addr)return;
  var network=prompt('الشبكة (TRC20/BEP20/...):');
  var currency=prompt('العملة (USDT/BNB/...):');
  var notes=prompt('ملاحظات:');
  api('/wallets','POST',{name:name,address:addr,network:network,currency:currency,notes:notes}).then(loadWallets);
}

function editWallet(name,addr,network,currency,notes){
  var newAddr=prompt('العنوان:',addr);
  if(!newAddr)return;
  var newNet=prompt('الشبكة:',network);
  var newCur=prompt('العملة:',currency);
  var newNotes=prompt('ملاحظات:',notes);
  api('/wallets','POST',{name:name,address:newAddr,network:newNet,currency:newCur,notes:newNotes}).then(loadWallets);
}

async function deleteWallet(name){
  if(confirm('حذف '+name+'؟')){
    await api('/wallets','DELETE',{name:name});
    loadWallets();
  }
}

async function toggleWallet(name){
  await api('/wallets/toggle','POST',{name:name});
  loadWallets();
}

function previewWallet(name){
  api('/wallets').then(function(d){
    if(d.success){
      var w=d.wallets[name];
      if(!w)return;
      var popup=document.createElement('div');
      popup.style.cssText='position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:2000;display:flex;align-items:center;justify-content:center';
      popup.onclick=function(e){if(e.target==popup)popup.remove()};
      popup.innerHTML='<div style="background:#1a1a2e;border:1px solid #333;border-radius:16px;padding:30px;max-width:400px;width:90%;text-align:center">'+
        '<h3 style="color:#a78bfa;margin-bottom:15px">💳 '+name+'</h3>'+
        '<p style="color:#888;font-size:12px;margin:5px 0">الشبكة: '+(w.network||'غير محدد')+'</p>'+
        '<p style="color:#888;font-size:12px;margin:5px 0">العملة: '+(w.currency||'غير محدد')+'</p>'+
        '<div style="background:#0f0f1a;border:1px solid #333;border-radius:8px;padding:15px;margin:15px 0;word-break:break-all;font-size:11px;color:#e0e0e0">'+w.address+'</div>'+
        '<button onclick="navigator.clipboard.writeText(\''+w.address+'\');alert(\'تم النسخ\')" style="background:#7c3aed;color:#fff;border:none;padding:10px 30px;border-radius:8px;cursor:pointer;margin:5px">📋 نسخ</button>'+
        '<button onclick="this.parentElement.parentElement.remove()" style="background:#2d2d3f;color:#e0e0e0;border:1px solid #444;padding:10px 30px;border-radius:8px;cursor:pointer;margin:5px">إغلاق</button>'+
        '</div>';
      document.body.appendChild(popup);
    }
  });
}

function copyWallet(text){
  navigator.clipboard.writeText(text).then(function(){
    alert('تم النسخ');
  });
}
