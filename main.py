from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/trends', methods=['GET'])
def get_trends():
    keyword = request.args.get('keyword', '')
    geo = request.args.get('geo', 'CO')
    
    if not keyword:
        return jsonify({'error': 'keyword requerida'}), 400
    
    try:
        pytrends = TrendReq(hl='es-CO', tz=300)
        pytrends.build_payload([keyword], cat=0, timeframe='today 12-m', geo=geo)
        data = pytrends.interest_over_time()
        
        if data.empty:
            return jsonify({'keyword': keyword, 'promedio': 0, 'tiene_demanda': False})
        
        promedio = int(data[keyword].mean())
        return jsonify({
            'keyword': keyword,
            'promedio': promedio,
            'tiene_demanda': promedio > 20
        })
    except Exception as e:
        return jsonify({'error': str(e), 'keyword': keyword, 'promedio': 0, 'tiene_demanda': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
