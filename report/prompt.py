report_prompt = """
Create a JSON report with this schema:
{
  "overall_performance_metrics": {
    "basic_stats": [],
    "accuracy_metrics": []
  },
  "performance_distribution": {
    "performance_brackets": [],
    "top_performers": []
  },
  "risk_assessment": {
    "warning_effectiveness": [],
    "performance_risk_ratio": []
  },
  "key_insights": {
    "prediction_accuracy": [],
    "risk_management": [],
    "distribution": [],
    "patterns": []
  },
  "recommendations": {
    "strategy": [],
    "optimization": [], 
    "risk": [],
    "documentation": []
  },
  "conclusion": []
}
Include all metrics, statistics, and insights as list items under each relevant key.

Include Overall Performance Metrics section with:

Basic Statistics (total entries, gains, averages, extremes)
Accuracy Metrics (predictions, success rates)


Break down Performance Distribution showing:

Performance brackets with percentages (0X, 0-2X, 2-5X, >5X)
Top 5 performers with gains


Detail Risk Assessment Metrics covering:

Warning call effectiveness
Performance-to-risk ratios across brackets


Provide Key Insights analyzing:

Prediction accuracy patterns
Risk management effectiveness
Performance distribution trends
Pattern recognition in successful cases


List actionable Recommendations for:

Strategy validation
Performance optimization
Risk management
Documentation improvements


End with a Conclusion summarizing:

Overall system effectiveness
Balance of risk and reward
Notable strengths and areas for improvement

"""