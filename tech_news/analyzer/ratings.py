from tech_news.database import db


# Requisito 10
def top_5_news():
    pipeline_top_news = [
        {
            "$project": {
                "title": 1,
                "url": 1,
                "popularity": {"$sum": ["$shares_count", "$comments_count"]},
            }
        },
        {"$sort": {"popularity": -1, "title": 1}},
        {"$limit": 5},
    ]
    found_news = db.news.aggregate(pipeline_top_news)
    news = [(new["title"], new["url"]) for new in found_news]
    return news


# Requisito 11
def top_5_categories():
    pipeline_categories = [
        {"$unwind": "$categories"},
        {
            "$group": {
                "_id": {"categories": "$categories"},
                "total": {"$sum": 1},
            }
        },
        {"$sort": {"total": -1, "_id.categories": 1}},
        {"$limit": 5},
        {"$project": {"_id.categories": 1, "total": 1}},
    ]
    found_categories = db.news.aggregate(pipeline_categories)
    category = [category["_id"]["categories"] for category in found_categories]
    return category
