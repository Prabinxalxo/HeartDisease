def get_diet_recommendations(has_heart_disease):
    """
    Return diet recommendations based on heart disease prediction.
    
    Args:
        has_heart_disease (bool): Whether the user has heart disease or not
    
    Returns:
        dict: Dictionary containing diet recommendations
    """
    # Base recommendations for everyone
    base_recommendations = {
        "Foods to Include": [
            "Fresh fruits and vegetables (aim for 5+ servings daily)",
            "Whole grains (brown rice, whole wheat bread, oats)",
            "Lean proteins (fish, skinless poultry, legumes)",
            "Healthy fats (olive oil, avocados, nuts)",
            "Low-fat dairy or dairy alternatives"
        ],
        "Limit or Avoid": [
            "Processed foods high in sodium",
            "Added sugars and sweetened beverages",
            "Excessive alcohol consumption",
            "Deep-fried foods and trans fats"
        ]
    }
    
    # Additional recommendations for those with heart disease risk
    if has_heart_disease:
        heart_disease_recommendations = {
            "Foods to Include": [
                "Omega-3 rich fish (salmon, mackerel, sardines) at least twice weekly",
                "Berries (especially blueberries and strawberries)",
                "Oats and barley for their beta-glucan content",
                "Nuts and seeds (walnuts, flaxseeds, chia seeds)",
                "Green leafy vegetables (spinach, kale)",
                "Beans and legumes for plant protein and fiber",
                "Low-sodium herbs and spices for flavoring"
            ],
            "Specific Heart-Healthy Tips": [
                "Limit sodium to less than 1,500 mg per day",
                "Reduce saturated fat to less than 7% of daily calories",
                "Avoid trans fats completely",
                "Limit added sugars to less than 25g (6 teaspoons) per day",
                "Consider the DASH or Mediterranean diet approach",
                "Stay hydrated with water instead of sugary beverages",
                "Limit red meat to once a week or less"
            ],
            "Dietary Pattern Recommendation": [
                "Follow a Mediterranean-style diet rich in fruits, vegetables, whole grains, and healthy fats",
                "Consider consulting with a registered dietitian for a personalized plan",
                "Keep a food journal to track sodium, fat, and sugar intake",
                "Prepare meals at home to control ingredients and portion sizes"
            ]
        }
        
        # Combine base and heart disease specific recommendations
        recommendations = {}
        for key in set(list(base_recommendations.keys()) + list(heart_disease_recommendations.keys())):
            if key in base_recommendations and key in heart_disease_recommendations:
                recommendations[key] = base_recommendations[key] + heart_disease_recommendations[key]
            elif key in base_recommendations:
                recommendations[key] = base_recommendations[key]
            else:
                recommendations[key] = heart_disease_recommendations[key]
                
        return recommendations
    else:
        # For those without heart disease, add general health maintenance tips
        maintenance_recommendations = {
            "Heart Health Maintenance": [
                "Maintain a balanced diet with plenty of fruits and vegetables",
                "Choose whole grains over refined grains",
                "Include lean proteins and plant-based protein sources",
                "Stay physically active with at least 150 minutes of moderate exercise weekly",
                "Maintain a healthy weight",
                "Consider regular health check-ups to monitor blood pressure and cholesterol"
            ]
        }
        
        # Combine base and maintenance recommendations
        recommendations = base_recommendations.copy()
        recommendations.update(maintenance_recommendations)
        
        return recommendations
