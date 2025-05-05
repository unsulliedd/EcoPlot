# EcoPlot/models/recommendation.py
from EcoPlot import db
from datetime import datetime
import json

class RecommendationHistory(db.Model):
    """Model for storing user recommendation history"""
    __tablename__ = 'recommendation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Overall metrics
    estimated_monthly_savings = db.Column(db.Float)
    carbon_reduction_potential = db.Column(db.Float)
    
    # Store the complete recommendations JSON
    recommendations_json = db.Column(db.Text)
    
    # Metadata
    device_count = db.Column(db.Integer)
    has_solar = db.Column(db.Boolean, default=False)
    has_ev = db.Column(db.Boolean, default=False)
    has_battery = db.Column(db.Boolean, default=False)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('recommendation_history', lazy=True))
    
    def __repr__(self):
        return f'<RecommendationHistory {self.id} for User {self.user_id}>'
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'estimated_monthly_savings': self.estimated_monthly_savings,
            'carbon_reduction_potential': self.carbon_reduction_potential,
            'device_count': self.device_count,
            'has_solar': self.has_solar,
            'has_ev': self.has_ev,
            'has_battery': self.has_battery,
            'recommendations': json.loads(self.recommendations_json) if self.recommendations_json else {}
        }
    
    @classmethod
    def create_from_response(cls, user_id, recommendations_data, device_count, has_solar, has_ev, has_battery):
        """
        Create a recommendation history entry from API response data
        
        Args:
            user_id (int): User ID
            recommendations_data (dict): Recommendations data from Gemini
            device_count (int): Number of user devices
            has_solar (bool): Whether user has solar panels
            has_ev (bool): Whether user has an electric vehicle
            has_battery (bool): Whether user has battery storage
            
        Returns:
            RecommendationHistory: New history entry
        """
        # Extract recommendations data
        recs = recommendations_data.get('recommendations', {})
        
        history = cls(
            user_id=user_id,
            estimated_monthly_savings=recs.get('estimated_monthly_savings', 0),
            carbon_reduction_potential=recs.get('carbon_reduction_potential', 0),
            recommendations_json=json.dumps(recs),
            device_count=device_count,
            has_solar=has_solar,
            has_ev=has_ev,
            has_battery=has_battery
        )
        
        return history