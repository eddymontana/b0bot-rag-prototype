import os
from flask import Flask, request, jsonify, render_template
from services.AgentService import app_graph
from cybernews.CyberNews import CyberNews  # <--- Import your service
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Initialize CyberNews instance once (singleton-style)
    news_service = CyberNews()

    @app.route('/')
    def index():
        return render_template('index.html')

    # --- NEW: NEWS ENDPOINT ---
    @app.route('/news', methods=['GET'])
    def get_cyber_news():
        """
        Retrieves news from the knowledge base.
        Usage: /news?category=general
        """
        category = request.args.get('category', 'general')
        
        try:
            # 1. Fetch from our verified service
            news_items = news_service.get_news(category)
            
            # 2. Return JSend-compliant JSON
            return jsonify({
                "status": "success",
                "data": {
                    "category": category,
                    "count": len(news_items),
                    "articles": news_items
                }
            }), 200
        except Exception as e:
            app.logger.error(f"News Route Error: {str(e)}")
            return jsonify({"status": "error", "message": "Failed to fetch news."}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy", 
            "service": "b0bot-agent",
            "version": "2.1.0"
        }), 200

    @app.route('/analyze', methods=['POST'])
    def analyze_threats():
        # ... (Your existing logic for LangGraph analyze_threats remains the same)
        pass

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)