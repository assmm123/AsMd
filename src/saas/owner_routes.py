"""Owner Panel Routes - لوحة المالك"""
import json, os
from flask import render_template, request, jsonify
from src.auth.jwt import create_token
from src.auth.models import db, save_db
from src.saas.logger import get_recent_logs
from datetime import datetime, timedelta


def register_owner_routes(app):
    
    @app.route('/owner')
    def owner_page():
        return render_template('owner.html')
    
    @app.route('/owner/api/login', methods=['POST'])
    def owner_api_login():
        data = request.json
        owner_pass = os.getenv("OWNER_PASSWORD", "admin123")
        if data.get('password') == owner_pass:
            token = create_token('owner', role='admin')
            return jsonify({'success': True, 'token': token})
        return jsonify({'success': False, 'error': 'Wrong password'}), 401
    
    @app.route('/owner/api/dashboard')
    def owner_api_dashboard():
        users = db.get_all_users()
        today = datetime.utcnow().strftime('%Y-%m-%d')
        
        total_users = len(users)
        requests_today = sum(u.get('daily_requests',0) for u in users)
        active_users = len([u for u in users if u.get('daily_requests',0) > 0])
        
        # الإيرادات
        prices = {'basic':5, 'pro':15, 'unlimited':30}
        config_file = 'data/owner_config.json'
        if os.path.exists(config_file):
            cfg = json.load(open(config_file))
            prices.update(cfg.get('prices',{}))
        revenue = sum(prices.get(u.get('tier','free'),0) for u in users if u.get('tier','free') != 'free')
        
        # آخر 7 أيام طلبات
        usage_file = 'data/daily_usage.json'
        usage_history = []
        if os.path.exists(usage_file):
            usage = json.load(open(usage_file))
        else:
            usage = {}
        for i in range(6, -1, -1):
            d = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
            usage_history.append({'date': d, 'count': usage.get(d, 0)})
        
        # أكثر 5 مستخدمين نشاطاً
        top_users = sorted(users, key=lambda u: u.get('daily_requests',0), reverse=True)[:5]
        top_users_list = [{'username': u.get('username'), 'tier': u.get('tier','free'), 'daily': u.get('daily_requests',0)} for u in top_users]
        
        # آخر العمليات
        recent_logs = get_recent_logs(10)
        
        return jsonify({
            'success': True,
            'total_users': total_users,
            'requests_today': requests_today,
            'active_users': active_users,
            'revenue': revenue,
            'requests_history': usage_history,
            'top_users': top_users_list,
            'recent_logs': recent_logs
        })
    
    @app.route('/owner/api/users')
    def owner_api_users():
        users = db.get_all_users()
        return jsonify({'success': True, 'users': [{
            'username': u.get('username'),
            'email': u.get('email',''),
            'tier': u.get('tier','free'),
            'daily_requests': u.get('daily_requests',0)
        } for u in users]})
    
    @app.route('/owner/api/users/tier', methods=['POST'])
    def owner_api_change_tier():
        data = request.json
        user = db.get_user(data.get('username'))
        if user:
            user['tier'] = data.get('tier','free')
            save_db()
        return jsonify({'success': True})
    
    @app.route('/owner/api/wallets', methods=['GET','POST','DELETE'])
    def owner_api_wallets():
        config_file = 'data/owner_config.json'
        os.makedirs('data', exist_ok=True)
        
        if request.method == 'POST':
            data = request.json
            config = {}
            if os.path.exists(config_file):
                config = json.load(open(config_file))
            config['wallets'] = config.get('wallets',{})
            config['wallets'][data['name']] = {
                'address': data.get('address',''),
                'network': data.get('network',''),
                'currency': data.get('currency',''),
                'active': data.get('active', True),
                'notes': data.get('notes',''),
                'added_at': datetime.utcnow().strftime('%Y-%m-%d')
            }
            json.dump(config, open(config_file,'w'))
            return jsonify({'success': True})
        
        if request.method == 'DELETE':
            data = request.json
            config = {}
            if os.path.exists(config_file):
                config = json.load(open(config_file))
            if data.get('name') in config.get('wallets',{}):
                del config['wallets'][data['name']]
                json.dump(config, open(config_file,'w'))
            return jsonify({'success': True})
        
        # GET
        config = {}
        if os.path.exists(config_file):
            config = json.load(open(config_file))
        wallets = config.get('wallets',{})
        # Mask addresses for security
        safe_wallets = {}
        for k, v in wallets.items():
            addr = v.get('address','') if isinstance(v, dict) else v
            masked = addr[:6] + '...' + addr[-4:] if len(addr) > 10 else addr
            safe_wallets[k] = {
                'address': addr,
                'masked': masked,
                'network': v.get('network','') if isinstance(v, dict) else '',
                'currency': v.get('currency','') if isinstance(v, dict) else '',
                'active': v.get('active', True) if isinstance(v, dict) else True,
                'notes': v.get('notes','') if isinstance(v, dict) else '',
                'added_at': v.get('added_at','') if isinstance(v, dict) else ''
            }
        return jsonify({'success': True, 'wallets': safe_wallets})
    
    @app.route('/owner/api/wallets/toggle', methods=['POST'])
    def owner_api_toggle_wallet():
        config_file = 'data/owner_config.json'
        data = request.json
        if os.path.exists(config_file):
            config = json.load(open(config_file))
            if data['name'] in config.get('wallets',{}):
                w = config['wallets'][data['name']]
                if isinstance(w, dict):
                    w['active'] = not w.get('active', True)
                else:
                    config['wallets'][data['name']] = {'address': w, 'active': False}
                json.dump(config, open(config_file,'w'))
        return jsonify({'success': True})
    
    @app.route('/owner/api/pricing', methods=['GET','POST','DELETE'])
    def owner_api_pricing():
        config_file = 'data/owner_config.json'
        os.makedirs('data', exist_ok=True)
        
        if request.method == 'POST':
            data = request.json
            config = {}
            if os.path.exists(config_file):
                config = json.load(open(config_file))
            config['plans'] = config.get('plans',{})
            config['plans'][data['tier']] = {
                'name': data.get('name', data['tier']),
                'price': data.get('price', 0),
                'limit': data.get('limit', 10),
                'description': data.get('description', ''),
                'active': data.get('active', True)
            }
            json.dump(config, open(config_file,'w'))
            return jsonify({'success': True})
        
        if request.method == 'DELETE':
            data = request.json
            config = {}
            if os.path.exists(config_file):
                config = json.load(open(config_file))
            if data.get('tier') in config.get('plans',{}):
                del config['plans'][data['tier']]
                json.dump(config, open(config_file,'w'))
            return jsonify({'success': True})
        
        # GET
        config = {}
        if os.path.exists(config_file):
            config = json.load(open(config_file))
        plans = config.get('plans', {
            'free': {'name':'مجاني','price':0,'limit':5,'description':'للتجربة','active':True},
            'basic': {'name':'أساسي','price':5,'limit':20,'description':'للمطورين','active':True},
            'pro': {'name':'محترف','price':15,'limit':50,'description':'للفرق','active':True},
            'unlimited': {'name':'غير محدود','price':30,'limit':100,'description':'للشركات','active':True}
        })
        return jsonify({'success': True, 'plans': plans})
    
    @app.route('/owner/api/pricing/preview/<tier>')
    def owner_api_preview_plan(tier):
        config_file = 'data/owner_config.json'
        plans = {'free': {'name':'مجاني','price':0,'limit':5},'basic': {'name':'أساسي','price':5,'limit':20},'pro': {'name':'محترف','price':15,'limit':50},'unlimited': {'name':'غير محدود','price':30,'limit':100}}
        if os.path.exists(config_file):
            cfg = json.load(open(config_file))
            plans.update(cfg.get('plans',{}))
        plan = plans.get(tier, {})
        return jsonify({'success': True, 'plan': plan})
    
    
    @app.route('/owner/api/users/<username>')
    def owner_api_user_detail(username):
        user = db.get_user(username)
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        # تاريخ الاشتراك
        created = user.get('created_at', 'غير معروف')
        expires = user.get('expires_at', 'غير محدد')
        # آخر دخول
        last_login = 'غير معروف'
        logs = get_recent_logs(500)
        for l in logs:
            if l['user'] == username:
                last_login = l['time']
                break
        # سجل الطلبات
        user_logs = [l for l in logs if l['user'] == username][:10]
        return jsonify({
            'success': True,
            'user': {
                'username': username,
                'email': user.get('email',''),
                'tier': user.get('tier','free'),
                'daily_requests': user.get('daily_requests',0),
                'created_at': created,
                'expires_at': expires,
                'last_login': last_login,
                'is_blocked': user.get('blocked', False),
                'recent_activity': user_logs
            }
        })
    
    @app.route('/owner/api/users/<username>/block', methods=['POST'])
    def owner_api_block_user(username):
        user = db.get_user(username)
        if user:
            user['blocked'] = not user.get('blocked', False)
            save_db()
        return jsonify({'success': True, 'blocked': user.get('blocked', False)})
    
    @app.route('/owner/api/users/<username>', methods=['DELETE'])
    def owner_api_delete_user(username):
        if username in db.users:
            del db.users[username]
            save_db()
        return jsonify({'success': True})
    
    @app.route('/owner/api/users/export/csv')
    def owner_api_export_csv():
        users = db.get_all_users()
        csv = 'username,email,tier,daily_requests,created_at\n'
        for u in users:
            csv += f"{u.get('username','')},{u.get('email','')},{u.get('tier','free')},{u.get('daily_requests',0)},{u.get('created_at','')}\n"
        from flask import Response
        return Response(csv, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=users.csv'})

    @app.route('/owner/api/logs')
    def owner_api_logs():
        return jsonify({'success': True, 'logs': get_recent_logs(50)})
