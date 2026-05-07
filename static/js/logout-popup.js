/**
 * Logout Popup - تأكيد خروج منسق
 */

function showLogoutPopup() {
  // إذا موجود، نظهره فقط
  var lp = document.getElementById('logoutPopup');
  if (lp) {
    lp.style.display = 'flex';
    return;
  }

  // إنشاء popup جديد
  lp = document.createElement('div');
  lp.id = 'logoutPopup';
  lp.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:2000;display:flex;align-items:center;justify-content:center';

  lp.innerHTML = ''
    + '<div style="background:#1a1a2e;border:1px solid #333;border-radius:16px;padding:30px;text-align:center;max-width:300px;width:90%">'
    + '<p style="font-size:40px;margin-bottom:10px">🚪</p>'
    + '<p style="color:#e0e0e0;font-size:16px;margin-bottom:20px">هل تريد تسجيل الخروج؟</p>'
    + '<button onclick="doLogout()" style="background:#ef4444;color:#fff;border:none;padding:12px 40px;border-radius:8px;font-size:15px;margin:5px;cursor:pointer">نعم</button>'
    + '<button onclick="document.getElementById(\'logoutPopup\').remove()" style="background:#2d2d3f;color:#e0e0e0;border:1px solid #444;padding:12px 40px;border-radius:8px;font-size:15px;margin:5px;cursor:pointer">لا</button>'
    + '</div>';

  document.body.appendChild(lp);
}

function doLogout() {
  localStorage.removeItem('token');
  var lp = document.getElementById('logoutPopup');
  if (lp) lp.remove();
  var ud = document.getElementById('userDisplay');
  if (ud) ud.style.display = 'none';
  var li = document.getElementById('loginIcon');
  if (li) li.style.display = 'inline';
}
